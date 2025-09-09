def print_board(board):
    print()
    for i in range(0, 9, 3):
        print(board[i], "|", board[i+1], "|", board[i+2])
        if i < 6:
            print("--+---+--")
    print()

def check_winner(board, player):
    winners = [ (0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in winners:
      if board[a]==board[b]==board[c]==player:
        return True
    return False

def tic_tac_toe():
    board = [""] * 9
    player = "X"

    while True:
        print_board(board)
        move = int(input(f"Player {player} (choose 1-9): ")) - 1

        if board[move] != "":
            print("That spot is already taken! Try again.")
            continue

        board[move] = player

        if check_winner(board, player):
            print_board(board)
            print(f"Player {player} wins!")
            break

        if "" not in board:
            print_board(board)
            print("It's a draw!")
            break
        player = "O" if player == "X" else "X"

tic_tac_toe()
