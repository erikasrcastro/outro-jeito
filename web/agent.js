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
    const possibility = document.createElement("p");
    const title = `${index + 1}. ${path.title}`;
    button.type = "button";
    button.textContent = title + " — ver exemplo";
    possibility.textContent = path.possibility;
    possibility.hidden = true;
    possibility.id = "oj-path-" + index;
    button.setAttribute("aria-expanded", "false");
    button.setAttribute("aria-controls", possibility.id);
    button.onclick = () => {
      const opening = possibility.hidden;
      possibility.hidden = !opening;
      button.textContent = title + (opening ? " — fechar" : " — ver exemplo");
      button.setAttribute("aria-expanded", String(opening));
    };
    item.append(button, possibility);
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
