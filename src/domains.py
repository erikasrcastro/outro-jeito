"""Domínios permitidos; pistas não são prova de elegibilidade."""
DOMAINS = {
    "protection": ("Proteção e violência", "violencia agressao ameaca socorro protecao contatos autonomia"),
    "family": ("Família e guarda", "guarda custodia convivencia pensao divorcio separacao alimentos visitas"),
    "work": ("Trabalho e renda", "emprego trabalho desemprego renda salario qualificacao curso"),
    "welfare": ("Assistência social", "cras creas cadunico beneficio assistencia bpc bolsafamilia"),
    "housing": ("Moradia", "moradia aluguel habitacao abrigo despejo"),
    "health": ("Saúde", "saude sus atendimento medico psicologo terapia hospital"),
    "accessibility": ("Inclusão e acessibilidade", "acessibilidade deficiencia autismo discriminacao"),
    "children": ("Crianças e adolescentes", "crianca adolescente menor escola infancia dependencia"),
    "justice": ("Acesso à justiça", "defensoria advogado justica processo documento juridica"),
}
LAWS = {  # Lei federal, número e ano; cada consulta requer prova real do Senado.
    "protection": (11340, 2006), "family": (10406, 2002),
    "welfare": (8742, 1993), "housing": (11124, 2005),
    "health": (8080, 1990), "accessibility": (13146, 2015),
    "children": (8069, 1990),
}

def candidates(concerns):
    seen = set(concerns)
    mapped = {"reporting":"protection", "financial_control":"justice",
              "custody_concern":"family", "property_split":"family"}
    seen.update(mapped[tag] for tag in concerns if tag in mapped)
    return [key for key, (_, terms) in DOMAINS.items() if seen.intersection(terms.split()) or key in seen]
