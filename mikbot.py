import chess
import os
import random
import tkinter as tk
from tkinter import messagebox

class ChessGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tal_bot Chess Game")

        self.board = chess.Board()
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.piece_images = {}  
        self.load_images()  

        self.selected_square = None  
        self.update_board()
        self.canvas.bind("<Button-1>", self.on_board_click)

    def load_images(self):
        
        image_directory = r"D:\bot\bot\pieces"
        pieces = {'P': 'p.png', 'N': 'n.png', 'B': 'b.png', 'R': 'r.png', 'Q': 'q.png', 'K': 'k.png',
                  'p': 'bp.png', 'n': 'bn.png', 'b': 'bb.png', 'r': 'br.png', 'q': 'bq.png', 'k': 'bk.png'}
        for piece, filename in pieces.items():
            path = os.path.join(image_directory, filename)
            self.piece_images[piece] = tk.PhotoImage(file=path)

    def update_board(self):
        
        self.canvas.delete("all")

        
        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "brown"
                if self.selected_square == (row, col):
                    color = "blue"  
                self.canvas.create_rectangle(
                    col * 50, row * 50, (col + 1) * 50, (row + 1) * 50, fill=color
                )

        
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is not None:
                image = self.piece_images[piece.symbol()]
                self.canvas.create_image(
                    (chess.square_file(square) + 0.5) * 50,
                    (7 - chess.square_rank(square) + 0.5) * 50,
                    image=image,
                )

    def get_legal_moves(self, square):
        piece = self.board.piece_at(square)
        if piece is not None:
            return [move.uci() for move in self.board.legal_moves if move.from_square == square]
        return []

    def on_board_click(self, event):
        col_size = self.canvas.winfo_reqwidth() // 8
        row_size = self.canvas.winfo_reqheight() // 8
        clicked_square = (event.y // row_size, event.x // col_size)  

        if self.selected_square == clicked_square:
            
            start_square = self.selected_square
            end_square = clicked_square

            start_uci = self.square_to_uci(start_square)
            end_uci = self.square_to_uci(end_square)
            move_uci = start_uci + end_uci

            if chess.Move.from_uci(move_uci) in self.board.legal_moves:
                self.board.push(chess.Move.from_uci(move_uci))
                self.update_board()

                if not self.board.is_game_over():
                    
                    mikhal_move = self.get_random_move()
                    self.board.push(mikhal_move) 
                    self.update_board()

                    if self.board.is_game_over():
                        self.show_game_result()

                
                self.selected_square = None
        else:
            
            self.selected_square = clicked_square
            legal_moves = self.get_legal_moves(chess.square(clicked_square[1], 7 - clicked_square[0]))
            print(f"Legal moves: {legal_moves}")  
            self.update_board()

    def square_to_uci(self, square):
        
        row, col = square
        return chr(ord('a') + col) + str(8 - row)

    def show_game_result(self):
        result = self.board.result()
        messagebox.showinfo("Game Over", f"Game Result: {result}")

    def get_random_move(self):
        legal_moves = list(self.board.legal_moves)
        return random.choice(legal_moves)


def print_board(board):
    print(board)

def get_human_move(board):
    while True:
        try:
            move = input("Enter your move (e.g., e2e4): ")
            uci_move = chess.Move.from_uci(move)
            
            if uci_move in board.legal_moves:
                return uci_move  # Return the Move object directly
            else:
                print("Illegal move. Please enter a legal move.")
        except ValueError:
            print("Invalid move. Please enter a move in the format 'e2e4'.")

if __name__ == "__main__":
    root = tk.Tk()
    chess_game = ChessGameGUI(root)
    
    def play_game():
        # Human player's turn
        if not chess_game.board.is_game_over():
            chess_game.update_board()
            human_move = get_human_move(chess_game.board)
            chess_game.board.push(human_move)

        # Mikhal's turn (random move)
        if not chess_game.board.is_game_over():
            chess_game.update_board()
            mikhal_move = chess_game.get_random_move()
            print(f"Mikhal plays: {mikhal_move}")
            chess_game.board.push(mikhal_move)
        
        # Check if the game is over
        if chess_game.board.is_game_over():
            chess_game.show_game_result()
        else:
            root.after(1000, play_game)  # Schedule the next move after 1000 milliseconds

    root.after(100, play_game)  # Start the game loop after 100 milliseconds
    root.mainloop()
