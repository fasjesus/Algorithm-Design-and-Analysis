import itertools

def tsp_with_budget(n, cost_matrix, values, budget):
    # Inicialização das tabelas de programação dinâmica
    CUSTO = {}
    VALOR = {}
    CAMINHO = {}

    # Inicialização para o nó de origem
    nodes = list(range(2, n+1))

    # Inicializar os custos e valores para conjuntos com um único nó
    for l in nodes:
        if cost_matrix[0][l-1] <= budget:
            CUSTO[frozenset([l]), l] = cost_matrix[0][l-1]
            VALOR[frozenset([l]), l] = values[l-1] + values[0]  # Inclui valor do nó de origem
            CAMINHO[frozenset([l]), l] = [1, l]
        else:
            CUSTO[frozenset([l]), l] = float('inf')
            VALOR[frozenset([l]), l] = 0
            CAMINHO[frozenset([l]), l] = []

    # Processamento intermediário para subconjuntos maiores
    for subset_size in range(2, len(nodes) + 1):
        for subset in itertools.combinations(nodes, subset_size):
            subset = frozenset(subset)
            for l in subset:
                min_cost = float('inf')
                max_val = 0
                best_path_cost = []
                best_path_value = []
                for m in subset:
                    if m != l:
                        prev_cost = CUSTO.get((subset - frozenset([l]), m), float('inf'))
                        new_cost = prev_cost + cost_matrix[m-1][l-1]
                        if new_cost <= budget:
                            new_val = VALOR.get((subset - frozenset([l]), m), 0) + values[l-1]
                            if new_cost < min_cost:
                                min_cost = new_cost
                                best_path_cost = CAMINHO.get((subset - frozenset([l]), m), []) + [l]
                            if new_val > max_val:
                                max_val = new_val
                                best_path_value = CAMINHO.get((subset - frozenset([l]), m), []) + [l]
                if min_cost <= budget:
                    CUSTO[subset, l] = min_cost
                    CAMINHO[subset, l] = best_path_cost
                VALOR[subset, l] = max_val
                CAMINHO[subset, l] = best_path_value

    # Encontrar os caminhos válidos que terminam no nó 1 e respeitam o orçamento
    valid_paths = []
    for subset, l in CUSTO:
        cost = CUSTO[subset, l]
        if cost + cost_matrix[l-1][0] <= budget:
            total_cost = cost + cost_matrix[l-1][0]
            value = VALOR[subset, l]
            path = CAMINHO[subset, l] + [1]
            valid_paths.append((total_cost, value, path))

    # Encontrar o caminho de menor custo e o de maior valor
    min_cost_path = None
    min_cost = float('inf')
    min_value_of_min_cost_path = 0
    max_value_path = None
    max_value = 0
    max_cost_of_max_value_path = 0
    for path in valid_paths:
        total_cost, value, p = path
        if total_cost < min_cost:
            min_cost = total_cost
            min_cost_path = p
            min_value_of_min_cost_path = value
        if value > max_value:
            max_value = value
            max_value_path = p
            max_cost_of_max_value_path = total_cost

    # Verifica se nenhum caminho válido foi encontrado
    if min_cost == float('inf'):
        min_cost_result = "Não há caminho válido dentro do orçamento"
        min_cost_path = []
    else:
        min_cost_result = f"Custo mínimo: {min_cost}\nValor do caminho de custo mínimo: {min_value_of_min_cost_path}"
        min_cost_path = min_cost_path

    if not max_value_path:
        max_value_result = "Não há caminho válido dentro do orçamento"
        max_value_path = []
    else:
        max_value_result = f"\nValor máximo: {max_value}\nCusto do caminho de valor máximo: {max_cost_of_max_value_path}"
        max_value_path = max_value_path

    return min_cost_result, min_cost_path, max_value_result, max_value_path

def main():
    # Leitura do arquivo de entrada com codificação UTF-8
    with open('Problema 09 - Caixeiro Viajante com Restrição de Custo/input.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    n = int(lines[0].strip())
    cost_matrix = [list(map(int, line.strip().split())) for line in lines[1:n+1]]
    values = list(map(int, lines[n+1].strip().split()))
    budget = int(lines[n+2].strip())

    min_cost_result, min_cost_path, max_value_result, max_value_path = tsp_with_budget(n, cost_matrix, values, budget)

    # Mapeamento de números para letras (1-based index)
    def map_nodes_to_letters(path):
        mapping = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J'}
        return [mapping[node] for node in path]

    # Escrita no arquivo de saída com codificação UTF-8
    with open('Problema 09 - Caixeiro Viajante com Restrição de Custo/output.txt', 'w', encoding='utf-8') as file:
        file.write(f"{min_cost_result}\n")
        if min_cost_path:
            file.write(f"Caminho para custo mínimo: {' -> '.join(map_nodes_to_letters(min_cost_path))}\n")
        file.write(f"{max_value_result}\n")
        if max_value_path:
            file.write(f"Caminho para valor máximo: {' -> '.join(map_nodes_to_letters(max_value_path))}\n")

if __name__ == "__main__":
    main()
