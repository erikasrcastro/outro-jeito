import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {runInNewContext} from "node:vm";
const code=readFileSync(new URL("../web/guidance.js",import.meta.url),"utf8")+"\n"+
  readFileSync(new URL("../web/app.js",import.meta.url),"utf8");
const nodes=Object.fromEntries(["result","chosen","message","primary","back","context","help","switch"].map(id=>
  [id,{dataset:{},addEventListener(){},scrollIntoView(){},querySelector(){return{focus(){}}},focus(){}}]));
let guide=null;
const calls=[],listeners={};
for(const [id,node] of Object.entries(nodes))node.addEventListener=(ev,fn)=>listeners[id+ev]=fn;
const dom={getElementById:id=>id==="oj-source-guide"?guide:nodes[id],
  createElement:tag=>({tag,children:[],setAttribute(){},append(...items){this.children.push(...items);},
    focus(){this.focused=true},remove(){if(this===guide)guide=null}}),
  querySelector:sel=>sel==="#result .actions"?{before(box){guide=box}}:{focus(){}},
  querySelectorAll:()=>[]};
const sandbox={renderPaths:()=>{},document:dom,
  window:{open:(...args)=>calls.push(args),confirm:()=>true},AbortController};
runInNewContext(code,sandbox);
runInNewContext(`show({status:'conditional',message:'Registro oficial',source:{url:'https://legis.senado.gov.br/norma/572125'},primary_action:{id:'open_official_source',label:'Entender a lei'},secondary_action:{id:'return_home',label:'Voltar'}})`,sandbox);
listeners.primaryclick();
assert.equal(calls.length,0,"mostrar explicação antes de abrir outra aba");
assert.equal(guide.children[0].textContent,"Lei Maria da Penha — Lei 11.340/2006");
guide.children[3].onclick();
assert.equal(calls.length,1);
assert.equal(calls[0][0],"https://legis.senado.gov.br/norma/572125");
runInNewContext(`show({status:'conditional',message:'Erro',source:{url:'https://example.com/evil'},primary_action:{id:'open_official_source',label:'Ver fonte'},secondary_action:{id:'return_home',label:'Voltar'}})`,sandbox);
assert.equal(guide,null,"explicação anterior retirada");
listeners.primaryclick();
assert.equal(calls.length,1,"URL externa não autorizada bloqueada");
console.log("PASS — explicação antes da fonte e URL arbitrária bloqueada.");
