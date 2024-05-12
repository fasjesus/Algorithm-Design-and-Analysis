# Universidade Estadual de Santa Cruz
# Discente: Flávia Alessandra Santos de Jesus.

# Problema dos Intervalos Coloridos:

# QuickSort recursivo
# Complexidade O(n²)

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def read_intervals_from_file(filename):
    intervals = []
    with open(filename, 'r') as file:
        for line in file:
            start, end = map(int, line.strip().split())
            intervals.append((start, end))
    return intervals

def write_colored_intervals_to_file(intervals, colors, num_colors, filename):
    with open(filename, 'w') as file:
        file.write(f"\n")
        for i in range(len(intervals)):
            file.write(f"Intervalo {intervals[i]}: Cor {colors[i]}\n")
        file.write(f"\nForam usadas {num_colors} cores para colorir {len(intervals)} intervalos.")

def color_intervals(intervals):
    intervals = quicksort(intervals)  # Ordenar os intervalos usando quicksort
    colors = [-1] * len(intervals)  # Inicializar cores como -1 (não atribuídas)

    next_color = 0
    for i, (start, end) in enumerate(intervals):
        used_colors = set()
        for j in range(i):
            if intervals[j][1] > start:  # Se o intervalo j se intersecta com o intervalo i
                used_colors.add(colors[j])
        available_color = 0
        while available_color in used_colors:
            available_color += 1
        colors[i] = available_color
        next_color = max(next_color, available_color)

    return colors, next_color + 1

input_filename = "Problema 06 - Intervalos Coloridos/input.txt"
output_filename = "Problema 06 - Intervalos Coloridos/output.txt"

intervals = read_intervals_from_file(input_filename)
colors, num_colors = color_intervals(intervals)
write_colored_intervals_to_file(intervals, colors, num_colors, output_filename)
