import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {runInNewContext} from "node:vm";
const read = name => readFileSync(new URL(`../web/${name}`, import.meta.url), "utf8");
const inspect = runInNewContext(`${read("privacy.js")}; inspect;`);
const node = {value:"",addEventListener() {}};
const sent = [], shown = [];
const sandbox = {activeTopic:"direitos",generation:0,pending:null,inspect, AbortController,
  setTimeout,clearTimeout,$:()=>node,show:r=>shown.push(r),
  fetch:async (url,opts)=>{sent.push({url,body:JSON.parse(opts.body)});return {ok:true,json:async()=>({status:"futures"})};}};
runInNewContext(`${read("flow.js")}\n${read("agent.js")}`, sandbox);
await runInNewContext('submit("direitos", "Meu nome é Maria e moro na Rua Bauru")', sandbox);
assert.equal(shown.at(-1).status,"privacy");
await runInNewContext('submit("direitos", "socorro, está me agredindo agora")', sandbox);
assert.equal(shown.at(-1).status,"urgent");
node.value = "Alguém controla meus contatos e renda, CANARIO999";
runInNewContext('submit("direitos", documentText)', {...sandbox,documentText:node.value});
assert.equal(shown.at(-1).status,"confirm");
assert.equal(sent.length,0,"Nenhuma API antes da confirmação");
await runInNewContext("sendConfirmed()",sandbox);
assert.equal(sent.length,1);
assert.equal(sent[0].body.context,"contatos renda");
assert.equal(node.value, "");
assert.doesNotMatch(JSON.stringify(sent),/Alguém|CANARIO999|Maria|Bauru/);
console.log("PASS — consentimento antes do envio; texto original nunca sai.");
