# cspell:disable
"""Tic Tac Toe vs Bot (GUI Tkinter) - bot memakai Minimax + Alpha-Beta, tidak mungkin kalah.

Jalankan: python tictactoe_gui.py
"""

import tkinter as tk

WIN_LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
             (0, 3, 6), (1, 4, 7), (2, 5, 8),
             (0, 4, 8), (2, 4, 6)]


# ================================================================ LOGIKA
def get_winner(board):
    for a, b, c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a], (a, b, c)
    return None, None


def is_full(board):
    return " " not in board


def minimax(board, turn, bot, human, depth, alpha, beta):
    """Skor + jika bot menang, - jika human menang, 0 jika seri (dengan alpha-beta pruning)."""
    winner, _ = get_winner(board)
    if winner == bot:
        return 10 - depth
    if winner == human:
        return depth - 10
    if is_full(board):
        return 0

    if turn == bot:
        best = -100
        for i in range(9):
            if board[i] == " ":
                board[i] = bot
                best = max(best, minimax(board, human, bot, human, depth + 1, alpha, beta))
                board[i] = " "
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return best

    best = 100
    for i in range(9):
        if board[i] == " ":
            board[i] = human
            best = min(best, minimax(board, bot, bot, human, depth + 1, alpha, beta))
            board[i] = " "
            beta = min(beta, best)
            if beta <= alpha:
                break
    return best


def best_move(board, bot, human):
    if all(c == " " for c in board):      # papan kosong: tengah = langkah optimal
        return 4
    best_score, move = -100, None
    for i in range(9):
        if board[i] == " ":
            board[i] = bot
            score = minimax(board, human, bot, human, 1, -100, 100)
            board[i] = " "
            if score > best_score:
                best_score, move = score, i
    return move


# ================================================================== GUI
class FlatButton(tk.Label):
    """Tombol datar dengan efek hover (tampil sama di Windows/Mac/Linux)."""

    def __init__(self, master, text, command, bg, hover, fg="#11111b",
                 width=14, size=11):
        super().__init__(master, text=text, bg=bg, fg=fg, width=width, pady=7,
                         font=("Segoe UI", size, "bold"), cursor="hand2")
        self._bg, self._hover = bg, hover
        self.bind("<Enter>", lambda e: self.config(bg=self._hover))
        self.bind("<Leave>", lambda e: self.config(bg=self._bg))
        self.bind("<Button-1>", lambda e: command())


class TicTacToeApp:
    # ukuran tetap -> tampilan tidak pernah berubah/loncat
    WIN_W, WIN_H = 440, 690
    CELL, GAP, MARGIN = 112, 8, 10
    BOARD = 3 * CELL + 2 * GAP + 2 * MARGIN          # 372 px

    C = {
        "bg": "#1e1e2e", "panel": "#181825", "cell": "#313244", "hover": "#45475a",
        "text": "#cdd6f4", "muted": "#7f849c",
        "X": "#89b4fa", "O": "#f38ba8", "win": "#f9e2af",
        "green": "#a6e3a1", "green_h": "#c3f0bf",
        "blue": "#89b4fa", "blue_h": "#b4d0fb",
        "red": "#f38ba8", "red_h": "#f7b0c3",
        "grey": "#45475a", "grey_h": "#585b70",
    }

    def __init__(self, root):
        self.root = root
        c = self.C
        root.title("Tic Tac Toe vs Bot")
        root.configure(bg=c["bg"])
        root.resizable(False, False)
        x = (root.winfo_screenwidth() - self.WIN_W) // 2
        y = max(0, (root.winfo_screenheight() - self.WIN_H) // 2 - 20)
        root.geometry(f"{self.WIN_W}x{self.WIN_H}+{x}+{y}")

        # ---- judul
        tk.Label(root, text="TIC TAC TOE", font=("Segoe UI", 24, "bold"),
                 fg=c["text"], bg=c["bg"]).pack(pady=(16, 0))
        tk.Label(root, text="Kamu vs Bot (Minimax)", font=("Segoe UI", 10),
                 fg=c["muted"], bg=c["bg"]).pack(pady=(0, 10))

        # ---- papan skor (ukuran tetap)
        score_row = tk.Frame(root, bg=c["bg"])
        score_row.pack()
        self.score_labels = {}
        for key, name, color in (("human", "KAMU", c["X"]), ("draw", "SERI", c["muted"]),
                                 ("bot", "BOT", c["O"])):
            card = tk.Frame(score_row, bg=c["panel"], width=110, height=64)
            card.pack(side="left", padx=5)
            card.pack_propagate(False)
            tk.Label(card, text=name, font=("Segoe UI", 9, "bold"), fg=color,
                     bg=c["panel"]).pack(pady=(8, 0))
            lbl = tk.Label(card, text="0", font=("Segoe UI", 18, "bold"),
                           fg=c["text"], bg=c["panel"])
            lbl.pack()
            self.score_labels[key] = lbl
        self.scores = {"human": 0, "draw": 0, "bot": 0}

        # ---- status (lebar tetap, teks panjang apapun tidak mengubah ukuran)
        status_box = tk.Frame(root, bg=c["bg"], width=self.BOARD, height=44)
        status_box.pack(pady=(10, 0))
        status_box.pack_propagate(False)
        self.status = tk.Label(status_box, text="", font=("Segoe UI", 13, "bold"),
                               fg=c["text"], bg=c["bg"])
        self.status.pack(expand=True)

        # ---- area papan (kanvas + kartu overlay)
        self.board_frame = tk.Frame(root, bg=c["bg"], width=self.BOARD, height=self.BOARD)
        self.board_frame.pack()
        self.board_frame.pack_propagate(False)
        self.canvas = tk.Canvas(self.board_frame, width=self.BOARD, height=self.BOARD,
                                bg=c["panel"], highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Motion>", self.on_motion)
        self.canvas.bind("<Leave>", lambda e: self.set_hover(None))
        self.canvas.bind("<Button-1>", self.on_click)

        self.card = tk.Frame(self.board_frame, bg=c["bg"], highlightthickness=2,
                             highlightbackground=c["blue"])

        # ---- tombol bawah
        bottom = tk.Frame(root, bg=c["bg"])
        bottom.pack(pady=16)
        FlatButton(bottom, "Game Baru", self.ask_first, c["green"], c["green_h"],
                   width=13).pack(side="left", padx=6)
        FlatButton(bottom, "Reset Skor", self.reset_scores, c["grey"], c["grey_h"],
                   fg=c["text"], width=13).pack(side="left", padx=6)

        # ---- state
        self.board = [" "] * 9
        self.human, self.bot = "X", "O"
        self.turn = "X"
        self.game_over = True
        self.busy = True          # true = klik papan diabaikan
        self.hover = None
        self.game_id = 0          # untuk membatalkan callback lama
        self.draw_board()
        self.ask_first()

    # ------------------------------------------------ util
    def later(self, ms, fn):
        """root.after yang otomatis batal kalau game sudah diganti."""
        gid = self.game_id
        self.root.after(ms, lambda: fn() if gid == self.game_id else None)

    def set_status(self, text, color=None):
        self.status.config(text=text, fg=color or self.C["text"])

    def cell_box(self, i):
        r, col = divmod(i, 3)
        x0 = self.MARGIN + col * (self.CELL + self.GAP)
        y0 = self.MARGIN + r * (self.CELL + self.GAP)
        return x0, y0, x0 + self.CELL, y0 + self.CELL

    def cell_at(self, x, y):
        for i in range(9):
            x0, y0, x1, y1 = self.cell_box(i)
            if x0 <= x <= x1 and y0 <= y <= y1:
                return i
        return None

    def rounded_rect(self, x0, y0, x1, y1, r, **kw):
        pts = [x0 + r, y0, x1 - r, y0, x1, y0, x1, y0 + r, x1, y1 - r, x1, y1,
               x1 - r, y1, x0 + r, y1, x0, y1, x0, y1 - r, x0, y0 + r, x0, y0]
        return self.canvas.create_polygon(pts, smooth=True, **kw)

    # ------------------------------------------------ menggambar
    def draw_board(self):
        self.canvas.delete("all")
        for i in range(9):
            self.rounded_rect(*self.cell_box(i), 18, fill=self.C["cell"],
                              outline="", tags=f"cell{i}")

    def set_hover(self, idx):
        if idx == self.hover:
            return
        if self.hover is not None:
            self.canvas.itemconfig(f"cell{self.hover}", fill=self.C["cell"])
        self.hover = idx
        if idx is not None:
            self.canvas.itemconfig(f"cell{idx}", fill=self.C["hover"])
        self.canvas.config(cursor="hand2" if idx is not None else "")

    def animate_mark(self, i, mark, done, step=0, steps=12):
        x0, y0, x1, y1 = self.cell_box(i)
        cx, cy, r = (x0 + x1) / 2, (y0 + y1) / 2, self.CELL * 0.26
        t = (step + 1) / steps
        tag, color = f"mark{i}", self.C[mark]
        self.canvas.delete(tag)
        if mark == "X":
            t1, t2 = min(1, t * 2), max(0, t * 2 - 1)
            self.canvas.create_line(cx - r, cy - r, cx - r + 2 * r * t1, cy - r + 2 * r * t1,
                                    width=12, fill=color, capstyle="round", tags=tag)
            if t2 > 0:
                self.canvas.create_line(cx + r, cy - r, cx + r - 2 * r * t2, cy - r + 2 * r * t2,
                                        width=12, fill=color, capstyle="round", tags=tag)
        else:
            self.canvas.create_arc(cx - r, cy - r, cx + r, cy + r, start=90,
                                   extent=-359.9 * t, style="arc", width=12,
                                   outline=color, tags=tag)
        if step + 1 < steps:
            self.later(16, lambda: self.animate_mark(i, mark, done, step + 1, steps))
        else:
            done()

    # ------------------------------------------------ kartu overlay
    def show_card(self, title, subtitle, buttons, accent=None):
        c = self.C
        for w in self.card.winfo_children():
            w.destroy()
        self.card.config(highlightbackground=accent or c["blue"])
        tk.Label(self.card, text=title, font=("Segoe UI", 20, "bold"),
                 fg=accent or c["text"], bg=c["bg"]).pack(pady=(24, 2))
        tk.Label(self.card, text=subtitle, font=("Segoe UI", 10),
                 fg=c["muted"], bg=c["bg"]).pack(pady=(0, 14))
        for text, cmd, bg, hov in buttons:
            FlatButton(self.card, text, cmd, bg, hov, width=20).pack(pady=4)
        self.card.pack_propagate(True)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.lift()

    def hide_card(self):
        self.card.place_forget()

    def ask_first(self):
        self.game_id += 1          # batalkan animasi/langkah bot yang tertunda
        self.busy = True
        self.game_over = True
        self.set_hover(None)
        c = self.C
        self.set_status("Pilih siapa yang jalan duluan", c["muted"])
        self.show_card("Siapa duluan?", "Yang jalan duluan memakai X",
                       [("Saya (X)", lambda: self.start_game(True), c["blue"], c["blue_h"]),
                        ("Bot (X)", lambda: self.start_game(False), c["red"], c["red_h"])])

    # ------------------------------------------------ alur game
    def start_game(self, human_first):
        self.game_id += 1
        self.hide_card()
        self.board = [" "] * 9
        self.draw_board()
        self.hover = None
        self.game_over = False
        self.human, self.bot = ("X", "O") if human_first else ("O", "X")
        self.turn = "X"
        if human_first:
            self.busy = False
            self.set_status(f"Giliranmu  ({self.human})", self.C[self.human])
        else:
            self.busy = True
            self.set_status("Bot sedang berpikir...", self.C[self.bot])
            self.later(500, self.bot_turn)

    def on_motion(self, e):
        if self.busy or self.game_over:
            return self.set_hover(None)
        i = self.cell_at(e.x, e.y)
        self.set_hover(i if i is not None and self.board[i] == " " else None)

    def on_click(self, e):
        if self.busy or self.game_over:
            return
        i = self.cell_at(e.x, e.y)
        if i is None or self.board[i] != " ":
            return
        self.set_hover(None)
        self.play(i, self.human)

    def bot_turn(self):
        move = best_move(self.board, self.bot, self.human)
        self.play(move, self.bot)

    def play(self, i, mark):
        self.busy = True
        self.board[i] = mark
        self.canvas.itemconfig(f"cell{i}", fill=self.C["cell"])
        self.animate_mark(i, mark, self.after_move)

    def after_move(self):
        winner, line = get_winner(self.board)
        if winner or is_full(self.board):
            return self.end_game(winner, line)
        self.turn = "O" if self.turn == "X" else "X"
        if self.turn == self.human:
            self.busy = False
            self.set_status(f"Giliranmu  ({self.human})", self.C[self.human])
        else:
            self.set_status("Bot sedang berpikir...", self.C[self.bot])
            self.later(350, self.bot_turn)

    def end_game(self, winner, line):
        c = self.C
        self.game_over, self.busy = True, True
        if winner:
            x0, y0, _, _ = self.cell_box(line[0])
            _, _, x1, y1 = self.cell_box(line[2])
            a, b = self.cell_box(line[0]), self.cell_box(line[2])
            self.canvas.create_line((a[0] + a[2]) / 2, (a[1] + a[3]) / 2,
                                    (b[0] + b[2]) / 2, (b[1] + b[3]) / 2,
                                    width=10, fill=c["win"], capstyle="round")
        if winner == self.human:
            key, title, color = "human", "Kamu menang!", c["green"]
        elif winner == self.bot:
            key, title, color = "bot", "Bot menang!", c["red"]
        else:
            key, title, color = "draw", "Seri!", c["win"]
        self.scores[key] += 1
        self.score_labels[key].config(text=str(self.scores[key]))
        self.set_status(title, color)
        self.later(900, lambda: self.show_card(
            title, "Mau main lagi?",
            [("Main Lagi", self.ask_first, c["green"], c["green_h"])], accent=color))

    def reset_scores(self):
        self.scores = {"human": 0, "draw": 0, "bot": 0}
        for lbl in self.score_labels.values():
            lbl.config(text="0")


if __name__ == "__main__":
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()