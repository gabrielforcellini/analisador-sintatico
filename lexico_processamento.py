import numpy as np
from lexico_utils import *
from parsing import TabParsing
from semantico import AnaliseSemantica

def verificar_regras_semanticas(tokens, tabela_simbolos):
    variaveis_funcao = set()
    funcao_atual = None

    for i in range(len(tokens)):
        token = tokens[i]

        # Detecta a declaração da função
        if token == 'procedure':
            funcao_atual = tokens[i + 1]

        # Verifica se a função atual foi chamada
        if funcao_atual and token == funcao_atual:
            parametros_esperados = tabela_simbolos[funcao_atual]['params']
            argumentos_chamada = tokens[i + 1:i + 1 + len(parametros_esperados)]

            for idx, arg in enumerate(argumentos_chamada):
                tipo_esperado = parametros_esperados[idx]['type']
                if tabela_simbolos[arg]['type'] != tipo_esperado:
                    print(f"Erro semântico: Tipo incorreto para o argumento {idx + 1} da função '{funcao_atual}'. Esperado: {tipo_esperado}, Recebido: {tabela_simbolos[arg]['type']}.")
                    return False
                
    for i in range(len(tokens) - 1):
        token = tokens[i]
        if token in tabela_simbolos:
            tipo = tabela_simbolos[token]['type']

            if tipo == 'constante' and tokens[i + 1] == ':=':
                print(f"Erro semântico: Tentativa de modificar uma constante na linha {i + 1}.")
                return False

            if tipo == 'string' and tokens[i + 1] in {'+', '-', '*', '/'}:
                print(f"Erro semântico: Uso de string em operação matemática não é permitido na linha {i + 1}.")
                return False

            # Adapte para incluir outras regras semânticas conforme necessário...
    return True


def le_arquivo(caminho):
    # Lê o arquivo e garante que será fechado automaticamente
    with open(caminho, "r") as arquivo:
        return processar_arquivo(arquivo)


def processar_arquivo(arquivo):

    # Dicionário para armazenar os tokens e lexemas
    tokens_lexemas = {
        1: "while",
        2: "var",
        3: "to",
        4: "then",
        5: "string",
        6: "real",
        7: "read",
        8: "program",
        9: "procedure",
        10: "print",
        11: "nreal",
        12: "nint",
        13: "literal",
        14: "integer",
        15: "if",
        16: "ident",
        17: "for",
        18: "end",
        19: "else",
        20: "do",
        21: "const",
        22: "begin",
        23: "vstring",
        24: ">=",
        25: ">",
        26: "=",
        27: "<>",
        28: "<=",
        29: "<",
        30: "+",
        31: ";",
        32: ":=",
        33: ":",
        34: "/",
        35: ".",
        36: ",",
        37: "*",
        38: ")",
        39: "(",
        40: "{",
        41: "}",
        42: "-"
    }
    
    valores_a_excluir = {"nreal", "nint", "literal", "ident", "vstring"}

    tokens_lexemas_filtrado = {chave: valor for chave, valor in tokens_lexemas.items() if valor not in valores_a_excluir}
    
    lexemas_array = list(tokens_lexemas.values())
    lexemas_filtrados = list(tokens_lexemas_filtrado.values())

    tokens = []
    lexemas = []
    linha_atual = []
    in_comment = False
    token_ident = {} # Será utilizado para associar o token ao seu nome
    cont = 0 # Será utilizado para contar os identificadores

    for linha_numero, linha in enumerate(arquivo, start=1):
        lexema = ''
        i = 0

        while i < len(linha):
            if in_comment:
                # Dentro do comentário de bloco, ingora os caracteres até encontrar a sequencia '*/'
                if linha[i:i+2] == '*/':
                    in_comment = False
                    i += 2
                else:
                    i += 1
                continue

            if linha[i:i+2] == '//':
                # Comentário de linha, ignora o restante da linha
                break

            if linha[i:i+2] == '/*':
                # Inicio do comentário de bloco
                in_comment = True
                i += 2
                continue

            if linha[i] in lexemas_filtrados: 
                if lexema.strip() != '':
                    cont += 1 # Incrementa 1 no contador de idents
                    # Identificador
                    validar_identificador(linha_numero, lexema)
                    token = lexemas_array.index('ident') + 1
                    token_ident[cont] = lexema
                    adicionar_token_e_lexema(tokens, lexemas, token, lexema, linha_numero, linha_atual)
                lexema = linha[i]
            elif linha[i] != ' ' or lexema.startswith("'"):
                lexema = lexema + linha[i]

            if (lexema in lexemas_filtrados):
                # Verifica se o próximo caractere forma um operador composto. Casos do tipo <> :=
                if i + 1 < len(linha) and lexema + linha[i + 1] in lexemas_filtrados: 
                    lexema += linha[i + 1]
                    token = lexemas_array.index(lexema) + 1
                    i += 2
                    adicionar_token_e_lexema(tokens, lexemas, token, lexema, linha_numero, linha_atual)
                    lexema = ''
                    continue

                token = lexemas_array.index(lexema) + 1
                adicionar_token_e_lexema(tokens, lexemas, token, lexema, linha_numero, linha_atual)
                lexema = ''
            else:
                # Verifica se é uma string
                if verificar_string(lexema):
                    validar_string(linha_numero, lexema)
                    token = lexemas_array.index('vstring') + 1
                # Verifica se é um número
                elif verificar_numero_inteiro(lexema):
                    while i + 1 < len(linha) and verificar_numero_inteiro(linha[i + 1]):
                        lexema += linha[i + 1]
                        i += 1
                    # Verifica se é real
                    if linha[i + 1] == '.':
                        lexema += linha[i + 1]
                        i += 1
                        while i + 1 < len(linha) and verificar_numero_inteiro(linha[i + 1]):
                            lexema += linha[i + 1]
                            i += 1
                        if verificar_numero_real(lexema):
                            validar_numero_real(linha_numero, lexema)
                            token = lexemas_array.index('nreal') + 1
                    else:          
                        validar_numero_inteiro(linha_numero, lexema)
                        token = lexemas_array.index('nint') + 1
                # Verifica se é um literal
                elif lexema == '"':
                    while i + 1 < len(linha):
                        lexema += linha[i + 1]
                        i += 1
                        if linha[i] == '"' and not lexema == '"':
                            break
                    validar_literal(linha_numero, lexema)
                    token = lexemas_array.index('literal') + 1
                else:
                    token = ''

                if token != '':
                    adicionar_token_e_lexema(tokens, lexemas, token, lexema, linha_numero, linha_atual)
                    lexema = ''

            i += 1
    
    if in_comment:
        print("Erro léxico: Comentário de bloco não foi fechado.")

    #exibir_tokens_e_lexemas(tokens, lexemas, linha_atual) # Apenas para entendimento, não é necessário para o funcionamento
    tokens = np.array(tokens)
    
    #tokenchumbado = [8,16,31,21,16,26,12,31,21,16,26,12,31,2,16,33,14,31,9,16,39,16,33,14,38,31,22,10,40,13,41,31,18,31,22,18,35] # Para testar com tokens especificos
    analise_sintatica(tokens, token_ident)
    return tokens


def adicionar_token_e_lexema(tokens, lexemas, token, lexema, linha, linha_atual):
    tokens.append(token)
    lexemas.append(lexema)
    linha_atual.append(linha)

def exibir_tokens_e_lexemas(tokens, lexemas, linha_atual):
    for token, lexema, linha in zip(tokens, lexemas, linha_atual):
        print(f'Token: {token} - Lexema: {lexema} - Linha: {linha}')
    print(tokens) # [array de tokens] Apenas para entendimento, não é necessário para o funcionamento

def analise_sintatica(tokens, tokens_idents):
    print(tokens)
    print(tokens_idents)

    erro = False
    erroMsg = ''
    nivel = 0 # Inicia nível como Global, nível Local será 1
    varZone = False # Indica quando está na zona de declaração de variáveis para inserir na tabela de símbolos
    procedureZone = False # Indica quando está na zona de declaração de uma procedure para inserir na tabela de símbolos
    constZone = False # Indica quando está na zona de declaração de uma const para inserir na tabela de símbolos
    cont = 1 # Contador de tokens de identificadores

    # Inicializar a Matriz de Parsing com zeros.
    tabParsing = TabParsing()
    tabParsing.inicializarTab()
    tabParsing.inicializarProdu()

    # Inicializar a Tabela de Simbolos
    analise_semantica = AnaliseSemantica()

    # Tabela de parsing populada
    tabelaParsing = tabParsing.tabParsing

    # Tabela de produções populada
    producoes = tabParsing.producoes

    pilha = [43] #$ topo da pilha - gramatica

    pilha = np.hstack([producoes[1][:], pilha])
    pilha = pilha[pilha != 0]

    print(pilha)

    X = pilha[0]
    a = tokens[0]

    while X != 43: #enquanto pilha nao estiver vazia
        print("X: "+ str(X))
        print("a: " + str(a))
        print(pilha)
        if X == 44: #se o topo da pilha for vazio
            pilha = np.delete(pilha,[0])
            X = pilha[0]
        else:
            if X <= 44: #topo da pilha é um terminal
                if X == a: #deu match

                    # ---- Parte semântica ----
                    if a == 2:
                        varZone = True # Está na zona de inserção das variaveis na tabela de simbolos
                    
                    # Se está na zona de variaveis e encontra 'procedure' ou 'begin' então acabou a zona de variável
                    if varZone and ((a == 22) or (a == 9)):
                        varZone = False
                    
                    if a == 9:
                       procedureZone = True # Está inserindo uma procedure
                       nivel = 1 # Quando chega na procedure muda para o nível 1 (Local)

                    # Se está inserindo uma procedure e encontra o token '(' deve sair desse estado
                    if procedureZone and a == 39:
                        procedureZone = False

                    # Está inserindo uma constante
                    if a == 21:
                        constZone = True

                    # Se está inserindo uma constante e encontra o token ';' deve sair desse estado
                    if constZone and a == 31:
                        constZone = False                    
                    
                    # Colocar aqui as inserções/exclusões na tabela de símbolos
                    # e validações que devem ocorrer, se quiser fazer uma função
                    # fora daqui pode ser também. Exemplo:
                    if varZone and a == 16:
                        nome_ident = tokens_idents[cont] # Acessa o dicionário no index onde está o ident
                        if constZone:
                            categoria = 'constante'
                        elif procedureZone:
                            categoria = 'procedure'
                        elif varZone:
                            categoria = 'variavel'
                            
                        analise_semantica.adicionar_simbolo(nome_ident, categoria, '', nivel)
                        cont += 1

                    pilha = np.delete(pilha,[0])
                    tokens = np.delete(tokens,[0])
                    X = pilha[0]
                    if tokens.size != 0:
                        a = tokens[0]
                else:
                    erro = True
                    erroMsg = 'Error, mismatch'
                    break
            else:
                if int(tabelaParsing[X][a]) != 0: # se existe uma producao
                    print('producao: '+str(tabelaParsing[X][a]))    
                    pilha = np.delete(pilha,[0])
                    pilha = np.hstack([producoes[int(tabelaParsing[X][a])][:], pilha]) #empilha as producoes correspondentes
                    pilha = pilha[pilha != 0]  
                    X = pilha[0]
                else:
                    erro = True
                    erroMsg = 'Error, no production'
                    break
    if erro:
        print(erroMsg)
    else:
        analise_semantica.visualizar_tabela()
        print('Pilha: ')                
        print(pilha)
        print('Entrada: ')
        print(tokens)
        print('Sentença reconhecida com sucesso')
