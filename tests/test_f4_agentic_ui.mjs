import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {runInNewContext} from "node:vm";
const src = readFileSync(new URL("../web/agent.js",import.meta.url),"utf8");
const panel={hidden:true,children:[],replaceChildren(){this.children=[];},append(e){this.children.push(e);}};
const document={getElementById:id=>id==="paths"?panel:null,createElement:tag=>({tag,
  hidden:false,children:[],textContent:"",append(...items){this.children.push(...items);},
  setAttribute(){},focus(){this.focused=true;}})};
const sandbox={document};
const paths=[{title:"Conhecer opções",possibility:"Uma possibilidade é estudar normas.",question:"Onde consultar a norma?"},
  {title:"Buscar orientação",possibility:"Outra possibilidade é buscar orientação.",question:"Qual serviço procurar?"}];
runInNewContext(`${src}\nrenderPaths({paths:pathsFromTest})`,{...sandbox,pathsFromTest:paths});
assert.equal(panel.hidden,false);
assert.equal(panel.children.length,2);
assert.match(panel.children[0].children[1].textContent,/estudar normas/);
assert.doesNotMatch(panel.children[0].children[1].textContent,/não verificada/);
panel.children[0].children[0].onclick();
assert.match(panel.children[0].children[2].textContent,/Onde consultar/);
assert.equal(panel.children[0].children[2].focused,true);
runInNewContext(`${src}\nrenderPaths({status:"error"})`,sandbox);
assert.equal(panel.hidden,true);
console.log("PASS — possibilidades dinâmicas, clique executável e limpeza de estado.");
