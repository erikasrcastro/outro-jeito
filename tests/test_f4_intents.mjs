import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {runInNewContext} from "node:vm";
const source = readFileSync(new URL("../web/privacy.js", import.meta.url), "utf8");
const {inspect} = runInNewContext(`${source}; ({inspect});`);
const cases = [
  ["onde posso denunciar agressão?", "reporting"],
  ["ele pode tomar conta do meu dinheiro?", "financial_control"],
  ["ele pode tomar meus filhos de mim?", "custody_concern"],
  ["como fica minha casa se eu me separar?", "property_split"],
  ["onde registrar denúncia de violência?", "reporting"],
  ["posso perder a guarda da minha filha?", "custody_concern"],
  ["quem administra meus rendimentos?", "financial_control"],
  ["como dividir o imóvel no divórcio?", "property_split"]
];
for (const [text, intent] of cases) {
  const result = inspect(text);
  assert(result.safe.split(" ").includes(intent), `${intent} não identificado`);
  assert(!result.safe.includes(text), "Texto livre nunca deve sair");
  assert(!result.urgent, "Pergunta informativa não é emergência confirmada");
}
for (const text of ["quero construir uma casa", "como guardar dinheiro", "quero emprego"])
  assert(!inspect(text).safe.includes("property_split"));
assert(!inspect("quero guardar dinheiro").safe.includes("guarda"));
assert(inspect("denunciar agressão e levar meus filhos").safe.includes("custody_concern"));
assert(inspect("meu nome é Maria e moro na Rua Exemplo").pii);
console.log("PASS — oito intenções contextuais, privacidade e perguntas sem perigo imediato.");
