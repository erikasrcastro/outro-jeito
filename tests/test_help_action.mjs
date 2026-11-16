import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { runInNewContext } from "node:vm";
const read = f => readFileSync(new URL(`../web/${f}`, import.meta.url), "utf8");
const listeners = {}, calls = [];
const el = Object.fromEntries(["result","chosen","message","primary","back","context","help","switch","explore"].map(id => [id, {
  id, hidden:true, dataset:{}, value:"", textContent:"", open:false,
  addEventListener:(event,cb)=>listeners[`${id}:${event}`]=cb,
  scrollIntoView:()=>calls.push("scroll"),
  querySelector:()=>({focus:()=>calls.push("focus")})
}]));
const document = {getElementById:id=>el[id],querySelectorAll:()=>[],querySelector:()=>({focus(){}})};
const sandbox = {renderPaths:()=>{},document, AbortController, setTimeout, clearTimeout,
  inspect:()=>({safe:"",urgent:false,pii:false}), fetch:async()=>({ok:true,json:async()=>({})})};
runInNewContext(read("app.js"), sandbox);  // Must not fail before flow.js defines reviewText.
runInNewContext(read("flow.js"), sandbox);
assert.equal(typeof listeners["primary:click"], "function");
runInNewContext('show({status:"urgent",message:"Ajuda",primary_action:{id:"show_help",label:"Ver opções de ajuda"},secondary_action:{id:"switch_game",label:"Trocar"}})', sandbox);
listeners["primary:click"]();
assert.equal(el.help.open, true);
assert.deepEqual(calls.slice(-2), ["scroll", "focus"]);
assert.equal(el.primary.dataset.action, "show_help");
console.log("PASS — ações registradas; Ajuda abre e recebe foco.");
