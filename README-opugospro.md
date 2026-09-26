# opugospro

仿照 [ophub/amlogic-s9xxx-armbian](https://github.com/ophub/amlogic-s9xxx-armbian) 的工程模式，
为各类 NAS 硬件构建 **UGOS Pro** 移植镜像的独立项目。

> 与 ophub 仓库的关系：**模式借鉴，不是代码合并**。ophub 的 rootfs 是 GPL 的 Armbian；
> opugospro 的用户层是绿联专有 payload——不进 git、不进公共仓库，构建时从私有镜像源拉取。

## 架构（对应 ophub 的四要素）

| ophub | opugospro | 本仓库位置 |
|---|---|---|
| 通用 rootfs | UGOS payload（官方固件抽取的 squashfs/initfs/ugreen.bz2） | `payload/`（gitignore，构建时拉取） |
| 每板 u-boot+DTB 配置 | `boards/<id>/`（bootloader blob + Image + DTB + rootfs-overlay + profile.json） | `boards/` |
| 内核独立预编译仓库 | BSP 内核从官方固件提取，随 board 资产分发 | boards 内 / 服务器 `/build-inputs/` |
| 一条 CI 流水线 | `base/scripts/build-ugos-arm-image.py`（纯 Python，Linux/Windows 通用） | `.github/workflows/` |

## 目录

```
base/                     arm64 底包构建器 + profiles（自包含）
boards/                   板级资产（大文件 gitignore，构建时从镜像源拉取）
payload/                  gitignore：官方固件抽取的 UGOS 用户层
core-preinstall/          gitignore：预装包 tar（构建器可从 UPK 重生成）
x86/                      x86_64 底包（独立维护，不进 CI）
vps/                      自建源服务器工具（目录签名、固件监控、部署脚本）
docs/                     项目索引与状态文档
.archive-local/           历史设备线归档（本地保留，不进 git）
```

## 构建闭环

```
绿联官方下载中心（ugnas.com，28 产品）
   │ vps/ugos-sync.py（systemd timer 每日 06:00，VPS 上运行）
   ▼
VPS /www/official/（按产品+架构归档官方固件，文件名自带 arm64/amd64）
   │ 抽取 payload + @cache UPK → /www/packages/ → gen-catalog.py 重签 repo.json
   ▼
https://ugospro.135246.xyz（自建源：签名目录 + UPK + 系统镜像）
   │                    │
   │ GitHub CI 拉取构建输入   │ 板端 repo.json 拉取 + 原生 uginstall
   ▼                    ▼
各板子 UGOS Pro 镜像        应用/系统增量更新
```

## 新增一块板子

1. 拿到该板官方固件，提取 bootloader blob / Image / DTB / modules
2. `boards/<id>-base/` 按既有结构放入资产
3. `base/profiles/<id>/profile.json` 填写身份/串口/DTB/早加载模块（依赖闭包按 modules.dep 核对）
4. 本地跑一次构建 → 刷卡 → 串口/HDMI/网络验收 → 通过后进 boards 发布

## 安全边界

- 绿联专有 payload 不进 git、不进公开下载；镜像源 `/build-inputs/` 有 basic auth
- UPK 安装走 UGOS 原生校验（uginstall），签名目录仅保证自建源完整性
- 不伪造绿联服务器签名、不冒充官方 OTA
