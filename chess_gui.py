import chess
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io
import cairosvg

class ChessGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tal_bot Chess Game")

        self.board = chess.Board()

        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.update_board()

        self.canvas.bind("<Button-1>", self.on_board_click)

    def update_board(self):
        # Convert SVG data to PNG using cairosvg
        svg_data = chess.svg.board(board=self.board)
        png_data = cairosvg.svg2png(bytestring=svg_data.encode('utf-8'))

        # Create a PhotoImage from the PNG data
        image = Image.open(io.BytesIO(png_data))
        tk_image = ImageTk.PhotoImage(image)

        # Display the image on the canvas
        self.canvas.create_image(0, 0, anchor="nw", image=tk_image)
        self.canvas.image = tk_image

    def get_random_move(self):
        legal_moves = list(self.board.legal_moves)
        return random.choice(legal_moves)

    def on_board_click(self, event):
        # Human player's turn
        col_size = self.canvas.winfo_reqwidth() // 8
        row_size = self.canvas.winfo_reqheight() // 8
        clicked_square = (event.x // col_size, event.y // row_size)

        human_move = self.square_to_uci(clicked_square)
        if chess.Move.from_uci(human_move) in self.board.legal_moves:
            self.board.push(chess.Move.from_uci(human_move))
            self.update_board()

            if not self.board.is_game_over():
                # Mikhal's turn (random move)
                mikhal_move = self.get_random_move()
                self.board.push(mikhal_move)
                self.update_board()

                if self.board.is_game_over():
                    self.show_game_result()

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
