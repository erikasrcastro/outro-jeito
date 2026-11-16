import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {runInNewContext} from "node:vm";
const web = new URL("../web/", import.meta.url);
const page = readFileSync(new URL("index.html", web), "utf8");
for (const file of ["privacy.js", "app.js", "flow.js", "agent.js", "styles.css"])
  assert(page.includes(`${file}?v=${file === "styles.css" ? "f4-3-3" : "simples-v1"}`), `Versão não fixada: ${file}`);
const inserted = [];
const document = {
  createElement(tag) { return {
    tag, children: [], append(...nodes) { this.children.push(...nodes); },
    set textContent(value) { this.text = value; }, set type(value) { this.kind = value; }
  }; },
  querySelector(selector) {
    assert.equal(selector, ".choices");
    return {append(node) {inserted.push(node);}};
  }
};
const source = readFileSync(new URL("privacy.js", web), "utf8");
runInNewContext(source, {document});
assert.equal(inserted.length, 1);
assert.equal(inserted[0].children.filter(x => x.tag === "button").length, 9);
console.log("PASS — seletor de nove assuntos montado e assets versionados.");
