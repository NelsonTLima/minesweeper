from random import randint
from os import system

class Ansi:
    def red(string):
        return "\033[31m" + string + "\033[0m"

    def green(string):
        return "\033[32m" + string + "\033[0m"

    def yellow(string):
        return "\033[33m" + string + "\033[0m"

    def blue(string):
        return f"\033[34m{string}\033[0m"

    def magenta(string):
        return f"\033[35m{string}\033[0m"

    def cyan(string):
        return f"\033[36m{string}\033[0m"

    def white(string):
        return f"\033[37m{string}\033[0m"

class Game():
    def __init__(self, difficulty):
        match difficulty:
            case 1:
                self.row_length = 9
                self.column_length = 9
                self.mine_odds = 10
            case 2:
                self.row_length = 16
                self.column_length = 16
                self.mine_odds = 15
            case 3:
                self.row_length = 30
                self.column_length = 16
                self.mine_odds = 20

    def in_bounds(self, row, column):
        if row >= 0 and row < self.column_length and column >= 0 and column < self.row_length:
            return True
        return False

    def build(self):
        # 9 means the cell has a mine.
        # 0-8 will be the number of mines nearby.
        self.field_matrix = []
        self.user_matrix = []
        for row in range(self.column_length):
            field_row = []
            user_row = []
            for column in range(self.row_length):
                if randint(0,99) > self.mine_odds:
                    has_mine = '0'
                else:
                    has_mine = '9'
                field_row.append(has_mine)
                user_row.append(' ')
            self.user_matrix.append(user_row)
            self.field_matrix.append(field_row)

    def set_numbers(self):
        for row in range(self.column_length):
            for column in range(self.row_length):
                mine_count = Game.count_mines(self, row, column)
                if self.field_matrix[row][column] != '9':
                    self.field_matrix[row][column] = str(mine_count)

    def count_mines(self, row, column):
        mine_count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if Game.in_bounds(self, row + i, column + j) and self.field_matrix[row + i][column + j] == '9':
                    mine_count +=1
        return mine_count


    def reveal(self, row, column):
        if not Game.in_bounds(self, row, column):
            return
        if self.field_matrix[row][column] != '0':
            self.user_matrix[row][column] = self.field_matrix[row][column]

        if self.user_matrix[row][column] == ' ':
            self.user_matrix[row][column] = '0'
            for i in range(-1,2):
                for j in range(-1,2):
                    self.reveal(row + i, column + j)

        return self.field_matrix[row][column]

    def colorize(string):
        match string:
            case ' ':
                cell = ' '
            case '0':
                cell = Ansi.cyan(string)
            case '1':
                cell = Ansi.blue(string)
            case '2':
                cell = Ansi.magenta(string)
            case '9':
                cell = Ansi.red('x')
            case _:
                cell = Ansi.yellow(string)
        return cell


    def render_user_interface(self):
        first_row = f"  \\ "
        for i in range(self.row_length):
            first_row += f" {Ansi.green(str(i))} |"

        for i in range(self.column_length):
            if i > 9:
                first_row += f"\n{Ansi.green(str(i))} |"
            else:
                first_row += f"\n{Ansi.green(str(i))}  |"

            for j in range(self.row_length):
                if j > 9:
                    first_row += f" {Game.colorize(self.user_matrix[i][j])}  |"
                else:
                    first_row += f" {Game.colorize(self.user_matrix[i][j])} |"

        print(first_row)

    def reveal_mines(self):
        for row in range(self.column_length):
            for column in range(self.row_length):
                if self.field_matrix[row][column] == '9':
                    self.reveal(row, column)

def main():
    difficulty = int(input("1 - Easy\n2 - Medium\n3 - Hard\n-> "))
    game = Game(difficulty)
    game.build()
    game.set_numbers()

    reveal = ''
    while reveal != '9':
        system('clear')
        game.render_user_interface()
        x, y = input("\n(x y): ").split()
        x, y = int(x), int(y)
        reveal = game.reveal(x, y)
    game.reveal_mines()
    print("\n\033[31mGame over\033[0m\nAll mines:\n")
    game.render_user_interface()



if __name__ == '__main__':
    main()
