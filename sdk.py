def column(x):
    column = []
    for i in board:
        column.append(i[x])

    return column


def box(x, y):
    global board
    square = []
    for yy in range(3):
        for xx in range(3):
            square.append(board[yy + y // 3 * 3][xx + x // 3 * 3])

    return square


print("Type in your sodoku. Like so:\n" +
      "    1 0 0 0 0 0 0 0 0\n" +
      "    0 2 0 0 0 0 0 0 0\n" +
      "    0 0 3 0 0 0 0 0 0\n" +
      "    0 0 0 0 0 4 0 0 0\n" +
      "    0 0 0 0 5 0 0 0 0\n" +
      "    0 0 0 6 0 0 0 0 0\n" +
      "    0 0 0 0 0 0 7 0 0\n" +
      "    0 0 0 0 0 0 0 8 0\n" +
      "    0 0 0 0 0 0 0 0 9\n")

board = []
for i in range(9):
    board.append(input(">>>    ").split(' '))

# Seid ihr das Essen? Nein, wir sind der Jäger!
# to stop and edit
blank = 0
past = []
for y in range(9):
    for x in range(9):
        board[y][x] = int(board[y][x])
        if not board[y][x]:
            board[y][x] = []
            blank += 1

shadow = 82
while blank:
    # empty method
    for y in range(9):
        for x in range(9):
            lone = []
            if isinstance(board[y][x], list):
                # possibilities
                board[y][x] = []
                for n in range(1, 10):
                    # conditions
                    if n not in board[y] and n not in column(x) and n not in box(x, y):
                        board[y][x].append(n)

                # only one option
                if len(board[y][x]) == 1:
                    board[y][x] = board[y][x][0]
                    blank -= 1

                # bad guess
                elif len(board[y][x]) == 0:
                    while True:
                        if past[-1][3] + 1 < past[-1][4]:
                            # matrix shit
                            chuugoku = []
                            for i in past[-1][0]:
                                chuugoku.append(i[:])

                            board = chuugoku
                            blank = past[-1][5]
                            past[-1][3] += 1

                            # stroke
                            (board[past[-1][1]]
                                  [past[-1][2]]) = (board[past[-1][1]]
                                                         [past[-1][2]]
                                                         [past[-1][3]])
                            break

                        else:
                            past.pop(-1)

    if blank == shadow:
        # number method
        for i in range(9):
            for n in range(1, 10):
                form = i % 3 * 3
                ula = i // 3 * 3
                for c in range(3):
                    circuits = [board[i], column(i), box(form, ula)]
                    if n not in circuits[c]:
                        lone = []
                        for j in range(9):
                            if isinstance(circuits[c][j], list):
                                if n in circuits[c][j]:
                                    lone.append(j)

                        # only one option
                        if len(lone) == 1:
                            if circuits[c] == board[i]:
                                board[i][lone[0]] = n

                            elif circuits[c] == column(i):
                                board[lone[0]][i] = n

                            else:
                                (board[ula + lone[0] // 3]
                                      [form + lone[0] % 3]) = n

                            blank -= 1

        if blank == shadow:
            # find first uncertainty
            for y in range(9):
                for x in range(9):
                    if isinstance(board[y][x], list):
                        blank -= 1

                        # copies matrix
                        chuugoku =[]
                        for i in board:
                            chuugoku.append(i[:])

                        past.append([chuugoku, y, x, 0, len(chuugoku[y][x]), blank])
                        board[y][x] = board[y][x][0]
                        stop = True
                        break

                if stop:
                    stop = False
                    break

    shadow = blank

print("\nHere you go:")
for y in range(9):
    for x in range(9):
        if not x:
            print()
        print(board[y][x], end=' ')
