// Referências técnicas são resumidas antes de abrir páginas externas.
const DEFENSORES = "https://www.cnj.jus.br/poder-judiciario/defensoria-publica/";
const OLD_GUIDE = "https://www.cnj.jus.br/defensoria-publica-e-ministerio-publico-o-que-faz-cada-um/";
const NORMS = {
  "10406/2002": ["Código Civil — Lei 10.406/2002", "552282", "Reúne normas sobre família, guarda, bens e outras relações civis. A lei não define sozinha o resultado de uma situação pessoal."],
  "8069/1990": ["Estatuto da Criança e do Adolescente — Lei 8.069/1990", "549945", "Reúne direitos e proteção de crianças e adolescentes. A aplicação depende das circunstâncias concretas."],
  "8742/1993": ["Lei Orgânica da Assistência Social — Lei 8.742/1993", "550618", "Organiza a assistência social. Esta consulta não confirma acesso individual a benefícios ou serviços."],
  "11124/2005": ["Lei de Habitação de Interesse Social — Lei 11.124/2005", "570573", "Institui mecanismos nacionais de habitação de interesse social. Não comprova disponibilidade nem elegibilidade."],
  "8080/1990": ["Lei Orgânica da Saúde — Lei 8.080/1990", "549956", "Dispõe sobre a organização do SUS. A consulta não comprova atendimento disponível."],
  "13146/2015": ["Lei Brasileira de Inclusão — Lei 13.146/2015", "584958", "Estabelece direitos da pessoa com deficiência. Medidas específicas dependem de condições aplicáveis."]
};
const MARIA = ["Lei Maria da Penha — Lei 11.340/2006", "572125", "Prevê mecanismos de enfrentamento à violência doméstica e familiar contra a mulher. A consulta não avalia o risco ou a elegibilidade individual."];
function openDefenderDirectory() {
  if (window.confirm("O site externo pode registrar sua visita. É seguro continuar?"))
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
  warning.textContent = "Referência oficial consultada. Isso não confirma direitos ou medidas para um caso individual. A consulta externa pode ficar registrada no dispositivo.";
  open.type = "button"; open.className = "quiet"; open.textContent = "Ler a lei no Senado";
  open.onclick = () => { if (window.confirm("Abrir o Senado em outra aba? O histórico pode registrar a visita."))
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
      "Moradia, uso do imóvel e partilha podem ter requisitos distintos. O resultado depende de circunstâncias e orientação profissional. Não informe dados pessoais aqui.",
      source:{url:DEFENSORES},primary_action:{id:"find_defensoria",label:"Encontrar Defensoria"},
      secondary_action:{id:"choose_topic",label:"Explorar outro assunto"}});
  }
  if (/^https:\/\/(www\.gov\.br|www\.cnj\.jus\.br|legis\.senado\.gov\.br)\//.test(sourceLink) &&
      window.confirm("Abrir site oficial? A visita pode ficar visível no histórico do dispositivo."))
    window.open(sourceLink, "_blank", "noopener,noreferrer");
}
