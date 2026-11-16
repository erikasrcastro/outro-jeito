// Orientação antes de abrir fonte externa: sem identificação e sem rede adicional.
const DEFENSORES = "https://www.cnj.jus.br/poder-judiciario/defensoria-publica/";
const OLD_GUIDE = "https://www.cnj.jus.br/defensoria-publica-e-ministerio-publico-o-que-faz-cada-um/";
function openDefenderDirectory() {
  if (window.confirm("O site externo pode registrar sua visita e pedir dados caso você escolha solicitar atendimento. É seguro continuar?"))
    window.open(DEFENSORES, "_blank", "noopener,noreferrer");
}
function openOfficialSource() {
  if ([DEFENSORES, OLD_GUIDE].includes(sourceLink)) {
    return show({status:"orientacao", message:
      "Sobre a casa após a separação, são questões diferentes: onde morar agora, uso do imóvel e eventual partilha. " +
      "O resultado pode depender de aluguel, financiamento ou propriedade, de quando foi adquirido e do regime de bens. " +
      "Sem informar esses dados aqui, você pode localizar orientação jurídica na Defensoria do seu estado, sujeita a critérios de atendimento.", source:{url:DEFENSORES},
      primary_action:{id:"find_defensoria",label:"Encontrar Defensoria do meu estado"},
      secondary_action:{id:"choose_topic",label:"Explorar outro caminho"}});
  }
  const official = /^https:\/\/(www\.gov\.br|www\.cnj\.jus\.br|legis\.senado\.gov\.br)\//.test(sourceLink);
  const senate = /^https:\/\/legis\.senado\.leg\.br\/dadosabertos\/legislacao\/LEI\/(10406\/2002|8069\/1990|8742\/1993|11124\/2005|8080\/1990|13146\/2015)\.json$/.test(sourceLink);
  if ((official || senate) && window.confirm("Abrir site oficial? A visita pode ficar visível no histórico deste dispositivo."))
    window.open(sourceLink, "_blank", "noopener,noreferrer");
}
