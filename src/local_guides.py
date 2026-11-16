"""Catálogo oficial simplificado; sem prometer atendimento ou benefícios."""
GUIDES = {
    "protection": ("O Ligue 180 orienta mulheres e informa onde pedir ajuda. O aplicativo não liga para ninguém.",
                   "https://www.gov.br/mulheres/pt-br/ligue180", "Entender o Ligue 180"),
    "family": ("A Defensoria Pública pode explicar regras sobre filhos e casa, caso você possa ser atendida.",
               "https://www.cnj.jus.br/poder-judiciario/defensoria-publica/", "Conhecer a Defensoria do meu estado"),
    "work": ("O Sine mostra como buscar emprego. Por exemplo: onde procurar vagas. Não sabemos se há vaga agora.",
             "https://www.gov.br/pt-br/servicos/buscar-emprego-no-sistema-nacional-de-emprego-sine", "Conhecer o Sine"),
    "welfare": ("O Cadastro Único pode ajudar a conhecer programas sociais. Cada programa tem regras.",
                "https://www.gov.br/pt-br/servicos/inscrever-se-no-cadastro-unico-para-programas-sociais-do-governo-federal/", "Entender o Cadastro Único"),
    "housing": ("Há programas de moradia, mas cada um tem regras. Não sabemos se há vagas nem quem pode participar.",
                "https://www.gov.br/cidades/pt-br/acesso-a-informacao/perguntas-frequentes/habitacao", "Conhecer ajuda com moradia"),
    "health": ("O SUS oferece atendimento público. Não sabemos se há vagas ou horários disponíveis agora.",
               "https://www.gov.br/saude/pt-br", "Conhecer o SUS"),
    "accessibility": ("Existem direitos para pessoas com deficiência. Cada pedido pode ter regras diferentes.",
                      "https://www.gov.br/mdh/pt-br/navegue-por-temas/pessoa-com-deficiencia/publicacoes/guia-pratico-de-direitos-de-acessibilidade", "Conhecer direitos de acesso"),
    "children": ("Há serviços que orientam famílias em risco. Não sabemos quais estão abertos agora.",
                 "https://www.gov.br/mds/pt-br/acoes-e-programas/SUAS/unidades-de-atendimento/centro-de-referencia-especializado-de-assistencia-social-creas", "Conhecer ajuda à família"),
    "justice": ("A Defensoria Pública pode orientar sobre filhos, casa ou dinheiro, conforme as regras de atendimento.",
                "https://www.cnj.jus.br/poder-judiciario/defensoria-publica/", "Conhecer a Defensoria"),
}

def response(category, status="orientation"):
    message, url, label = GUIDES[category]
    if status == "senado":
        message = "Não consegui conferir a lei no Senado agora. " + message
    return {"status": status, "evidence": "UNVERIFIED", "phase": "F4", "simulated": False,
            "message": message, "source": {"url": url, "source_kind": "official_guide"},
            "primary_action": {"id": "open_official_source", "label": label},
            "secondary_action": {"id": "choose_topic", "label": "Ver outro assunto"}}
