# Utility module for gomoku game.
import re


def in_board(x, y):
    """Check if the given position is in the board."""
    return (0 <= x < 15) and (0 <= y < 15)


def str_to_board(str):
    return [list(row) for row in str.split()]


def file_to_board(file):
    with open(file) as f:
        return [list(line.strip()) for line in f]


def diagonal_line(board, x, y, direction):
    """Return the board layout on a diagonal line.

    :param board: 2D array of board info.
    :param x: Starting x coordinate.
    :param y: Starting y coordinate.
    :param direction: Should be '\\' or '/'
    :return: A list containing board info along the given direction starting from (x, y)
    """
    l = []
    if direction == '\\':
        while in_board(x, y):
            l.append(board[x][y])
            x += 1
            y += 1
    elif direction == '/':
        while in_board(x, y):
            l.append(board[x][y])
            x -= 1
            y += 1
    else:
        raise Exception(r"direction should be either '/' or '\\'")
    return l


def scan_patterns(board, pattern_file):
    """Return a list of the occurrence of patterns.
    :param board: List representation of the board.
    :param pattern_file: The file to read the patterns.
    :return: A list of pattern occurrence corresponds to each pattern in the file.
    """
    with open(pattern_file) as file:
        patterns = [line.strip() for line in file]
    occurrence = [0] * len(patterns)

    lines = []
    # get horizontal lines
    lines += [''.join(raw) for raw in board]
    # get vertical lines
    lines += [''.join(raw) for raw in zip(*board)]
    # get '\' lines
    # we start from the first row then the first column
    for c in range(15):
        line = ''.join(diagonal_line(board, c, 0, '\\'))
        lines.append(line)
    for r in range(1, 15):
        line = ''.join(diagonal_line(board, 0, r, '\\'))
        lines.append(line)
    # get '/' lines
    # we start from the first row then the last column
    for c in range(15):
        line = ''.join(diagonal_line(board, c, 0, '/'))
        lines.append(line)
    for r in range(1, 15):
        line = ''.join(diagonal_line(board, 14, r, '/'))
        lines.append(line)

    for i, p in enumerate(patterns):
        for line in lines:
            if 'b' in p:
                _p = p.replace('.', '[^b]')
            elif 'w' in p:
                _p = p.replace('.', '[^w]')
            occurrence[i] += len(re.findall(r'(?=(%s))' % _p, line))

    return occurrence
