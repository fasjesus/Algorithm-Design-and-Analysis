# Universidade Estadual de Santa Cruz
# Discente: Flávia Alessandra Santos de Jesus.

# Problema do Elemento Mais Frequente: dado um vetor de entrada com elementos de um tipo qualquer, utilize a divisão e conquista para encontrar o 
# elemento mais frequente.

# complexidade 𝑂(𝑛)
def merge(left, right, output_file):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][0] < right[j][0]:
            result.append(left[i])
            i += 1
        elif left[i][0] > right[j][0]:
            result.append(right[j])
            j += 1
        else:
            result.append((left[i][0], left[i][1] + right[j][1]))
            i += 1
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    output_file.write(f"{result}\n")  # Escreve resultado em output.txt
    return result


# complexidade 𝑂(n log 𝑛)
def count_frequencies(stringui, output_file):
    stack = [[(elem, 1)] for elem in stringui]
    output_file.write("\nInitial Stack:\n")
    for sublist in stack:
        output_file.write(f"{sublist}\n")  # Escreve a sublista em output.txt
    while len(stack) > 1:
        new_stack = []
        for i in range(0, len(stack), 2):
            if i+1 < len(stack):
                merged = merge(stack[i], stack[i+1], output_file)
                new_stack.append(merged)
            else:
                new_stack.append(stack[i])
                
        stack = new_stack
        output_file.write("\nMerged Stack:\n")
        for sublist in stack:
            output_file.write(f"{sublist}\n")  # Escreve a sublista em output.txt
    return stack[0]


# complexidade O(nlogn)
def most_frequent_character(s):
    with open('Problema 05 - Elemento Mais Frequente/output.txt', 'w', encoding='utf-8') as output_file:
        frequencies = count_frequencies(s, output_file)
        maxFreq = -1
        mostFreqChars = []
        for char, freq in frequencies:
            if freq > maxFreq:
                maxFreq = freq
                mostFreqChars = [char]
            elif freq == maxFreq:
                mostFreqChars.append(char)
        
        output_file.write(f'\nO(s) elemento(s) mais frequente(s) é(são): {", ".join(mostFreqChars)}.\n')
        output_file.write(f'\nFrequência dos elementos:\n')

        # Ordena os elementos em ordem decrescente de frequência
        frequencies.sort(key=lambda x: x[1], reverse=True)
        for char, freq in frequencies:
            output_file.write(f'* {char}: {freq} vez(es)\n')
        return mostFreqChars

# linear
def read_input_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().strip()

filename = 'Problema 05 - Elemento Mais Frequente\input.txt'  
input = read_input_from_file(filename)
result = most_frequent_character(input)