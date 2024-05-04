def quick_sort(intervals):
    if len(intervals) <= 1:
        return intervals
    
    pivot = intervals[len(intervals) // 2]
    left = [interval for interval in intervals if interval[0] < pivot[0]]
    middle = [interval for interval in intervals if interval[0] == pivot[0]]
    right = [interval for interval in intervals if interval[0] > pivot[0]]
    
    return quick_sort(left) + middle + quick_sort(right)

def greedy_coloring(intervals):
    # Ordena os intervalos usando o quickSort
    intervals = quick_sort(intervals)
    
    colors = {}  # Dicionário para armazenar as cores atribuídas a cada intervalo
    used_colors = set()  # Conjunto para armazenar as cores já usadas
    
    # Percorre os intervalos
    for interval in intervals:
        start, end = interval
        
        # Verifica cores usadas pelos intervalos que se interceptam
        available_colors = set(range(len(used_colors) + 1))
        for c in colors.values():
            if c in used_colors and (intervals[c][0] < end and intervals[c][1] > start):
                available_colors.discard(c)
        
        # Atribui a menor cor admissível ao intervalo
        if available_colors:
            color = min(available_colors)
            colors[interval] = color
            used_colors.add(color)
        else:
            # Se não houver cores disponíveis, atribui uma nova cor
            color = len(used_colors)
            colors[interval] = color
            used_colors.add(color)
    
    return colors, len(used_colors)

def read_intervals_from_file(filename):
    intervals = []
    with open(filename, 'r') as file:
        for line in file:
            start, end = map(int, line.strip().split())
            intervals.append((start, end))
    return intervals

def write_result_to_file(colors, num_colors, filename):
    with open(filename, 'w') as file:
        file.write("Intervalos coloridos:\n")
        for interval, color in colors.items():
            interval_str = f"[{', '.join(map(str, interval))}]"
            file.write(f"Intervalo {interval_str}: Cor {color}\n")
        file.write(f"\nQuantidade de cores usadas: {num_colors}\n")

def main():
    # Lê os intervalos do arquivo de entrada
    intervals = read_intervals_from_file('input.txt')

    # Executa o algoritmo de coloração gulosa
    colors, num_colors = greedy_coloring(intervals)

    # Escreve o resultado no arquivo de saída
    write_result_to_file(colors, num_colors, 'output.txt')

if __name__ == "__main__":
    main()
