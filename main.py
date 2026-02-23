"""
Human–Agent Interaction - Tic-Tac-Toe with Minimax AI

- Command-line interface for playing against the AI.
- Validates human input.
- Displays game state after each move.
- Detects and reports win, loss, or draw.
- Optional: choose starting player; show nodes expanded (performance metric).
"""

import sys
from typing import Optional, Tuple
from game import GameState, PLAYER_X, PLAYER_O
from minimax import MinimaxAgent


def parse_move(s: str) -> Optional[Tuple[int, int]]:
    """
    Parse human input. Accept formats: "1 1", "1,1", "0 0" (0-indexed).
    Returns (row, col) or None if invalid.
    """
    s = s.strip().replace(",", " ")
    parts = s.split()
    if len(parts) != 2:
        return None
    try:
        r, c = int(parts[0]), int(parts[1])
        if 0 <= r <= 2 and 0 <= c <= 2:
            return (r, c)
    except ValueError:
        pass
    return None


def get_human_move(state: GameState) -> Tuple[int, int]:
    """Prompt until valid move; return (row, col)."""
    legal = state.get_legal_actions()
    while True:
        inp = input("Your move (row col, 0-2, e.g. 1 1): ").strip()
        if inp.lower() in ("quit", "q", "exit"):
            sys.exit(0)
        move = parse_move(inp)
        if move is not None and move in legal:
            return move
        print("Invalid move. Enter two numbers 0-2 (row and column), e.g. 0 0 or 1 2.")


def run_game(
    human_plays_x: bool = True,
    use_alpha_beta: bool = True,
    show_metrics: bool = True,
    max_depth: Optional[int] = None,
) -> None:
    """
    Run one game. Human is X if human_plays_x else O.
    max_depth: None = full depth; integer = depth-limited with heuristic.
    """
    state = GameState()
    agent = MinimaxAgent(use_alpha_beta=use_alpha_beta, max_depth=max_depth)
    human_symbol = PLAYER_X if human_plays_x else PLAYER_O
    ai_symbol = PLAYER_O if human_plays_x else PLAYER_X

    depth_info = f" (depth limit: {max_depth}, heuristic)" if max_depth is not None else " (full depth)"
    print("\n--- Tic-Tac-Toe (You vs Minimax AI)" + depth_info + " ---")
    print("Cells are (row, col) with indices 0, 1, 2.")
    print(state.display())
    print()

    while not state.is_terminal():
        if state.current_player == human_symbol:
            move = get_human_move(state)
        else:
            move = agent.get_action(state, ai_symbol)
            if move is None:
                break
            if show_metrics:
                print(f"  [AI expanded {agent.get_nodes_expanded()} nodes]")
            print(f"AI plays: {move[0]} {move[1]}")

        state = state.result(move)
        print()
        print(state.display())
        print()

    # Game over - report outcome
    winner = state._has_winner()
    if winner is None:
        print("Result: Draw.")
    elif winner == human_symbol:
        print("Result: You win!")
    else:
        print("Result: AI wins.")


def main() -> None:
    print("Minimax Tic-Tac-Toe Agent")
    print("You play as X, AI plays as O. Moves are (row col) with indices 0, 1, 2.")
    choice = input("Do you want to play first? (y/n, default y): ").strip().lower() or "y"
    human_first = choice != "n"
    use_ab = True
    show_metrics = True
    max_depth: Optional[int] = None
    depth_choice = input("Use depth-limited search with heuristic? (y/n, default n): ").strip().lower() or "n"
    if depth_choice == "y":
        while True:
            try:
                d = input("Max search depth (3–8, e.g. 4): ").strip() or "4"
                max_depth = int(d)
                if 3 <= max_depth <= 8:
                    break
                print("Enter a number between 3 and 8.")
            except ValueError:
                print("Enter a valid number.")
    run_game(human_plays_x=human_first, use_alpha_beta=use_ab, show_metrics=show_metrics, max_depth=max_depth)


if __name__ == "__main__":
    main()
