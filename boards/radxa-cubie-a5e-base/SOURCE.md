# radxa-cubie-a5e-base 来源与提取记录

提取时间：2026-09-22

## 上游镜像

- 文件：`downloads/radxa-cubie-a5e/radxa-cubie-a5e_bullseye_cli_r7.output_512.img.xz`
- 来源：`https://github.com/radxa-build/radxa-cubie-a5e/releases/download/rsdk-r7/radxa-cubie-a5e_bullseye_cli_r7.output_512.img.xz`（Radxa 官方文档 docs.radxa.com/cubie/a5e/download 推荐的 rsdk-r7 GPT 镜像）
- 大小：500,889,824 字节
- SHA-512：`7fe2890166ac5a2ac04dd3cd7a36b28c610e487553c6f93f154f0526a4ab7e9f54beeb6ca85825542d9e44f90fe708dea0470f7693049e1bfd082bb24b089a44`（与官方 sha512sum 一致）

## 上游 GPT 布局

- p1 16–32 MiB FAT16 `config`（rsetup 首启配置 + logo，未使用）
- p2 32–332 MiB FAT16 `efi`（空）
- p3 332 MiB–3.28 GiB ext4 `rootfs`

## 启动链位置（对 TF/SD 启动关键）

- boot0（eGON.BT0）：镜像偏移 128 KiB（LBA 256），签名在 +4 字节处
- U-Boot（`sunxi-package` 容器）：镜像偏移 12 MiB（LBA 24576），内含 sun55i 设备串与 U-Boot 主体
- 底包镜像将上游 0–16 MiB 原样保存为 `bootloader-region-16m.bin`，构建时写到 0 偏移，
  随后清零 LBA 1–63 消除 GPT 残留；p1 固定从 16 MiB 开始，与上游布局兼容

## 提取物

| 本目录文件 | 上游位置 | 校验 |
|---|---|---|
| `bootloader-region-16m.bin` | 镜像字节 0–16 MiB | 见构建 manifest magic 校验 |
| `bootfs/Image` | rootfs `/boot/vmlinuz-5.15.147-20-aw2501` | 25,369,088 字节 |
| `bootfs/dtb/allwinner/sun55i-a527-cubie-a5e.dtb` | rootfs `/usr/lib/linux-image-5.15.147-20-aw2501/allwinner/` | 161,179 字节 |
| `rootfs-overlay/usr/lib/modules/5.15.147-20-aw2501/` | rootfs `/lib/modules/5.15.147-20-aw2501/`（完整树，含 modules.dep 与 aic8800 DKMS 模块） | — |
| `radxa-cubie-a5e-modules.tar.gz` | 上述模块树打包（构建器自动生成） | — |

## 板型结论

- DTB 名 `sun55i-a527-cubie-a5e.dtb` 证实 A5E 实机为 **Allwinner A527**（sun55iw3），非 T527、非 RK3576
- BSP 内核 5.15.147-20-aw2501（Allwinner aw2501 分支）
- 调试串口：`ttyAS0,115200`（earlycon `sunxi-uart,0x2500000`，取自上游 extlinux.conf）
- 关键驱动内建（CONFIG=y）：AW_MMC（SD/eMMC 主控）、AW_DWMAC_SUNXI（千兆网）、AW_SERIAL_CONSOLE、USB（EHCI/OHCI/XHCI/SUNXI_DWC3）、SCSI、DEVTMPFS_MOUNT
- 模块（m）：loop、fat、vfat、squashfs、overlay——这些已在底包构建期解压并嵌入 initramfs
- `MODULE_COMPRESS_XZ=y` 且无内核态解压，busybox insmod 不能加载 .ko.xz（构建期已解压处理）

## 注意

- `build`/`source` 符号链接因 Windows 权限未能提取（7-Zip 报错 1 项），运行期无影响
- 上游内核参数含 `clk_ignore_unused`（BSP 必需）与 cgroup 参数，已写入 profile `bootargs_extra`
