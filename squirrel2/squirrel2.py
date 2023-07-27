import math
import random
import time
from bookmoves import is_book

BOARD_SIZE = 8

EMPTY = 0
BLACK = 1
WHITE = 2

DIRECTIONS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


def init_board():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board[3][3] = WHITE
    board[4][4] = WHITE
    board[3][4] = BLACK
    board[4][3] = BLACK
    return board


def print_board(board):
    print("   ", end="")
    for i in range(BOARD_SIZE):
        print(chr(ord('a') + i), end=" ")
    print()
    print("  +" + "-" * (2 * BOARD_SIZE - 1) + "+")
    for i in range(BOARD_SIZE):
        print(str(i + 1).rjust(2) + "|", end="")
        for j in range(BOARD_SIZE):
            if board[i][j] == EMPTY:
                print(".", end=" ")
            elif board[i][j] == BLACK:
                print("X", end=" ")
            else:
                print("O", end=" ")
        print("|" + str(i + 1).ljust(2))
    print("  +" + "-" * (2 * BOARD_SIZE - 1) + "+")
    print("   ", end="")
    for i in range(BOARD_SIZE):
        print(chr(ord('a') + i), end=" ")
    print()


def get_valid_moves(board, player):
    valid_moves = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if is_valid_move(board, player, (i, j)):
                valid_moves.append((i, j))
    return valid_moves


def is_valid_move(board, player, move):
    if board[move[0]][move[1]] != EMPTY:
        return False
    for direction in DIRECTIONS:
        x, y = move[0] + direction[0], move[1] + direction[1]
        if x < 0 or x >= BOARD_SIZE or y < 0 or y >= BOARD_SIZE or board[x][y] == EMPTY or board[x][y] == player:
            continue
        while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == 3 - player:
            x += direction[0]
            y += direction[1]
            if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == player:
                return True
    return False


def make_move(board, player, move):
    new_board = [row[:] for row in board]
    new_board[move[0]][move[1]] = player
    for direction in DIRECTIONS:
        x, y = move[0] + direction[0], move[1] + direction[1]
        if x < 0 or x >= BOARD_SIZE or y < 0 or y >= BOARD_SIZE or new_board[x][y] == EMPTY or new_board[x][
                y] == player:
            continue
        while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and new_board[x][y] == 3 - player:
            x += direction[0]
            y += direction[1]
            if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and new_board[x][y] == player:
                while x != move[0] + direction[0] or y != move[1] + direction[1]:
                    x -= direction[0]
                    y -= direction[1]
                    new_board[x][y] = player
                break
    return new_board


def f(x):
    return math.sqrt(-x + BOARD_SIZE ** 2) / (2 * math.sqrt(2))


fx = [i for i in range(BOARD_SIZE ** 2 + 1)]
fy = [f(x) for x in fx]
f_table = {x: y for x, y in zip(fx, fy)}


def h(x):
    return 1 - (BOARD_SIZE ** 2 * 3 / 16) / ((x - (BOARD_SIZE ** 2 * 3 / 8)) ** 2 + (BOARD_SIZE ** 2 * 3 / 4))


hx = [i for i in range(BOARD_SIZE ** 2 + 1)]
hy = [h(x) for x in hx]
h_table = {x: y for x, y in zip(hx, hy)}


def m(x):
    if x >= 48:
        return 0
    elif x < 41:
        return 2 * ((-x + BOARD_SIZE ** 2 * 0.625) ** (1/3) + 2)
    else:
        return 2 * (-abs(-x + BOARD_SIZE ** 2 * 0.625) ** (1/3) + 2)


mx = [i for i in range(BOARD_SIZE ** 2 + 1)]
my = [m(x) for x in mx]
m_table = {x: y for x, y in zip(mx, my)}


def mobility(board, player):
    mob = len(get_valid_moves(board, player)) - len(get_valid_moves(board, 3 - player))
    return mob


def snail(array, sig):
    out = []
    while len(array):
        out += array.pop(0)
        for i in range(2 * sig + 1):
            array = list(zip(*array))[::-1]
    return out


def stable_discs(board, player):
    discs = 0
    conner = [(0, 0), (0, BOARD_SIZE - 1), (BOARD_SIZE - 1, 0), (BOARD_SIZE - 1, BOARD_SIZE - 1)]
    if board[conner[0][0]][conner[0][1]] != player and board[conner[1][0]][conner[1][1]] != player and board[conner[2][0]][conner[2][1]] != player and board[conner[3][0]][conner[3][1]] != player:
        return 0
    stable = [[3 for _ in range(BOARD_SIZE + 2)] for _ in range(BOARD_SIZE + 2)]
    new_board = [[3 for _ in range(BOARD_SIZE + 2)] for _ in range(BOARD_SIZE + 2)]
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            new_board[i + 1][j + 1] = board[i][j]
            stable[i + 1][j + 1] = 0
    for k in range(2):
        coor = snail([[(i + 1, j + 1) for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)], k)
        for i in coor:
            if stable[i[0]][i[1]] == player:
                continue
            elif new_board[i[0]][i[1]] == player:
                if (stable[i[0] - 1][i[1] - 1] == 3 or stable[i[0] + 1][i[1] + 1] == 3 or stable[i[0] - 1][i[1] - 1] == player or stable[i[0] + 1][i[1] + 1] == player)\
                        and (stable[i[0] + 1][i[1] - 1] == 3 or stable[i[0] - 1][i[1] + 1] == 3 or stable[i[0] + 1][i[1] - 1] == player or stable[i[0] - 1][i[1] + 1] == player)\
                        and (stable[i[0]][i[1] - 1] == 3 or stable[i[0]][i[1] + 1] == 3 or stable[i[0]][i[1] - 1] == player or stable[i[0]][i[1] + 1] == player)\
                        and (stable[i[0] + 1][i[1]] == 3 or stable[i[0] - 1][i[1]] == 3 or stable[i[0] + 1][i[1]] == player or stable[i[0] - 1][i[1]] == player):
                    stable[i[0]][i[1]] = player
                    discs += 1
    return discs


def move_ordering(board, player, r):
    scored_moves = []
    valid_moves = get_valid_moves(board, player)
    for move in valid_moves:
        new_board = make_move(board, player, move)
        score = evaluate(new_board, player)
        scored_moves.append((move, score))
    random.shuffle(scored_moves)
    scored_moves.sort(key=lambda x: -x[1])
    ordered_moves = [move for move, _ in scored_moves]
    if len(ordered_moves) > 4:
        del ordered_moves[round(len(ordered_moves) * r):]
    return ordered_moves


def evaluate(board, player):
    score = 0
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == player:
                score += 1
            elif board[i][j] == 3 - player:
                score -= 1

    conner = [(0, 0), (0, BOARD_SIZE - 1), (BOARD_SIZE - 1, 0), (BOARD_SIZE - 1, BOARD_SIZE - 1)]
    x_sq = [(1, 1), (1, BOARD_SIZE - 2), (BOARD_SIZE - 2, 1), (BOARD_SIZE - 2, BOARD_SIZE - 2)]
    c_sq = [(0, 1), (1, 0), (0, BOARD_SIZE - 2), (1, BOARD_SIZE - 1), (BOARD_SIZE - 1, 1), (BOARD_SIZE - 2, 0), (BOARD_SIZE - 1, BOARD_SIZE - 2), (BOARD_SIZE - 2, BOARD_SIZE - 1)]
    for i in range(len(conner)):
        if board[conner[i][0]][conner[i][1]] == player:
            score += f_table[is_full(board)[1]] * 1.5
        elif board[conner[i][0]][conner[i][1]] == 3 - player:
            score -= f_table[is_full(board)[1]] * 1.5
        else:
            continue
        conner[i] = 0

    for i in range(len(x_sq)):
        if conner[i] != 0:
            if board[x_sq[i][0]][x_sq[i][1]] == player:
                score -= f_table[is_full(board)[1]] * 2.6
            elif board[x_sq[i][0]][x_sq[i][1]] == 3 - player:
                score += f_table[is_full(board)[1]] * 2.6

    for i in range(len(c_sq)):
        if conner[round(i / 2 - 0.5)] != 0:
            if board[c_sq[i][0]][c_sq[i][1]] == player:
                score -= f_table[is_full(board)[1]] * 1.5
            elif board[c_sq[i][0]][c_sq[i][1]] == 3 - player:
                score += f_table[is_full(board)[1]] * 1.5

    score += mobility(board, player) * m_table[is_full(board)[1]]
    score += f_table[is_full(board)[1]] * stable_discs(board, player) * 8
    score -= f_table[is_full(board)[1]] * stable_discs(board, 3 - player) * 8

    return score


def is_end(board):
    if len(get_valid_moves(board, 1)) == 0 and len(get_valid_moves(board, 2)) == 0:
        return True
    else:
        return False


def is_full(board):
    m, n = len(board), len(board[0])
    count = 0
    for i in range(m):
        for j in range(n):
            if board[i][j] != 0:
                count += 1
    return count == m * n, count


def minimax(board, player, depth, alpha, beta, max_player, op, full):
    if depth == 0:
        return evaluate(board, op), None
    if full:
        ordered_moves_1 = get_valid_moves(board, player)
        ordered_moves_2 = get_valid_moves(board, player)
    else:
        ordered_moves_1 = move_ordering(board, player, 0.8)
        ordered_moves_2 = move_ordering(board, player, h_table[is_full(board)[1]])
    if not ordered_moves_1:
        return minimax(board, 3 - player, depth - 1, alpha, beta, max_player, op, full)
    if max_player:
        max_score = float("-inf")
        best_move = None
        for move in ordered_moves_1:
            new_board = make_move(board, player, move)
            score, _ = minimax(new_board, 3 - player, depth - 1, alpha, beta, max_player=False, op=op, full=full)
            if score > max_score:
                max_score = score
                best_move = move
            alpha = max(alpha, max_score)
            if alpha >= beta:
                break
        return max_score, best_move
    else:
        min_score = float("inf")
        best_move = None
        for move in ordered_moves_2:
            new_board = make_move(board, player, move)
            score, _ = minimax(new_board, 3 - player, depth - 1, alpha, beta, max_player=True, op=op, full=full)
            if score < min_score:
                min_score = score
                best_move = move
            beta = min(beta, min_score)
            if alpha >= beta:
                break
        return min_score, best_move


def ai_move(board, player, depth, moves):
    start = time.time()
    if is_book(moves) and BOARD_SIZE == 8:
        score, move = "book", is_book(moves)
    elif BOARD_SIZE ** 2 - len(moves) / 2 < 17:
        score, move = minimax(board, player, 17, alpha=float("-inf"), beta=float("inf"), max_player=True, op=player, full=True)
        score = round(score, 2)
    else:
        valid_moves = get_valid_moves(board, player)
        if len(valid_moves) == 1:
            score, move = None, valid_moves[0]
        else:
            score, move = minimax(board, player, depth, alpha=float("-inf"), beta=float("inf"), max_player=True, op=player, full=False)
            score = round(score, 2)
    return move, time.time() - start, score


def game_loop(w, l, d, black, white, depth):
    board = init_board()
    current_player = BLACK
    black_time = 0
    white_time = 0
    moves = ""
    while True:
        print_board(board)
        valid_moves = get_valid_moves(board, current_player)
        t = time.time()
        if is_end(board):
            print_board(board)
            black_score = sum(row.count(BLACK) for row in board)
            white_score = sum(row.count(WHITE) for row in board)
            if black_score == white_score:
                print("Game over. It's a tie.")
                d += 1
            elif black_score > white_score:
                print("Game over. Player BLACK wins with score {}:{}.".format(black_score, white_score))
                w += 1
            else:
                print("Game over. Player WHITE wins with score {}:{}.".format(white_score, black_score))
                l += 1
            break
        if not valid_moves and not is_end(board):
            print("Player {} has no valid move. Pass.".format(current_player))
            current_player = 3 - current_player
            continue
        if current_player == BLACK:
            if black:
                coordinate = input(f"Player BLACK's turn. Enter coordinate (a1-h8): ")
                row = int(coordinate[1].format(BOARD_SIZE))
                col = ord(coordinate[0].format(chr(ord('a') + BOARD_SIZE - 1))) - ord('a')
                move = (row - 1, col)
                t = time.time() - t
            else:
                move, t, score = ai_move(board, current_player, depth, moves)
                print(f"Current score: {score}")
                print("BLACK chooses move {}.".format(chr(move[1] + ord('a')) + str(move[0] + 1)))
            print("BLACK used {} seconds to think.".format(round(t, 2)))
            black_time += t
        else:
            if white:
                coordinate = input(f"Player WHITE's turn. Enter coordinate (a1-h8): ")
                row = int(coordinate[1].format(BOARD_SIZE))
                col = ord(coordinate[0].format(chr(ord('a') + BOARD_SIZE - 1))) - ord('a')
                move = (row - 1, col)
                t = time.time() - t
            else:
                move, t, score = ai_move(board, current_player, depth, moves)
                print(f"Current score: {score}")
                print("WHITE chooses move {}.".format(chr(move[1] + ord('a')) + str(move[0] + 1)))
            print("WHITE used {} seconds to think.".format(round(t, 2)))
            white_time += t
        if 0 > move[0] or move[0] > 7 or 0 > move[1] or move[1] > 7:
            print("Invalid move. Please try again.")
            continue
        elif not is_valid_move(board, current_player, move):
            print("Invalid move. Please try again.")
            continue
        board = make_move(board, current_player, move)
        current_player = 3 - current_player
        if not valid_moves and not is_end(board):
            print("Player {} has no valid move. Pass.".format(current_player))
            current_player = 3 - current_player
            continue
        moves += f"{chr(move[1] + 97)}{str(move[0] + 1)}"
        if is_end(board):
            print_board(board)
            black_score = sum(row.count(BLACK) for row in board)
            white_score = sum(row.count(WHITE) for row in board)
            if black_score == white_score:
                print("Game over. It's a tie.")
                d += 1
            elif black_score > white_score:
                print("Game over. Player BLACK wins with score {}:{}.".format(black_score, white_score))
                w += 1
            else:
                print("Game over. Player WHITE wins with score {}:{}.".format(white_score, black_score))
                l += 1
            break
    print(f"WHITE: {round(white_time, 2)}\nBLACK: {round(black_time, 2)}")
    print("Transcript:", moves)
    return w, l, d


win, lose, draw = 0, 0, 0
while True:
    b = input("Black: player/com (p/c)\n").lower()
    w = input("White: player/com (p/c)\n").lower()
    d = int(input("Depth: (7 is standard, higher depth means stronger but thinks longer.)\n"))
    if b == "p":
        b = True
    else:
        b = False
    if w == "p":
        w = True
    else:
        w = False
    win, lose, draw = game_loop(win, lose, draw, b, w, d)
    print(f"Black:{win}, White:{lose}, Draw:{draw}")
