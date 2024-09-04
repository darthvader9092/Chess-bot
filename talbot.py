import chess
import random  

def print_board(board):
    print(board)

def get_human_move(board):
    while True:
        try:
            move = input("Enter your move (e.g., e2e4): ")
            uci_move = chess.Move.from_uci(move)
            
            if uci_move in board.legal_moves:
                return move
            else:
                print("Illegal move. Please enter a legal move.")
        except ValueError:
            print("Invalid move. Please enter a move in the format 'e2e4'.")

def get_random_move(board):
    legal_moves = [move.uci() for move in board.legal_moves]
    return legal_moves[random.randint(0, len(legal_moves) - 1)]

def play_game():
    board = chess.Board()

    while not board.is_game_over():
        print_board(board)

        # Human player's turn
        human_move = get_human_move(board)
        board.push(chess.Move.from_uci(human_move))

        if board.is_game_over():
            break

        print_board(board)

        # Mikhal's turn 
        
        mikhail_move = get_random_move(board)
        print(f"Mikhail Tal plays: {mikhail_move}")
        board.push(chess.Move.from_uci(mikhail_move))

    print("Game Over")
    print("Result: " + board.result())

if __name__ == "__main__":
    play_game()
