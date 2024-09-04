import sqlite3
import chess
import os
import random
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class ChessGameGUI:
    def __init__(self, root, db_connection):
        self.root = root
        self.root.title("Tal_bot Chess Game")

        self.db_connection = db_connection
        self.create_tables()

        self.board = chess.Board()
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.piece_values = {'K': float('inf'), 'Q': 9, 'B': 3, 'N': 4, 'R': 5, 'P': 1,
                             'k': float('inf'), 'q': 9, 'b': 3, 'n': 4, 'r': 5, 'p': 1}

        self.piece_images = {}
        self.load_images()

        self.selected_square = None
        self.selected_piece = None  # Keep track of the selected piece for dragging
        self.drag_start = None  # Initial position of the drag
        self.update_board()
        self.canvas.bind("<Button-1>", self.on_board_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.start_time = datetime.now()  # Initialize start_time when the game starts
        self.player_name = None
        self.player_place = None
        self.player_experience = None
        self.player_score = 0  # Initialize player score

    def create_tables(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS moves (
                            id INTEGER PRIMARY KEY,
                            move TEXT,
                            time_taken FLOAT,
                            player_name TEXT,
                            player_place TEXT,
                            player_experience INTEGER,
                            player_score INTEGER,
                            move_evaluation TEXT
                          )''')
        self.db_connection.commit()

    def load_images(self):
        image_directory = r"D:\bot\bot\pieces"  # Assuming images are in the same directory as the script
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
                    tags=piece.symbol()  # Add tag to identify the piece
                )

    def on_board_click(self, event):
        col_size = self.canvas.winfo_reqwidth() // 8
        row_size = self.canvas.winfo_reqheight() // 8
        clicked_square = (event.y // row_size, event.x // col_size)
        self.selected_square = clicked_square

        # Check if there's a piece on the selected square
        tags = self.canvas.gettags(tk.CURRENT)
        if tags:
            self.selected_piece = tags[0]  # Set the selected piece
            self.drag_start = event.x, event.y  # Record the start of the drag
            self.canvas.tag_raise(self.selected_piece)  # Raise the piece to the top

        self.update_board()

    def on_drag(self, event):
        if self.selected_piece:
            delta_x, delta_y = event.x - self.drag_start[0], event.y - self.drag_start[1]
            self.canvas.move(self.selected_piece, delta_x, delta_y)
            self.drag_start = event.x, event.y

    def on_release(self, event):
        if self.selected_piece:
            # Calculate the new square based on the release position
            col_size = self.canvas.winfo_reqwidth() // 8
            row_size = self.canvas.winfo_reqheight() // 8
            released_square = (event.y // row_size, event.x // col_size)

            # Convert square coordinates to algebraic notation
            start_square = chess.square(chess.square_file(self.selected_square[1]), 7 - self.selected_square[0])
            end_square = chess.square(chess.square_file(released_square[1]), 7 - released_square[0])
            move = chess.Move(start_square, end_square)

            # Check if the move is legal
            if move in self.board.legal_moves:
                self.board.push(move)
                self.update_board()

                # Perform bot move if the game is not over
                if not self.board.is_game_over():
                    mikhal_move = self.get_best_move() if random.random() > 0.3 else self.get_random_move()
                    self.board.push(mikhal_move)
                    self.update_board()

                    # Show game result if the game is over
                    if self.board.is_game_over():
                        self.show_game_result()

        # Reset selection and dragging variables
        self.selected_square = None
        self.selected_piece = None
        self.drag_start = None

    def square_to_uci(self, square):
        row, col = square
        return chr(ord('a') + col) + str(8 - row)

    def show_game_result(self):
        result = self.board.result()
        messagebox.showinfo("Game Over", f"Game Result: {result}")

    def get_random_move(self):
        legal_moves = list(self.board.legal_moves)
        return random.choice(legal_moves)

    def evaluate_move(self, move):
        piece = self.board.piece_at(move.to_square)
        value = self.get_piece_value(piece.symbol()) if piece else 0
        return value

    def get_piece_value(self, piece):
        return self.piece_values.get(piece, 0)

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_board()

        legal_moves = list(self.board.legal_moves)
        if maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, alpha, beta, False)
                self.board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval

    def get_best_move(self):
        best_move = None
        max_eval = float('-inf')
        legal_moves = list(self.board.legal_moves)
        for move in legal_moves:
            self.board.push(move)
            eval = self.minimax(2, float('-inf'), float('inf'), False)  # Adjust depth as needed
            self.board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move

    def evaluate_board(self):
        # Simple evaluation function for demonstration
        score = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is not None:
                score += self.get_piece_value(piece.symbol())
        return score

def get_player_info():
    name = input("Enter player name: ")
    place = input("Enter player place: ")
    experience = int(input("Enter player experience points: "))
    return name, place, experience

def main():
    db_connection = sqlite3.connect("chess_game.db")  # Connect to SQLite database
    root = tk.Tk()
    chess_game = ChessGameGUI(root, db_connection)

    chess_game.player_name, chess_game.player_place, chess_game.player_experience = get_player_info()

    # Function to insert move into the database
    def insert_move_into_db(move, time_taken, move_evaluation):
        cursor = db_connection.cursor()
        cursor.execute("INSERT INTO moves (move, time_taken, player_name, player_place, player_experience, player_score, move_evaluation) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (move, time_taken, chess_game.player_name, chess_game.player_place, chess_game.player_experience, chess_game.player_score, move_evaluation))
        db_connection.commit()

    def play_game():
        # Human player's turn
        if not chess_game.board.is_game_over():
            chess_game.update_board()

        # Mikhal's turn (best move or random move)
        if not chess_game.board.is_game_over():
            chess_game.update_board()
            mikhal_move = chess_game.get_best_move() if random.random() > 0.3 else chess_game.get_random_move()
            print(f"Mikhal plays: {mikhal_move}")
            chess_game.board.push(mikhal_move)
            move_evaluation = chess_game.evaluate_move(mikhal_move)
            insert_move_into_db(str(mikhal_move), 0, move_evaluation)  # Bot doesn't take time
            chess_game.player_score -= move_evaluation  # Deduct damage from player's score
        
        # Check if the game is over
        if chess_game.board.is_game_over():
            chess_game.show_game_result()
        else:
            root.after(1000, play_game)  # Schedule the next move after 1000 milliseconds

    root.after(100, play_game)  # Start the game loop after 100 milliseconds
    root.mainloop()

if __name__ == "__main__":
    main()
