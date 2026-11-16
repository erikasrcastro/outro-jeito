const localReplies = {
  urgent:{status:"urgent",message:"Se há perigo agora, sua segurança vem primeiro. Você pode conhecer ajuda sem precisar explicar.",primary_action:{id:"show_help",label:"Ver opções de ajuda"},secondary_action:{id:"switch_game",label:"Trocar de tela"}},
  privacy:{status:"privacy",message:"Seu texto parece conter dados identificáveis. Podemos continuar sem eles.",primary_action:{id:"edit_text",label:"Revisar meu texto"},secondary_action:{id:"use_guided_options",label:"Continuar sem detalhes"}},
  offline:{status:"offline",message:"Não consegui consultar o serviço agora. Você ainda pode ver opções gerais.",primary_action:{id:"show_general",label:"Ver possibilidades gerais"},secondary_action:{id:"return_home",label:"Voltar ao início"}}
};
let previewSafe = "";
function submit(topic, text) {
  activeTopic = topic;
  generation++; pending?.abort(); pending = null;
  const checked = inspect(text);
  if (checked.urgent) { $("context").value = ""; return show(localReplies.urgent); }
  if (checked.pii) return show(localReplies.privacy);
  if (!checked.safe) return show({status:"clarify", message:"Que assunto deseja explorar?", primary_action:{id:"choose_topic",label:"Escolher tema"},secondary_action:{id:"show_help",label:"Ver opções de ajuda"}});
  previewSafe = checked.safe;
  const names = {reporting:"denúncia",financial_control:"controle financeiro",
    custody_concern:"guarda dos filhos",property_split:"moradia na separação"};
  const summary = checked.safe.split(" ").map(term => names[term] || term).join(", ");
  show({status:"confirm",message:`Enviar apenas estes assuntos gerais à IA: ${summary}. Sua frase original não será enviada. Deseja continuar?`,
    primary_action:{id:"confirm_preview",label:"Confirmar e explorar"},
    secondary_action:{id:"edit_text",label:"Editar descrição"}});
}
function reviewText() {
  const input = $("context"), tags = inspect(input.value).safe.split(" ").filter(Boolean);
  input.value = tags.length ? `Quero conhecer possibilidades sobre ${tags.join(" e ")}.` : "Quero conhecer direitos.";
  show({status:"review",message:"Preparei uma versão genérica. Confira e confirme antes de enviar apenas as categorias.",
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
