class AnaliseSemantica:
    def __init__(self):
        self.tabela_simbolos = {}
    
    def adicionar_simbolo(self, nome, categoria, tipo, nivel):
        if (nome and nivel) not in self.tabela_simbolos:
            self.tabela_simbolos[nome] = {'Categoria': categoria, 'Tipo': tipo, 'Nivel': nivel}
        else:
            print(f"Símbolo '{nome}' já existe na tabela de símbolos.")

    def remover_simbolo(self, nome):
        if nome in self.tabela_simbolos:
            del self.tabela_simbolos[nome]
            print(f"Símbolo '{nome}' removido da tabela de símbolos.")
        else:
            print(f"Símbolo '{nome}' não encontrado na tabela de símbolos.")

    def visualizar_tabela(self):
        print("Tabela de Símbolos:")
        for nome, info in self.tabela_simbolos.items():
            print(f"[{nome} | {info['Categoria']} | {info['Tipo']} | {info['Nivel']}]")
    
    # Definir aqui as funções para validar as regras semanticas separadamente
    # Exemplo: def ident_nao_declarado...


    