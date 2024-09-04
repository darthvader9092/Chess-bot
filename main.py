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

        self.piece_images = {}  # Dictionary to store images
        self.load_images()  # Load images

        self.update_board()
        self.canvas.bind("<Button-1>", self.on_board_click)

    def load_images(self):
        # Load and store chess piece images
        image_directory = r"D:\bot\bot\pieces"
        pieces = {'P': 'p.png', 'N': 'n.png', 'B': 'b.png', 'R': 'r.png', 'Q': 'q.png', 'K': 'k.png',
                  'p': 'bp.png', 'n': 'bn.png', 'b': 'bb.png', 'r': 'br.png', 'q': 'bq.png', 'k': 'bk.png'}
        for piece, filename in pieces.items():
            path = os.path.join(image_directory, filename)
            self.piece_images[piece] = tk.PhotoImage(file=path)

    def update_board(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Draw the chessboard
        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "b"
                self.canvas.create_rectangle(
                    col * 50, row * 50, (col + 1) * 50, (row + 1) * 50, fill=color
                )

        # Draw pieces
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is not None:
                image = self.piece_images[piece.symbol()]
                self.canvas.create_image(
                    (chess.square_file(square) + 0.5) * 50,
                    (7 - chess.square_rank(square) + 0.5) * 50,
                    image=image,
                )

    def get_random_move(self):
        legal_moves = list(self.board.legal_moves)
        return random.choice(legal_moves)

    
    def on_board_click(self, event):
        col_size = self.canvas.winfo_reqwidth() // 8
        row_size = self.canvas.winfo_reqheight() // 8
        clicked_square = (event.x // col_size, event.y // row_size)

        # Check if this is the first click (selecting piece)
        if not hasattr(self, 'selected_square'):
            self.selected_square = clicked_square
        else:
            # Second click (moving the piece)
            start_square = self.selected_square
            end_square = clicked_square

            start_uci = self.square_to_uci(start_square)
            end_uci = self.square_to_uci(end_square)
            move_uci = start_uci + end_uci

            print(f"Generated move: {move_uci}")  # Debug print

            if chess.Move.from_uci(move_uci) in self.board.legal_moves:
                self.board.push(chess.Move.from_uci(move_uci))
                self.update_board()

                if not self.board.is_game_over():
                    # Mikhal's turn (random move)
                    mikhal_move = self.get_random_move()
                    self.board.push(mikhal_move)
                    self.update_board()

                    if self.board.is_game_over():
                        self.show_game_result()

            # Reset the selected square after the move
            del self.selected_square


        def square_to_uci(self, square):
            # Convert (row, col) to UCI format
            row, col = square
            return chr(ord('a') + col) + str(8 - row)

    def show_game_result(self):
        result = self.board.result()
        messagebox.showinfo("Game Over", f"Game Result: {result}")

def main():
    root = tk.Tk()
    chess_game = ChessGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()