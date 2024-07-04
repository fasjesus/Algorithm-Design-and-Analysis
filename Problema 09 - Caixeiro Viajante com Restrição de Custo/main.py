import itertools

def caixeiro_viajante_com_orcamento(n, matriz_custos, valores, orcamento):
    # Tabelas de programação dinâmica
    CUSTO = {}
    VALOR = {}
    CAMINHO = {}

    # Inicialização para o nó de origem
    nos = list(range(2, n+1))

    # Inicializar os custos e valores para conjuntos com um único nó
    for l in nos:
        if matriz_custos[0][l-1] <= orcamento:
            CUSTO[frozenset([l]), l] = matriz_custos[0][l-1]
            VALOR[frozenset([l]), l] = valores[l-1] + valores[0]  # Inclui valor do nó de origem
            CAMINHO[frozenset([l]), l] = [1, l]
        else:
            CUSTO[frozenset([l]), l] = float('inf')
            VALOR[frozenset([l]), l] = 0
            CAMINHO[frozenset([l]), l] = []

    # Processamento intermediário para subconjuntos maiores
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

    # Encontrar os caminhos válidos que terminam no nó 1 e respeitam o orçamento
    caminhos_validos = []
    for subconjunto, l in CUSTO:
        custo = CUSTO[subconjunto, l]
        if custo + matriz_custos[l-1][0] <= orcamento:
            custo_total = custo + matriz_custos[l-1][0]
            valor = VALOR[subconjunto, l]
            caminho = CAMINHO[subconjunto, l] + [1]
            # Verifica se o caminho contém pelo menos 2 expansões além do nó de origem
            if len(caminho) > 2:  # Exclui o nó de origem que aparece no início e no final
                caminhos_validos.append((custo_total, valor, caminho))

    # Separar caminhos por comprimento
    caminhos_por_comprimento = {}
    for caminho in caminhos_validos:
        custo_total, valor, c = caminho
        comprimento_caminho = len(c) - 1  # Desconsiderar o nó de origem na contagem de vértices
        if comprimento_caminho not in caminhos_por_comprimento:
            caminhos_por_comprimento[comprimento_caminho] = {'custo_minimo': float('inf'), 'valor_maximo': 0, 'caminho_custo_minimo': None, 'caminho_valor_maximo': None}

        # Atualizar caminho de menor custo para esse comprimento
        if custo_total < caminhos_por_comprimento[comprimento_caminho]['custo_minimo']:
            caminhos_por_comprimento[comprimento_caminho]['custo_minimo'] = custo_total
            caminhos_por_comprimento[comprimento_caminho]['caminho_custo_minimo'] = c
            caminhos_por_comprimento[comprimento_caminho]['valor_caminho_custo_minimo'] = valor

        # Atualizar caminho de maior valor para esse comprimento
        if valor > caminhos_por_comprimento[comprimento_caminho]['valor_maximo']:
            caminhos_por_comprimento[comprimento_caminho]['valor_maximo'] = valor
            caminhos_por_comprimento[comprimento_caminho]['caminho_valor_maximo'] = c
            caminhos_por_comprimento[comprimento_caminho]['custo_caminho_valor_maximo'] = custo_total

    # Selecionar o comprimento de caminho que tem um caminho válido tanto para custo mínimo quanto para valor máximo
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

def main():
    # Leitura do arquivo de entrada 
    with open('Problema 09 - Caixeiro Viajante com Restrição de Custo/input.txt', 'r', encoding='utf-8') as file:
        linhas = file.readlines()
    
    n = int(linhas[0].strip())
    matriz_custos = [list(map(int, linha.strip().split())) for linha in linhas[1:n+1]]
    valores = list(map(int, linhas[n+1].strip().split()))
    orcamento = int(linhas[n+2].strip())

    resultado_custo_minimo, caminho_custo_minimo, resultado_valor_maximo, caminho_valor_maximo = caixeiro_viajante_com_orcamento(n, matriz_custos, valores, orcamento)

    # Mapeamento de números para letras 
    def mapear_nos_para_letras(caminho):
        mapeamento = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J'}
        return [mapeamento[no] for no in caminho]

    # Escrita no arquivo de saída 
    with open('Problema 09 - Caixeiro Viajante com Restrição de Custo/output.txt', 'w', encoding='utf-8') as file:
        file.write(f"{resultado_custo_minimo}\n")
        if caminho_custo_minimo:
            file.write(f"Caminho para custo mínimo: {' -> '.join(mapear_nos_para_letras(caminho_custo_minimo))}\n")
        file.write(f"{resultado_valor_maximo}\n")
        if caminho_valor_maximo:
            file.write(f"Caminho para valor máximo: {' -> '.join(mapear_nos_para_letras(caminho_valor_maximo))}\n")

if __name__ == "__main__":
    main()
