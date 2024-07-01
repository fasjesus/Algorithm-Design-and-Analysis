# RESTRIÇÃO DE ADJACÊNCIA DIAGONAL, EXCETO PARA AS DIAGONAIS PRINCIPAL E SECUNDÁRIA

import time

def is_valid(board, row, col, color, n):
    # Verificar adjacências horizontais e verticais
    if row > 0 and board[row-1][col] == color:
        return False
    if col > 0 and board[row][col-1] == color:
        return False
    if row < n-1 and board[row+1][col] == color:
        return False
    if col < n-1 and board[row][col+1] == color:
        return False
    
    # Verificar adjacências diagonais, exceto as diagonais principal e secundária
    if (row > 0 and col > 0 and board[row-1][col-1] == color) and (row != col and row != n-1-col):
        return False
    if (row > 0 and col < n-1 and board[row-1][col+1] == color) and (row != col and row != n-1-col):
        return False
    if (row < n-1 and col > 0 and board[row+1][col-1] == color) and (row != col and row != n-1-col):
        return False
    if (row < n-1 and col < n-1 and board[row+1][col+1] == color) and (row != col and row != n-1-col):
        return False
    
    return True

def check_diagonals(board, n):
    # Verificar se as diagonais principal e secundária são espelhadas
    for i in range(n):
        if board[i][i] != board[i][n-1-i]:
            return False
    return True

def solve(board, row, col, n, colors, start_time, time_limit, solutions):
    # Verificar tempo decorrido
    if time.time() - start_time > time_limit:
        return False
    
    if row == n:
        # Encontrou uma solução válida
        if check_diagonals(board, n):
            solutions.append([row[:] for row in board])
            # Pare se encontrar 2 soluções
            if len(solutions) == 2:
                return True
        return False
    
    next_row = row if col < n-1 else row + 1
    next_col = (col + 1) % n
    
    if board[row][col] != -1:
        return solve(board, next_row, next_col, n, colors, start_time, time_limit, solutions)
    
    found_solution = False
    for color in range(colors):
        print(f"Verificando validade para cor {color} na posição ({row}, {col})")
        if is_valid(board, row, col, color, n):
            board[row][col] = color
            if solve(board, next_row, next_col, n, colors, start_time, time_limit, solutions):
                found_solution = True
            board[row][col] = -1
    
    return found_solution

def coloracao_tabuleiro(n, colors):
    board = [[-1 for _ in range(n)] for _ in range(n)]
    solutions = []
    
    # Definir limite de tempo em segundos
    time_limit = 120  # por exemplo, 120 segundos
    start_time = time.time()  # tempo de início
    
    if solve(board, 0, 0, n, colors, start_time, time_limit, solutions):
        # Gravar até 2 soluções e a quantidade total de soluções
        with open('Problema 08 - Coloração de Tabuleiro com Restrições/teste.txt', 'w', encoding='utf-8') as f:
            f.write(f"Para o Tabuleiro {n}x{n}, com {colors} cores. Temos as seguintes soluções encontradas:\n\n")
            if solutions:
                for i, solution in enumerate(solutions):
                    f.write(f"Solução {i + 1}:\n")
                    for row in solution:
                        f.write(' '.join(map(str, row)) + '\n')
                    if i < len(solutions) - 1:
                        f.write("\n")
                f.write(f"\nQuantidade de soluções encontradas: {len(solutions)}\n")
            else:
                f.write("A quantidade de soluções é zero.\n")
    else:
        with open('Problema 08 - Coloração de Tabuleiro com Restrições/teste.txt', 'w', encoding='utf-8') as f:
            f.write(f"Para o Tabuleiro {n}x{n}, com {colors} cores. Tempo limite excedido. A quantidade de soluções pode ser zero ou não encontrada.\n")

# Definir o tamanho do tabuleiro e o número de cores
n = 3  # tamanho do tabuleiro n x n
colors = 5  # número de cores

# Executar a função principal com os parâmetros definidos
coloracao_tabuleiro(n, colors)
