# UGOS Pro 1.19 Universal VPS Installer

This directory is based on `bin456789/reinstall` commit
`5db051675101f31bbe2fb3e093432fa4d1af8dcc`. The small `--ugos` extension
keeps the upstream DD flow and injects the network detected by reinstall into
UGOS partition 7 before reboot.

## Upload layout

Serve this directory at:

```text
http://5.181.177.120/ugos-installer/
```

Serve the image at:

```text
http://5.181.177.120/ugospro-1.19.1.126-amd64-universal-bios-uefi-gpt-dd.img.zst
```

## One-line install

```bash
curl -fsSL http://5.181.177.120/ugos-installer/ugos-install.sh | sh
```

An explicit target disk is recommended when a provider exposes metadata disks:

```bash
curl -fsSL http://5.181.177.120/ugos-installer/ugos-install.sh | \
  sh -s -- --target-disk /dev/vda
```

BIOS/UEFI can be forced with `--force-boot-mode bios` or
`--force-boot-mode efi`.

## UGOS extension

After upstream reinstall writes the raw image, `trans.sh` mounts USER-DATA and
writes a first-boot network profile. The profile:

- matches the target interface by MAC instead of assuming `eth0`;
- falls back to the first live physical interface if the kernel renames it;
- preserves static IPv4, static IPv6, off-link gateways, extra IPv6 addresses,
  and DNS collected by reinstall;
- falls back to DHCP/RA when the source system used dynamic addressing.

The image itself expands USER-DATA on first boot and can expose unused space as
a sparse 32-GiB-or-larger virtual SCSI disk when no real data disk is present.
On firmware 1.19.1.126 that virtual path is mapped to an internal SATA bay, so
UGOS can use it for a Basic storage pool instead of listing it as external USB.

Expected first-boot URL:

```text
http://<current-vps-ip>:9999
```
