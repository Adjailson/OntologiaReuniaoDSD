from owlready2 import get_ontology
import random

class AgenteGeradorLink:
    def __init__(self, ontologia_path):
        """
        Inicializa o Agente GeradorLink.
        ontologia_path: Caminho para o arquivo OWL/RDF da ontologia.
        """
        self.ontologia = get_ontology(ontologia_path).load()
        self.links_base = {
            "Zoom": "https://zoom.us/j/",
            "GoogleMeet": "https://meet.google.com/",
            "MicrosoftTeams": "https://teams.microsoft.com/l/"
        }

    def gerar_link(self, conteudos, numero_participantes):
        ferramentas = list(self.ontologia.FerramentaComunicacao.subclasses())
        print(f"Verificando {len(ferramentas)} ferramentas na ontologia...")

        for ferramenta in ferramentas:
            num_participantes = getattr(ferramenta, "numParticipantes", None)
            tipo_conteudo = getattr(ferramenta, "tipoConteudo", [])

            # Resolver listas ou valores complexos
            if isinstance(num_participantes, list):
                num_participantes = num_participantes[0] if num_participantes else None

            print(f"Analisando ferramenta: {ferramenta.name}")
            print(f"  - Num participantes: {num_participantes}")
            print(f"  - Tipo conteúdo: {tipo_conteudo}")

            # Verificar restrições de número de participantes
            if num_participantes is not None and numero_participantes > num_participantes:
                print(f"  -> Rejeitada: número de participantes excede o máximo.")
                continue

            # Verificar se todos os conteúdos OWL estão disponíveis
            if not all(conteudo in tipo_conteudo for conteudo in conteudos):
                print(f"  -> Rejeitada: conteúdos não compatíveis.")
                continue

            print(f"  -> Ferramenta aceita: {ferramenta.name}")
            return {
                "ferramenta": ferramenta.name,
                "link": f"{self.links_base[ferramenta.name]}{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            }

        return {
            "ferramenta": None,
            "link": "Nenhuma ferramenta disponível para os requisitos especificados."
        }
