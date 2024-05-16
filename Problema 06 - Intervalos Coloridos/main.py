# Universidade Estadual de Santa Cruz
# Discente: Flávia Alessandra Santos de Jesus.

# Problema dos Intervalos Coloridos: dado um conjunto de intervalos, onde cada intervalo pode ser definido por seu início e seu fim, 
# colorir todos os intervalos com a menor quantidade possível de cores de maneira que dois intervalos com a mesma cor nunca se interceptem.

# Complexidade O(n²)
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# linear
def read_intervals(filename):
    intervals = []
    with open(filename, 'r') as file:
        for line in file:
            start, end = map(int, line.strip().split())
            intervals.append((start, end))
    return intervals

# linear
def write_result(intervals, colors, numColors, filename):
    with open(filename, 'w') as file:
        file.write(f"\n")
        for i in range(len(intervals)):
            file.write(f"Intervalo {intervals[i]}: Cor {colors[i]}\n")
        file.write(f"\nForam usadas {numColors} cores para colorir {len(intervals)} intervalos.")

# Complexidade O(n²)
def color_intervals(intervals):
    intervals = quick_sort(intervals)  # Ordenar os intervalos usando quicksort
    colors = [-1] * len(intervals)  # Inicializar cores como -1 (não atribuídas)

    nextColor = 0
    for i, (start, end) in enumerate(intervals):
        usedColors = set()
        for j in range(i):
            if intervals[j][1] > start:  # Se o intervalo j se intersecta com o intervalo i
                usedColors.add(colors[j])
        availableColor = 0
        while availableColor in usedColors:
            availableColor += 1
        colors[i] = availableColor
        nextColor = max(nextColor, availableColor)

    return colors, nextColor + 1

inputFilename = "Problema 06 - Intervalos Coloridos/input.txt"
outputFilename = "Problema 06 - Intervalos Coloridos/output.txt"

intervals = read_intervals(inputFilename)
colors, numColors = color_intervals(intervals)
write_result(intervals, colors, numColors, outputFilename)
