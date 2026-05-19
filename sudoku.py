import numpy as np
from pycsp3 import *
from myCSP.mycsp import *
from board import Board
from refresher import *

class Layout:
    """
    Represents a Sudoku puzzle layout and provides methods to solve it using different CSP algorithms.

    This class reads a Sudoku layout from a file, initializes the puzzle grid, and provides solving functions
    using both PyCSP and a our csp solver, mycsp (YAY!!!). The solutions enforce constraints such as row,
    column, and 3x3 block uniqueness, and allow for various heuristic optimizations.

    Attributes:
        clues (list[list[int]]): A 9x9 grid representing the initial Sudoku puzzle state.
    """
    def __init__(self, path):
        """Initializes the Sudoku layout by reading a file and parsing the puzzle grid."""
        with open(path, "r") as file:
            text = file.read()
            words = text.split()
            numbers = []
            for w in words:
                if w == "_":
                    numbers.append(0)
                else:
                    numbers.append(int(w))

        self.clues = np.reshape(numbers, (9, 9)).tolist()

    def get_clues(self):
        """Returns the initial Sudoku clues."""
        return self.clues

    def pycsp_solve(self, board: Board) -> bool:
        """
        Solves the Sudoku puzzle using the PyCSP3 solver.
        Returns True if a solution is found, False otherwise.
        """
        clear()

        try:
            x = VarArray(size=[9, 9], dom=range(1, 10))

            block_constraints = [
                AllDifferent(x[i:i + 3, j:j + 3])
                for i in [0, 3, 6] for j in [0, 3, 6]
            ]

            clue_constraints = [
                x[i][j] == board.layout_board[i][j]
                for i in range(9) for j in range(9)
                if board.layout_board[i][j] > 0
            ]

            satisfy(
                AllDifferent(x, matrix=True),
                block_constraints,
                clue_constraints
            )

            if solve() is SAT:
                board.answer_board = values(x)
                return True

        except Exception as e:
            print("Error in pycsp_solve:", e)

        return False

    def mycsp_solve(self,
                    board: Board,
                    do_unary_check: bool,
                    do_arc_consistency: bool,
                    do_mrv: bool,
                    do_lcv: bool,
                    real_time: bool,
                    refresh: Callable[[],None],
                    get_stop_event: Callable[[], bool]) -> bool:
        """
        Solves the Sudoku puzzle using our csp solver (mycsp) with various heuristics.
        Returns True if solution found, False otherwise.
        """
        # YOUR CODE
        my_clear()

        variables = myVarArray(name="mycsp", size=[9, 9], dom=range(1, 10))
        refresher = Refresher(variables, board, real_time, refresh, get_stop_event)

        column_constraints = []
        for j in range(9):
            column = [variables[i, j] for i in range(9)]
            column_constraints.append(myAllDifferent(column))

        clue_constraints = []
        for i in range(9):
            for j in range(9):
                if board.layout_board[i][j] != 0:
                    clue_constraints.append(myUnaryConstraint(variables[i, j], board.layout_board[i][j], "="))

        row_constraints = []
        for i in range(9):
            row = [variables[i, j] for j in range(9)]
            row_constraints.append(myAllDifferent(row))

        block_constraints = []

        for start_row_index in range(0, 9, 3):
            for start_column_index in range(0, 9, 3):
                block = []
                for row in range(3):
                    for column in range(3):
                        block.append(variables[start_row_index + row, start_column_index + column])
                block_constraints.append(myAllDifferent(block))

        all_constraints = row_constraints + column_constraints + block_constraints + clue_constraints
        my_satisfy(*all_constraints)

        is_successful = my_solve(do_unary_check, do_arc_consistency, do_mrv, do_lcv, refresher)

        if is_successful:
            board.answer_board = [[variables[i, j].value for j in range(9)] for i in range(9)]
            return True

        return False



    def solve(self,
              algorithm: str,
              do_unary_check: bool,
              do_arc_consistency: bool,
              do_mrv: bool,
              do_lcv: bool,
              real_time: bool,
              board: Board,
              refresh: Callable[[],bool],
              get_stop_event: Callable[[], bool]):
        """Solves the Sudoku puzzle using the selected CSP algorithm."""
        # print(f"the algorithm is {algorithm} *****")
        if algorithm == 'pycsp':
            return self.pycsp_solve(board)
        else:
            return self.mycsp_solve(board, do_unary_check,
                                    do_arc_consistency,
                                    do_mrv,
                                    do_lcv,
                                    real_time,
                                    refresh,
                                    get_stop_event)