import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { runInNewContext } from "node:vm";
const root = new URL("../web/", import.meta.url);
const file = name => readFileSync(new URL(name, root), "utf8");
const inspect = runInNewContext(`${file("privacy.js")}; inspect;`);
const case1 = inspect("Meu nome é Maria e moro na Rua 12: quero direitos");
assert.equal(case1.pii, true);
assert.equal(case1.safe, "direitos");
assert.equal(inspect("socorro, está me agredindo agora").urgent, true);
assert.equal(inspect("não está armado").urgent, false);
assert.equal(inspect("li uma notícia dizendo socorro").urgent, false);
assert.equal(inspect("quero entender meus direitos").pii, false);
const html = file("index.html"), flow = file("flow.js"), app = file("app.js");
for (const id of ["context", "primary", "back", "help", "switch", "game", "explore"]) {
  assert.match(html, new RegExp(`id="${id}"`));
}
assert.match(file("agent.js"), /context:previewSafe/);
assert.match(flow, /confirm_preview/);
assert.doesNotMatch(flow, /context:text/);
assert.match(app, /actions\[\$\(id\)\.dataset\.action\]/);
assert.match(app, /showHelp/);
assert.match(flow, /scanned\.urgent/);
assert.match(flow, /reviewText/);
assert.match(html, /<noscript>/);
console.log("PASS — privacidade local, urgência, ações reais e HTML fallback.");
