#!/usr/bin/env python3
import argparse
import gzip
import io
import json
import os
import shutil
import stat
import tarfile
from pathlib import Path


CORE_UPKS = [
    "01_arm64_com.ugreen.logmgr.upk",
    "02_arm64_com.ugreen.gateway_pro.upk",
    "03_arm64_com.ugreen.storagemgr.upk",
    "05_arm64_com.ugreen.ctlmgr.upk",
    "06_arm64_com.ugreen.desktop.upk",
    "07_arm64_com.ugreen.wizard.upk",
    "08_arm64_com.ugreen.filemgr.upk",
    "09_arm64_com.ugreen.appmgr.upk",
    "10_arm64_com.ugreen.ctlmgr.index.upk",
    "11_arm64_com.ugreen.taskmgr.upk",
    "12_arm64_com.ugreen.globalsearch.upk",
    "13_arm64_com.ugreen.helpmgr.upk",
    "18_arm64_com.ugreen.jobmgr.upk",
    "19_arm64_com.ugreen.ugos_serv.upk",
]


def parse_field_blob(data: bytes, field: bytes) -> bytes:
    marker = field + b":"
    start = data.find(marker)
    if start == -1:
        raise ValueError(f"missing {field.decode()} field")
    length_start = start + len(marker)
    length_end = data.find(b":", length_start)
    if length_end == -1:
        raise ValueError(f"missing {field.decode()} length terminator")
    length = int(data[length_start:length_end])
    payload_start = length_end + 1
    return data[payload_start : payload_start + length]


def extract_upk(upk_bytes: bytes, app_dir: Path) -> None:
    payload_gz = parse_field_blob(upk_bytes, b"ugb")
    with gzip.GzipFile(fileobj=io.BytesIO(payload_gz)) as gz:
        payload_tar = gz.read()
    tmp_dir = app_dir.parent / (app_dir.name + ".tmp")
    shutil.rmtree(tmp_dir, ignore_errors=True)
    tmp_dir.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(payload_tar), mode="r:") as tar:
        tar.extractall(tmp_dir)
    ugb_files = sorted(tmp_dir.glob("*.ugb"))
    if not ugb_files:
        raise ValueError("no .ugb payload in UPK")
    shutil.rmtree(app_dir, ignore_errors=True)
    app_dir.mkdir(parents=True)
    with tarfile.open(ugb_files[0], mode="r:*") as tar:
        tar.extractall(app_dir)
    shutil.rmtree(tmp_dir, ignore_errors=True)


def add_file(tar: tarfile.TarFile, source: Path, arcname: str) -> None:
    tar.add(source, arcname=arcname, recursive=False)


def add_tree(tar: tarfile.TarFile, source: Path, arc_prefix: str) -> None:
    for path in sorted(source.rglob("*")):
        rel = path.relative_to(source).as_posix()
        tar.add(path, arcname=f"{arc_prefix}/{rel}", recursive=False)


def add_bytes(tar: tarfile.TarFile, arcname: str, data: bytes, mode: int = 0o644) -> None:
    info = tarfile.TarInfo(arcname)
    info.size = len(data)
    info.mode = mode
    info.mtime = 0
    tar.addfile(info, io.BytesIO(data))


def add_symlink(tar: tarfile.TarFile, arcname: str, target: str) -> None:
    info = tarfile.TarInfo(arcname)
    info.type = tarfile.SYMTYPE
    info.linkname = target
    info.mode = 0o777
    info.mtime = 0
    tar.addfile(info)


def service_dropin(service: str) -> tuple[str, bytes]:
    # v8 (2026-09-24): GOMEMLIMIT 256MiB GC-thrashed the Go services on the 2 GB A5E,
    # and ctl_serv (310 MB app, heavy first init) exceeded the systemd default 90 s
    # TimeoutStartSec -> killed mid-init in a restart loop, web panel never READY.
    body = f"""[Service]
Environment=GOMEMLIMIT=1GiB
Environment=GOGC=75
TimeoutStartSec=900
"""
    return f"etc/systemd/system/{service}.d/zero3-lowmem.conf", body.encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--out", default="staging/core-preinstall/core-preinstall.tar.gz")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    out_path = (project_dir / args.out).resolve()
    work_dir = project_dir / "work" / "core-preinstall"
    apps_dir = work_dir / "apps"
    shutil.rmtree(work_dir, ignore_errors=True)
    apps_dir.mkdir(parents=True)

    ugreen_tar = project_dir / "payload" / "ugreen.bz2"
    summaries = []
    with tarfile.open(ugreen_tar, mode="r:*") as src_tar:
        members = {Path(m.name).name: m for m in src_tar.getmembers() if m.isfile()}
        for upk in CORE_UPKS:
            member = members.get(upk)
            if member is None:
                raise FileNotFoundError(f"missing {upk} in {ugreen_tar}")
            with src_tar.extractfile(member) as src:
                upk_bytes = src.read()
            app_dir = apps_dir / upk.replace(".upk", "")
            extract_upk(upk_bytes, app_dir)
            config = json.loads((app_dir / "config.json").read_text(encoding="utf-8"))
            app_id = config["appId"]
            summaries.append(
                {
                    "upk": upk,
                    "appId": app_id,
                    "serviceName": config.get("serviceName"),
                    "route": config.get("route"),
                    "appDir": str(app_dir),
                    "appBytes": sum(p.stat().st_size for p in app_dir.rglob("*") if p.is_file()),
                }
            )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(out_path, mode="w:gz", compresslevel=6) as tar:
        for item in summaries:
            app_dir = Path(item["appDir"])
            app_id = item["appId"]
            add_tree(tar, app_dir, f"ugreen/@appstore/{app_id}")
            add_file(tar, app_dir / "config.json", f"var/lib/ugb/{app_id}/config.json")

            http_dir = app_dir / "http.d"
            if http_dir.exists():
                for path in sorted(http_dir.iterdir()):
                    if path.is_file():
                        add_file(tar, path, f"etc/nginx/conf.d/{path.name}")

            init_dir = app_dir / "init.d"
            if init_dir.exists():
                for path in sorted(init_dir.iterdir()):
                    if path.suffix == ".service":
                        add_file(tar, path, f"etc/systemd/system/{path.name}")
                    elif path.suffix == ".sh":
                        add_file(tar, path, f"etc/sysconfig/{path.name}")

            sbin_dir = app_dir / "sbin"
            if sbin_dir.exists():
                for path in sorted(sbin_dir.iterdir()):
                    if path.is_file():
                        wrapper = f'#!/bin/sh\nexec "/ugreen/@appstore/{app_id}/sbin/{path.name}" "$@"\n'
                        add_bytes(tar, f"var/targets/{path.name}", wrapper.encode("utf-8"), 0o755)

        ctl_app = apps_dir / "05_arm64_com.ugreen.ctlmgr"
        for rel, dest in [
            ("sbin/domain_tool", "usr/sbin/domain_tool"),
            ("domain_tool/domain_tool.service", "lib/systemd/system/domain_tool.service"),
            ("smbftpd/smbftpd.service", "lib/systemd/system/smbftpd.service"),
            ("sbin/webdav", "usr/sbin/webdav"),
            ("webdav/webdav.service", "lib/systemd/system/webdav.service"),
            ("sbin/conf_tool", "usr/sbin/conf_tool"),
        ]:
            src = ctl_app / rel
            if src.exists():
                add_file(tar, src, dest)

        # zero3_debug.conf REMOVED (2026-09-24): UGOS nginx.conf includes conf.d/*.conf
        # at the MAIN context, so a server{} block there killed nginx -t with
        # '"server" directive is not allowed here' -- web panel never came up (A5E v6).

        telnet_service = """[Unit]
Description=Zero3 always-on debug telnet on 2323
After=network.target

[Service]
Type=simple
ExecStart=/usr/sbin/telnetd -F -p 2323 -l /bin/login
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
"""
        add_bytes(tar, "etc/systemd/system/zero3-debug-telnet.service", telnet_service.encode("utf-8"))
        add_symlink(
            tar,
            "etc/systemd/system/multi-user.target.wants/zero3-debug-telnet.service",
            "../zero3-debug-telnet.service",
        )

        for svc in [
            "log_serv.service",
            "gateway_serv.service",
            "entry_serv.service",
            "ctl_serv.service",
            "storage_serv.service",
            "discovery_serv.service",
            "app_serv.service",
        ]:
            arc, data = service_dropin(svc)
            add_bytes(tar, arc, data)

        # v9 (2026-09-25): redis-server.service ships full Debian sandboxing
        # (PrivateUsers/SystemCallFilter/NoExecPaths/...).  The A527 BSP kernel
        # lacks user-namespace support, so redis dies with 'Failed to set up
        # user namespacing: Operation not permitted' and the whole app chain
        # (ctl_serv -> web panel -> wizard) starves.  Drop-in disables the
        # sandbox suite for redis on this platform -- function first.
        redis_compat = """[Service]
PrivateUsers=no
PrivateTmp=no
PrivateDevices=no
ProtectHome=no
ProtectSystem=no
ProtectProc=no
ProcSubset=all
ProtectClock=no
ProtectControlGroups=no
ProtectHostname=no
ProtectKernelLogs=no
ProtectKernelModules=no
ProtectKernelTunables=no
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
RestrictNamespaces=no
RestrictRealtime=no
RestrictSUIDSGID=no
LockPersonality=no
MemoryDenyWriteExecute=no
NoNewPrivileges=no
SystemCallArchitectures=
SystemCallFilter=
NoExecPaths=
CapabilityBoundingSet=
"""
        add_bytes(tar, "etc/systemd/system/redis-server.service.d/ugos-arm-compat.conf", redis_compat.encode("utf-8"))

        add_bytes(
            tar,
            "etc/zero3-preinstall-manifest.json",
            json.dumps(summaries, ensure_ascii=False, indent=2).encode("utf-8"),
        )

    summary_path = out_path.with_suffix(out_path.suffix + ".json")
    summary_path.write_text(json.dumps(summaries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"preinstall={out_path}")
    print(f"bytes={out_path.stat().st_size}")
    print(f"summary={summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
