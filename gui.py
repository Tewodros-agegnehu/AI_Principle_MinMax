"""
Graphical UI for Tic-Tac-Toe vs Minimax AI

- Click cells to make your move.
- Choose who plays first; nodes-expanded metric.
- Restart to play again.
"""

import tkinter as tk
from tkinter import font as tkfont, messagebox
from typing import Optional, List, Tuple

from game import GameState, PLAYER_X, PLAYER_O, EMPTY
from minimax import MinimaxAgent


# Theme
BG = "#0d1117"
SURFACE = "#161b22"
CELL_BG = "#21262d"
CELL_BORDER = "#30363d"
CELL_HOVER = "#388bfd"
X_COLOR = "#ff7b72"
O_COLOR = "#79c0ff"
TEXT = "#e6edf3"
TEXT_MUTED = "#8b949e"
ACCENT = "#58a6ff"
WIN_BG = "#238636"
WIN_FG = "#ffffff"
BTN_BG = "#21262d"
BTN_HOVER = "#30363d"
GAP = 4
CELL_PAD = 20
BOARD_PAD = 16
WINDOW_PAD = 24


class TicTacToeGUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe vs Minimax AI")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.state: Optional[GameState] = None
        self.agent: Optional[MinimaxAgent] = None  # created in _start_game with chosen max_depth
        self.human_symbol = PLAYER_X
        self.ai_symbol = PLAYER_O
        self.human_first = True
        self.cell_buttons: List[List[tk.Button]] = []
        self.winning_line: Optional[List[Tuple[int, int]]] = None

        self._build_ui()
        self._center_window()
        self._show_start_choices()

    def _center_window(self) -> None:
        self.root.update_idletasks()
        w = self.root.winfo_reqwidth()
        h = self.root.winfo_reqheight()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"+{x}+{max(0, y - 40)}")

    def _build_ui(self) -> None:
        try:
            title_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
            subtitle_font = tkfont.Font(family="Segoe UI", size=10)
            cell_font = tkfont.Font(family="Segoe UI", size=42, weight="bold")
            status_font = tkfont.Font(family="Segoe UI", size=12)
            btn_font = tkfont.Font(family="Segoe UI", size=11)
        except tk.TclError:
            title_font = tkfont.Font(size=18, weight="bold")
            subtitle_font = tkfont.Font(size=10)
            cell_font = tkfont.Font(size=42, weight="bold")
            status_font = tkfont.Font(size=12)
            btn_font = tkfont.Font(size=11)

        # Header
        header = tk.Frame(self.root, bg=BG)
        header.pack(pady=(WINDOW_PAD, 8))
        self.title_label = tk.Label(
            header,
            text="Tic-Tac-Toe",
            font=title_font,
            fg=TEXT,
            bg=BG,
        )
        self.title_label.pack()
        tk.Label(
            header,
            text="Minimax AI • Adversarial Search",
            font=subtitle_font,
            fg=TEXT_MUTED,
            bg=BG,
        ).pack(pady=(2, 0))

        # Optional: depth-limited search
        self.options_frame = tk.Frame(self.root, bg=BG)
        self.options_frame.pack(pady=(10, 4))
        tk.Label(
            self.options_frame,
            text="AI search:",
            font=status_font,
            fg=TEXT_MUTED,
            bg=BG,
        ).pack(side=tk.LEFT, padx=(0, 6))
        self.depth_var = tk.StringVar(value="Full depth")
        depth_menu = tk.OptionMenu(
            self.options_frame,
            self.depth_var,
            "Full depth",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
        )
        depth_menu.config(
            font=btn_font,
            bg=BTN_BG,
            fg=TEXT,
            activebackground=BTN_HOVER,
            activeforeground=TEXT,
            highlightthickness=0,
        )
        depth_menu.pack(side=tk.LEFT, padx=2)
        tk.Label(
            self.options_frame,
            text="(Full = optimal; number = depth-limited + heuristic)",
            font=tkfont.Font(size=9),
            fg=TEXT_MUTED,
            bg=BG,
        ).pack(side=tk.LEFT, padx=(8, 0))

        # Start choices
        self.start_frame = tk.Frame(self.root, bg=BG)
        self.start_frame.pack(pady=12)
        tk.Label(
            self.start_frame,
            text="Who plays first?",
            font=status_font,
            fg=TEXT_MUTED,
            bg=BG,
        ).pack(side=tk.LEFT, padx=(0, 10))
        for label, first in [("You (X)", True), ("AI (O)", False)]:
            b = tk.Button(
                self.start_frame,
                text=label,
                font=btn_font,
                bg=BTN_BG,
                fg=TEXT,
                activebackground=BTN_HOVER,
                activeforeground=TEXT,
                relief=tk.FLAT,
                padx=16,
                pady=8,
                cursor="hand2",
                highlightthickness=0,
                borderwidth=0,
                command=lambda f=first: self._start_game(human_first=f),
            )
            b.pack(side=tk.LEFT, padx=3)
            b.bind("<Enter>", lambda e, btn=b: btn.configure(bg=BTN_HOVER))
            b.bind("<Leave>", lambda e, btn=b: btn.configure(bg=BTN_BG))

        # Board container with border
        board_outer = tk.Frame(self.root, bg=CELL_BORDER, padx=GAP, pady=GAP)
        board_outer.pack(pady=16, padx=WINDOW_PAD)

        for r in range(3):
            row_buttons = []
            for c in range(3):
                btn = tk.Button(
                    board_outer,
                    text="",
                    font=cell_font,
                    width=2,
                    height=1,
                    bg=CELL_BG,
                    fg=TEXT,
                    activebackground=CELL_HOVER,
                    activeforeground=TEXT,
                    relief=tk.FLAT,
                    cursor="hand2",
                    highlightthickness=0,
                    borderwidth=0,
                    command=lambda row=r, col=c: self._on_cell_click(row, col),
                )
                btn.grid(row=r, column=c, padx=GAP, pady=GAP, sticky="nsew")
                btn.bind(
                    "<Enter>",
                    lambda e, b=btn, rw=r, cl=c: self._cell_enter(b, rw, cl),
                )
                btn.bind(
                    "<Leave>",
                    lambda e, b=btn, rw=r, cl=c: self._set_cell_color(b, rw, cl),
                )
                row_buttons.append(btn)
            self.cell_buttons.append(row_buttons)

        for i in range(3):
            board_outer.grid_rowconfigure(i, weight=1, minsize=72)
            board_outer.grid_columnconfigure(i, weight=1, minsize=72)

        # Status
        self.status_label = tk.Label(
            self.root,
            text="",
            font=status_font,
            fg=TEXT,
            bg=BG,
        )
        self.status_label.pack(pady=(12, 4))

        self.metrics_label = tk.Label(
            self.root,
            text="",
            font=tkfont.Font(size=10),
            fg=TEXT_MUTED,
            bg=BG,
        )
        self.metrics_label.pack(pady=2)

        # New Game button
        new_btn = tk.Button(
            self.root,
            text="New Game",
            font=btn_font,
            bg=ACCENT,
            fg=BG,
            activebackground=CELL_HOVER,
            activeforeground=TEXT,
            relief=tk.FLAT,
            padx=24,
            pady=10,
            cursor="hand2",
            highlightthickness=0,
            command=self._restart,
        )
        new_btn.pack(pady=(12, WINDOW_PAD))
        new_btn.bind("<Enter>", lambda e: new_btn.configure(bg=CELL_HOVER, fg=TEXT))
        new_btn.bind("<Leave>", lambda e: new_btn.configure(bg=ACCENT, fg=BG))

    def _cell_enter(self, btn: tk.Button, row: int, col: int) -> None:
        if btn["text"] == "" and not (self.winning_line and (row, col) in self.winning_line):
            btn.configure(bg=CELL_HOVER)

    def _set_cell_color(
        self,
        btn: tk.Button,
        row: int,
        col: int,
    ) -> None:
        if self.winning_line and (row, col) in self.winning_line:
            btn.configure(bg=WIN_BG, fg=WIN_FG)
            return
        if btn["text"] == "X":
            btn.configure(bg=CELL_BG, fg=X_COLOR)
        elif btn["text"] == "O":
            btn.configure(bg=CELL_BG, fg=O_COLOR)
        else:
            btn.configure(bg=CELL_BG, fg=TEXT)

    def _get_max_depth(self) -> Optional[int]:
        v = self.depth_var.get().strip()
        if v == "Full depth" or not v:
            return None
        try:
            d = int(v)
            return d if 3 <= d <= 8 else None
        except ValueError:
            return None

    def _show_start_choices(self) -> None:
        self.options_frame.pack(pady=(10, 4))
        self.start_frame.pack(pady=12)
        self.status_label.config(text="")
        self.metrics_label.config(text="")
        self._clear_board_display()

    def _start_game(self, human_first: bool) -> None:
        self.human_first = human_first
        self.human_symbol = PLAYER_X if human_first else PLAYER_O
        self.ai_symbol = PLAYER_O if human_first else PLAYER_X
        max_depth = self._get_max_depth()
        self.agent = MinimaxAgent(use_alpha_beta=True, max_depth=max_depth)
        self.state = GameState()
        self.winning_line = None
        self.options_frame.pack_forget()
        self.start_frame.pack_forget()
        self._refresh_board()
        self._update_status()
        self.metrics_label.config(text="")
        if not human_first:
            self.root.after(400, self._ai_move)

    def _clear_board_display(self) -> None:
        for r in range(3):
            for c in range(3):
                btn = self.cell_buttons[r][c]
                btn.config(text="", bg=CELL_BG, fg=TEXT)
        self.winning_line = None

    def _refresh_board(self) -> None:
        if self.state is None:
            return
        for r in range(3):
            for c in range(3):
                sym = self.state.board[r][c]
                btn = self.cell_buttons[r][c]
                if sym == PLAYER_X:
                    btn.config(text="X", fg=X_COLOR)
                elif sym == PLAYER_O:
                    btn.config(text="O", fg=O_COLOR)
                else:
                    btn.config(text="", fg=TEXT)
                self._set_cell_color(btn, r, c)

    def _update_status(self) -> None:
        if self.state is None:
            return
        if self.state.is_terminal():
            winner = self.state._has_winner()
            if winner is None:
                self.status_label.config(text="Draw!", fg=TEXT_MUTED)
            elif winner == self.human_symbol:
                self.status_label.config(text="You win!", fg=X_COLOR)
            else:
                self.status_label.config(text="AI wins!", fg=O_COLOR)
            return
        if self.state.current_player == self.human_symbol:
            self.status_label.config(text="Your turn — click a cell", fg=TEXT)
        else:
            self.status_label.config(text="AI thinking...", fg=TEXT_MUTED)

    def _on_cell_click(self, row: int, col: int) -> None:
        if self.state is None or self.state.is_terminal():
            return
        if self.state.current_player != self.human_symbol:
            return
        legal = self.state.get_legal_actions()
        if (row, col) not in legal:
            return
        self.state = self.state.result((row, col))
        self._refresh_board()
        self._update_status()
        if self.state.is_terminal():
            self._show_game_over()
            return
        self.root.after(350, self._ai_move)

    def _ai_move(self) -> None:
        if self.state is None or self.state.is_terminal() or self.agent is None:
            return
        move = self.agent.get_action(self.state, self.ai_symbol)
        if move is None:
            return
        nodes = self.agent.get_nodes_expanded()
        depth_info = f" [depth limit: {self.agent.max_depth}]" if self.agent.max_depth is not None else ""
        self.metrics_label.config(text=f"Nodes expanded (last move): {nodes}{depth_info}")
        self.state = self.state.result(move)
        self._refresh_board()
        self._update_status()
        if self.state.is_terminal():
            self._show_game_over()

    def _show_game_over(self) -> None:
        if self.state is None:
            return
        winner = self.state._has_winner()
        if winner is not None:
            self._highlight_win_line()
        if winner == self.human_symbol:
            messagebox.showinfo("Game Over", "You win!")
        elif winner == self.ai_symbol:
            messagebox.showinfo("Game Over", "AI wins!")
        else:
            messagebox.showinfo("Game Over", "Draw!")

    def _highlight_win_line(self) -> None:
        if self.state is None:
            return
        from game import WIN_LINES
        winner = self.state._has_winner()
        if winner is None:
            return
        for line in WIN_LINES:
            symbols = [self.state.board[r][c] for r, c in line]
            if symbols[0] != EMPTY and all(s == symbols[0] for s in symbols):
                self.winning_line = line
                for r, c in line:
                    self.cell_buttons[r][c].configure(bg=WIN_BG, fg=WIN_FG)
                return

    def _restart(self) -> None:
        self.state = None
        self.winning_line = None
        self._clear_board_display()
        self._show_start_choices()

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = TicTacToeGUI()
    app.run()


if __name__ == "__main__":
    main()
