"""Mensagens curtas para erros e situações sem resposta."""
MESSAGES = {
    "clarify": ("Você quer saber sobre casa, filhos, trabalho ou outro tema? Escolha um assunto. Não precisa contar sua história.", "choose_topic", "Escolher assunto"),
    "urgent": ("Se há perigo agora, sua segurança vem primeiro. Veja onde pedir ajuda, se for seguro.", "show_help", "Ver ajuda agora"),
    "privacy": ("Seu texto pode mostrar quem você é. Podemos continuar sem nomes ou endereços.", "edit_text", "Mudar meu texto"),
    "groq": ("Não consegui buscar as informações agora. Você pode ver opções gerais.", "show_general", "Ver opções gerais"),
    "json": ("Não consegui conferir a resposta. Vamos escolher um assunto de novo.", "choose_topic", "Escolher assunto"),
    "senado": ("Não consegui conferir a lei no Senado agora. Não vou dizer que ela vale para você.", "show_general", "Ver opções gerais"),
    "general": ("Ainda não sei qual assunto você quer. Por exemplo: casa, filhos, trabalho ou saúde. Escolha um tema.", "choose_topic", "Escolher um assunto"),
    "preview": ("Esta é uma versão de teste. Ainda não foi possível usar as fontes externas.", "show_general", "Ver opções gerais"),
    "invalid": ("Não consegui entender o pedido. Escolha um assunto para começar.", "choose_topic", "Escolher assunto"),
    "custody": ("Sobre os filhos, cada família pode ter regras diferentes. A Defensoria Pública pode orientar, conforme as regras de atendimento.", "open_official_source", "Conhecer a Defensoria"),
    "work": ("Ainda não buscamos vagas de emprego. O Sine mostra onde procurar, mas não garante uma vaga.", "open_official_source", "Conhecer o Sine"),
}


def fallback(code):
    message, action, label = MESSAGES[code]
    other = {"privacy": ("use_guided_options", "Continuar sem detalhes"),
             "urgent": ("switch_game", "Trocar de tela")}.get(code, ("return_home", "Voltar ao início"))
    return {"status": code, "message": message,
            "primary_action": {"id": action, "label": label},
            "secondary_action": {"id": other[0], "label": other[1]},
            "evidence": "UNVERIFIED", "phase": "F2", "simulated": True}
