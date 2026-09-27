import { createPrivateKey, createPublicKey, sign } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import path from "node:path";

const root = path.resolve(new URL("..", import.meta.url).pathname.replace(/^\/(.:)/, "$1"));
const keyPath = path.join(root, "private", "release-key.pem");
const target = process.argv[2];
if (!target) { console.error("usage: node sign-release.mjs <file-to-sign>"); process.exit(1); }

const data = await readFile(target);
const sha256 = createHash("sha256").update(data).digest("hex");
const privateKey = createPrivateKey(await readFile(keyPath));
const publicKey = createPublicKey(privateKey);
const pubDer = publicKey.export({ type: "spki", format: "der" });
const keyId = createHash("sha256").update(pubDer).digest("hex").slice(0, 16);
const signature = sign(null, data, privateKey).toString("base64");

const manifest = {
  file: path.basename(target),
  size: data.length,
  sha256,
  signedAt: new Date().toISOString(),
  signature: { algorithm: "Ed25519", keyId, value: signature },
};
await writeFile(target + ".sig.json", JSON.stringify(manifest, null, 2) + "\n");
console.log(`signed: ${manifest.file}`);
console.log(`  size:   ${manifest.size}`);
console.log(`  sha256: ${sha256}`);
console.log(`  keyId:  ${keyId}`);
console.log(`  sig:    ${target}.sig.json`);
