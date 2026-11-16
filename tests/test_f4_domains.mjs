import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {runInNewContext} from "node:vm";
const source = readFileSync(new URL("../web/privacy.js", import.meta.url), "utf8");
const data = runInNewContext(`${source}; ({themes, inspect});`);
assert.equal(data.themes.length, 9);
for (const [label, word] of data.themes) {
  assert(label && word);
  assert(data.inspect(`Quero conhecer ${word}.`).safe.includes(word));
}
assert.equal(data.inspect("Meu nome é Maria e moro na Rua Exemplo").pii, true);
assert.equal(data.inspect("Socorro").urgent, true);
console.log("PASS — 9 temas guiados, minimização e urgência local.");
