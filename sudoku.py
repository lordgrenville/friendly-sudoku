import numpy as np
from itertools import product

board = np.array(
    [
        [9, 1, 7, 0, 0, 6, 8, 4, 0],
        [2, 0, 0, 8, 0, 4, 7, 0, 0],
        [8, 0, 5, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 7, 4, 2, 8],
        [0, 0, 0, 3, 0, 2, 0, 0, 0],
        [7, 2, 9, 4, 0, 0, 0, 5, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 4],
        [0, 0, 1, 9, 0, 5, 0, 0, 6],
        [0, 6, 8, 7, 0, 0, 5, 3, 9],
    ]
)


def _get_block(row, col):
    """Get the numbers in the block of a given square"""
    r, c = row // 3 * 3, col // 3 * 3
    return board[r : r + 3, c : c + 3]


def get_options(row, col) -> set:
    """Take in a square and say what it can legally be"""
    square = _get_block(row, col).flatten()
    existing = set(board[row]) | set(board[:, col]) | set(square)
    return set(range(1, 10)) - existing


def get_missing_elements(unit) -> set:
    """Take in a unit (row/column/block) and say what it is missing"""
    return set(range(10)) - set(x[0] for x in unit)


def check_squares():
    """Go through square by square and solve squares with only one solution"""
    for row, col in product(range(9), range(9)):
        if board[row, col] == 0:
            solution = get_options(row, col)
            if len(solution) == 1:
                print(f"{row}, {col} must be {solution}")
                board[row, col] = solution.pop()


def fix_unit(unit) -> bool:
    """Take in a unit and calculate candidates for each blank square. Then see if there is one candidate that only
    one square can have, and if so fill it in. Returns true if a change was made and these should be regenerated"""
    if 0 not in [x[0] for x in unit]:
        return False
    candidates_dict = {i: get_options(x, y) for i, (val, (x, y)) in enumerate(unit) if val == 0}
    if len(candidates_dict) == 1:
        ((k, answer),) = candidates_dict.items()
        print(candidates_dict)
        print(f"{answer} is the only option at {unit[k][1]}, adding it")
        board[unit[k][1]] = answer.pop()
        return True
    for k, v in candidates_dict.items():
        other_candidate_opts = set.union(*[v_ for k_, v_ in candidates_dict.items() if k_ != k])
        if len(v.difference(other_candidate_opts)) == 1:
            answer = v.difference(other_candidate_opts).pop()
            print(f"{answer} is the only option at {unit[k][1]}, adding it")
            board[unit[k][1]] = answer
            return True
    return False


def get_units(board):
    rows = [list(zip(board[x], [(x, n) for n in range(9)])) for x in range(9)]
    cols = [list(zip(board.T[x], [(n, x) for n in range(9)])) for x in range(9)]
    blocks = []
    for top_left_x in range(0, 9, 3):
        for top_left_y in range(0, 9, 3):
            blocks.append(
                list(
                    zip(
                        board[top_left_x : top_left_x + 3, top_left_y : top_left_y + 3].flatten(),
                        product(range(top_left_x, top_left_x + 3), range(top_left_y, top_left_y + 3)),
                    )
                )
            )
    return rows + cols + blocks


def _test_unit(unit):
    """Test a single unit is valid"""
    vals = [x[0] for x in unit]
    return len(vals) == len(set(vals))


def test_board(board):
    """Check that board is valid. It can be empty or full, but must be legal"""
    return all(map(_test_unit, get_units(board)))


make_board = lambda board_string: np.array([int(x) for x in list(board_string)]).reshape(9, 9)

if __name__ == "__main__":
    board = make_board("000020600079005000200469500000002030908000705060500000004916007000700480007040000")
    while 0 in board:
        check_squares()
        units = get_units(board)
        for unit in units:
            if fix_unit(unit):  # we have found a match, regenerate units
                break
