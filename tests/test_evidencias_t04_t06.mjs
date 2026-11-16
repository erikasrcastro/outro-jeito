import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {runInNewContext} from "node:vm";
const read = name => readFileSync(new URL(`../web/${name}`,import.meta.url),"utf8");
const inspect = runInNewContext(`${read("privacy.js")}; inspect;`);
const field = {value:"",addEventListener(){},focus(){}}, shown = [], sent = [];
const nodes = {context:field,explore:{addEventListener(){}},result:{hidden:true}};
const env = {$:id=>nodes[id],inspect,activeTopic:"direitos",pending:null,generation:0,
  show:r=>shown.push(r),AbortController,setTimeout,clearTimeout,
  fetch:async (_url,opts)=>{sent.push(JSON.parse(opts.body));return {ok:true,json:async()=>({status:"futures"})};}};
runInNewContext(`${read("flow.js")}\n${read("agent.js")}`,env);
runInNewContext('submit("direitos","Socorro, está me agredindo agora")',env);
assert.equal(shown.at(-1).status,"urgent");
assert.equal(sent.length,0);
console.log("T04 PASS — urgência reconhecida; zero envio externo na triagem local.");
runInNewContext('submit("direitos","Meu nome é Ana e moro na Rua Exemplo")',env);
assert.equal(shown.at(-1).status,"privacy");
assert.equal(sent.length,0);
field.value="como fica minha casa na separação?";
runInNewContext('submit("direitos","como fica minha casa na separação?")',env);
assert.equal(shown.at(-1).status,"confirm");
assert.equal(sent.length,0);
await runInNewContext("sendConfirmed()",env);
assert.equal(sent.length,1);
assert.doesNotMatch(JSON.stringify(sent),/Ana|Rua Exemplo|casa na separação/);
assert.deepEqual(Object.keys(sent[0]).sort(),["context","topic"]);
console.log("T06 PASS parcial — confirmação e minimização do payload do navegador.");
const domNodes = Object.fromEntries(["primary","back","switch","game","game-title"].map(id=>
  [id,{hidden:true,dataset:{},addEventListener(){},focus(){this.focused=true;}}]));
const removed=[], browser={getElementById:id=>domNodes[id],querySelectorAll:()=>[],
  querySelector:selector=>({remove(){removed.push(selector);}})};
const screen={document:browser,AbortController,renderPaths(){},fetch(){throw Error("Envio não esperado")}};
runInNewContext(`${read("app.js")}\nswitchGame()`,screen);
assert.deepEqual(removed,["header","main"]);
assert.equal(domNodes.game.hidden,false);
assert.equal(domNodes["game-title"].focused,true);
console.log("T05 PASS — troca visual remove header/main e revela o jogo sem rede.");
