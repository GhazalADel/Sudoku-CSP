# Sudoku CSP Solver

**Course**: Fundamentals and Applications of Artificial Intelligence — Spring 1404  
**University**: Amirkabir University of Technology  

## Overview

Solving Sudoku as a Constraint Satisfaction Problem (CSP) using two approaches: the `pycsp3` library and a custom-built `myCSP` library implemented from scratch.

## Implemented Components

**Part 1 — pycsp3**
- `solve_pycsp()` in `sudoku.py`: models and solves Sudoku using the pycsp3 library

**Part 2 — myCSP (custom library)**
- `node_consistency()` — unary constraint propagation
- `backtrack()` — backtracking search
- `arc_consistency()` + `revise()` — AC-3 algorithm
- `minimum_remaining_values()` — MRV heuristic
- `least_constraining_value()` — LCV heuristic
- `solve_mycsp()` in `sudoku.py`: wires everything together

## Modified Files

- `sudoku.py` — pycsp3 and myCSP solvers
- `myCSP/mycsp.py` — all CSP algorithm implementations

## Requirements

- Python 3.10+
- Java 11+ (required by pycsp3 solvers ACE/Choco)

```bash
pip install -r requirements.txt
python main.py
```

## Project Structure

```
├── myCSP/          # Custom CSP library
├── layouts/        # Sudoku puzzle files (.sudoku)
├── sudoku.py       # Sudoku problem definition & solvers
├── board.py        # Board state (layout, guess, answer, domains)
├── refresher.py    # Real-time UI update helper
└── main.py         # GUI entry point
```
