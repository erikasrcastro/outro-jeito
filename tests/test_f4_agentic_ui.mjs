import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {runInNewContext} from "node:vm";
const src=readFileSync(new URL("../web/agent.js",import.meta.url),"utf8");
const panel={hidden:true,children:[],replaceChildren(){this.children=[];},append(e){this.children.push(e);}};
const document={getElementById:id=>id==="paths"?panel:null,createElement:tag=>({
  tag,hidden:false,children:[],textContent:"",attrs:{},
  append(...items){this.children.push(...items);},
  setAttribute(key,value){this.attrs[key]=value;},focus(){this.focused=true;}})};
const paths=[{title:"Entender a casa",possibility:"Se a casa é alugada, há regras.",question:"Quer saber mais?"},
  {title:"Pedir orientação",possibility:"Caso queira, pode buscar ajuda.",question:"O que prefere?"}];
runInNewContext(`${src}\nrenderPaths({paths:pathsFromTest})`,{document,pathsFromTest:paths});
assert.equal(panel.hidden,false);
assert.equal(panel.children.length,2);
const first=panel.children[0],button=first.children[0],detail=first.children[1];
assert.equal(first.children.length,2,"nenhuma pergunta redundante na tela");
assert.equal(detail.hidden,true);
assert.equal(button.attrs["aria-expanded"],"false");
assert.match(button.textContent,/ver exemplo/);
button.onclick();
assert.equal(detail.hidden,false);
assert.equal(button.attrs["aria-expanded"],"true");
assert.match(detail.textContent,/casa é alugada/);
assert.doesNotMatch(detail.textContent,/Quer saber|Se quiser, pense/);
button.onclick();
assert.equal(detail.hidden,true);
assert.equal(button.attrs["aria-expanded"],"false");
runInNewContext(`${src}\nrenderPaths({status:"error"})`,{document});
assert.equal(panel.hidden,true);
console.log("PASS — exemplos expansíveis e sem perguntas repetidas.");
