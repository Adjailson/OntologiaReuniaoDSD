
class AgenteOrganizador:

    def __init__(self, continentes):
        """
        Inicializa o Agente Organizador.
        Lista onde a posição 0 é o continente de origem e as demais posições são continentes participantes.
        
        continentes: List[str] - Continentes envolvidos na reunião.
        """
        self.continentes = continentes #Utilizei para validar com os fusos horários, sem PLN

    def solicitar_horario(self, agente_inteligente, horarioSugerido):
        """
        Envia um horário de escolha;
        retorna um outro horário que melhor atende para todos
        """
        return agente_inteligente.confirmar_horario(horarioSugerido)


    def solicitar_link(self, agente_gerador_link, conteudos, numero_participantes):
        """
        Solicita a geração do link ao Agente GeradorLink.
        
        agente_gerador: AgenteGeradorLink - Instância do Agente GeradorLink.
        conteudos: List[str] - Lista de conteúdos da reunião.
        numero_participantes: int - Número de participantes na reunião.
        retorno de um dicionário contendo a ferramenta escolhida e o link gerado.
        """
        print(f"Solicitando link com os seguintes requisitos:")
        print(f" - Conteúdos: {conteudos}")
        print(f" - Número de participantes: {numero_participantes}")
        return agente_gerador_link.gerar_link(conteudos, numero_participantes)
