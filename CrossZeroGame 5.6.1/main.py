# Функция рисует поле игры
def draw_field(matrix):
    print("   1 2 3")
    print(" a", *matrix[0], "\n", "b", *matrix[1], "\n", "c", *matrix[2])
    return False


# Проверка на конец игры
def continue_the_game(matrix):
    def who_on(field):
        if field == "X":
            print("\n", "PC wins")
        else:
            print("\n", "Player wins")

    for element in matrix:
        if element[0] == element[1] == element[2] != "#":
            who_on(element[0])
            return False

    for i in range(3):
        if matrix[0][i] == matrix[1][i] == matrix[2][i] != "#":
            who_on(matrix[0][i])
            return False

    # это диоганали
    if matrix[0][0] == matrix[1][1] == matrix[2][2] != "#":
        who_on(matrix[0][0])
        return False

    if matrix[0][2] == matrix[1][1] == matrix[2][0] != "#":
        who_on(matrix[0][2])
        return False

    for i in range(3):
        for j in range(3):
            if matrix[i][j] == "#":
                return True

    print("\n", "Game draw")
    return True


# Функция обрабатывающая ход игрока
def player_action(matrix):
    str_move = input("Lead your move ")
    i = "#"
    j = "#"

    if len(str_move) > 2:
        print("Enter the correct move")
        return True

    if str_move[0].upper() == "A":
        j = 0
    elif str_move[0].upper() == "B":
        j = 1
    elif str_move[0].upper() == "C":
        j = 2

    if int(str_move[1]) <= 3:
        i = int(str_move[1]) - 1

    if i == "#" or j == "#":
        print("Enter the correct move")
        return True

    if matrix[j][i] == "#":
        matrix[j][i] = "O"
    else:
        print("The field is busy")
        return True

    return False


# Функция хода компа
def pc_action(matrix):
    # Это блок хода противника если он почти собрал столбец
    for i in range(3):
        length_row = ''.join(matrix[i]).count("O")
        if length_row == 2:
            for j in range(3):
                if matrix[i][j] == "#":
                    matrix[i][j] = "X"
                    return True
    # Это блок хода противника если он почти собрал строку
    for j in range(3):
        length_row = str(matrix[0][j] + matrix[1][j] + matrix[2][j]).count("O")
        if length_row == 2:
            for i in range(3):
                if matrix[i][j] == "#":
                    matrix[i][j] = "X"
                    return True
    # Это блок хода противника если он почти собрал диагональ
    length_row = str(matrix[0][0] + matrix[1][1] + matrix[2][2]).count("O")
    if length_row == 2:
        for i, j in zip(range(3), range(3)):
            if matrix[i][j] == "#":
                matrix[i][j] = "X"
                return True
    # Это блок хода противника если он почти собрал обратная диагональ
    length_row = str(matrix[0][2] + matrix[1][1] + matrix[2][0]).count("O")
    if length_row == 2:
        for i, j in zip(range(2, -1, -1), range(0, 3, 1)):
            if matrix[i][j] == "#":
                matrix[i][j] = "X"
                return True

    # Если не блокируем ход соперника то делаем свой в свободные линии
    # Стараемся занять свободную линию
    for i in range(3):
        length_row = ''.join(matrix[i]).count("#")
        if length_row == 3:
            for j in range(3):
                if matrix[i][j] == "#":
                    matrix[i][j] = "X"
                    return True

    for j in range(3):
        length_row = str(matrix[0][j] + matrix[1][j] + matrix[2][j]).count("#")
        if length_row == 2:
            for i in range(3):
                if matrix[i][j] == "#":
                    matrix[i][j] = "X"
                    return True

    length_row = str(matrix[0][0] + matrix[1][1] + matrix[2][2]).count("#")
    if length_row == 3:
        for i, j in zip(range(3), range(3)):
            if matrix[i][j] == "#":
                matrix[i][j] = "X"
                return True

    length_row = str(matrix[0][2] + matrix[1][1] + matrix[2][0]).count("#")
    if length_row == 3:
        for i, j in zip(range(2, -1, -1), range(0, 3, 1)):
            if matrix[i][j] == "#":
                matrix[i][j] = "X"
                return True

    # Пытаеся занять просто свободное пространство
    for i in range(3):
        for j in range(3):
            if matrix[i][j] == "#":
                matrix[i][j] = "X"
                return True
    return False


matrix_Cross_Zero = (["#", "#", "#"], ["#", "#", "#"], ["#", "#", "#"])

draw_field(matrix_Cross_Zero)

while continue_the_game(matrix_Cross_Zero):
    while player_action(matrix_Cross_Zero):
        pass
    pc_action(matrix_Cross_Zero)
    print("\n" * 2, "Current round")
    draw_field(matrix_Cross_Zero)
