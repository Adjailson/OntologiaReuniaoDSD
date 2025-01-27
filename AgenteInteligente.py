from owlready2 import get_ontology

import pytz
from datetime import datetime
import spacy

# Carregar modelo de PLN para identificação de localizações
nlp = spacy.load("en_core_web_sm")

class AgenteInteligente:
    def __init__(self, ontologia_path):
        """
        Inicializa o Agente Inteligente com a ontologia carregada.
        ontologia_path: Caminho para o arquivo OWL/RDF da ontologia.
        """
        self.ontologia = get_ontology(ontologia_path).load()

    def validar_continentes(self, continentes):#Apenas para melhor calcular fuso horário sem PLN
        """
        Valida se os continentes fornecidos existem na ontologia.
        continentes: Lista de continentes.
        Tem como retorno uma Lista de continentes válidos.
        """

        continentes_validos = [
            cont for cont in continentes
            if cont in [c.name for c in self.ontologia.Continente.subclasses()]
        ]
        return continentes_validos
    
    def confirmar_horario(self, horario_sugerido):
        """
        Pergunta ao usuário se o horário está de acordo, ajustando pelo fuso horário do usuário.
        
        horario_sugerido: str - Horário sugerido pelo Agente Inteligente no formato 'HH:MM'.
        return List - Hoorário e True se o usuário confirmar, False caso contrário.
        """

        # Converter horário sugerido para um objeto datetime (assumindo UTC como base)
        horario_base = datetime.strptime(horario_sugerido, "%H:%M")
        horario_base = pytz.utc.localize(horario_base)  # Supondo que o horário está em UTC

        # Perguntar ao usuário o local ou fuso horário
        print(f"Horário sugerido (UTC): {horario_sugerido}")
        localizacao = input("Informe sua localização ou fuso horário (ex: 'America/Sao_Paulo', 'Brasil', 'New York'): ")

        # Analisar a localização com PLN
        doc = nlp(localizacao)
        entidades = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]  # GPE = Localizações políticas
        if not entidades:
            print("Não foi possível identificar sua localização. Usando UTC como padrão.")
            horario_local = horario_base
        else:
            # Mapear localização para fuso horário
            try:
                timezone = pytz.timezone(self.mapear_localizacao_para_timezone(entidades[0]))
                horario_local = horario_base.astimezone(timezone)
                print(f"Horário ajustado para sua localização ({timezone}): {horario_local.strftime('%H:%M')}")
            except Exception as e:
                print(f"Erro ao calcular o fuso horário: {e}")
                horario_local = horario_base

        # Confirmar o horário ajustado
        while True:
            resposta = input(f"O horário ajustado ({horario_local.strftime('%H:%M')}) está de acordo? ").lower() 
            #resposta = input(f"O horário ajustado ({horario_local.strftime('%H:%M')}) está de acordo? (s/n): ").strip().lower()
            if resposta == 's':
                return [horario_local.strftime('%H:%M'),True]
            else:
                return [horario_sugerido,False]

    
    def mapear_localizacao_para_timezone(self, localizacao):
        """
        Mapeia uma localização para um fuso horário válido usando nomes conhecidos.
        
        localizacao: str - Nome do local identificado (ex: 'Brasil', 'New York').
        retorno str - Nome do fuso horário (ex: 'America/Sao_Paulo').
        """
        # Dicionário básico para mapeamento (adicione mais conforme necessário)
        mapeamento = {
            "Brasil": "America/Sao_Paulo",
            "New York": "America/New_York",
            "London": "Europe/London",
            "Tokyo": "Asia/Tokyo",
            "India": "Asia/Kolkata",
            "Europa": "Europe/Berlin",
            "Asia": "Asia/Shanghai",
            "America": "America/Los_Angeles"
        }
        return mapeamento.get(localizacao, "UTC")  # Retorna UTC como padrão