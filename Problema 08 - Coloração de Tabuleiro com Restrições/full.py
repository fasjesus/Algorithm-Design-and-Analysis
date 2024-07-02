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
        
    # Verificar adjacências diagonais
    if row > 0 and col > 0 and board[row-1][col-1] == color:
        return False
    if row > 0 and col < n-1 and board[row-1][col+1] == color:
        return False
    if row < n-1 and col > 0 and board[row+1][col-1] == color:
        return False
    if row < n-1 and col < n-1 and board[row+1][col+1] == color:
        return False
    
    return True

def check_diagonals(board, n):
    # Verificar se as diagonais principal e secundária são espelhadas
    for i in range(n):
        if board[i][i] != board[i][n-1-i]:
            return False
    return True

def check_subgrids(board, n):
    # Verificar se há subtabuleiros 2x2 com a mesma configuração
    for i in range(n-1):
        for j in range(n-1):
            # Verificar se todos os elementos do subtabuleiro 2x2 são preenchidos
            if board[i][j] != -1 and board[i][j+1] != -1 and board[i+1][j] != -1 and board[i+1][j+1] != -1:
                # Subtabuleiro 2x2 atual
                current_subgrid = [
                    [board[i][j], board[i][j+1]],
                    [board[i+1][j], board[i+1][j+1]]
                ]
                # Comparar com todos os outros subtabuleiros 2x2
                for k in range(n-1):
                    for l in range(n-1):
                        if (i != k or j != l) and board[k][l] != -1 and board[k][l+1] != -1 and board[k+1][l] != -1 and board[k+1][l+1] != -1:
                            # Subtabuleiro 2x2 para comparação
                            compare_subgrid = [
                                [board[k][l], board[k][l+1]],
                                [board[k+1][l], board[k+1][l+1]]
                            ]
                            # Verificar se as configurações são iguais
                            if current_subgrid == compare_subgrid:
                                return False
    return True

def solve(board, row, col, n, colors, start_time, time_limit, solutions):
    # Verificar tempo decorrido
    if time.time() - start_time > time_limit:
        return False
    
    if row == n:
        # Encontrou uma solução válida
        if check_diagonals(board, n) and check_subgrids(board, n):
            solutions.append([r[:] for r in board])
            # Pare se encontrar 1 soluções
            if len(solutions) == 1:
                return True
        return False
    
    next_row = row if col < n-1 else row + 1
    next_col = (col + 1) % n
    
    if board[row][col] != -1:
        return solve(board, next_row, next_col, n, colors, start_time, time_limit, solutions)
    
    found_solution = False
    for color in range(colors):
        if is_valid(board, row, col, color, n):
            board[row][col] = color
            if solve(board, next_row, next_col, n, colors, start_time, time_limit, solutions):
                found_solution = True
            board[row][col] = -1  # Backtracking step - remove a cor e tenta a próxima
    
    return found_solution

def coloracao_tabuleiro(n, colors):
    board = [[-1 for _ in range(n)] for _ in range(n)]
    solutions = []
    
    time_limit = 12 
    start_time = time.time()  
    
    if solve(board, 0, 0, n, colors, start_time, time_limit, solutions):
        end_time = time.time()
        elapsed_time = end_time - start_time
        with open('Problema 08 - Coloração de Tabuleiro com Restrições/full.txt', 'w', encoding='utf-8') as f:
            f.write(f"Para o Tabuleiro {n}x{n}, com {colors} cores. Temos as seguintes soluções encontradas:\n\n")
            if solutions:
                for i, solution in enumerate(solutions):
                    f.write(f"Solução {i + 1}:\n")
                    for row in solution:
                        f.write(' '.join(map(str, row)) + '\n')
                    if i < len(solutions) - 1:
                        f.write("\n")
                f.write(f"\nQuantidade de soluções encontradas: {len(solutions)}\n")
                f.write(f"Tempo gasto: {elapsed_time:.2f} segundos\n")
            else:
                f.write("A quantidade de soluções é zero.\n")
    else:
        with open('Problema 08 - Coloração de Tabuleiro com Restrições/full.txt', 'w', encoding='utf-8') as f:
            f.write(f"Para o Tabuleiro {n}x{n}, com {colors} cores. Tempo limite excedido. A quantidade de soluções pode ser zero ou não encontrada.\n")
            f.write(f"Tempo gasto: {elapsed_time:.2f} segundos\n")
# ======================================================== INPUTS =======================================================================
n = 5  # tamanho do tabuleiro n x n
colors = 5  # número de cores

# Processo
coloracao_tabuleiro(n, colors)
