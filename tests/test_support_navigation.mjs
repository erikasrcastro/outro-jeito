import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {createContext, runInContext} from "node:vm";
const script = readFileSync(new URL("../web/guidance.js", import.meta.url), "utf8");
let shown, opened = [], confirmations = 0;
const state = {sourceLink:"https://www.cnj.jus.br/poder-judiciario/defensoria-publica/",
  show:x => shown=x, window:{confirm:()=>{confirmations++;return true;},
  open:(...args)=>opened.push(args)}};
const sandbox = createContext(state);
runInContext(script,sandbox);
runInContext("openOfficialSource();",sandbox);
assert.equal(opened.length,0,"não abre site antes de explicar");
assert.equal(shown.primary_action.id,"find_defensoria");
assert.match(shown.message,/partilha/);
assert.match(shown.message,/estado/);
runInContext("openDefenderDirectory();",sandbox);
assert.equal(opened.length,1);
assert.match(opened[0][0],/poder-judiciario\/defensoria-publica/);
assert.equal(confirmations,1);
state.sourceLink="https://evil.example/steal";
runInContext("openOfficialSource();",sandbox);
assert.equal(opened.length,1,"destino arbitrário bloqueado");
console.log("PASS — orientação dentro do app, diretório estadual só após confirmação e URL arbitrária bloqueada.");
