// Referências técnicas são resumidas antes de abrir páginas externas.
const DEFENSORES = "https://www.cnj.jus.br/poder-judiciario/defensoria-publica/";
const OLD_GUIDE = "https://www.cnj.jus.br/defensoria-publica-e-ministerio-publico-o-que-faz-cada-um/";
const NORMS = {
  "10406/2002": ["Código Civil — Lei 10.406/2002", "552282", "Essa lei fala de família, filhos e bens, como uma casa. Por exemplo: casa alugada e casa comprada podem ter regras diferentes após uma separação."],
  "8069/1990": ["Estatuto da Criança e do Adolescente — Lei 8.069/1990", "549945", "Essa lei fala dos direitos das crianças e dos jovens. Por exemplo: receber cuidados e proteção. Cada situação é diferente."],
  "8742/1993": ["Lei Orgânica da Assistência Social — Lei 8.742/1993", "550618", "Essa lei fala da ajuda do governo a quem precisa. Por exemplo: alguns benefícios têm regras. Não sabemos quem pode receber."],
  "11124/2005": ["Lei de Habitação de Interesse Social — Lei 11.124/2005", "570573", "Essa lei fala de programas para ajudar com moradia. Por exemplo: ter acesso a uma casa depende das regras de cada programa."],
  "8080/1990": ["Lei Orgânica da Saúde — Lei 8.080/1990", "549956", "Essa lei ajuda a organizar o SUS, o serviço público de saúde. Por exemplo: posto de saúde. Não sabemos se há vaga agora."],
  "13146/2015": ["Lei Brasileira de Inclusão — Lei 13.146/2015", "584958", "Essa lei protege pessoas com deficiência. Por exemplo: poder usar serviços e lugares com mais facilidade. Cada pedido tem regras."]
};
const MARIA = ["Lei Maria da Penha — Lei 11.340/2006", "572125", "Essa lei fala de proteger mulheres em situações de violência em casa ou na família. Por exemplo: buscar ajuda para ficar mais segura."];
function openDefenderDirectory() {
  if (window.confirm("O site pode guardar que você entrou nele. Quer abrir mesmo assim?"))
    window.open(DEFENSORES, "_blank", "noopener,noreferrer");
}
function showLawGuide(info) {
  document.getElementById("oj-source-guide")?.remove();
  const box = document.createElement("section"), title = document.createElement("h3");
  const explanation = document.createElement("p"), warning = document.createElement("p");
  const open = document.createElement("button"), close = document.createElement("button");
  box.id = "oj-source-guide"; box.className = "help"; box.setAttribute("role", "region");
  title.textContent = info[0]; title.tabIndex = -1;
  explanation.textContent = info[2];
  warning.textContent = "Esta lei não diz, sozinha, o que vale para você. Se abrir o Senado, a visita pode aparecer no histórico do aparelho.";
  open.type = "button"; open.className = "quiet"; open.textContent = "Ler a lei no Senado";
  open.onclick = () => { if (window.confirm("Quer abrir o site do Senado? Isso pode ficar no histórico do celular ou computador."))
    window.open("https://legis.senado.gov.br/norma/" + info[1], "_blank", "noopener,noreferrer"); };
  close.type = "button"; close.className = "quiet"; close.textContent = "Fechar explicação";
  close.onclick = () => box.remove();
  box.append(title, explanation, warning, open, close);
  document.querySelector("#result .actions").before(box); title.focus();
}
function openOfficialSource() {
  const match = /^https:\/\/legis\.senado\.leg\.br\/dadosabertos\/legislacao\/LEI\/(\d+)\/(\d+)\.json$/.exec(sourceLink);
  if (match) { const found = NORMS[match[1] + "/" + match[2]];
    return found ? showLawGuide(found) : undefined; }
  if (sourceLink === "https://legis.senado.gov.br/norma/572125")
    return showLawGuide(MARIA);
  if ([DEFENSORES, OLD_GUIDE].includes(sourceLink)) {
    return show({status:"orientacao", message:
      "Uma casa alugada e uma casa comprada têm regras diferentes. Por exemplo: morar numa casa não quer dizer que ela é sua. Você pode pedir ajuda à Defensoria para entender melhor, sem contar seus dados aqui.",
      source:{url:DEFENSORES},primary_action:{id:"find_defensoria",label:"Encontrar Defensoria"},
      secondary_action:{id:"choose_topic",label:"Explorar outro assunto"}});
  }
  if (/^https:\/\/(www\.gov\.br|www\.cnj\.jus\.br|legis\.senado\.gov\.br)\//.test(sourceLink) &&
      window.confirm("Abrir site oficial? A visita pode ficar visível no histórico do dispositivo."))
    window.open(sourceLink, "_blank", "noopener,noreferrer");
}
