import { generateKeyPairSync } from "node:crypto";
import { writeFile, mkdir } from "node:fs/promises";
import { createHash } from "node:crypto";
import path from "node:path";

const root = path.resolve(new URL("..", import.meta.url).pathname.replace(/^\/(.:)/, "$1"));
await mkdir(path.join(root, "private"), { recursive: true });
const { publicKey, privateKey } = generateKeyPairSync("ed25519");
await writeFile(path.join(root, "private", "release-key.pem"), privateKey.export({ type: "pkcs8", format: "pem" }));
const pubDer = publicKey.export({ type: "spki", format: "der" });
await writeFile(path.join(root, "release-public-key.pem"), publicKey.export({ type: "spki", format: "pem" }));
const keyId = createHash("sha256").update(pubDer).digest("hex").slice(0, 16);
await writeFile(path.join(root, "release-key-id.txt"), keyId + "\n");
console.log(`release keypair generated. keyId=${keyId}`);
console.log(`public key: release/release-public-key.pem (commit this)`);
console.log(`private key: release/private/release-key.pem (NEVER commit)`);
