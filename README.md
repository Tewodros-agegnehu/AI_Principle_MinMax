# Adversarial Search – Minimax Tic-Tac-Toe Agent

A two-player Tic-Tac-Toe game where a human plays against an AI agent that uses the **Minimax algorithm** (with optional **Alpha-Beta pruning**) to choose optimal moves. The implementation satisfies the assignment requirements for adversarial search in a deterministic, turn-based, zero-sum, perfect-information game.

## Requirements

- **Python 3.8+** (no external libraries required; uses only the standard library)

## How to Run

### Graphical UI (recommended)

```bash
python gui.py
```

- Choose **You (X)** or **AI (O)** to pick who plays first.
- Click an empty cell to make your move. The AI responds automatically using Minimax.
- **New Game** restarts and lets you choose who goes first again.
- The winning line is highlighted in gold; nodes expanded are shown below the board.

### Command-line interface

```bash
python main.py
```

- When prompted, choose whether you play first (y/n).
- Enter moves as **row** and **column** (0–2), e.g. `1 1` for center.
- The game ends when there is a win or a draw; the result is printed in the terminal.

## Project Structure

| File        | Purpose |
|------------|---------|
| `game.py`  | Game representation: states, legal actions, terminal detection, utility function |
| `minimax.py` | Minimax algorithm (and Alpha-Beta pruning), AI agent |
| `main.py`  | Command-line interface, human–agent interaction, game loop |
| `gui.py`   | Graphical UI (Tkinter): click-to-play, choose first player, restart, metrics |

## Features

- **Game representation**: Formal state (`GameState`), legal actions, terminal states, utility (+1 / -1 / 0).
- **Minimax**: Recursive implementation with distinct maximizing and minimizing players; terminal states evaluated via the utility function.
- **Human–agent interaction**: CLI for valid human input and display of the board after each move.
- **Game termination**: Correct detection of win, loss, and draw with clear outcome messages.

### Optional (Bonus)

- **Alpha–Beta pruning**: Used by default to reduce the number of nodes expanded.
- **Starting player**: Option to let the human or the AI play first.
- **Performance metric**: Number of nodes expanded per AI move is printed when the AI plays.

## Compiling and Running (Summary)

- No compilation step; run with: `python main.py`
- Dependencies: none (standard library only)

## Author

Addis Ababa University – AI Assignment 2 (Adversarial Search – Minimax)
