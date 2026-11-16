import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {runInNewContext} from "node:vm";
const read = name => readFileSync(new URL(`../web/${name}`,import.meta.url),"utf8");
const inspect = runInNewContext(`${read("privacy.js")}; inspect;`);
const field = {value:"",focus(){},addEventListener(){}};
const result = {hidden:true,addEventListener(){}};
const nodes = {context:field,result,explore:{addEventListener(){}}};
const listeners = {};
for (const [id,n] of Object.entries(nodes)) n.addEventListener=(type,fn)=>listeners[`${id}:${type}`]=fn;
const shown=[], sent=[];
const sandbox={$:id=>nodes[id],inspect,generation:0,pending:null,activeTopic:"direitos",
  show:r=>shown.push(r),AbortController,setTimeout,clearTimeout,
  fetch:async (_url,opts)=>{sent.push(JSON.parse(opts.body));return {ok:true,json:async()=>({status:"futures"})};}};
runInNewContext(`${read("flow.js")}\n${read("agent.js")}`,sandbox);
field.value="Socorro, é uma agressão"; listeners["context:input"]();
assert.equal(shown.at(-1).status,"urgent");
assert.equal(sent.length,0);
field.value="Meu nome é Maria e moro na Rua Exemplo";listeners["context:input"]();
assert.equal(shown.at(-1).status,"privacy");
runInNewContext("reviewText()",sandbox);
assert.doesNotMatch(field.value,/Maria|Rua Exemplo/);
listeners["explore:click"]();
assert.equal(shown.at(-1).status,"confirm");
assert.equal(sent.length,0);
await runInNewContext("sendConfirmed()",sandbox);
assert.equal(sent.length,1);
assert.doesNotMatch(JSON.stringify(sent),/Maria|Rua Exemplo|Socorro/);
console.log("PASS — urgência local, revisão e confirmação antes do envio.");
