const $ = id => document.getElementById(id);
let activeTopic = "direitos", pending = null, generation = 0, sourceLink = "";
const actionNames = new Set(["show_general", "return_home", "choose_topic", "show_help", "switch_game", "edit_text", "use_guided_options", "retry_on_click", "open_official_source", "confirm_preview", "find_defensoria"]);
function show(response) {
  $("result").hidden = false;
  $("chosen").textContent = response.status === "urgent" ? "Ajuda disponível" : "Seu próximo passo";
  $("message").textContent = response.message;
  sourceLink = response.source?.url || "";
  renderPaths(response);
  for (const [element, action] of [["primary", response.primary_action], ["back", response.secondary_action]]) {
    const button = $(element), allowed = action && actionNames.has(action.id);
    button.hidden = !allowed;
    if (allowed) { button.textContent = action.label; button.dataset.action = action.id; }
  }
  $("result").scrollIntoView({ block: "nearest" });
}
function home() {
  generation++; pending?.abort(); pending = null;
  $("result").hidden = true;
  renderPaths({});
  $("context").value = "";
  document.querySelector("[data-topic]").focus();
}
function showHelp() { $("help").open = true; $("help").scrollIntoView({block:"start"}); $("help").querySelector("summary").focus(); }
function switchGame() {
  generation++; pending?.abort(); pending = null;
  document.querySelector("header").remove(); document.querySelector("main").remove();
  $("game").hidden = false; $("game-title").focus();
}
function general() {
  show({status:"general", message:"Estes são assuntos gerais para explorar, sem confirmação para seu caso. Escolha um tema ou consulte as opções de ajuda.", primary_action:{id:"choose_topic",label:"Escolher assunto"}, secondary_action:{id:"show_help",label:"Ver opções de ajuda"}});
}
const actions = {
  return_home: home, choose_topic: () => { home(); document.querySelector(".choices details")?.setAttribute("open", ""); }, show_help: showHelp, switch_game: switchGame,
  edit_text: () => reviewText(),
  use_guided_options: () => { $("context").value = ""; submit(activeTopic, ""); },
  show_general: general, retry_on_click: () => submit(activeTopic, $("context").value),
  confirm_preview: () => sendConfirmed(),
  open_official_source: () => openOfficialSource(),
  find_defensoria: () => openDefenderDirectory(),
};
for (const id of ["primary", "back"]) $(id).addEventListener("click", () => actions[$(id).dataset.action]?.());
for (const button of document.querySelectorAll("[data-topic]")) button.addEventListener("click", () => submit(button.dataset.topic, $("context").value));
$("switch").addEventListener("click", switchGame);
