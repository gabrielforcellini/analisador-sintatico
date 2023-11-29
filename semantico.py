class AnaliseSemantica:
    def __init__(self):
        self.tabela_simbolos = {}
    
    # Adiciona um simbolo na tabela de simbolos
    def adicionar_simbolo(self, nome, categoria, tipo, nivel):
        if (nome and nivel) not in self.tabela_simbolos:
            self.tabela_simbolos[nome] = {'Categoria': categoria, 'Tipo': tipo, 'Nivel': nivel}
        else:
            print(f"Símbolo '{nome}' já existe na tabela de símbolos.")
    
    # Busca um simbolo na tabela de simbolos, retornando True quando encontrado
    # e False quando não encontrado.
    def busca_simbolo(self, nome, categoria, tipo, nivel):
        if (nome and nivel) not in self.tabela_simbolos:
            return True
        
        return False

    # Faz a remoção de um simbolo pelo seu nome.
    def remover_simbolo(self, nome):
        if nome in self.tabela_simbolos:
            del self.tabela_simbolos[nome]
            print(f"Símbolo '{nome}' removido da tabela de símbolos.")
        else:
            print(f"Símbolo '{nome}' não encontrado na tabela de símbolos.")

    # Imprime a tabela - Apenas para desenvolvimento
    def visualizar_tabela(self):
        print("Tabela de Símbolos:")
        for nome, info in self.tabela_simbolos.items():
            print(f"[{nome} | {info['Categoria']} | {info['Tipo']} | {info['Nivel']}]")

    # Remove todos os simbolos de um mesmo nivel - Será utilizado para fazer remoção dos simbolos de uma
    # procedure por exemplo.
    # O código usa uma compreensão de lista para criar uma lista de todos os símbolos que têm o mesmo nível e,
    # em seguida, itera sobre essa lista para removê-los da tabela. 
    def remove_simbolos_nivel(self, nivel):
        simbolos_a_remover = [nome for nome, info in self.tabela_simbolos.items() if info['Nivel'] == nivel]
        for nome in simbolos_a_remover:
            del self.tabela_simbolos[nome]
        print(f"Removidos todos os símbolos do nível {nivel}.")
    
    # Definir aqui as funções para validar as regras semanticas separadamente
    # Exemplo: def ident_nao_declarado...


    