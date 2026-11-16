// Mostra escolhas geradas, sem tratar hipóteses como direitos verificados.
function renderPaths(response) {
  const panel = document.getElementById("paths");
  if (!panel) return;
  panel.replaceChildren();
  panel.hidden = !Array.isArray(response.paths) || !response.paths.length;
  if (panel.hidden) return;
  for (const [index, path] of response.paths.entries()) {
    const item = document.createElement("section");
    const button = document.createElement("button");
    const question = document.createElement("p");
    const possibility = document.createElement("p");
    button.type = "button";
    button.textContent = `${index + 1}. ${path.title} — entender melhor`;
    question.hidden = true;
    possibility.textContent = path.possibility;
    button.onclick = () => {
      question.textContent = `Se quiser, pense nesta pergunta: ${path.question} Você não precisa responder aqui.`;
      question.hidden = false;
      question.setAttribute("tabindex", "-1");
      question.focus();
    };
    item.append(button, possibility, question);
    panel.append(item);
  }
}

async function sendConfirmed() {
  const text = $("context").value, inspected = inspect(text);
  if (inspected.urgent || inspected.pii || inspected.safe !== previewSafe) return submit(activeTopic, text);
  $("context").value = "";
  const controller = new AbortController(), token = ++generation;
  pending?.abort(); pending = controller;
  show({status:"loading", message:"Vou buscar informações. Você pode parar quando quiser.",
    primary_action:{id:"return_home",label:"Cancelar e voltar"},
    secondary_action:{id:"show_help",label:"Ajuda imediata"}});
  const timeout = setTimeout(() => controller.abort(), 25000);
  try {
    const response = await fetch("/api/v1/explore", {
      method:"POST", headers:{"Content-Type":"application/json"}, signal:controller.signal,
      body:JSON.stringify({topic:activeTopic,context:previewSafe})});
    if (!response.ok) throw Error("Serviço indisponível");
    const data = await response.json();
    if (generation === token) show(data);
  } catch (_) { if (generation === token) show(localReplies.offline); }
  finally { clearTimeout(timeout); if (pending === controller) pending = null; }
}
