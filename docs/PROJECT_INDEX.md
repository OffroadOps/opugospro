# UGOS Pro 适配项目总账

更新时间：2026-09-24

## 项目口径

- 主目标：把 UGOS Pro 适配到不同 CPU/设备平台。
- **2026-09-24 起只维护两个底包**：x86_64（`_out/` + `build_ugos_dd.py`）和 arm64
  （`base/` 通用构建器 + `base/profiles/` + `staging/<id>-base/`）。其余设备线全部归档，
  脚本与报告仅作参考；它们的经验已沉淀进 arm64 底包（标记分区发现、quota/watchdog/MMC
  并发教训、exportfs 依赖）。
- **镜像不做版本号文件**：arm64 输出固定为 `base/out/ugos-arm64-<device>.img` 覆盖式更新，
  构建中间文件成功后自动清理；"发布"只由硬件验收产生（记录验收日期 + SHA-256）。
- 构建成功不等于硬件验收成功。每个设备必须分别记录镜像、哈希、写盘、启动、网络、Web、存储和服务验证。
- 历史窗口中的视觉识别、GBBox、PVE、普通 Linux 运维和"双 NAS 缝合怪"讨论不作为 UGOS Pro 适配进度；只有能约束设备启动或硬件兼容性的结论保留。
- 不移动现有大文件。下表给出当前权威路径，避免为整理目录而破坏脚本引用。

## 设备总览

| 设备窗口 | 架构 / SoC | 当前真实进度 | 权威证据 | 下一验收点 |
|---|---|---|---|---|
| x86_64 通用 | amd64 / x86_64 | 已用 1.19.1.126/6.18.15 固件与其声明依赖的 1.17 base 层全新构建通用 BIOS+UEFI GPT DD 包；BIOS、UEFI、rootfs 全层挂载和 zstd 完整性均已验证。安装器同步到 `bin456789/reinstall` 提交 `5db0516`，支持按源 MAC 注入动态网卡名、静态/动态 IPv4、IPv6、离链网关和 DNS。80 GiB VPS 的约 46.6 GiB 稀疏 `tcm_loop` 数据盘曾因 sysfs 路径被归为外置 USB；现已反编译确认 1.19.1.126 的设备分类逻辑，并在校验原始字节后只把 `/devices/virtual/` 映射为 DXP6800 Plus/Pro 的一个内部 SATA 槽。官方应用目录另有厂商服务器签名，不能仅改 URL；已建立独立 Ed25519 验签的 `ugos-community-store/` 社区源，UPK 仍交给 UGOS 原生安装校验 | `_out/README-1.19.1.126.md`、`_out/ugospro-1.19.1.126-amd64-universal-bios-uefi-gpt-dd.img.zst`、`_out/SHA256SUMS-1.19.1.126.txt`、`build_ugos_dd.py`、`ugos-installer/`、`ugos-community-store/` | 部署新镜像与安装器，在一次干净 VPS 重装中显式指定系统盘；首次启动后验收虚拟盘显示为内部 SATA、可选择 Basic 并实际创建卷。官方商店空白仍需在 SSH 可用后采集 app_serv 出网/签名日志；社区源可先发布已被 UGOS 接受的本地 UPK |
| Orange Pi Zero 3 | arm64 / Allwinner H618 | 板级 U-Boot、DTB、kernel/modules、UGOS payload、脚本及 v18 工作文件仍在；文档记录已产出 v17 镜像加 v18 补丁包并推进到 UGOS 服务/网页阶段，但这些完整成品位于旧用户路径，当前本机不可访问，不能重新核验哈希；未形成日用版验收 | `UGOS arm/README.md`、`UGOS arm/STATUS.md`、`UGOS arm/profiles/orange-pi-zero-3/` | 先找回或重建可核验的 v17/v18 成品，再用串口和网络验证核心服务、9999/9443 页面、存储与重启稳定性 |
| RK3399 EAIDK-610 | arm64 / Rockchip RK3399 | Armbian 基线、启动区、kernel/modules、staging 与构建脚本仍在；状态文件记录的 v2 发布镜像、manifest 和 SHA-256 当前已不存在，脚本默认 v4 成品也不存在，只剩工作中间镜像，因此目前没有可安全刷写的发布件，也没有硬件验收 | `UGOS arm/STATUS.md`、`UGOS arm/scripts/build-rk3399-eaidk610-image.py`、`work/rk3399-eaidk610-layout/` | 从现存输入重建成品并生成新 manifest/SHA-256，完成独立校验后才可上板验证 |
| Radxa Cubie A5E | arm64 / Allwinner A527（官方 DTB `sun55i-a527-cubie-a5e.dtb` 证实） | 2026-09-23 用 HDMI 采集卡完成无串口定位：v3"冻结"实为 overlay 依赖 `exportfs` 缺失导致根组装从未成功 + 268MB 解包灌入 initramfs 内存盘 OOM；v6 已把 exportfs 加入早加载模块。成品改为规范名 `base/out/ugos-arm64-radxa-cubie-a5e.img`（SHA-256 `ec706768…8feb6e4`，marker `A5E-UGOS-SD-V6`），待写入 TF 卡实机验收。板级资产与根因记录见 `staging/radxa-cubie-a5e-base/SOURCE.md`、`UGOS arm/RADXA-A5E-STATUS.md` | `base/README.md`（双底包铁律 + ophub 式维护模式）、`base/out/ugos-arm64-radxa-cubie-a5e.img.manifest.json` | 写卡（write-a5e-sd-v6-admin.ps1）→ HDMI+网络验收 9999/9443、存储、重启稳定；实机内存变体确认后修正 profile |
| Radxa Cubie A7Z | arm64 / Allwinner A733 | 已确认 A733、LPDDR4X/UFS 的硬件资料；旧窗口已有视觉节点成果，但那不是 UGOS Pro 适配。当前未发现 UGOS Pro 镜像或上板验收 | 外部历史任务 `01a07040-065f-7432-9ad7-bd3f88e7ebdb`；本总账只保留硬件约束 | 采集官方启动链、kernel/DTB/modules 和串口基线，再建立 UGOS profile；不要把视觉识别服务当作适配完成 |
| Radxa Dragon Q8B | arm64 / Qualcomm SC8280XP（Snapdragon 8cx Gen 3） | 已完成 9 分区镜像、单一零等待启动项、身份/profile、UGRelay 无密钥接收端、写盘全量读回；`regulator_ignore_unused` 已解决约 40 秒掉电。最新实机阻塞为 `storage_serv` 高 CPU 死循环使 `done.service` 等待，随后 `ugos_serv` 关闭 SSH/Web；修正版 initrd 已构建但尚未在线应用 | `UGOS arm/FINAL-Q8B-REPORT.md`、`UGOS arm/Q8B-V4-RUNTIME-DIAGNOSIS.md`、`UGOS arm/profiles/radxa-dragon-q8b/`、`UGOS arm/scripts/patch-q8b-rebuild-targets.py` | 用户手动断电重启后，在 SSH 窗口出现时应用修正版 initrd，固化 SSH，再验收 9999 与核心服务；不要重走 watchdog 路线 |
| OES BOX（网心云 OES 一代，实机型号 OneThing Cloud OES Mode A） | arm64 / Amlogic A311D | **已放弃（2026-09-17，用户决定）**。研究深度：AML burn 容器 v2 完全解析 + ampack 打包链验证；Secure Boot 定性（SECURE_BOOT_SET=可复用密钥）；EPT 20 分区与 DTB 双表实测；ophub USB 启动链破译；UGOS 三分区方案全构件在实机构建成功（p20 2.9G rootfs / p18 /ugreen / p16 pivot）。放弃原因：底包为 RAM overlay 且运行期写回 p16/p18（运行时部署必被覆盖）、vendor 内核 USB 口默认设备模式（otg_device=1，U 盘不可见且 fw_setenv 不进 bootm 预置 bootargs）、底包 sshd 大流量后必挂死、Burning Tool 在该机成功率低——迭代通道全部不可用，非技术方案失败。产物已清理（-31GB），仅存研究报告与工具 | `UGOS arm/OESBOX-A311D-STATUS.md`（终章含五大根因/成果清单/重启路径/设备恢复方法）、`UGOS arm/profiles/oes-box-a311d/`、`downloads/oesbox-a311d/{tools,research-archive,ugos_*.sh}` | 已归档。若重启：先把 Armbian 装进 eMMC（Burning Tool 一次或换兼容 U 盘引导），再在运行中的 Armbian 上做 UGOS——不在 vendor 底包上迭代 |
| OEC BOX WXY4（用户原称 OECT） | arm64 / Rockchip RK3566 | 已确认 4× Cortex-A55、4 GB RAM、8 GB eMMC、60 GB 原生 SATA、无 HDMI；已保存 eMMC 前 16 MiB、kernel `6.1.115-rk35xx-ophub`、DTB/modules 并建立独立 profile。UGOS ARM 1.17.0.0095 USB v1 镜像已生成，源哈希通过。64 GB Lexar USB 3.0 盘和 8 GB USB 2.0 测试盘均完成整盘写入及 6.43 GiB 全量读回 SHA-256 校验。2026-09-09 首次使用 Lexar 实机重启后回到原 Armbian；Linux 识别 Lexar 身份但未生成 `/dev/sdb`，反复 reset 后 disconnect；内部 eMMC/SATA 未改写。USB 2.0 测试盘已写好但尚未上机 | `UGOS arm/OECT-RK3566-STATUS.md`、`UGOS arm/profiles/oec-t-rk3566/`、`UGOS arm/scripts/build-oect-rk3566-image.py`、`UGOS arm/out/ugos-oect-rk3566-usb-v1.img.manifest.json` | 将已校验 USB 2.0 测试盘插入 OEC-T，先在 Armbian 下确认 High-Speed 块设备和 payload 标记，再重测启动。若 U 盘稳定但仍进入 Armbian，再用串口/可回退的最小 eMMC 引导切换 |

## 已验证的失败路线与边界

- Q8B 的约 40 秒掉电不是 UGOS 定时器，也不是 Qualcomm watchdog；真正有效的稳定性修复是保留未使用稳压器，避免延迟关闭关键电源轨。
- Q8B 的 project-quota 初始化会让 overlay 只读并触发服务循环；运行时镜像必须避免重新启用 `quota/project`。
- Q8B 当前固件没有 `/dev/kvm`，启动日志为 `HYP mode not available`；在固件/UEFI 暴露 EL2 前不能宣称 KVM 可用。
- Q8B 的 Qualcomm TEE 不能替代绿联 RK3588 的 OP-TEE 私有身份、TA 和硬件根密钥；禁止复制参考机身份或伪造云端授权。
- Orange Pi Zero 3 不能直接刷绿联 RK3588 固件；必须保留 H618 自己的 SPL/U-Boot、DTB、kernel 和 modules，仅复用 UGOS arm64 用户层/应用层。
- A7Z 的视觉识别、Orange Pi 的普通 Linux SSD 迁移、GBBox 移植均不是 UGOS Pro 功能验收。
- Radxa Cubie A5E 是 Allwinner A527 平台（2026-09-22 由官方 rsdk-r7 镜像内 DTB 名证实），不是 RK3576；A5E 与 A7Z（A733）不能按同 SoC 合并。
- OES BOX（A311D）适配终止的核心教训：网心云底包是 RAM overlay 系统（/low=system、/high=backup 运行期回写），在其运行时写 eMMC 分区必被覆盖且损坏运行态；vendor 内核 cmdline 含 otg_device=1（USB 设备模式）且 fw_setenv 修改不进 bootm 预置 bootargs，U 盘在底包内核下不可见；vendor u-boot 2015.01 上 U 盘冷启动引导未复现（热插拔正常）。在此类"加密 boot + 低成功率烧录 + RAM overlay 底包"设备上，远程迭代路线不成立；可行路径 = 先落地主线内核系统（Armbian）再在其上做用户层。

## 历史窗口整理口径

- 当前整理窗口保留为协调总线。
- 旧 `D:\img` 总窗口内容去重后分别交接到 Q8B、Orange Pi Zero 3、RK3399 EAIDK-610 和 x86_64 窗口，然后归档。
- x86_64 镜像查询和 S3 上传窗口交接到 x86_64 窗口后归档。
- A7Z 的硬件资料窗口只提取启动/内存/UFS约束；视觉节点实现作为非 UGOS 噪声不并入适配进度，旧窗口可归档。
- 已归档的 Q8B 测试签名调查保留原档，不恢复；其唯一有效约束是 Windows 驱动签名问题，与当前 Linux/UGOS 主线分开。
- `GBBox Q8B 无授权移植` 属于 `GBBOX` 项目，不跨项目归档或合并。

## 权威任务窗口

| 设备 | 任务 ID |
|---|---|
| 项目协调总线 | `01a08441-83dd-7301-8bf0-21f4cbafe70c` |
| x86_64 通用 | `01a08454-a0c3-7970-b91a-18fb8ecc915e` |
| Orange Pi Zero 3 | `01a08454-a41f-7240-b1e6-a40633bbddb8` |
| RK3399 EAIDK-610 | `01a08454-a74d-7bc2-8128-669b3251fae7` |
| Radxa Cubie A5E | `01a08454-a9d2-7593-86c5-1443f718e18e` |
| Radxa Cubie A7Z | `01a08454-abfd-7dd0-a1c4-3595acad5015` |
| Radxa Dragon Q8B | `01a08454-ae7a-79c3-9f7c-856dc63465f5` |
| OEC BOX WXY4（RK3566） | `01a08454-b0b6-7083-8f25-4ce57e1e23db` |

## 文件保留策略

- 保留：发行镜像、校验文件、manifest、板级 boot/kernel/DTB/modules、构建脚本、profile、诊断报告和能证明失败原因的小型日志。
- 新增（2026-09-22）：`base/` 为硬件无关底包（通用构建器 + `base/profiles/` + 构建输出）；各板级资产仍按惯例放 `staging/<device-id>-base/`。底包构建器引用 `UGOS arm/payload/` 原文件，不移动、不复制大文件。
- 可清理：源码目录生成的 `__pycache__`、已由报告替代的视频抽帧目录、工具缓存中的零字节旧索引。
- 暂不删除：`downloads/`、`payload/`、`staging/`、`work/`、`_ugreen_analysis/`、`_ugreen_payload/`、`_tools/`、`new/`。这些目录虽大，但仍被构建脚本引用或包含唯一输入；未做哈希去重和重建验证前不能当垃圾删除。

## 2026-09-09 清理记录

- 已移入 Windows 回收站：25 个源码/工具 `__pycache__` 文件、25 个 Q8B 视频分析派生帧、5 个零字节 Cygwin 旧索引，共 55 个文件，约 3.53 MiB。
- 已删除对应空目录；这些内容可重新生成，也可在需要时从回收站恢复。
- 未删除任何发行镜像、校验文件、manifest、构建输入、板级 profile、诊断报告或原始任务记录。

## 2026-09-09 窗口归档记录

- 已归档旧总窗口：`01a05dc6-8a42-74e0-b63d-3b962e238e77`。
- 已归档 x86_64 镜像查询与 S3 上传窗口：`01a08052-c780-75b3-8a56-7cd9bc778d04`、`01a0806b-4551-7330-aa43-8f2cc276b86a`。
- 已归档 A7Z 硬件/视觉历史窗口：`01a07040-065f-7432-9ad7-bd3f88e7ebdb`、`01a0702d-15af-7cf1-a0ca-7b2362dc54c2`。
- 已归档 Orange Pi Zero 3 普通 Linux 运维窗口：`01a07066-f5d5-70e3-b05e-1d81714e7db9`。
- Q8B 测试签名调查此前已经归档；`GBBox Q8B 无授权移植` 属于其他项目，未动。

> **2026-09-24 迁移注记**：项目已从 D:\img 迁移至 H:\ugos，并按双底包重构目录（base/=arm64 底包、x86/=x86_64 底包、payload/、boards/、core-preinstall/、archive/）。
> 本文以下表格中的历史路径（D:\img、UGOS arm、_out、staging 等）新对应关系见 H:\ugos\README.md。
