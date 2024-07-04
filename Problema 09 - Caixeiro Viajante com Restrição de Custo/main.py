import itertools

def inicializar_tabelas(n, matriz_custos, valores, orcamento):

    # Tabelas de programação dinâmica CUSTO, VALOR e CAMINHO para conjuntos de um único nó.
    CUSTO = {}
    VALOR = {}
    CAMINHO = {}

    nos = list(range(2, n+1))

    for l in nos:
        if matriz_custos[0][l-1] <= orcamento:
            CUSTO[frozenset([l]), l] = matriz_custos[0][l-1]
            VALOR[frozenset([l]), l] = valores[l-1] + valores[0]  # Inclui valor do nó de origem
            CAMINHO[frozenset([l]), l] = [1, l]
        else:
            CUSTO[frozenset([l]), l] = float('inf')
            VALOR[frozenset([l]), l] = 0
            CAMINHO[frozenset([l]), l] = []
    
    return CUSTO, VALOR, CAMINHO


def processar_subconjuntos(nos, matriz_custos, valores, orcamento, CUSTO, VALOR, CAMINHO):
    
    # Processa subconjuntos maiores para calcular os custos e valores usando programação dinâmica.
    for tamanho_subconjunto in range(2, len(nos) + 1):
        for subconjunto in itertools.combinations(nos, tamanho_subconjunto):
            subconjunto = frozenset(subconjunto)
            for l in subconjunto:
                custo_minimo = float('inf')
                valor_maximo = 0
                melhor_caminho_custo = []
                melhor_caminho_valor = []
                for m in subconjunto:
                    if m != l:
                        custo_anterior = CUSTO.get((subconjunto - frozenset([l]), m), float('inf'))
                        novo_custo = custo_anterior + matriz_custos[m-1][l-1]
                        if novo_custo <= orcamento:
                            novo_valor = VALOR.get((subconjunto - frozenset([l]), m), 0) + valores[l-1]
                            if novo_custo < custo_minimo:
                                custo_minimo = novo_custo
                                melhor_caminho_custo = CAMINHO.get((subconjunto - frozenset([l]), m), []) + [l]
                            if novo_valor > valor_maximo:
                                valor_maximo = novo_valor
                                melhor_caminho_valor = CAMINHO.get((subconjunto - frozenset([l]), m), []) + [l]
                if custo_minimo <= orcamento:
                    CUSTO[subconjunto, l] = custo_minimo
                    CAMINHO[subconjunto, l] = melhor_caminho_custo
                VALOR[subconjunto, l] = valor_maximo
                CAMINHO[subconjunto, l] = melhor_caminho_valor


def encontrar_caminhos_validos(CUSTO, VALOR, CAMINHO, matriz_custos, orcamento):

    # Encontra os caminhos válidos que terminam no nó 1 e respeitam o orçamento.
    caminhos_validos = []
    for subconjunto, l in CUSTO:
        custo = CUSTO[subconjunto, l]
        if custo + matriz_custos[l-1][0] <= orcamento:
            custo_total = custo + matriz_custos[l-1][0]
            valor = VALOR[subconjunto, l]
            caminho = CAMINHO[subconjunto, l] + [1]
            if len(caminho) > 2:  # Exclui o nó de origem que aparece no início e no final
                caminhos_validos.append((custo_total, valor, caminho))
    
    return caminhos_validos


def separar_caminhos_por_comprimento(caminhos_validos):
    
    # Separa os caminhos válidos por comprimento e encontra o caminho de menor custo e maior valor para cada comprimento.
    caminhos_por_comprimento = {}
    for caminho in caminhos_validos:
        custo_total, valor, c = caminho
        comprimento_caminho = len(c) - 1  # Desconsiderar o nó de origem na contagem de vértices
        if comprimento_caminho not in caminhos_por_comprimento:
            caminhos_por_comprimento[comprimento_caminho] = {
                'custo_minimo': float('inf'),
                'valor_maximo': 0,
                'caminho_custo_minimo': None,
                'caminho_valor_maximo': None
            }

        if custo_total < caminhos_por_comprimento[comprimento_caminho]['custo_minimo']:
            caminhos_por_comprimento[comprimento_caminho]['custo_minimo'] = custo_total
            caminhos_por_comprimento[comprimento_caminho]['caminho_custo_minimo'] = c
            caminhos_por_comprimento[comprimento_caminho]['valor_caminho_custo_minimo'] = valor

        if valor > caminhos_por_comprimento[comprimento_caminho]['valor_maximo']:
            caminhos_por_comprimento[comprimento_caminho]['valor_maximo'] = valor
            caminhos_por_comprimento[comprimento_caminho]['caminho_valor_maximo'] = c
            caminhos_por_comprimento[comprimento_caminho]['custo_caminho_valor_maximo'] = custo_total
    
    return caminhos_por_comprimento


def selecionar_resultados(caminhos_por_comprimento):
    
    # Seleciona o comprimento de caminho que tem um caminho válido tanto para custo mínimo quanto para valor máximo.
    if caminhos_por_comprimento:
        comprimento_maximo = max(caminhos_por_comprimento.keys())
        caminho_custo_minimo = caminhos_por_comprimento[comprimento_maximo]['caminho_custo_minimo']
        custo_minimo = caminhos_por_comprimento[comprimento_maximo]['custo_minimo']
        valor_caminho_custo_minimo = caminhos_por_comprimento[comprimento_maximo]['valor_caminho_custo_minimo']
        caminho_valor_maximo = caminhos_por_comprimento[comprimento_maximo]['caminho_valor_maximo']
        valor_maximo = caminhos_por_comprimento[comprimento_maximo]['valor_maximo']
        custo_caminho_valor_maximo = caminhos_por_comprimento[comprimento_maximo]['custo_caminho_valor_maximo']
    else:
        resultado_custo_minimo = "Não há caminho válido dentro do orçamento"
        caminho_custo_minimo = []
        resultado_valor_maximo = "Não há caminho válido dentro do orçamento"
        caminho_valor_maximo = []

    if caminho_custo_minimo:
        resultado_custo_minimo = f"Custo mínimo: {custo_minimo}\nValor do caminho de custo mínimo: {valor_caminho_custo_minimo}"
    if caminho_valor_maximo:
        resultado_valor_maximo = f"\nValor máximo: {valor_maximo}\nCusto do caminho de valor máximo: {custo_caminho_valor_maximo}"

    return resultado_custo_minimo, caminho_custo_minimo, resultado_valor_maximo, caminho_valor_maximo


def mapear_nos_para_letras(caminho):
    
    # Mapeia números de nós para letras (A, B, C, ...).
    mapeamento = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J'}
    return [mapeamento[no] for no in caminho]


def ler_entrada(arquivo):
    
    # Leitura dos dados de entrada
    with open(arquivo, 'r', encoding='utf-8') as file:
        linhas = file.readlines()
    
    n = int(linhas[0].strip())
    matriz_custos = [list(map(int, linha.strip().split())) for linha in linhas[1:n+1]]
    valores = list(map(int, linhas[n+1].strip().split()))
    orcamento = int(linhas[n+2].strip())
    
    return n, matriz_custos, valores, orcamento


def escrever_saida(arquivo, resultado_custo_minimo, caminho_custo_minimo, resultado_valor_maximo, caminho_valor_maximo):

    # Escreve os resultados no arquivo de saída.
    with open(arquivo, 'w', encoding='utf-8') as file:
        file.write(f"{resultado_custo_minimo}\n")
        if caminho_custo_minimo:
            file.write(f"Caminho para o custo mínimo: {' -> '.join(mapear_nos_para_letras(caminho_custo_minimo))}\n")
        file.write(f"{resultado_valor_maximo}\n")
        if caminho_valor_maximo:
            file.write(f"Caminho para o valor máximo: {' -> '.join(mapear_nos_para_letras(caminho_valor_maximo))}\n")


def main():
    entrada_arquivo = 'Problema 09 - Caixeiro Viajante com Restrição de Custo/input.txt'
    saida_arquivo = 'Problema 09 - Caixeiro Viajante com Restrição de Custo/output.txt'
    
    n, matriz_custos, valores, orcamento = ler_entrada(entrada_arquivo)
    CUSTO, VALOR, CAMINHO = inicializar_tabelas(n, matriz_custos, valores, orcamento)
    processar_subconjuntos(list(range(2, n+1)), matriz_custos, valores, orcamento, CUSTO, VALOR, CAMINHO)
    caminhos_validos = encontrar_caminhos_validos(CUSTO, VALOR, CAMINHO, matriz_custos, orcamento)
    caminhos_por_comprimento = separar_caminhos_por_comprimento(caminhos_validos)
    resultado_custo_minimo, caminho_custo_minimo, resultado_valor_maximo, caminho_valor_maximo = selecionar_resultados(caminhos_por_comprimento)
    
    escrever_saida(saida_arquivo, resultado_custo_minimo, caminho_custo_minimo, resultado_valor_maximo, caminho_valor_maximo)


if __name__ == "__main__":
    main()
