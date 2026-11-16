"""Catálogo local: instituições oficiais; não afirma atendimento disponível."""
GUIDES = {
    "protection": ("Ligue 180 oferece orientação sobre a rede de atendimento; não fazemos contato automático.",
                   "https://www.gov.br/mulheres/pt-br/ligue180", "Conhecer o Ligue 180"),
    "family": ("Dúvidas familiares exigem avaliar circunstâncias. O CNJ lista as Defensorias por estado, que podem orientar conforme critérios de atendimento.",
               "https://www.cnj.jus.br/poder-judiciario/defensoria-publica/", "Encontrar Defensoria do meu estado"),
    "work": ("O Sine informa formas de procurar emprego. Não verificamos vagas em tempo real.",
             "https://www.gov.br/pt-br/servicos/buscar-emprego-no-sistema-nacional-de-emprego-sine", "Conhecer o Sine"),
    "welfare": ("O Cadastro Único pode ser uma porta de entrada para programas sociais, mas cada programa tem regras próprias.",
                "https://www.gov.br/pt-br/servicos/inscrever-se-no-cadastro-unico-para-programas-sociais-do-governo-federal/", "Conhecer Cadastro Único"),
    "housing": ("Existem políticas habitacionais com requisitos específicos. Não verificamos elegibilidade ou vagas.",
                "https://www.gov.br/cidades/pt-br/acesso-a-informacao/perguntas-frequentes/habitacao", "Conhecer política habitacional"),
    "health": ("O SUS dispõe de informações sobre acesso à saúde; não consultamos disponibilidade de atendimento.",
               "https://www.gov.br/saude/pt-br", "Conhecer canais do SUS"),
    "accessibility": ("Há referências oficiais sobre acessibilidade; cada medida pode ter condições de acesso.",
                      "https://www.gov.br/mdh/pt-br/navegue-por-temas/pessoa-com-deficiencia/publicacoes/guia-pratico-de-direitos-de-acessibilidade", "Conhecer guia de acessibilidade"),
    "children": ("A rede socioassistencial pode orientar famílias em risco ou com direitos violados; não verificamos unidades abertas.",
                 "https://www.gov.br/mds/pt-br/acoes-e-programas/SUAS/unidades-de-atendimento/centro-de-referencia-especializado-de-assistencia-social-creas", "Conhecer orientação do CREAS"),
    "justice": ("Para orientação jurídica sobre família, moradia ou patrimônio, encontre o serviço da Defensoria do seu estado. O atendimento depende dos critérios locais.",
                "https://www.cnj.jus.br/poder-judiciario/defensoria-publica/", "Encontrar Defensoria do meu estado"),
}

def response(category, status="orientation"):
    message, url, label = GUIDES[category]
    if status == "senado":
        message = "Não consegui confirmar a norma no Senado agora. " + message
    return {"status": status, "evidence": "UNVERIFIED", "phase": "F4", "simulated": False,
            "message": message, "source": {"url": url, "source_kind": "official_guide"},
            "primary_action": {"id": "open_official_source", "label": label},
            "secondary_action": {"id": "choose_topic", "label": "Conhecer outro tema"}}
