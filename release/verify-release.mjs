import { createPublicKey, verify } from "node:crypto";
import { readFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import path from "node:path";

const root = path.resolve(new URL("..", import.meta.url).pathname.replace(/^\/(.:)/, "$1"));
const pubPath = path.join(root, "release-public-key.pem");
const sigPath = process.argv[2]; // .sig.json
if (!sigPath) { console.error("usage: node verify-release.mjs <file> <file.sig.json>"); process.exit(1); }

const manifest = JSON.parse(await readFile(sigPath, "utf8"));
const target = process.argv[3] || manifest.file;
const data = await readFile(target);
const sha256 = createHash("sha256").update(data).digest("hex");
if (sha256 !== manifest.sha256) {
  console.error(`FAIL: sha256 mismatch\n  expected ${manifest.sha256}\n  actual   ${sha256}`);
  process.exit(1);
}
const publicKey = createPublicKey(await readFile(pubPath));
const ok = verify(null, data, publicKey, Buffer.from(manifest.signature.value, "base64"));
if (!ok) { console.error("FAIL: Ed25519 signature invalid"); process.exit(1); }
console.log(`OK: ${manifest.file}`);
console.log(`  sha256: ${sha256}`);
console.log(`  keyId:  ${manifest.signature.keyId}`);
console.log(`  signed: ${manifest.signedAt}`);
