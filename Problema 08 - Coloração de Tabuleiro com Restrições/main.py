def is_valid(board, row, col, color, n=7):
    # Verificar adjacências
    if row > 0 and board[row-1][col] == color:
        return False
    if col > 0 and board[row][col-1] == color:
        return False
    if row < n-1 and board[row+1][col] == color:
        return False
    if col < n-1 and board[row][col+1] == color:
        return False
    
    # Verificar sub tabuleiros 2x2
    if row > 0 and col > 0 and board[row-1][col-1] == color and board[row-1][col] == color and board[row][col-1] == color:
        return False
    if row > 0 and col < n-1 and board[row-1][col+1] == color and board[row-1][col] == color and board[row][col+1] == color:
        return False
    if row < n-1 and col > 0 and board[row+1][col-1] == color and board[row+1][col] == color and board[row][col-1] == color:
        return False
    if row < n-1 and col < n-1 and board[row+1][col+1] == color and board[row+1][col] == color and board[row][col+1] == color:
        return False
    
    # Verificar diagonais
    if row == col or row + col == n-1:
        for i in range(n):
            if board[i][i] != -1 and board[i][i] != color:
                return False
            if board[i][n-1-i] != -1 and board[i][n-1-i] != color:
                return False
    
    return True

def get_next_position(board, row, col, n=7):
    for i in range(row, n):
        for j in range(n):
            if board[i][j] == -1:
                return (i, j)
    return (-1, -1)

def solve(board, row, col, n=7, colors=5):
    row, col = get_next_position(board, row, col, n)
    if row == -1:
        return True
    
    for color in range(colors):
        if is_valid(board, row, col, color, n):
            board[row][col] = color
            if solve(board, row, col, n, colors):
                return True
            board[row][col] = -1
    
    return False

def coloracao_tabuleiro():
    n = 7
    colors = 5
    
    board = [[-1 for _ in range(n)] for _ in range(n)]
    
    result = ""
    if solve(board, 0, 0, n, colors):
        for row in board:
            result += ' '.join(map(str, row)) + '\n'
    else:
        result = "A quantidade de soluções é zero.\n"
    
    # Escrita do resultado no arquivo de saída
    with open('Problema 08 - Coloração de Tabuleiro com Restrições/output.txt', 'w') as f:
        f.write(result)

# Executar a função principal
coloracao_tabuleiro()
