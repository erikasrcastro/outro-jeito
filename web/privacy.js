// Triagem local preliminar; texto livre jamais é enviado integralmente.
function inspect(text) {
  const value = text.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  const quote = /li uma noticia|num filme|em um filme|no livro|era uma citacao/.test(value);
  const threat = /\bsocorro\b|\bme trancou\b|\best[aao]+ armado|\best[aao]+ me agredindo|\b(vai|quer) me matar|\bnao consigo (respirar|sair)|\bsangramento intenso/.test(value);
  const denial = /nao (esta|ta) armado|nao me trancou|nao estou em perigo/.test(value);
  const urgent = threat && !quote && !(denial && !/vai me matar|me agredindo|nao consigo respirar|socorro/.test(value));
  const pii = /[\w.+-]+@[\w.-]+\.[a-z]{2,}|\d{3}[. ]?\d{3}[. ]?\d{3}[-. ]?\d{2}|\d{5}-?\d{3}|\b(?:\+?55\s?)?(?:\(?\d{2}\)?\s?)?9\d{4}[- ]?\d{4}\b|\b(rua|avenida|travessa|alameda|cep|meu nome e|me chamo|se chama)\b/i.test(value);
  const labels = ["reporting", "financial_control", "custody_concern", "property_split", "contatos", "controle", "moradia", "renda", "protecao", "direitos", "guarda", "custodia", "trabalho", "emprego", "agressao", "violencia", "ameaca", "convivencia", "pensao", "divorcio", "separacao", "alimentos", "cras", "creas", "cadunico", "beneficio", "assistencia", "bpc", "aluguel", "habitacao", "saude", "sus", "acessibilidade", "deficiencia", "autismo", "crianca", "adolescente", "defensoria", "advogado", "justica"];
  const reports = /\b(denunci\w*|delegacia|boletim de ocorrencia)\b/.test(value) && /\b(agress\w*|violenc\w*|ameac\w*|abuso)\b/.test(value);
  const finance = /\b(dinheiro|salario|rendimentos|conta bancaria|financas|bens)\b/.test(value) && /\b(tomar|control\w*|reter|imped\w*|apropri\w*|administr\w*)\b/.test(value);
  const custody = /\b(filh[oa]s?|crianc[as]+|guarda|custodia)\b/.test(value) && /\b(tomar|tomou|tirar|tirou|levar|levou|perder|afastar|ficar com)\b/.test(value);
  const property = /\b(casa|imovel|apartamento|moradia|partilha|bens)\b/.test(value) && /\b(separ\w*|divorci\w*|partilh\w*|terminar|rompimento)\b/.test(value);
  const hints = [reports && "reporting", finance && "financial_control", custody && "custody_concern", property && "property_split"].filter(Boolean);
  const safe = [...new Set([...labels.filter(word => new RegExp("\\b" + word + "\\b").test(value)), ...hints])].join(" ");
  return { pii, urgent, safe };
}
// Assuntos guiados: escolha local, sem envio da narrativa original.
const themes = [
  ["Proteção e violência", "protecao", "direitos"],
  ["Família e guarda", "guarda", "direitos"],
  ["Trabalho e renda", "trabalho", "caminhos"],
  ["Assistência social", "assistencia", "apoio"],
  ["Moradia", "moradia", "caminhos"],
  ["Saúde", "saude", "apoio"],
  ["Inclusão e acessibilidade", "acessibilidade", "direitos"],
  ["Crianças e adolescentes", "crianca", "direitos"],
  ["Acesso à justiça", "defensoria", "direitos"],
];
if (typeof document !== "undefined") {
const picker = document.createElement("details"), title = document.createElement("summary");
title.textContent = "Escolher um assunto específico";
picker.append(title);
for (const [label, word, topic] of themes) {
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = label;
  button.onclick = () => {
    document.getElementById("context").value = `Quero conhecer ${word}.`;
    picker.open = false;
    submit(topic, document.getElementById("context").value);
  };
  picker.append(button);
}
document.querySelector(".choices").append(picker);
}
