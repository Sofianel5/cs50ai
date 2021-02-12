"""
Tic Tac Toe Player
"""

import math
from operator import itemgetter
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    flat = [move for sublist in board for move in sublist]
    os = flat.count(O)
    xs = flat.count(X)
    return O if xs > os else X


def actions(board):
    actions = []
    for row in range(3):
        for col in range(3):
            if board[row][col] is EMPTY:
                actions.append((row,col))
    return actions


def result(board, action, inplace=True):
    if not inplace:
        board = copy.deepcopy(board)
    item = player(board)
    row,col = action 
    board[row][col] = item 
    return board

def winner(board):
    # check if fulfilled in a row
    for row in board:
        if row.count(row[0]) == len(row):
            if row[0] is not EMPTY:
                return row[0]
    
    # check if fulfilled in a column
    for i in range(3):
        if board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            if board[0][i] is not EMPTY:
                return board[0][i]
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] is not EMPTY:
                return board[0][0]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[0][2] is not EMPTY:
                return board[0][2]
    return None


def terminal(board):
    is_won = winner(board) is not None
    if is_won:
        return True 
    flat = [move for sublist in board for move in sublist]
    if flat.count(EMPTY) == 0:
        return True 
    return False


def utility(board):
    player_won = winner(board) 
    if player_won == X:
        return 1
    elif player_won == O:
        return -1 
    return 0

def max_value_of(board):
    if terminal(board):
        return utility(board)
    else:
        possibilities = [result(board,action,inplace=False) for action in actions(board)]
        values = []
        for possible_board in possibilities:
            values.append(max_value_of(possible_board))
        return max(values)

def min_value_of(board):
    if terminal(board):
        return utility(board)
    else:
        possibilities = [result(board,action,inplace=False) for action in actions(board)]
        values = []
        for possible_board in possibilities:
            values.append(max_value_of(possible_board))
        return min(values)

def minimax(board):
    local_board = copy.deepcopy(board)
    if terminal(local_board):
        return None
    qtablemax = {action: max_value_of(result(local_board,action,inplace=False)) for action in actions(board)}
    qtablemin = {action: min_value_of(result(local_board,action,inplace=False)) for action in actions(board)}
    current_player = player(board)
    if current_player is X:
        return max(qtablemax.items(), key = itemgetter(1))[0]
    else:
        return min(qtablemin.items(), key = itemgetter(1))[0]
        