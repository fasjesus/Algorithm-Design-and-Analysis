
# QuickSort recursivo
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
    usedColors = set()  # Conjunto para armazenar as cores já usadas
    
    # Percorre os intervalos
    for interval in intervals:
        start, end = interval
        
        # Verifica cores usadas pelos intervalos que se interceptam
        availableColors = set(range(len(usedColors) + 1))
        for c in colors.values():
            if c in usedColors and (intervals[c][0] < end and intervals[c][1] > start):
                availableColors.discard(c)
        
        # Atribui a menor cor admissível ao intervalo
        if availableColors:
            color = min(availableColors)
            colors[interval] = color
            usedColors.add(color)
        else:
            # Se não houver cores disponíveis, atribui uma nova cor
            color = len(usedColors)
            colors[interval] = color
            usedColors.add(color)
    
    return colors, len(usedColors)

def read_intervals_from_file(filename):
    intervals = []
    with open(filename, 'r') as file:
        for line in file:
            start, end = map(int, line.strip().split())
            intervals.append((start, end))
    return intervals

def write_result_to_file(colors, numColors, lenIntervals, filename):
    with open(filename, 'w') as file:
        file.write("\nIntervalos coloridos:\n\n")
        for interval, color in colors.items():
            interval_str = f"[{', '.join(map(str, interval))}]"
            file.write(f"Intervalo {interval_str}: Cor {color}\n")
        file.write(f"\nForam usadas {numColors} cores para colorir {lenIntervals} intervalos.\n")

def main():
    # Lê os intervalos do arquivo de entrada
    intervals = read_intervals_from_file('Problema 06 - Intervalos Coloridos\input.txt')
    lenIntervals = len(intervals)

    # Executa o algoritmo de coloração gulosa
    colors, numColors = greedy_coloring(intervals)

    # Escreve o resultado no arquivo de saída
    write_result_to_file(colors, numColors, lenIntervals, 'Problema 06 - Intervalos Coloridos\output.txt')

if __name__ == "__main__":
    main()
