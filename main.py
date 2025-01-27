from AgenteOrganizador import AgenteOrganizador
from AgenteInteligente import AgenteInteligente
from AgenteGeradorLink import AgenteGeradorLink

from owlready2 import get_ontology
ontologia = get_ontology("ReuniaoDSD.rdf").load()
"""
Teste dos agentes
"""
# Lista de continentes
continentes = [ontologia.America, ontologia.Europa, ontologia.Asia]

# Inicializar agentes
agente_organizador = AgenteOrganizador(continentes)
agente_inteligente = AgenteInteligente("ReuniaoDSD.rdf")
agente_gerador_link = AgenteGeradorLink("ReuniaoDSD.rdf")

# Horário sugerido pelo Agente Inteligente
horario_sugerido = "14:00"

# Organizador -> Inteligente
confirmarHorario = agente_organizador.solicitar_horario(agente_inteligente, horario_sugerido)
#confirmarHorario : retorna na primeira posição o horário sugerido, na posicao 1 a confirmação True ou False
print(f"Horário ajustado: {confirmarHorario[0]}")

# Verificar e confirmar o horário
if confirmarHorario[1]:
    # Organizador -> GeradorLink
    resultado = agente_organizador.solicitar_link(agente_gerador_link, [ontologia.Audio,ontologia.Slide], 250)
    
    # Tratar o resultado da geração de link
    if resultado["ferramenta"] is None:
        print("Nenhuma ferramenta disponível para os requisitos especificados.")
    else:
        print(f"Ferramenta Escolhida: {resultado['ferramenta']}")
        print(f"Link Gerado: {resultado['link']}")
else:
    print("Horário da reunião não confirmado.")