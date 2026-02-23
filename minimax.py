"""
Minimax Algorithm Implementation

- Recursive Minimax with clear max/min player distinction.
- Terminal states evaluated via game utility function.
- Optional: Alpha-Beta pruning, depth-limited search with heuristic, node metrics.
"""

from typing import Tuple, Optional
from game import GameState, PLAYER_X, PLAYER_O


class MinimaxAgent:
    """
    Agent that selects actions using the Minimax decision rule.
    Assumes the opponent plays optimally (minimizing player).
    Supports Alpha-Beta pruning and optional depth limit with heuristic evaluation.
    """

    def __init__(
        self,
        use_alpha_beta: bool = True,
        max_depth: Optional[int] = None,
    ):
        self.use_alpha_beta = use_alpha_beta
        self.max_depth = max_depth  # None = search to terminal (full depth)
        self.nodes_expanded = 0

    def get_action(self, state: GameState, maximizing_player: str) -> Optional[Tuple[int, int]]:
        """
        Return best action for the current player (maximizing_player)
        from the given state. Uses Minimax (with optional alpha-beta and depth limit).
        """
        self.nodes_expanded = 0
        legal = state.get_legal_actions()
        if not legal:
            return None

        best_value = float("-inf")
        best_action = None
        depth = 0

        for action in legal:
            successor = state.result(action)
            if self.use_alpha_beta:
                value = self._minimax_alpha_beta(
                    successor, maximizing_player, float("-inf"), float("inf"), False, depth + 1
                )
            else:
                value = self._minimax(successor, maximizing_player, False, depth + 1)
            if value > best_value:
                best_value = value
                best_action = action
        return best_action

    def _eval(self, state: GameState, maximizing_player: str) -> float:
        """Terminal: utility; non-terminal at depth limit: heuristic."""
        if state.is_terminal():
            return float(state.utility(maximizing_player))
        return state.heuristic_eval(maximizing_player)

    def _minimax(
        self,
        state: GameState,
        maximizing_player: str,
        is_max_turn: bool,
        depth: int = 0,
    ) -> float:
        """
        Recursive Minimax. Optional depth limit with heuristic at cutoff.
        """
        self.nodes_expanded += 1
        if state.is_terminal() or (self.max_depth is not None and depth >= self.max_depth):
            return self._eval(state, maximizing_player)

        legal = state.get_legal_actions()
        if is_max_turn:
            value = float("-inf")
            for action in legal:
                successor = state.result(action)
                value = max(value, self._minimax(successor, maximizing_player, False, depth + 1))
            return value
        else:
            value = float("inf")
            for action in legal:
                successor = state.result(action)
                value = min(value, self._minimax(successor, maximizing_player, True, depth + 1))
            return value

    def _minimax_alpha_beta(
        self,
        state: GameState,
        maximizing_player: str,
        alpha: float,
        beta: float,
        is_max_turn: bool,
        depth: int = 0,
    ) -> float:
        """
        Minimax with Alpha-Beta pruning. Optional depth limit with heuristic at cutoff.
        """
        self.nodes_expanded += 1
        if state.is_terminal() or (self.max_depth is not None and depth >= self.max_depth):
            return self._eval(state, maximizing_player)

        legal = state.get_legal_actions()
        if is_max_turn:
            value = float("-inf")
            for action in legal:
                successor = state.result(action)
                value = max(
                    value,
                    self._minimax_alpha_beta(
                        successor, maximizing_player, alpha, beta, False, depth + 1
                    ),
                )
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value
        else:
            value = float("inf")
            for action in legal:
                successor = state.result(action)
                value = min(
                    value,
                    self._minimax_alpha_beta(
                        successor, maximizing_player, alpha, beta, True, depth + 1
                    ),
                )
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    def get_nodes_expanded(self) -> int:
        """Return number of nodes expanded in the last get_action call."""
        return self.nodes_expanded
