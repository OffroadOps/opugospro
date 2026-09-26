# UGOS 社区应用源

这是与绿联官方应用目录并行的独立社区源，不替换 `center.ugnas.com`，也不关闭 UGOS 对 UPK 的原生校验。

安全边界分成两层：

1. `repo.json` 使用本仓库自己的 Ed25519 私钥签名，网页内置验证逻辑，防止清单或下载地址被篡改。
2. 下载的 `.upk` 仍由 UGOS 应用中心的原生安装器检查。仓库签名不能把不受 UGOS 接受的包“变成可信包”，也不冒充绿联官方签名。

## 首次初始化

```powershell
cd D:\img\ugos-community-store
npm run keygen
```

私钥只保存在 `private/signing-key.pem`，不要上传到 Web 服务器、镜像或 Git；服务器只需要 `public` 目录。

## 发布应用

把可由 UGOS 手动安装的 UPK 放入 `packages`，复制并修改 `packages/example.package.json.template`（保存为以 `.package.json` 结尾的文件），然后：

```powershell
npm run build
npm run verify
npm run serve
```

访问 `http://服务器IP:8080/`。生产环境可直接用 nginx、Caddy 或对象存储托管 `public` 目录。

当前安全版本采用“签名目录 + 下载 UPK + UGOS 应用中心手动安装”的方式。官方应用中心的云目录还有一层绿联服务器签名校验，因此只把域名或 URL 指向自建服务器会被拒绝；除非绿联公开第三方源接口，否则不应绕过该验证。
