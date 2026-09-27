# 安全与免责声明

## 固件完整性验证

本项目发布的所有固件镜像均使用 Ed25519 私钥签名。**任何未经签名的固件与本项目无关。**

### 验证方法

```bash
# 1. 校验 SHA256（快速完整性检查）
certutil -hashfile opugospro-a5e-xxx.7z SHA256        # Windows
sha256sum opugospro-a5e-xxx.7z                        # Linux/macOS

# 2. 校验 Ed25519 签名（防篡改，需 node.js）
node release/verify-release.mjs opugospro-a5e-xxx.7z.sig.json opugospro-a5e-xxx.7z
```

公钥指纹（keyId）：`b5c90a95e22dada4`，公钥文件：`release/release-public-key.pem`。
签名清单 `*.sig.json` 内含 keyId，与公钥指纹一致才可信。

### 免责声明

- 本项目是绿联 UGOS Pro 在非官方硬件上的**个人研究性移植**，与绿联官方无任何关系。
- 从本仓库 Releases 或关联服务器下载的固件，**仅限本项目作者及参与者自用测试**。
- 任何第三方篡改、重打包、二次分发的固件造成的数据丢失、硬件损坏或其他损失，
  **均与本项目无关**；请务必按上述方法验签后再刷写。
- 刷写固件有风险，请自行备份重要数据。

## 密钥管理

- `release/private/release-key.pem`：发布签名私钥，**永不进入 git/服务器/镜像**
- 私钥泄露时的轮换流程：`node release/keygen.mjs` 重新生成 → 更新 README 指纹 →
  之后所有 release 用新 keyId 签名
