from random import randint


# region классы корабля

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o > 0:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


# endregion

# region классы исключений

class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "координаты за пределами поля"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    pass


# endregion

# region игровое поле


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):
        res = ""
        res += "   | 1 | 2 | 3 | 4 | 5 | 6 |"
        alf = ["a", "b", "c", "d", "e", "f", "g"]
        for i, row in enumerate(self.field):
            res += f"\n {alf[i]} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "T"
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []


# endregion

# region классы игрока


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class PlayerPC:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        luck_shot = None
        offset = 0
        while True:
            try:
                # Имеет смысл пальнуть рядом если было попадание
                if luck_shot != None:
                    target = luck_shot
                    if offset == 0: target.x = target.x + 1
                    if offset == 1: target.y = target.x + 1
                    repeat = self.enemy.shot(target)
                    if repeat:
                        luck_shot = target
                    else:
                        if offset == 0: offset = 1
                        if offset == 1:
                            luck_shot = None
                            offset = 0

                target = self.ask()
                repeat = self.enemy.shot(target)
                if repeat: luck_shot = target
                return repeat
            except BoardException as e:
                print(e)


class AI(PlayerPC):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()
            x = transform_the_cordinate(cords[0][0])

            if len(cords[0]) != 2:
                print(" Кординаты не корректны ")
                continue

            if not cords[0][1].isdigit():
                print(" Кординаты не корректны ")
                continue

            y = int(cords[0][1]) - 1

            if len(cords) != 1:
                print(" Кординаты не корректны ")
                continue

            return Dot(x, y)


# endregion

# region функции
def pc_board(size=6):
    board = None
    while board is None:

        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size)
        attempts = 0
        for i in lens:
            while True:
                # На тот случай если не удаётся ни какими силами создать расстановку кораблей
                #  создаём её в ручную.
                attempts += 1
                if attempts > 2000:
                    board = None
                    board = Board(size)

                    ship = Ship(Dot(2, 2), 3, 1)
                    board.add_ship(ship)

                    ship = Ship(Dot(0, 0), 2, 0)
                    board.add_ship(ship)

                    ship = Ship(Dot(4, 0), 2, 0)
                    board.add_ship(ship)

                    ship = Ship(Dot(5, 2), 1, 0)
                    board.add_ship(ship)

                    ship = Ship(Dot(5, 4), 1, 0)
                    board.add_ship(ship)

                    ship = Ship(Dot(0, 5), 1, 0)
                    board.add_ship(ship)

                    ship = Ship(Dot(0, 2), 1, 0)
                    board.add_ship(ship)

                    board.begin()
                    return board

                ship = Ship(Dot(randint(0, size), randint(0, size)), i, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board


def us_board(size=6):
    board = None
    while board is None:

        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size)
        attempts = 0
        print("Введите координаты корабля и его направление. B и его поворот")
        print("Например a1 0 где 0 - вертикаль а 1 - горизонталь")
        print("Коробли можно ставит между собой только через клетку")
        for i in lens:
            board.hid = False
            print(board)
            while True:
                str_coordinates = input(" Корабль " + str(i) + " палубы: ").split()
                # print("\n"*15)
                coordinates = [transform_the_cordinate(str_coordinates[0][0]), str_coordinates[0][1],
                               str_coordinates[1]]
                coordinates = list(map(int, coordinates))
                ship = Ship(Dot(coordinates[0], coordinates[1] - 1), i, coordinates[2])
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board


def transform_the_cordinate(simbol):
    if simbol.lower() == "a": return 0
    if simbol.lower() == "b": return 1
    if simbol.lower() == "c": return 2
    if simbol.lower() == "d": return 3
    if simbol.lower() == "e": return 4
    if simbol.lower() == "f": return 5
    if simbol.lower() == "g": return 6
    return 100


# endregion

print("----------------------------------------------------------------------------")
print("                                морской бой                                 ")
print("----------------------------------------------------------------------------")

pc = pc_board()
pl = pc_board()
# pl = us_board()

pc.hid = True
pl.hid = False

ai = AI(pc, pl)
us = User(pl, pc)

num = 0

while True:
    print("_" * 75)
    print("Доска пользователя:")
    print(us.board)
    print("_" * 75)
    print("Доска компьютера:")
    print(ai.board)

    while True:
        print("_" * 75)
        print("Ходит пользователь!")
        repeat = us.move()
        if not repeat: break

    while True:
        print("_" * 75)
        print("Ходит компьютер!")
        repeat = ai.move()
        if not repeat: break

    if ai.board.count == 7:
        print("_" * 75)
        print("Пользователь выиграл!")
        break

    if us.board.count == 7:
        print("_" * 20)
        print("Компьютер выиграл!")
        break
    num += 1
