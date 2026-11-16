"""Todo fallback tem ação real e saída alternativa, sem LLM."""
MESSAGES = {
    "clarify": ("Sua pergunta pode envolver mais de um assunto. Qual você quer explorar primeiro? Não precisa contar detalhes.", "choose_topic", "Escolher um dos nove temas"),
    "urgent": ("Se existe perigo agora, sua segurança vem primeiro.", "show_help", "Ver opções de ajuda"),
    "privacy": ("O texto pode identificar alguém. Podemos seguir sem esses dados.", "edit_text", "Revisar meu texto"),
    "groq": ("A interpretação está indisponível. Nada foi confirmado.", "show_general", "Ver caminhos gerais"),
    "json": ("Não consegui validar a resposta com segurança.", "choose_topic", "Escolher assunto"),
    "senado": ("Não consegui confirmar a referência legal na fonte oficial.", "show_general", "Ver possibilidades gerais"),
    "general": ("Não consegui identificar o foco sem usar seu relato pessoal. Escolha um dos nove assuntos para ver uma orientação específica.", "choose_topic", "Escolher um assunto"),
    "preview": ("A triagem local funcionou. Groq e Senado ainda não foram conectados.", "show_general", "Ver possibilidades gerais"),
    "invalid": ("Essa entrada não pôde ser utilizada.", "choose_topic", "Escolher assunto"),
    "custody": ("Guarda de filhos exige análise própria; este MVP ainda não verifica essas normas. Consulte o diretório oficial de Defensorias por estado.", "open_official_source", "Encontrar Defensoria do meu estado"),
    "work": ("Ainda não consultamos vagas ou benefícios de trabalho. O Sine informa caminhos oficiais de busca de emprego, sem garantia de vaga.", "open_official_source", "Conhecer o Sine oficial"),
}


def fallback(code):
    message, action, label = MESSAGES[code]
    other = {"privacy": ("use_guided_options", "Continuar sem contar detalhes"),
             "urgent": ("switch_game", "Trocar de tela")}.get(code, ("return_home", "Voltar ao início"))
    return {"status": code, "message": message,
            "primary_action": {"id": action, "label": label},
            "secondary_action": {"id": other[0], "label": other[1]},
            "evidence": "UNVERIFIED", "phase": "F2", "simulated": True}
