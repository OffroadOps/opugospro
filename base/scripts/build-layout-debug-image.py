#!/usr/bin/env python3
import argparse
import gzip
import importlib.util
import io
import json
import shutil
import struct
import subprocess
import sys
import tarfile
import time
from pathlib import Path


SECTOR_SIZE = 512


def load_base_builder(project_dir: Path):
    script = project_dir / "scripts" / "build-squashfs-debug-image.py"
    spec = importlib.util.spec_from_file_location("ugos_squashfs_debug_builder", script)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def align_up(value: int, alignment: int) -> int:
    return ((value + alignment - 1) // alignment) * alignment


def require_file(path: Path, label: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Missing {label}: {path}")


def patch_init_script(text: str, module_version: str) -> str:
    text = text.replace(
        "PART_ERR=`sgdisk  -v /dev/mmcblk0  2>&1 | grep ERROR`",
        "PART_ERR=''",
    )
    text = text.replace(
        "mount -t $OVERLAY_FS -o rw,nosuid,nodev,noatime,nobarrier,quota,usrquota,grpquota,prjquota  $OVERLAY_DEV  /overlay",
        "mount -t $OVERLAY_FS -o rw,nosuid,nodev,noatime,nobarrier  $OVERLAY_DEV  /overlay",
    )
    marker = "mount -t tmpfs tmpfs /tmp\n"
    insert = f"""mount -t tmpfs tmpfs /tmp

echo 'zero3: prepare image partition and overlay module' > /dev/kmsg
mkdir -p /image
for i in 1 2 3 4 5 6 7 8 9 10; do
  [ -e /dev/mmcblk0p2 ] && break
  sleep 1
done
mount -t vfat -o ro /dev/mmcblk0p2 /image || mount -t auto -o ro /dev/mmcblk0p2 /image
if [ -f /usr/lib/modules/{module_version}/kernel/fs/overlayfs/overlay.ko.xz ]; then
  insmod /usr/lib/modules/{module_version}/kernel/fs/overlayfs/overlay.ko.xz || echo 'zero3: insmod overlay failed' > /dev/kmsg
fi
"""
    text = text.replace(marker, insert, 1)
    for name in ["rootfs-base.squashfs", "kernel.squashfs", "apt.squashfs", "fw.squashfs", "oem.squashfs"]:
        text = text.replace(f" -o loop {name} ", f" -o loop /image/{name} ")
    debug_hash = "$6$ugoszero3$RzcRRvFVpH1gTjzDZ1hKwj.LtEHTqtDJPd7NMb9YLcAA24vL5icxLHWTMpyJKFtDYKnasNUzgIcWWvZqmBMBc0"
    runtime_register_script = '''cat > /mnt/ugreen/script/zero3-register-services.sh <<'ZERO3_REGISTER_EOF'
#!/bin/sh
set +e

mkdir -p /etc/sysconfig /etc/systemd/system /usr/lib/systemd/system /etc/nginx/conf.d /etc/nginx/http.d /var/targets /var/ugreen/log /usr/local/sbin /run/zero3-register /ugreen/www

for app in /ugreen/@appstore/com.ugreen.*; do
	[ -d "$app/init.d" ] && cp -f "$app"/init.d/*.service /etc/systemd/system/ 2>/dev/null || true
	for unit in "$app"/init.d/*.service; do
		[ -f "$unit" ] && ln -sfn "$unit" "/usr/lib/systemd/system/$(basename "$unit")"
	done
	for cfg in "$app"/init.d/*.sh; do
		[ -f "$cfg" ] && ln -sfn "$cfg" "/etc/sysconfig/$(basename "$cfg")"
	done
	[ -f "$app/www/index.html" ] && ln -sfn "$app/www" "/ugreen/www/${app##*.}"
	for cfg in "$app"/http.d/*; do
		[ -f "$cfg" ] || continue
		case "$cfg" in
			*.stream) ln -sfn "$cfg" "/etc/nginx/http.d/$(basename "$cfg")" ;;
			*.conf|*.cros) ln -sfn "$cfg" "/etc/nginx/conf.d/$(basename "$cfg")" ;;
		esac
	done
	if [ -d "$app/sbin" ]; then
		for bin in "$app"/sbin/*; do
			[ -f "$bin" ] && ln -sfn "$bin" "/var/targets/$(basename "$bin")"
		done
	fi
done
chmod +x /etc/sysconfig/*.sh /var/targets/* 2>/dev/null || true

cat > /etc/systemd/system/done.service <<'ZERO3_DONE_EOF'
[Unit]
Description=System start complete with Zero3 UGOS registration
DefaultDependencies=no
After=ugreen-basic.target

[Service]
Type=oneshot
Environment=ZERO3_START_SERVICES=min
ExecStart=/usr/local/sbin/zero3-ugos-seed.sh
ExecStart=/usr/local/sbin/zero3-ugos-install-core.sh
ExecStart=/ugreen/script/zero3-register-services.sh systemd
ExecStart=/usr/local/sbin/zero3-ugos-reload-core.sh
ExecStart=/usr/ugreen/sbin/done.sh
ExecStart=/usr/local/sbin/zero3-ugos-seed.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
ZERO3_DONE_EOF

echo v18-preinstall-debug > /etc/zero3-build-marker
echo "service_count=$(find /etc/systemd/system -maxdepth 1 -type f -name '*_serv.service' | wc -l)" > /run/zero3-register/status
if [ "$1" != "init" ]; then
	systemctl daemon-reload >/dev/null 2>&1 || true
	if [ "$ZERO3_START_SERVICES" = "1" ] || [ "$ZERO3_START_SERVICES" = "min" ]; then
		if [ "$ZERO3_START_SERVICES" = "min" ]; then
			services="ugbus.service redis-server.service ugreen-psql.service log_serv.service gateway_serv.service entry_serv.service ctl_serv.service storage_serv.service ugos_serv.service discovery_serv.service app_serv.service"
		else
			services="ugbus.service redis-server.service ugreen-psql.service log_serv.service gateway_serv.service entry_serv.service ctl_serv.service storage_serv.service ugos_serv.service app_serv.service index_serv.service discovery_serv.service filemgr_serv.service vmnt_serv.service"
		fi
		echo "start_mode=$ZERO3_START_SERVICES" >> /run/zero3-register/status
		for svc in $services; do
			echo "start $svc" >> /run/zero3-register/status
			systemctl start --no-block "$svc" >/dev/null 2>&1 || true
			sleep 1
		done
	fi
fi
exit 0
ZERO3_REGISTER_EOF
chmod +x /mnt/ugreen/script/zero3-register-services.sh
'''
    seed_scripts = f'''target="${{ZERO3_TARGET:-/mnt}}"
cat > "$target/usr/local/sbin/zero3-ugos-seed.sh" <<'ZERO3_SEED_EOF'
#!/bin/sh
set +e

MODEL_NAME="DH4300PLUS"
MODEL_SERIES="dh4300plus"
PRODUCT_SERIES="nasync"
COLOR="gray"
SN="UGOSOPIZERO3DF0D8E2E"
MAC="02:00:DF:0D:8E:2E"
HOSTNAME="UGOS-OPI-ZERO3"
HASH='{debug_hash}'

write_file() {{
	path="$1"
	value="$2"
	mkdir -p "$(dirname "$path")"
	printf '%s\\n' "$value" > "$path"
}}

seed_file() {{
	write_file "$1" "$2"
}}

mkdir -p /tmp/factory /ugreen/.config/.nas/system /ugreen/.config/.nas/config /run/zero3-dmi /tmp/.cache /usr/ugreen/etc/dmi /var/lib/ugos/dmi
mkdir -p /tmp/.nas /etc/zero3-dmi /etc/ugos-zero3/dmi

if [ -e /dev/mmcblk0p3 ] && ! grep -q ' /tmp/factory ' /proc/mounts; then
	blkid /dev/mmcblk0p3 | grep -q ext4 || mkfs.ext4 -F /dev/mmcblk0p3
	mount -t ext4 /dev/mmcblk0p3 /tmp/factory 2>/dev/null || true
fi

for prefix in /tmp/factory /ugreen/.config/.nas /ugreen/.config/.nas/system /ugreen/.config/.nas/config; do
	seed_file "$prefix/sn.txt" "$SN"
	seed_file "$prefix/serial_number" "$SN"
	seed_file "$prefix/model" "$MODEL_NAME"
	seed_file "$prefix/model.txt" "$MODEL_NAME"
	seed_file "$prefix/product_name" "$MODEL_NAME"
	seed_file "$prefix/model_series" "$MODEL_SERIES"
	seed_file "$prefix/product_series" "$PRODUCT_SERIES"
	seed_file "$prefix/device_color" "$COLOR"
	seed_file "$prefix/manufacturer" "UGREEN"
done
seed_file /tmp/factory/activation_key.txt "$SN"

cat > /run/zero3-dmi/sysinfo.json <<ZERO3_JSON
{{"cpu_model":"Allwinner H618","manufacturer":"UGREEN","product_name":"$MODEL_NAME","bios_version":"UGOS-ZERO3","serial_number":"$SN","uuid":"297f42ed-4333-43ea-9400-2cd3ee3e0184","wakeup_type":"","sku_number":"$MODEL_SERIES","color":"$COLOR"}}
ZERO3_JSON
for path in /tmp/.cache/dmi.json /tmp/.cache/sysinfo.json /tmp/.cache/dmi_sysinfo.json /usr/ugreen/etc/dmi/sysinfo.json /usr/ugreen/etc/sysinfo.json /var/lib/ugos/dmi/sysinfo.json /ugreen/.config/.nas/sysinfo.json /ugreen/.config/.nas/system/sysinfo.json; do
	mkdir -p "$(dirname "$path")"
	cp /run/zero3-dmi/sysinfo.json "$path" 2>/dev/null || true
done
cp /run/zero3-dmi/sysinfo.json /tmp/.cache/.board_cache 2>/dev/null || true
cp /run/zero3-dmi/sysinfo.json /tmp/.nas/sysinfo.json 2>/dev/null || true
printf '63\\n' > /tmp/.nas/sata_sw

cat > /etc/led.build <<ZERO3_LED
[led]
json = {{"info":[{{"days":[7,6],"timeConfig":[{{"time":[],"bright":100}}]}},{{"days":[1,2,3,4,5],"timeConfig":[{{"time":[],"bright":100}}]}}],"model":"$MODEL_NAME","status":1}}
ZERO3_LED

cat > /ugreen/.config/power.build <<ZERO3_POWER
[power]
json = {{"power_boot":false,"wake_on":false,"enable_scheduled_power":false,"time_switches":[],"hard_drive_flag":true,"hard_drive_unit":"M","hard_drive_time":20,"hard_drive_strategy":1,"hard_drive_target_info":{{"pools":null,"free_disks":null}},"hard_drive_scope":{{"excluded_pool_names":null,"excluded_disk_devs":null}},"usb_hard_drive_flag":true,"usb_hard_drive_unit":"M","usb_hard_drive_time":20,"usb_hard_drive_strategy":1,"usb_hard_drive_target_info":{{"pools":null,"free_disks":null}},"usb_hard_drive_scope":{{"excluded_pool_names":null,"excluded_disk_devs":null}},"enable_hard_drive_sleep_log":false}}
ZERO3_POWER

write_dmi() {{
	printf '%s\\n' "$2" > "/etc/ugos-zero3/dmi/$1"
}}
write_dmi sys_vendor UGREEN
write_dmi product_name "$MODEL_NAME"
write_dmi product_version "1.0"
write_dmi product_serial "$SN"
write_dmi product_sku "$MODEL_SERIES"
write_dmi product_family "$COLOR"
write_dmi board_vendor UGREEN
write_dmi board_name "$MODEL_NAME"
write_dmi board_version "1.0"
write_dmi board_serial "$SN"
write_dmi chassis_vendor UGREEN
write_dmi chassis_type 3
write_dmi chassis_version "1.0"
write_dmi chassis_serial "$SN"
write_dmi bios_vendor UGREEN
write_dmi bios_version "UGOS-ZERO3"
write_dmi bios_date "06/26/2026"

for f in sys_vendor product_name product_version product_serial product_sku product_family board_vendor board_name board_version board_serial chassis_vendor chassis_type chassis_version chassis_serial bios_vendor bios_version bios_date; do
	[ -e "/sys/class/dmi/id/$f" ] || continue
	mountpoint -q "/sys/class/dmi/id/$f" 2>/dev/null && continue
	mount --bind "/etc/ugos-zero3/dmi/$f" "/sys/class/dmi/id/$f" 2>/dev/null || true
done

printf 'UGREEN %s\\0' "$MODEL_NAME" > /run/zero3-dmi/model
printf '%s\\0' "$SN" > /run/zero3-dmi/serial-number
for target in /proc/device-tree/model /sys/firmware/devicetree/base/model; do
	[ -e "$target" ] && mount --bind /run/zero3-dmi/model "$target" 2>/dev/null || true
done
for target in /proc/device-tree/serial-number /sys/firmware/devicetree/base/serial-number; do
	[ -e "$target" ] && mount --bind /run/zero3-dmi/serial-number "$target" 2>/dev/null || true
done

printf '%s\\n' "$HOSTNAME" > /etc/hostname
hostname "$HOSTNAME" 2>/dev/null || true
if [ -f /etc/shadow ]; then
	sed -i "s#^root:[^:]*:#root:$HASH:#" /etc/shadow
	grep -q '^debug:' /etc/passwd || echo 'debug:x:1000:1000:UGOS Zero3 Debug:/home/debug:/bin/bash' >> /etc/passwd
	grep -q '^debug:' /etc/group || echo 'debug:x:1000:' >> /etc/group
	grep -q '^debug:' /etc/shadow || echo "debug:$HASH:19723:0:99999:7:::" >> /etc/shadow
	mkdir -p /home/debug
	chown 1000:1000 /home/debug 2>/dev/null || true
fi
exit 0
ZERO3_SEED_EOF

cat > "$target/usr/local/sbin/zero3-ugos-start-services.sh" <<'ZERO3_START_EOF'
#!/bin/sh
set +e
/usr/local/sbin/zero3-ugos-seed.sh || true
mkdir -p /etc/sysconfig /etc/systemd/system /usr/lib/systemd/system /etc/systemd/system/ugreen-basic.target.wants /etc/nginx/conf.d /etc/nginx/http.d /var/targets /var/ugreen/log /var/ugreen/run /run/cache/pkgs /ugreen/www
for app in /ugreen/@appstore/com.ugreen.*; do
	[ -d "$app/init.d" ] && cp -f "$app"/init.d/*.service /etc/systemd/system/ 2>/dev/null || true
	for unit in "$app"/init.d/*.service; do
		[ -f "$unit" ] && ln -sfn "$unit" "/usr/lib/systemd/system/$(basename "$unit")"
	done
	for cfg in "$app"/init.d/*.sh; do
		[ -f "$cfg" ] && ln -sfn "$cfg" "/etc/sysconfig/$(basename "$cfg")"
	done
	[ -f "$app/www/index.html" ] && ln -sfn "$app/www" "/ugreen/www/${{app##*.}}"
	for cfg in "$app"/http.d/*; do
		[ -f "$cfg" ] || continue
		case "$cfg" in
			*.stream) ln -sfn "$cfg" "/etc/nginx/http.d/$(basename "$cfg")" ;;
			*.conf|*.cros) ln -sfn "$cfg" "/etc/nginx/conf.d/$(basename "$cfg")" ;;
		esac
	done
	if [ -d "$app/sbin" ]; then
		for bin in "$app"/sbin/*; do
			[ -f "$bin" ] && ln -sfn "$bin" "/var/targets/$(basename "$bin")"
		done
	fi
done
chmod +x /etc/sysconfig/*.sh /var/targets/* 2>/dev/null || true
systemctl daemon-reload >/dev/null 2>&1 || true
if [ "$ZERO3_START_SERVICES" = "1" ]; then
	for svc in ugbus.service redis-server.service ugreen-psql.service log_serv.service gateway_serv.service entry_serv.service ctl_serv.service storage_serv.service ugos_serv.service app_serv.service index_serv.service discovery_serv.service filemgr_serv.service vmnt_serv.service; do
		systemctl start --no-block "$svc" >/dev/null 2>&1 || true
	done
elif [ "$ZERO3_START_SERVICES" = "min" ]; then
	for svc in ugbus.service redis-server.service ugreen-psql.service log_serv.service gateway_serv.service entry_serv.service ctl_serv.service ugos_serv.service discovery_serv.service app_serv.service; do
		systemctl start --no-block "$svc" >/dev/null 2>&1 || true
		sleep 1
	done
fi
exit 0
ZERO3_START_EOF

cat > "$target/usr/local/sbin/zero3-ugos-install-core.sh" <<'ZERO3_INSTALL_CORE_EOF'
#!/bin/sh
set +e

LOG=/var/ugreen/log/zero3-uginstall.log
mkdir -p /run/cache/pkgs /var/lib/ugb /var/ugreen/log /etc/nginx/conf.d
/usr/local/sbin/zero3-ugos-seed.sh >> "$LOG" 2>&1 || true

install_upk() {{
	app_id="$1"
	upk="$2"
	if [ -f "/var/lib/ugb/$app_id/config.json" ]; then
		echo "skip $app_id" >> "$LOG"
		return 0
	fi
	if [ ! -f "$upk" ]; then
		echo "missing $upk" >> "$LOG"
		return 0
	fi
	echo "install $app_id from $upk" >> "$LOG"
	/usr/sbin/uginstall -upk "$upk" -task 1 >> "$LOG" 2>&1 || echo "install failed $app_id" >> "$LOG"
}}

install_upk com.ugreen.logmgr /ugreen/@cache/01_arm64_com.ugreen.logmgr.upk
install_upk com.ugreen.gateway_pro /ugreen/@cache/02_arm64_com.ugreen.gateway_pro.upk
install_upk com.ugreen.ctlmgr /ugreen/@cache/05_arm64_com.ugreen.ctlmgr.upk
install_upk com.ugreen.desktop /ugreen/@cache/06_arm64_com.ugreen.desktop.upk
install_upk com.ugreen.wizard /ugreen/@cache/07_arm64_com.ugreen.wizard.upk
install_upk com.ugreen.appmgr /ugreen/@cache/09_arm64_com.ugreen.appmgr.upk
install_upk com.ugreen.ctlmgr.index /ugreen/@cache/10_arm64_com.ugreen.ctlmgr.index.upk
install_upk com.ugreen.ugos_serv /ugreen/@cache/19_arm64_com.ugreen.ugos_serv.upk

echo done > /run/zero3-core-install.done
exit 0
ZERO3_INSTALL_CORE_EOF

cat > "$target/usr/local/sbin/zero3-ugos-reload-core.sh" <<'ZERO3_RELOAD_CORE_EOF'
#!/bin/sh
set +e

LOG=/var/ugreen/log/zero3-reload-core.log
mkdir -p /var/ugreen/log /run/zero3-register
echo "reload begin $(date -Iseconds 2>/dev/null)" >> "$LOG"
/usr/local/sbin/zero3-ugos-seed.sh >> "$LOG" 2>&1 || true
systemctl daemon-reload >> "$LOG" 2>&1 || true

for svc in ugbus.service redis-server.service ugreen-psql.service log_serv.service; do
	echo "ensure $svc" >> "$LOG"
	systemctl start "$svc" >> "$LOG" 2>&1 || true
	sleep 1
done

for svc in entry_serv.service ctl_serv.service ugos_serv.service discovery_serv.service app_serv.service gateway_serv.service; do
	echo "restart $svc" >> "$LOG"
	systemctl restart "$svc" >> "$LOG" 2>&1 || systemctl start "$svc" >> "$LOG" 2>&1 || true
	sleep 3
	systemctl is-active "$svc" >> "$LOG" 2>&1 || true
done

if command -v nginx >/dev/null 2>&1; then
	nginx -t >> "$LOG" 2>&1 && systemctl reload nginx >> "$LOG" 2>&1 || systemctl restart nginx >> "$LOG" 2>&1 || true
fi

echo done > /run/zero3-reload-core.done
echo "reload end $(date -Iseconds 2>/dev/null)" >> "$LOG"
exit 0
ZERO3_RELOAD_CORE_EOF

chmod +x "$target/usr/local/sbin/zero3-ugos-seed.sh" "$target/usr/local/sbin/zero3-ugos-start-services.sh" "$target/usr/local/sbin/zero3-ugos-install-core.sh" "$target/usr/local/sbin/zero3-ugos-reload-core.sh"

cat > "$target/etc/systemd/system/zero3-ugos-seed.service" <<'ZERO3_SEED_UNIT_EOF'
[Unit]
Description=Seed Orange Pi Zero 3 UGOS device identity
DefaultDependencies=no
After=local-fs.target
Before=basic.target discovery_serv.service gateway_serv.service entry_serv.service ctl_serv.service app_serv.service

[Service]
Type=oneshot
ExecStart=/usr/local/sbin/zero3-ugos-seed.sh
RemainAfterExit=yes

[Install]
WantedBy=basic.target
ZERO3_SEED_UNIT_EOF

cat > "$target/etc/systemd/system/zero3-ugos-start-services.service" <<'ZERO3_START_UNIT_EOF'
[Unit]
Description=Register UGOS app services on Orange Pi Zero 3
After=network.target zero3-ugos-seed.service
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/local/sbin/zero3-ugos-start-services.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
ZERO3_START_UNIT_EOF

mkdir -p "$target/etc/systemd/system/basic.target.wants" "$target/etc/systemd/system/multi-user.target.wants"
ln -sf ../zero3-ugos-seed.service "$target/etc/systemd/system/basic.target.wants/zero3-ugos-seed.service"
rm -f "$target/etc/systemd/system/multi-user.target.wants/zero3-ugos-start-services.service"
'''
    switch_root_tail = f'''
	echo "---zero3 switch_root path :" > /dev/kmsg

	[ -d /mnt/rom ] ||  mkdir -p /mnt/rom
	[ -d /mnt/rootfs ] ||  mkdir -p /mnt/rootfs
	[ -d /mnt/sys ] ||  mkdir -p /mnt/sys
	[ -d /mnt/run ] ||  mkdir -p /mnt/run
	[ -d /mnt/proc ] ||  mkdir -p /mnt/proc
	[ -d /mnt/dev ] ||  mkdir -p /mnt/dev
	[ -d /mnt/tmp ] ||  mkdir -p /mnt/tmp
	[ -d /mnt/boot ] ||  mkdir -p /mnt/boot
	[ -d /mnt/ugreen ] ||  mkdir -p /mnt/ugreen
	[ -d /mnt/overlay ] ||  mkdir -p /mnt/overlay
	echo "---zero3 postpone factory identity seed until target root is ready" > /dev/kmsg

	TFSTYPE=$(blkid /dev/mmcblk0p6 | grep -o ext4)
	if [ ! -n "$TFSTYPE" ]; then
		mkfs.ext4 -F /dev/mmcblk0p6
	fi
	TFSTYPE=$(blkid /dev/mmcblk0p6 | grep -o ext4)
	if [ -n "$TFSTYPE" ]; then
		e2fsck -f -y /dev/mmcblk0p6
		mount -t ext4 /dev/mmcblk0p6 /mnt/ugreen
		if [ -f /image/ugreen.bz2 ] && [ ! -f /mnt/ugreen/.zero3_ugreen_payload_extracted ]; then
			echo "---zero3 extract ugreen payload :" > /dev/kmsg
			tar -xf /image/ugreen.bz2 -C /mnt/ugreen && touch /mnt/ugreen/.zero3_ugreen_payload_extracted
		fi
		if [ -f /image/core-preinstall.tar.gz ] && [ ! -f /mnt/ugreen/.zero3_core_preinstall_extracted ]; then
			echo "---zero3 extract core preinstall payload :" > /dev/kmsg
			tar -xzf /image/core-preinstall.tar.gz -C /mnt && touch /mnt/ugreen/.zero3_core_preinstall_extracted
		fi
		mkdir -p /mnt/ugreen/.config/.nas/system /mnt/ugreen/.config/.nas/config
		echo 'UGOSOPIZERO3DF0D8E2E' > /mnt/ugreen/.config/.nas/sn.txt
		echo 'UGOSOPIZERO3DF0D8E2E' > /mnt/ugreen/.config/.nas/serial_number
		echo 'DH4300PLUS' > /mnt/ugreen/.config/.nas/model
		echo 'dh4300plus' > /mnt/ugreen/.config/.nas/model_series
		echo 'nasync' > /mnt/ugreen/.config/.nas/product_series
		echo 'gray' > /mnt/ugreen/.config/.nas/device_color
		echo 'UGOSOPIZERO3DF0D8E2E' > /mnt/ugreen/.config/.nas/system/sn.txt
		echo 'DH4300PLUS' > /mnt/ugreen/.config/.nas/system/model
		[ -d /mnt/ugreen/script ] || mkdir -p /mnt/ugreen/script
		{runtime_register_script}
	else
		echo 'zero3: ugreen dev fstype error' > /dev/kmsg
	fi

	if [ -e /dev/mmcblk0p5 ]; then
		blkid /dev/mmcblk0p5 | grep -q swap || mkswap /dev/mmcblk0p5
		swapon /dev/mmcblk0p5 || echo 'zero3: swapon p5 failed' > /dev/kmsg
	fi

	echo "---zero3 register ugreen app service files" > /dev/kmsg
	ROOT=/mnt
	[ -d "$ROOT/etc/sysconfig" ] || mkdir -p "$ROOT/etc/sysconfig"
	[ -d "$ROOT/etc/systemd/system" ] || mkdir -p "$ROOT/etc/systemd/system"
	[ -d "$ROOT/etc/systemd/system/basic.target.wants" ] || mkdir -p "$ROOT/etc/systemd/system/basic.target.wants"
	[ -d "$ROOT/etc/systemd/system/multi-user.target.wants" ] || mkdir -p "$ROOT/etc/systemd/system/multi-user.target.wants"
	[ -d "$ROOT/etc/systemd/system/ugreen-basic.target.wants" ] || mkdir -p "$ROOT/etc/systemd/system/ugreen-basic.target.wants"
	[ -d "$ROOT/usr/local/sbin" ] || mkdir -p "$ROOT/usr/local/sbin"
	[ -d "$ROOT/var/targets" ] || mkdir -p "$ROOT/var/targets"
	[ -d "$ROOT/var/ugreen/log" ] || mkdir -p "$ROOT/var/ugreen/log"
	mkdir -p "$ROOT/etc/nginx/conf.d" "$ROOT/etc/nginx/http.d" "$ROOT/usr/lib/systemd/system" /mnt/ugreen/www
	for app in /mnt/ugreen/@appstore/com.ugreen.*; do
		app_target="${{app#/mnt}}"
		[ -d "$app/init.d" ] && cp -f "$app"/init.d/*.service "$ROOT/etc/systemd/system/" 2>/dev/null || true
		for unit in "$app"/init.d/*.service; do
			[ -f "$unit" ] && ln -sfn "${{unit#/mnt}}" "$ROOT/usr/lib/systemd/system/$(basename "$unit")"
		done
		for cfg in "$app"/init.d/*.sh; do
			[ -f "$cfg" ] && ln -sfn "${{cfg#/mnt}}" "$ROOT/etc/sysconfig/$(basename "$cfg")"
		done
		[ -f "$app/www/index.html" ] && ln -sfn "$app_target/www" "/mnt/ugreen/www/${{app##*.}}"
		for cfg in "$app"/http.d/*; do
			[ -f "$cfg" ] || continue
			case "$cfg" in
				*.stream) ln -sfn "${{cfg#/mnt}}" "$ROOT/etc/nginx/http.d/$(basename "$cfg")" ;;
				*.conf|*.cros) ln -sfn "${{cfg#/mnt}}" "$ROOT/etc/nginx/conf.d/$(basename "$cfg")" ;;
			esac
		done
		if [ -d "$app/sbin" ]; then
			for bin in "$app"/sbin/*; do
				[ -f "$bin" ] && ln -sfn "$app_target/sbin/$(basename "$bin")" "$ROOT/var/targets/$(basename "$bin")"
			done
		fi
	done
	chmod +x "$ROOT/etc/sysconfig/"*.sh "$ROOT/var/targets/"* 2>/dev/null || true
	echo 'v18-preinstall-debug' > "$ROOT/etc/zero3-build-marker"
	echo "zero3: registered service files $(ls "$ROOT/etc/systemd/system/"*_serv.service 2>/dev/null | wc -l)" > /dev/kmsg
	ZERO3_TARGET="$ROOT"
	{seed_scripts}
	echo "---zero3 chroot register services" > /dev/kmsg
	chroot /mnt /ugreen/script/zero3-register-services.sh init || echo 'zero3: chroot register failed' > /dev/kmsg
	echo "zero3: chroot registered service files $(ls /mnt/etc/systemd/system/*_serv.service 2>/dev/null | wc -l)" > /dev/kmsg

	mount --move /rom /mnt/rom
	mount --move /proc /mnt/proc || mount -t proc proc /mnt/proc
	mount --move /sys /mnt/sys || mount -t sysfs sysfs /mnt/sys
	mount --move /dev /mnt/dev || mount -t devtmpfs devtmpfs /mnt/dev
	mount --move /tmp /mnt/tmp || mount -t tmpfs tmpfs /mnt/tmp
	mount --move /overlay /mnt/overlay || echo 'zero3: overlay move skipped' > /dev/kmsg
	mount -t tmpfs tmpfs /mnt/run || true

	export LOG_OUTPUT=FILE
	export LOG_DIR=/mnt/var/ugreen/log
	[ ! -d "$LOG_DIR" ] && mkdir -p $LOG_DIR

	echo "---zero3 set debug login password" > /dev/kmsg
	if [ -f /mnt/etc/shadow ]; then
		sed -i 's#^root:[^:]*:#root:{debug_hash}:#' /mnt/etc/shadow
		grep -q '^debug:' /mnt/etc/passwd || echo 'debug:x:1000:1000:UGOS Zero3 Debug:/home/debug:/bin/bash' >> /mnt/etc/passwd
		grep -q '^debug:' /mnt/etc/group || echo 'debug:x:1000:' >> /mnt/etc/group
		grep -q '^debug:' /mnt/etc/shadow || echo 'debug:{debug_hash}:19723:0:99999:7:::' >> /mnt/etc/shadow
		[ -d /mnt/home/debug ] || mkdir -p /mnt/home/debug
		chown 1000:1000 /mnt/home/debug 2>/dev/null || true
	fi

	echo "---zero3 install seed services" > /dev/kmsg
	[ -d /mnt/usr/local/sbin ] || mkdir -p /mnt/usr/local/sbin
	[ -d /mnt/etc/systemd/system ] || mkdir -p /mnt/etc/systemd/system
	{seed_scripts}
	chroot /mnt /usr/local/sbin/zero3-ugos-seed.sh || echo 'zero3: seed script failed' > /dev/kmsg

	echo "---zero3 skip generic ugreen installer; core upk install runs under systemd" > /dev/kmsg
	chroot /mnt /usr/sbin/mcu_ota_upgrader || echo 'zero3: mcu upgrader skipped' > /dev/kmsg

	echo "---zero3 exec switch_root /mnt /lib/systemd/systemd" > /dev/kmsg
	exec switch_root /mnt /lib/systemd/systemd
	echo "---zero3 switch_root failed" > /dev/kmsg
	exec sh
'''
    for marker in ['\techo "---go move proc :" > /dev/kmsg', 'echo "---go move proc :" > /dev/kmsg']:
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx] + switch_root_tail
            break
    return text


class NewcWriter:
    def __init__(self):
        self.buf = io.BytesIO()
        self.ino = 1

    def _pad4(self):
        pad = (-self.buf.tell()) % 4
        if pad:
            self.buf.write(b"\x00" * pad)

    def add(self, name: str, mode: int, data: bytes = b"", *, nlink: int = 1, mtime: int = 0):
        name = name.strip("/")
        if not name:
            return
        namesize = len(name.encode("utf-8")) + 1
        fields = [
            self.ino,
            mode,
            0,
            0,
            nlink,
            mtime,
            len(data),
            0,
            0,
            0,
            0,
            namesize,
            0,
        ]
        self.ino += 1
        header = "070701" + "".join(f"{field:08x}" for field in fields)
        self.buf.write(header.encode("ascii"))
        self.buf.write(name.encode("utf-8") + b"\x00")
        self._pad4()
        self.buf.write(data)
        self._pad4()

    def finish(self) -> bytes:
        self.add("TRAILER!!!", 0, b"")
        return self.buf.getvalue()


def normalize_tar_name(name: str) -> str:
    while name.startswith("./"):
        name = name[2:]
    return name.strip("/")


def build_initrd(project_dir: Path, out_path: Path, module_version: str) -> dict:
    initfs = project_dir / "payload" / "initfs.tar.gz"
    overlay_module = (
        project_dir
        / "staging"
        / "orangepi-zero3-rootfs-overlay"
        / "usr"
        / "lib"
        / "modules"
        / module_version
        / "kernel"
        / "fs"
        / "overlayfs"
        / "overlay.ko.xz"
    )
    require_file(initfs, "UGOS initfs.tar.gz")
    require_file(overlay_module, "Orange Pi Zero 3 overlay.ko.xz")

    writer = NewcWriter()
    symlink_count = 0
    hardlink_as_symlink_count = 0
    regular_count = 0
    dir_count = 0
    patched_init = False

    with tarfile.open(initfs, "r:gz") as tar:
        for member in tar.getmembers():
            name = normalize_tar_name(member.name)
            if not name:
                continue
            mtime = int(member.mtime or 0)
            if member.isdir():
                writer.add(name, 0o040000 | (member.mode & 0o777), b"", nlink=2, mtime=mtime)
                dir_count += 1
            elif member.issym():
                writer.add(name, 0o120000 | 0o777, member.linkname.encode("utf-8"), mtime=mtime)
                symlink_count += 1
            elif member.islnk():
                target = normalize_tar_name(member.linkname)
                writer.add(name, 0o120000 | 0o777, f"/{target}".encode("utf-8"), mtime=mtime)
                hardlink_as_symlink_count += 1
            elif member.isfile():
                extracted = tar.extractfile(member)
                data = extracted.read() if extracted is not None else b""
                if name == "usr/sbin/init":
                    data = patch_init_script(data.decode("utf-8", errors="replace"), module_version).encode("utf-8")
                    patched_init = True
                mode = 0o100000 | (member.mode & 0o777)
                writer.add(name, mode, data, mtime=mtime)
                regular_count += 1

    now = int(time.time())
    module_dirs = [
        "usr/lib/modules",
        f"usr/lib/modules/{module_version}",
        f"usr/lib/modules/{module_version}/kernel",
        f"usr/lib/modules/{module_version}/kernel/fs",
        f"usr/lib/modules/{module_version}/kernel/fs/overlayfs",
    ]
    for name in module_dirs:
        writer.add(name, 0o040755, b"", nlink=2, mtime=now)
    writer.add(
        f"usr/lib/modules/{module_version}/kernel/fs/overlayfs/overlay.ko.xz",
        0o100644,
        overlay_module.read_bytes(),
        mtime=now,
    )
    writer.add("init", 0o100755, b"#!/bin/sh\nexec /usr/sbin/init \"$@\"\n", mtime=now)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    raw = writer.finish()
    out_path.write_bytes(gzip.compress(raw, compresslevel=6, mtime=0))
    return {
        "initrd": str(out_path),
        "initrd_bytes": out_path.stat().st_size,
        "raw_cpio_bytes": len(raw),
        "patched_init": patched_init,
        "regular_files": regular_count,
        "directories": dir_count,
        "symlinks": symlink_count,
        "hardlinks_converted_to_symlinks": hardlink_as_symlink_count,
        "overlay_module": str(overlay_module),
    }


def partition_entry(part_type: int, start_lba: int, sectors: int, bootable: bool = False) -> bytes:
    entry = bytearray(16)
    entry[0] = 0x80 if bootable else 0x00
    entry[1:4] = b"\xFE\xFF\xFF"
    entry[4] = part_type
    entry[5:8] = b"\xFE\xFF\xFF"
    struct.pack_into("<I", entry, 8, start_lba)
    struct.pack_into("<I", entry, 12, sectors)
    return bytes(entry)


def write_mbr_and_ebr(image: Path, disk_signature: int, primary: list[dict], logicals: list[dict]) -> list[dict]:
    mbr = bytearray(SECTOR_SIZE)
    struct.pack_into("<I", mbr, 440, disk_signature)
    for index, part in enumerate(primary[:4]):
        mbr[446 + index * 16 : 446 + (index + 1) * 16] = partition_entry(
            part["type"], part["start_lba"], part["sectors"], part.get("bootable", False)
        )
    mbr[510:512] = b"\x55\xAA"

    with image.open("r+b") as f:
        f.seek(0)
        f.write(mbr)
        extended = primary[3]
        ext_start = extended["start_lba"]
        ext_end = ext_start + extended["sectors"]
        for idx, logical in enumerate(logicals):
            ebr_lba = logical["ebr_lba"]
            ebr = bytearray(SECTOR_SIZE)
            ebr[446:462] = partition_entry(logical["type"], logical["start_lba"] - ebr_lba, logical["sectors"])
            if idx + 1 < len(logicals):
                next_ebr = logicals[idx + 1]["ebr_lba"]
                ebr[462:478] = partition_entry(0x0F, next_ebr - ext_start, ext_end - next_ebr)
            ebr[510:512] = b"\x55\xAA"
            f.seek(ebr_lba * SECTOR_SIZE)
            f.write(ebr)
    return primary + logicals


def layout_partitions() -> tuple[list[dict], list[dict], int]:
    lba = 16 * 1024 * 1024 // SECTOR_SIZE
    p1 = {"number": 1, "type": 0x0C, "type_name": "W95 FAT32 LBA boot", "start_lba": lba, "sectors": 512 * 1024 * 1024 // SECTOR_SIZE, "bootable": True}
    lba = align_up(p1["start_lba"] + p1["sectors"], 2048)
    p2 = {"number": 2, "type": 0x0C, "type_name": "W95 FAT32 LBA UGOS images", "start_lba": lba, "sectors": 2304 * 1024 * 1024 // SECTOR_SIZE}
    lba = align_up(p2["start_lba"] + p2["sectors"], 2048)
    p3 = {"number": 3, "type": 0x83, "type_name": "Linux factory", "start_lba": lba, "sectors": 32 * 1024 * 1024 // SECTOR_SIZE}
    ext_start = align_up(p3["start_lba"] + p3["sectors"], 2048)

    logical_specs = [
        (5, 0x82, "Linux swap", 1024),
        (6, 0x83, "Linux /ugreen", 2048),
        (7, 0x83, "Linux reserved", 64),
        (8, 0x83, "Linux reserved", 64),
        (9, 0x83, "Linux overlay", 2048),
    ]
    logicals = []
    ebr_lba = ext_start
    for number, part_type, type_name, mib in logical_specs:
        data_lba = ebr_lba + 2048
        sectors = mib * 1024 * 1024 // SECTOR_SIZE
        logicals.append(
            {
                "number": number,
                "type": part_type,
                "type_name": type_name,
                "ebr_lba": ebr_lba,
                "start_lba": data_lba,
                "sectors": sectors,
            }
        )
        ebr_lba = align_up(data_lba + sectors, 2048)
    ext_end = ebr_lba
    p4 = {"number": 4, "type": 0x0F, "type_name": "W95 Ext'd LBA", "start_lba": ext_start, "sectors": ext_end - ext_start}
    primary = [p1, p2, p3, p4]
    return primary, logicals, ext_end * SECTOR_SIZE


def make_boot_tree(base, project_dir: Path, root_partuuid: str, cmdline_extra: str, initrd: Path):
    bootfs = project_dir / "staging" / "orangepi-zero3-bootfs"
    image = bootfs / "Image"
    dtb = bootfs / "dtb" / "allwinner" / "sun50i-h618-orangepi-zero3.dtb"
    require_file(image, "Orange Pi Zero 3 kernel Image")
    require_file(dtb, "Orange Pi Zero 3 DTB")
    bootargs = f"console=ttyS0,115200 console=tty0 root=/dev/ram0 rootwait overlay=/dev/mmcblk0p9 overlayfs=ext4 earlycon loglevel=7 net.ifnames=0 biosdevname=0 panic=10 {cmdline_extra}".strip()
    extlinux = f"""TIMEOUT 30
DEFAULT UGOS-ZERO3-LAYOUT

LABEL UGOS-ZERO3-LAYOUT
  LINUX /Image
  INITRD /initrd.gz
  FDT /dtb/allwinner/sun50i-h618-orangepi-zero3.dtb
  APPEND {bootargs}
"""
    boot_cmd = f"""setenv ugos_dtb /dtb/allwinner/sun50i-h618-orangepi-zero3.dtb
setenv ugos_kernel /Image
setenv ugos_initrd /initrd.gz
setenv bootargs {bootargs}
echo Loading UGOS Zero3 layout fallback boot script
load ${{devtype}} ${{devnum}}:${{distro_bootpart}} ${{ramdisk_addr_r}} ${{ugos_initrd}}
setenv ugos_initrd_size ${{filesize}}
load ${{devtype}} ${{devnum}}:${{distro_bootpart}} ${{kernel_addr_r}} ${{ugos_kernel}}
load ${{devtype}} ${{devnum}}:${{distro_bootpart}} ${{fdt_addr_r}} ${{ugos_dtb}}
fdt addr ${{fdt_addr_r}}
fdt resize 65536
booti ${{kernel_addr_r}} ${{ramdisk_addr_r}}:${{ugos_initrd_size}} ${{fdt_addr_r}}
"""
    readme = f"""UGOS Pro ARM Orange Pi Zero 3 layout debug image

This image boots with a patched UGOS initramfs.
It mounts /dev/mmcblk0p2 at /image, reads UGOS squashfs files from there, formats p9 as overlay, and then pivots into UGOS.
Root/boot PARTUUID marker: {root_partuuid}
"""
    root = base.FatNode("", True)
    base.add_file(root, "Image", source=image)
    base.add_file(root, "initrd.gz", source=initrd)
    base.add_file(root, "dtb/allwinner/sun50i-h618-orangepi-zero3.dtb", source=dtb)
    base.add_file(root, "extlinux/extlinux.conf", data=extlinux.encode("ascii"))
    base.add_file(root, "boot/extlinux/extlinux.conf", data=extlinux.encode("ascii"))
    boot_scr = base.make_uboot_script_image(boot_cmd, name="UGOS-ZERO3-LAYOUT")
    base.add_file(root, "boot.cmd", data=boot_cmd.encode("ascii"))
    base.add_file(root, "boot.scr", data=boot_scr)
    base.add_file(root, "boot.scr.uimg", data=boot_scr)
    base.add_file(root, "README-UGOS-ZERO3-LAYOUT.txt", data=readme.encode("ascii"))
    return root


def make_image_tree(base, project_dir: Path):
    payload = project_dir / "payload"
    preinstall = project_dir / "staging" / "core-preinstall" / "core-preinstall.tar.gz"
    names = ["rootfs-base.squashfs", "kernel.squashfs", "apt.squashfs", "fw.squashfs", "oem.squashfs", "ugreen.bz2"]
    root = base.FatNode("", True)
    for name in names:
        path = payload / name
        require_file(path, f"UGOS {name}")
        base.add_file(root, name, source=path)
    require_file(preinstall, "UGOS Zero3 core preinstall tarball")
    base.add_file(root, "core-preinstall.tar.gz", source=preinstall)
    names.append("core-preinstall.tar.gz")
    base.add_file(
        root,
        "README-UGOS-IMAGES.txt",
        data=b"UGOS squashfs payloads and /ugreen tar payload for the patched Orange Pi Zero 3 initramfs.\n",
    )
    return root, names


def copy_into(src: Path, dst: Path, offset: int, chunk_size: int = 1024 * 1024) -> None:
    with src.open("rb") as inf, dst.open("r+b") as outf:
        outf.seek(offset)
        shutil.copyfileobj(inf, outf, chunk_size)


def cleanup_old_desktop_images(out_image: Path, manifest_path: Path, sha_path: Path) -> list[str]:
    current = {out_image.name, manifest_path.name, sha_path.name}
    removed = []
    if out_image.parent.name.lower() != "img":
        return removed
    for old in out_image.parent.glob("ugos-opi-zero3-layout-debug-v*.img*"):
        if old.name in current:
            continue
        try:
            old.unlink()
            removed.append(str(old))
        except OSError:
            pass
    return removed


def main():
    parser = argparse.ArgumentParser(description="Build a UGOS layout-style Orange Pi Zero 3 debug image.")
    parser.add_argument("--project-dir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--out-image", default=None)
    parser.add_argument("--module-version", default="6.18.37-current-sunxi64")
    parser.add_argument("--disk-signature", default="0x55473044")
    parser.add_argument("--cmdline-extra", default="ip=dhcp systemd.show_status=1 systemd.log_level=debug ignore_loglevel")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    base = load_base_builder(project_dir)
    out_image = Path(args.out_image).resolve() if args.out_image else Path.home() / "Desktop" / "img" / "ugos-opi-zero3-layout-debug-v18-preinstall-debug.img"
    work_dir = project_dir / "work" / "layout-debug-image"
    boot_part = work_dir / "boot-fat32.img"
    image_part = work_dir / "ugos-images-fat32.img"
    initrd = work_dir / "initrd.gz"
    manifest_path = out_image.with_suffix(out_image.suffix + ".manifest.json")
    sha_path = out_image.with_suffix(out_image.suffix + ".sha256")

    disk_signature = int(args.disk_signature, 16 if str(args.disk_signature).lower().startswith("0x") else 10)
    root_partuuid = f"{disk_signature:08x}-01"

    subprocess.run(
        [sys.executable, str(project_dir / "scripts" / "build-core-preinstall.py"), "--project-dir", str(project_dir)],
        check=True,
    )
    initrd_info = build_initrd(project_dir, initrd, args.module_version)
    primary, logicals, image_size = layout_partitions()

    boot_tree = make_boot_tree(base, project_dir, root_partuuid, args.cmdline_extra.strip(), initrd)
    image_tree, image_files = make_image_tree(base, project_dir)
    base.build_fat32_image(boot_part, boot_tree, primary[0]["sectors"], primary[0]["start_lba"], disk_signature)
    base.build_fat32_image(image_part, image_tree, primary[1]["sectors"], primary[1]["start_lba"], disk_signature ^ 0x2222)

    bootloader = project_dir / "staging" / "orangepi-zero3-bootloader" / "u-boot-sunxi-with-spl.bin"
    require_file(bootloader, "Orange Pi Zero 3 U-Boot/SPL")

    out_image.parent.mkdir(parents=True, exist_ok=True)
    with out_image.open("wb") as f:
        f.truncate(image_size)
    partitions = write_mbr_and_ebr(out_image, disk_signature, primary, logicals)
    copy_into(bootloader, out_image, 8 * 1024)
    copy_into(boot_part, out_image, primary[0]["start_lba"] * SECTOR_SIZE)
    copy_into(image_part, out_image, primary[1]["start_lba"] * SECTOR_SIZE)

    with out_image.open("rb") as vf:
        mbr = vf.read(SECTOR_SIZE)
        vf.seek(8 * 1024)
        spl_head = vf.read(16)
    digest = base.sha256_file(out_image)
    sha_path.write_text(f"{digest}  {out_image.name}\n", encoding="ascii")
    manifest = {
        "image": str(out_image),
        "image_bytes": image_size,
        "sha256": digest,
        "disk_signature": f"0x{disk_signature:08x}",
        "bootloader": str(bootloader),
        "bootloader_write_offset": 8 * 1024,
        "cmdline_extra": args.cmdline_extra.strip(),
        "initrd": initrd_info,
        "partitions": partitions,
        "ugos_image_partition_files": image_files,
        "verification": {
            "mbr_signature_ok": mbr[510:512] == b"\x55\xAA",
            "uboot_egon_at_8k": b"eGON.BT0" in spl_head,
        },
        "notes": [
            "Layout image: p2 stores UGOS squashfs files plus ugreen.bz2, p3/p6/p9 are created for UGOS init.",
            "Patched initramfs extracts ugreen.bz2 into p6 /ugreen on first boot and enables p5 swap.",
            "Patched initramfs mounts p6 and enables p5 before moving /dev into the target root.",
            "Patched initramfs removes quota mount options from the p9 overlay mount for Orange Pi Zero 3 kernel compatibility.",
            "Patched initramfs postpones p3 factory identity seeding until target /dev, /proc, and /tmp are ready.",
            "Patched initramfs writes a persistent /ugreen/script/zero3-register-services.sh helper and runs it through chroot /mnt.",
            "done.service is overridden to seed x86-style identity caches, install core UPKs with uginstall, rerun registration, restart core UGOS services, and run final identity seeding after systemd reaches multi-user.",
            "p3, p6, and p9 are intentionally unformatted; patched init formats p6 and the identity helper formats p3 on first boot.",
            "Patched initramfs mounts /dev/mmcblk0p2 at /image, loads overlay.ko.xz, and uses switch_root.",
        ],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    removed = cleanup_old_desktop_images(out_image, manifest_path, sha_path)
    print(f"Wrote image: {out_image}")
    print(f"Wrote manifest: {manifest_path}")
    print(f"Wrote sha256: {sha_path}")
    print(f"Image size: {image_size} bytes")
    print(f"SHA256: {digest}")
    if removed:
        print("Removed old images:")
        for path in removed:
            print(f"  {path}")


if __name__ == "__main__":
    main()
