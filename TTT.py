import tkinter as tk
from tkinter import messagebox
from functools import partial

WIN_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6)              # diagonals
]

class TicTacToe:
    def __init__(self, root):
        self.root = root
        root.title("Tic Tac Toe")
        root.resizable(False, False)

        self.current_player = "X"
        self.board = [None] * 9  # None / "X" / "O"
        self.buttons = [None] * 9
        self.game_over = False

        # Top frame: title + reset
        top = tk.Frame(root, pady=8)
        top.pack()
        tk.Label(top, text="Tic Tac Toe", font=("Segoe UI", 18, "bold")).pack(side="left", padx=8)
        reset_btn = tk.Button(top, text="Reset", command=self.reset_game)
        reset_btn.pack(side="right", padx=8)

        # Info label
        self.info_label = tk.Label(root, text=f"Current: {self.current_player}", font=("Segoe UI", 12))
        self.info_label.pack(pady=(0, 8))

        # Board frame (3x3)
        board_frame = tk.Frame(root, padx=10, pady=10)
        board_frame.pack()

        for i in range(9):
            btn = tk.Button(board_frame,
                            text="",
                            width=6,
                            height=3,
                            font=("Segoe UI", 24, "bold"),
                            command=partial(self.on_click, i))
            btn.grid(row=i//3, column=i%3, padx=4, pady=4)
            self.buttons[i] = btn

        # Footer tips
        footer = tk.Label(root, text="Two players: X and O. Click a square to play.", font=("Segoe UI", 9), fg="gray")
        footer.pack(pady=(6, 8))

    def on_click(self, index):
        if self.game_over:
            return
        if self.board[index] is not None:
            return  # already taken

        # Place move
        self.board[index] = self.current_player
        self.buttons[index].config(text=self.current_player, state="disabled")

        # Check for win/draw
        winner, combo = self.check_winner()
        if winner:
            self.game_over = True
            self.highlight_win(combo)
            self.info_label.config(text=f"Winner: {winner}")
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
            return

        if all(x is not None for x in self.board):
            self.game_over = True
            self.info_label.config(text="Draw")
            messagebox.showinfo("Game Over", "It's a draw!")
            return

        # Switch player
        self.current_player = "O" if self.current_player == "X" else "X"
        self.info_label.config(text=f"Current: {self.current_player}")

    def check_winner(self):
        """Return (winner, winning_combo) or (None, None)."""
        for (a, b, c) in WIN_COMBINATIONS:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a], (a, b, c)
        return None, None

    def highlight_win(self, combo):
        for idx in combo:
            self.buttons[idx].config(bg="#90ee90")  # light green
        # disable all buttons
        for btn in self.buttons:
            btn.config(state="disabled")

    def reset_game(self):
        self.current_player = "X"
        self.board = [None] * 9
        self.game_over = False
        self.info_label.config(text=f"Current: {self.current_player}")
        for btn in self.buttons:
            btn.config(text="", state="normal", bg="SystemButtonFace")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
