from random import shuffle

with open("../book.sq2", "r") as f:
    lines = f.readlines()
    book = []
    for i in lines:
        book.append(i[:-1])
bad_white_book = ["c4c5d6c3e6f5c6", "c4c5d6c3e6f4e3", "c4c5d6c3e6d7c6", "c4c5d6c7d7c3e6", "c4c5d6e7d7c3e6", "c4c5d6e3c6b5e6", "c4e3f5c6c5", "c4e3f6b4f3g7e6", "c4e3f6b4f3e6d3", "c4e3f6c5c3", "c4e3f6c6e6c5c3e7f5", "c4e3f6c6e6b4c3", "c4e3f6c6e6e7f5g5d3", "c4e3f6c6e6e7f5b4d6c5d7", "c4e3f5e6f6g6f3c5d3f4g4", "c4c3d3e3f4c5c6d6b4b6c2a3f6", "c4c3d3c5d6e3f3f4d2f2b3c1f6", "c4c3d3c5b4e3d2d1e2c2b5", "c4c3d3e3d2c5b4a4b5b3e2", "e6f6f5d6c5e3d3f4f3e2g4g5f2h3f1e1d7"]
bad_black_book = ["c4c3f5b4d3e3", "c4c3e6b4d3e3", "c4c3c2c5c6b5a6e3", "c4e3f4c5d6f3e6c3d3e2", "c4e3f3c5d3b4", "c4e3f3c5e6d6c6f4", "c4e3f2c6e6f3f4d3", "c4c3d3c5f6e2c2d2", "c4c3d3c5f6e2b2c2", "c4c3d3c5b5d2c2b3", "c4c3d3c5b6e3", "c4c3d3e3f6b5b3b4", "c4c3d3e3f6b5b2b3", "c4c3d3e3e2b4b3c2", "c4c3d3e3f2c5", "c4e3f4c5e6d6b5b4", "c4e3f4c5d6f3e2d3c3e6", "c4e3f4c5d6f3e6c3d3e2d2e1f2c2", "c4e3f4c5d6f3d3c3b5f5g5b6", "c4e3f2c6e6f3f4f5"]


def coord(alg):
    return int(alg[1]) - 1, 'abcdefgh'.index(alg[0])


def lst_to_alg(s):
    return [f"{s[i]}{s[i + 1]}" for i in range(0, len(s), 2)]


def to_alg(c):
    return chr(c[1] + 97) + str(c[0] + 1)


def flip(opening):
    opening = [coord(lst_to_alg(opening)[i]) for i in range(len(opening) // 2)]
    dia_flip = lambda x: (x[1], x[0])
    turn_flip = lambda x: (7 - x[0], 7 - x[1])
    o1 = ''.join([to_alg(dia_flip(opening[i])) for i in range(len(opening))])
    o2 = ''.join([to_alg(turn_flip(opening[i])) for i in range(len(opening))])
    o3 = ''.join([to_alg(turn_flip(dia_flip(opening[i]))) for i in range(len(opening))])
    return o1, o2, o3


full_book = book.copy()
for i in range(len(book)):
    o1, o2, o3 = flip(book[i])
    full_book.append(o1)
    full_book.append(o2)
    full_book.append(o3)
full_bad_white_book = bad_white_book.copy()
for i in range(len(bad_white_book)):
    o1, o2, o3 = flip(bad_white_book[i])
    full_bad_white_book.append(o1)
    full_bad_white_book.append(o2)
    full_bad_white_book.append(o3)
full_bad_black_book = bad_black_book.copy()
for i in range(len(bad_black_book)):
    o1, o2, o3 = flip(bad_black_book[i])
    full_bad_black_book.append(o1)
    full_bad_black_book.append(o2)
    full_bad_black_book.append(o3)


def is_book(moves):
    satisfy = []
    for k in full_book:
        if k.startswith(moves) and k != moves:
            satisfy.append(k)
    if satisfy:
        shuffle(satisfy)
        return coord(satisfy[0][len(moves):len(moves)+2])
    if (len(moves) / 2) % 2 == 0:
        for k in full_bad_white_book:
            if k.startswith(moves) and k != moves:
                satisfy.append(k)
        if satisfy:
            shuffle(satisfy)
            return coord(satisfy[0][len(moves):len(moves)+2])
    else:
        for k in full_bad_black_book:
            if k.startswith(moves) and k != moves:
                satisfy.append(k)
        if satisfy:
            shuffle(satisfy)
            return coord(satisfy[0][len(moves):len(moves)+2])
    if not satisfy:
        return False
