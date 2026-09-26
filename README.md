# UGOS Pro 适配项目（H 盘版，2026-09-24 迁移）

只维护两个底包：**x86_64** 和 **arm64**。其余设备线全部归档。

```
H:\ugos\
  base\                    ★ arm64 底包（自包含）
    scripts\               构建器 build-ugos-arm-image.py + 依赖机制脚本 + 写卡脚本
    profiles\              设备 profile（每板一份 JSON）
    out\                   规范输出 ugos-arm64-<device>.img（覆盖式，无版本号）
  x86\                     ★ x86_64 底包
    build_ugos_dd.py
    out\                   通用 BIOS+UEFI GPT DD 成品 + 安装器 + 社区源
    payload\  analysis\    构建输入
    source\                官方 1.19.1.126 固件源
    ugos-community-store\  ugos-installer\
  payload\                 arm64 UGOS 用户层 payload（1.17.0.0095，squashfs/initfs/ugreen.bz2）
  core-preinstall\         核心应用预装包（core-preinstall.tar.gz，设备无关）
  boards\                  板级资产（每板一目录：bootloader blob / Image / DTB / modules）
    radxa-cubie-a5e-base\    ← 当前活跃
    （其余为归档板）
  archive\                 归档设备线（Zero3/RK3399/Q8B/OECT/OES 的脚本/文档/profile）
    ugos-arm\                 原 D:\img\UGOS arm（其 payload 与 core-preinstall 已上移）
    verify\  work\
  docs\                    PROJECT_INDEX.md、storage_serv 逆向分析、model_database.conf
  tools\                   7-Zip / QEMU / cygwin-ext4 / go / mc
  downloads\               板级来源镜像（A5E rsdk-r7 官方固件等）
```

## 构建命令（arm64）

```powershell
python H:\ugos\base\scripts\build-ugos-arm-image.py --profile H:\ugos\base\profiles\radxa-cubie-a5e\profile.json
```

- 输出固定为 `H:\ugos\base\out\ugos-arm64-radxa-cubie-a5e.img`，覆盖式更新，无版本号。
- 构建后以 `.manifest.json` 里的 sha256 为准（每次构建哈希会变，属正常）。
- work 中间文件成功后自动清理。

## 写卡

`H:\ugos\base\scripts\write-a5e-sd-admin.ps1`（UAC，身份锁 Disk2 + 摘盘符 + 单句柄写入 + 全量读回）。
若本机读卡器写通道不稳，用 Etcher/Rufus(DD) 自刷亦可。

## 用户个人文件

项目之外的旧文件全部归入 `H:\_user-files\`（nas-backup-scripts / tv-kiosk / media /
tools-projects / keys-certs / misc），未删除任何内容。
