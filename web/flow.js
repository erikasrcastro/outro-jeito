const localReplies = {
  urgent:{status:"urgent",message:"Se há perigo agora, sua segurança vem primeiro. Veja onde pedir ajuda, se isso for seguro.",primary_action:{id:"show_help",label:"Ver opções de ajuda"},secondary_action:{id:"switch_game",label:"Trocar de tela"}},
  privacy:{status:"privacy",message:"Seu texto pode mostrar quem você é. Podemos seguir sem esses dados.",primary_action:{id:"edit_text",label:"Revisar meu texto"},secondary_action:{id:"use_guided_options",label:"Continuar sem detalhes"}},
  offline:{status:"offline",message:"Não consegui buscar as informações agora. Você pode ver opções gerais.",primary_action:{id:"show_general",label:"Ver possibilidades gerais"},secondary_action:{id:"return_home",label:"Voltar ao início"}}
};
let previewSafe = "";
function submit(topic, text) {
  activeTopic = topic;
  generation++; pending?.abort(); pending = null;
  const checked = inspect(text);
  if (checked.urgent) { $("context").value = ""; return show(localReplies.urgent); }
  if (checked.pii) return show(localReplies.privacy);
  if (!checked.safe) return show({status:"clarify", message:"Sobre o que você quer saber? Escolha um tema.", primary_action:{id:"choose_topic",label:"Escolher tema"},secondary_action:{id:"show_help",label:"Ver opções de ajuda"}});
  previewSafe = checked.safe;
  const names = {reporting:"denúncia",financial_control:"controle financeiro",
    custody_concern:"guarda dos filhos",property_split:"moradia na separação"};
  const summary = checked.safe.split(" ").map(term => names[term] || term).join(", ");
  show({status:"confirm",message:`Vou enviar só estas palavras gerais: ${summary}. Não vou enviar sua frase. Tudo bem?`,
    primary_action:{id:"confirm_preview",label:"Sim, quero continuar"},
    secondary_action:{id:"edit_text",label:"Mudar meu texto"}});
}
function reviewText() {
  const input = $("context"), tags = inspect(input.value).safe.split(" ").filter(Boolean);
  input.value = tags.length ? `Quero conhecer possibilidades sobre ${tags.join(" e ")}.` : "Quero conhecer direitos.";
  show({status:"review",message:"Troquei sua frase por palavras gerais. Confira antes de continuar.",
    primary_action:{id:"retry_on_click",label:"Ver resumo para envio"},
    secondary_action:{id:"use_guided_options",label:"Continuar sem detalhes"}});
  input.focus();
}
$("context").addEventListener("input", () => {
  generation++; pending?.abort(); pending = null;
  const scanned = inspect($("context").value);
  if (scanned.urgent) return show(localReplies.urgent);
  if (scanned.pii) return show(localReplies.privacy);
  $("result").hidden = true;
});
$("explore").addEventListener("click", () => submit(activeTopic, $("context").value));
