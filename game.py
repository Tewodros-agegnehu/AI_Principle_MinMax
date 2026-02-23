"""
Game Representation Module - Tic-Tac-Toe

Formal definition of:
- Game states
- Legal actions
- Terminal states
- Utility function (win/loss/draw)
"""

from typing import List, Tuple, Optional
from copy import deepcopy

# Constants for players and board
EMPTY = " "
PLAYER_X = "X"  # Human (or first player)
PLAYER_O = "O"  # AI agent (or second player)
BOARD_SIZE = 3

# Win conditions: all possible lines (rows, columns, diagonals)
WIN_LINES = [
    [(0, 0), (0, 1), (0, 2)],  # Row 0
    [(1, 0), (1, 1), (1, 2)],  # Row 1
    [(2, 0), (2, 1), (2, 2)],  # Row 2
    [(0, 0), (1, 0), (2, 0)],  # Col 0
    [(0, 1), (1, 1), (2, 1)],  # Col 1
    [(0, 2), (1, 2), (2, 2)],  # Col 2
    [(0, 0), (1, 1), (2, 2)],  # Main diagonal
    [(0, 2), (1, 1), (2, 0)],  # Anti-diagonal
]


class GameState:
    """
    Formal representation of a Tic-Tac-Toe game state.
    State is immutable for search; we use copies when applying actions.
    """

    def __init__(
        self,
        board: Optional[List[List[str]]] = None,
        current_player: str = PLAYER_X,
    ):
        if board is None:
            board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.board = board
        self.current_player = current_player

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GameState):
            return False
        return (
            self.board == other.board and self.current_player == other.current_player
        )

    def __hash__(self) -> int:
        return hash((tuple(tuple(row) for row in self.board), self.current_player))

    def get_opponent(self) -> str:
        """Return the symbol of the opponent."""
        return PLAYER_O if self.current_player == PLAYER_X else PLAYER_X

    def get_legal_actions(self) -> List[Tuple[int, int]]:
        """
        Return list of legal (row, col) moves for the current player.
        Empty cells are legal moves.
        """
        actions = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == EMPTY:
                    actions.append((r, c))
        return actions

    def is_terminal(self) -> bool:
        """
        Terminal state: someone has won or the board is full (draw).
        """
        if self._has_winner() is not None:
            return True
        return all(
            self.board[r][c] != EMPTY
            for r in range(BOARD_SIZE)
            for c in range(BOARD_SIZE)
        )

    def _has_winner(self) -> Optional[str]:
        """Return winner symbol (X or O) if any, else None."""
        for line in WIN_LINES:
            symbols = [self.board[r][c] for r, c in line]
            if symbols[0] != EMPTY and all(s == symbols[0] for s in symbols):
                return symbols[0]
        return None

    def utility(self, perspective: str) -> int:
        """
        Utility from the perspective of 'perspective' (X or O).
        Convention: +1 win, -1 loss, 0 draw.
        Used by Minimax; we evaluate from the maximizer's view (AI = O).
        """
        winner = self._has_winner()
        if winner is None:
            return 0  # Draw
        if winner == perspective:
            return 1
        return -1

    def heuristic_eval(self, perspective: str) -> float:
        """
        Heuristic evaluation for non-terminal states (for depth-limited Minimax).
        Scores each line: 2 of perspective + 1 empty = strong; 1 of perspective + 2 empty = weak;
        same for opponent (negative). Returns value in [-1, 1] range.
        """
        score = 0.0
        opponent = PLAYER_O if perspective == PLAYER_X else PLAYER_X
        for line in WIN_LINES:
            cells = [self.board[r][c] for r, c in line]
            n_perspective = cells.count(perspective)
            n_opponent = cells.count(opponent)
            n_empty = cells.count(EMPTY)
            if n_opponent == 0:
                if n_perspective == 2 and n_empty == 1:
                    score += 0.5   # one move from win
                elif n_perspective == 1 and n_empty == 2:
                    score += 0.1   # potential
            if n_perspective == 0:
                if n_opponent == 2 and n_empty == 1:
                    score -= 0.5   # block opponent
                elif n_opponent == 1 and n_empty == 2:
                    score -= 0.1
        return max(-1.0, min(1.0, score))

    def result(self, action: Tuple[int, int]) -> "GameState":
        """
        Return new state after applying action (row, col) for current player.
        Does not modify self.
        """
        r, c = action
        if self.board[r][c] != EMPTY:
            raise ValueError(f"Invalid action: cell ({r},{c}) is not empty")
        new_board = deepcopy(self.board)
        new_board[r][c] = self.current_player
        next_player = self.get_opponent()
        return GameState(board=new_board, current_player=next_player)

    def display(self) -> str:
        """String representation of the board for CLI display."""
        lines = []
        for r in range(BOARD_SIZE):
            row_str = " | ".join(self.board[r])
            lines.append(row_str)
            if r < BOARD_SIZE - 1:
                lines.append("-" * (BOARD_SIZE * 4 - 3))
        return "\n".join(lines)
