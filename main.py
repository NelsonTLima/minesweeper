from random import randint
from os import system

class Matrix(list):
    def __init__(self, rows, columns):
        self.rows, self.columns = rows, columns
        for column in range(rows):
            self.append([' ' for i in range(columns)])

    def in_bounds(self, row, column):
        if row >= 0 and row < self.rows and column >= 0 and column < self.columns:
            return True
        return False

    def place_mines(self, odds):
        for row in range(len(self)):
            for element in range(len(self[row])):
                if randint(0, 99) > odds:
                    has_mine = '0'
                else:
                    has_mine = ' '
                self[row][element] = has_mine
        return self

    def set_numbers(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if self[row][column] == '0':
                    mine_count = Matrix.count_mines(self, row, column)
                    self[row][column] = str(mine_count)
        return self

    def count_mines(self, row, column):
        mine_count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.in_bounds(row + i, column + j) and self[row + i][column + j] == ' ':
                    mine_count +=1
        return mine_count

class Game():
    def __init__(self, difficulty):
        match difficulty:
            case 1:
                self.columns = 9
                self.rows = 9
                self.odds = 10
            case 2:
                self.columns = 16
                self.rows = 16
                self.odds = 15
            case 3:
                self.columns = 30
                self.rows = 16
                self.odds = 20

        self.user_matrix = Matrix(self.rows, self.columns)
        self.hidden_matrix = Matrix(self.rows, self.columns).place_mines(self.odds).set_numbers()
        self.status = 'running'

    def update(self, row, column):
        revelation = self.reveal(row, column)

        if self.user_matrix == self.hidden_matrix:
            self.status = "\n\033[35mYou Won!\033[0m"
        elif revelation == ' ':
            self.reveal_all_mines()
            self.status = '\n\033[31mGame over\033[0m'
        else:
            self.status = 'running'

        Interface.render(self)

    def reveal(self, row, column):
        if not self.user_matrix.in_bounds(row, column):
            return

        if self.hidden_matrix[row][column] != '0':
            self.user_matrix[row][column] = self.hidden_matrix[row][column]

        if self.user_matrix[row][column] == ' ' and self.hidden_matrix[row][column] != ' ':
            self.user_matrix[row][column] = '0'
            for i in range(-1,2):
                for j in range(-1,2):
                    self.reveal(row + i, column + j)

        return self.hidden_matrix[row][column]

    def reveal_all_mines(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if self.hidden_matrix[row][column] == ' ':
                    self.user_matrix[row][column] = 'x'

class Interface():
    def colorize(string):
        match string:
            case '0':
                return f"\033[37m{string}\033[0m" # white
            case '1':
                return f"\033[36m{string}\033[0m" #Cyan
            case '2':
                return f"\033[34m{string}\033[0m" #Blue
            case '3':
                return f"\033[33m{string}\033[0m" #Yellow
            case 'x':
                return f"\033[31m{string}\033[0m" # Red
            case _:
                return f"\033[35m{string}\033[0m" #magenta
        return cell

    def render(game):
        system('clear')
        print('Type "exit" to select another difficulty.\n')

        interface = f"  \\ "
        for i in range(game.columns):
            interface += f"\033[32m{i!s:^3}\033[0m|"

        for i in range(game.rows):
            interface += f"\n\033[32m{i!s:^3}\033[0m|"

            for j in range(game.columns):
                interface += f" {Interface.colorize(game.user_matrix[i][j])} |"
        print(interface)

class Player():
    def choose_difficulty():
        while True:
            difficulty = input('Type "exit" to exit.\n\n1 - Easy\n2 - Medium\n3 - Hard\n-> ')
            if difficulty == 'exit':
                break
            elif difficulty not in ['1', '2', '3']:
                system('clear')
                print('\033[31mInvalid difficulty\033[0m')
                continue
            else:
                return int(difficulty)

    def choose_axis(game):
        while True:
            row_index = input('\nChoose row index: ')
            if row_index == 'exit':
                return 'exit', 'exit'

            if row_index not in [str(i) for i in range(game.rows)]:
                system('clear')
                Interface.render(game)
                print('\033[31mInvalid index\033[0m')
                continue

            else:
                row_index = int(row_index)

            column_index = input('Choose column index: ')
            if column_index == 'exit':
                return 'exit', 'exit'

            if column_index not in [str(i) for i in range(game.columns)]:
                system('clear')
                Interface.render(game)
                print('\033[31mInvalid index\033[0m')
            else:
                return int(row_index), int(column_index)


        return row_index, column_index

while __name__ == '__main__':

    difficulty = Player.choose_difficulty()
    if difficulty == None:
        break

    game = Game(difficulty)
    Interface.render(game)
    while True:
        row_index, column_index = Player.choose_axis(game)
        if row_index == 'exit' or column_index == 'exit':
            break
        game.update(row_index, column_index)
        print(game.status)
        if game.status != 'running':
            break
