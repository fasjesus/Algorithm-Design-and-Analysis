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
    output_file.write(f"{result}\n")  # Write the result to the output file
    return result

def count_frequencies(stringui, output_file):
    stack = [[(elem, 1)] for elem in stringui]
    output_file.write("Initial Stack:\n")
    for sublist in stack:
        output_file.write(f"{sublist}\n")  # Write each sublist to the output file
    while len(stack) > 1:
        new_stack = []
        for i in range(0, len(stack), 2):
            if i+1 < len(stack):
                merged = merge(stack[i], stack[i+1], output_file)
                new_stack.append(merged)
            else:
                new_stack.append(stack[i])
                
        stack = new_stack
        output_file.write("Merged Stack:\n")
        for sublist in stack:
            output_file.write(f"{sublist}\n")  # Write each sublist to the output file
    return stack[0]

def most_frequent_character(s):
    with open('Problema 05\output.txt', 'w', encoding='utf-8') as output_file:
        string_with_frequencies = count_frequencies(s, output_file)
        max_freq = -1
        most_freq_char = None
        for char, freq in string_with_frequencies:
            if freq > max_freq:
                max_freq = freq
                most_freq_char = char
            elif freq == max_freq and char > most_freq_char:
                most_freq_char = char
        output_file.write(f'O elemento mais frequente é: {most_freq_char}\n')
        return most_freq_char

def read_input_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().strip()

filename = 'Problema 05\input.txt'  
input_data = read_input_from_file(filename)
result = most_frequent_character(input_data)