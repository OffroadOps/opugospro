# UGOS Pro 底包（Two Base Packages）

本仓库只维护**两个底包**，其他一概不做：

| 底包 | 架构 | 位置 | 成品 |
|---|---|---|---|
| x86_64 底包 | amd64 | `H:/ugos/x86/out/`（构建器 `build_ugos_dd.py`，输入 `_ugreen_payload/` + `_ugreen_analysis/` + 根目录固件） | `ugospro-1.19.1.126-amd64-universal-bios-uefi-gpt-dd.img.zst` + 安装器 |
| arm64 底包 | arm64 | `base/`（构建器 `base/scripts/build-ugos-arm-image.py`，输入 `H:/ugos/payload/` + `boards/<id>-base/`） | `base/out/ugos-arm64-<device>.img` |

设备差异全部收敛为 **profile + 板级资产目录**，构建器只有一个。

## 铁律（2026-09-24 定）

1. **只有两个底包**。新设备适配 = 新增一份 `profiles/<id>/profile.json` + 一份
   `boards/<id>-base/`（bootloader blob / Image / DTB / modules），不新建构建器。
2. **不做版本号文件**。构建输出永远是规范名 `out/ugos-arm64-<device>.img`，覆盖式更新。
   不产生 v1/v2/... 文件名——每次全量构建写 ~10GB，纯迭代会写坏硬盘。
   中间 work 文件构建成功后自动删除（`--keep-work` 仅调试用）。
3. **修复迭代优先动 initrd 层**：profile/补丁问题重跑构建器即可；只有 payload 升级
   （换 UGOS 版本）才值得动 `H:/ugos/payload/`。
4. **"发布"只由硬件验收产生**：构建成功不算数；一块板通过串口/HDMI+网络验收后，
   才在本文档记录"该 profile 于某日通过验收"，并归档当次 SHA-256。

## ophub/amlogic-s9xxx-armbian 模式对照

那个项目几百块板子没被版本拖死，靠的是四条，本项目已对齐：

| ophub 做法 | 本项目对应 |
|---|---|
| 通用 rootfs 一份，板子差异只是 u-boot+dtb+board 配置 | UGOS payload 一份（`H:/ugos/payload/`），板差异 = `profile.json` + `boards/<id>-base/` |
| 内核是独立仓库的预编译产物，按版本取用，不为板子改内核 | 板级内核取自厂商/Armbian 发行镜像（如 A5E 用 rsdk-r7 的 5.15.147 BSP），只提取不构建 |
| 一条流水线，`BOARD=xxx` 参数化，CI 矩阵出包 | 一条流水线 = `build-ugos-arm-image.py --profile profiles/<id>/profile.json` |
| 版本 = 内核版本+日期，不按修复次数堆文件 | 版本 = payload 版本 (1.17.0.0095) + 内核版本 + 验收日期，文件名固定 |

进一步可做（未实施）：把构建器放进 GitHub Actions（ophub 同款），本地零写入，
产物走 Release——本地硬盘只留输入和最终验收件。

## profile.json 规范

必填：`id` `display_name` `hostname` `serial` `kernel_version` `dtb` `console`。

| 字段 | 说明 |
|---|---|
| `compatibility_model` | UGOS 内部兼容型号，保持 `DH4300PLUS`（Q8B/OECT/A5E 均已验证可用） |
| `serial` / `uuid` / `mac` | 本地合成身份，禁止复制厂商序列号或硬件密钥 |
| `dtb` | 相对 `boards/<id>-base/bootfs/` 的 DTB 路径 |
| `console` / `console_secondary` / `earlycon` | 板级串口 + HDMI 控制台；`bootargs_extra` 放 BSP 必需参数 |
| `initramfs_modules` | initramfs 早加载模块名列表，**顺序敏感**（依赖必须在前）。`.ko.xz` 构建期解压成 `.ko`。A5E 教训：overlay 依赖 exportfs，缺它 = 根组装静默失败 |
| `marker` | p2 标记文件名，固定不带版本号（如 `A5E-UGOS-SD`） |
| `bootloader.image` | 原始 boot 区 blob，写 0 偏移；p1 固定 16MiB 起，LBA1–63 清零去 GPT 残留 |
| `bootloader.magic_checks` | 构建后校验（boot0 / uboot package magic） |
| `device_dir` | 板级资产目录（缺省 `boards/<id>-base`） |

## 分区布局（所有 arm64 设备统一）

MBR/EBR：p1 FAT32 boot 512M（Image/initrd.gz/DTB/extlinux/boot.scr/UBOOTOK 黑匣子）
· p2 FAT32 payload 1792M（5 squashfs + ugreen.bz2 + core-preinstall + 板级 modules + marker）
· p3 factory 32M · p5 swap 1G · p6 /ugreen 2G · p7/p8 保留 · p9 overlay 1G

## 黑匣子（无串口取证）

- U-Boot：boot.scr 成功执行 → p1 写 `UBOOTOK.TXT`
- initramfs：p2 `BOOT-STAGE.txt` 记录 stage2（标记分区找到）/ ugreen 解包完成 /
  stage4（payload+modules 解包）/ stage5（切根前健康检查）；`DMESG.TXT`/`STATUS.txt`
  仅在阶段事件一次性落卡（解包期间零并发写卡——A5E 冻结教训）
- 判读：无 UBOOTOK → 板没跑卡；有 stage5 无系统 → 真根内服务问题；
  卡在 ugreen/core 解包之间 → MMC 并发问题

## 构建命令（规范名，覆盖式）

```powershell
python "H:\ugos\base\scripts\build-ugos-arm-image.py" --profile "H:\ugos\base\profiles\radxa-cubie-a5e\profile.json"
```

## 写卡

`base/scripts/write-a5e-sd-v6-admin.ps1`（身份锁定 + 摘盘符 + 裸清 1MiB + 全量读回）。
可移动介质上 `Clear-Disk` 会静默失效，勿改回。

## 历史产线（已归档，不再维护）

Orange Pi Zero 3 / RK3399 / Q8B / OECT / OES 的脚本、profile、报告保留在
`UGOS arm/`（`FINAL-Q8B-REPORT.md`、`OECT-RK3566-STATUS.md`、`OESBOX-A311D-STATUS.md`
等），仅作参考；它们的结论已沉淀进底包（标记分区发现、quota 教训、watchdog 教训）。
