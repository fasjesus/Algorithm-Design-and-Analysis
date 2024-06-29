def is_valid(board, row, col, color, n, seen_subgrids):
    # Verificar adjacências
    if row > 0 and board[row-1][col] == color:
        return False
    if col > 0 and board[row][col-1] == color:
        return False
    if row < n-1 and board[row+1][col] == color:
        return False
    if col < n-1 and board[row][col+1] == color:
        return False
    
    # Adicionar a nova cor temporariamente
    board[row][col] = color
    
    # Verificar subtabuleiros 2x2
    for r in range(n-1):
        for c in range(n-1):
            subgrid = (board[r][c], board[r][c+1], board[r+1][c], board[r+1][c+1])
            if subgrid in seen_subgrids:
                board[row][col] = -1
                return False
            seen_subgrids.add(subgrid)
    
    # Verificar diagonais
    if row == col:
        # Checar a diagonal principal
        if any(board[i][i] != color and board[i][i] != -1 for i in range(n)):
            board[row][col] = -1
            return False
    if row + col == n-1:
        # Checar a diagonal secundária
        if any(board[i][n-1-i] != color and board[i][n-1-i] != -1 for i in range(n)):
            board[row][col] = -1
            return False
    
    board[row][col] = -1
    return True

def get_next_position(board, row, col, n):
    for i in range(row, n):
        for j in range(n):
            if board[i][j] == -1:
                return (i, j)
    return (-1, -1)

def solve(board, row, col, n, colors, seen_subgrids):
    if row == n:
        # Verificar se as diagonais estão devidamente preenchidas
        diag_color = board[0][0]
        sec_diag_color = board[0][n-1]
        if all(board[i][i] == diag_color for i in range(n)) and \
           all(board[i][n-1-i] == sec_diag_color for i in range(n)):
            return True
        return False
    
    next_row = row if col < n-1 else row + 1
    next_col = (col + 1) % n
    
    if board[row][col] != -1:
        return solve(board, next_row, next_col, n, colors, seen_subgrids)
    
    for color in range(colors):
        if is_valid(board, row, col, color, n, seen_subgrids):
            board[row][col] = color
            if solve(board, next_row, next_col, n, colors, seen_subgrids):
                return True
            board[row][col] = -1
    
    return False

def coloracao_tabuleiro(n, colors):
    board = [[-1 for _ in range(n)] for _ in range(n)]
    seen_subgrids = set()
    
    if solve(board, 0, 0, n, colors, seen_subgrids):
        with open('Problema 08 - Coloração de Tabuleiro com Restrições/output.txt', 'w') as f:
            for row in board:
                f.write(' '.join(map(str, row)) + '\n')
    else:
        with open('Problema 08 - Coloração de Tabuleiro com Restrições/output.txt', 'w') as f:
            f.write("A quantidade de soluções é zero.\n")

# Definir o tamanho do tabuleiro e o número de cores
n = 3  # tamanho do tabuleiro n x n
colors = 5  # número de cores

# Executar a função principal com os parâmetros definidos
coloracao_tabuleiro(n, colors)