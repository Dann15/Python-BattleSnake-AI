import random as rand


# marcus i will literally pay you to annotate your code
# if this code works perfectly then i guess we're fine

jeff_did_not_kill_himself = True


@TODO  # add apples respawning in accordance with the algorythm in thier source code.
def main():
    print("starting")
    game = Game(board_size=7, starting_apples=5, starting_pos_x=3, starting_pos_y=3, starting_length=3)
    print(game)
    game.move_snake("R")
    print(game)
    game.move_snake("R")
    print(game)
    game.move_snake("R")
    print(game)
    game.move_snake("R")
    print(game)
    game.move_snake("R")
    print(game)
    game.move_snake("R")
    print(game)
    print("finished")


class Game:
    def __init__(self, board_size, starting_apples=5, starting_pos_x=3, starting_pos_y=3, starting_length=3):
        self.board = Board(board_size)
        self.snake = Snake(starting_pos_x, starting_pos_y, starting_length)
        self.update_game()
        self.apple_list = []
        self.turns = 0
        for apple in range(starting_apples):
            self.apple_list.append(self.add_apple())

    def add_apple(self):
        while jeff_did_not_kill_himself:
            poss_coords_x, poss_coords_y = rand.randint(0, self.board.size), rand.randint(0, self.board.size)
            if self.board.whats_here(poss_coords_x, poss_coords_y) == " ":
                self.board.change_cell(poss_coords_x, poss_coords_y, "A")
                return [poss_coords_x, poss_coords_y]

    def move_snake(self, command):
        if self.is_hit_self(command):
            print("snake has big dumb and hit itself")
            exit(420)
        if self.is_hit_apple():
            self.snake.score += 1
            self.snake.length += 1
        self.snake.move(command)
        if self.is_out_of_bounds():
            print("dumbass went outta bounds")
            exit(69)
        self.update_game()

    def is_hit_apple(self):
        return [self.snake.head.x, self.snake.head.y] in self.apple_list

    def is_hit_self(self, command):
        x, y = self.snake.head.x, self.snake.head.y
        if command not in ["U", "D", "L", "R"]:
            command = self.snake.last_command
        if command == "U":
            x -= 1
        elif command == "D":
            x += 1
        elif command == "L":
            y -= 1
        elif command == "R":
            y += 1
        return [x, y] in self.snake.body_list

    def is_out_of_bounds(self):
        for snake_body_bit in self.snake.body_list:
            if snake_body_bit[0] > self.board.size or snake_body_bit[1] > self.board.size or snake_body_bit[0] < 0 or \
                    snake_body_bit[1] < 0:
                return True

    def update_game(self):
        for row in self.board.grid:
            for cell in row:
                if self.board.whats_here(cell.x, cell.y) == "#":
                    self.board.change_cell(cell.x, cell.y, " ")
                if [cell.x, cell.y] in self.snake.body_list:
                    self.board.change_cell(cell.x, cell.y, "#")
        self.turns += 1

    def __repr__(self):
        return str(self.board)


class Snake:
    def __init__(self, head_x: int, head_y: int, length: int):
        self.length = length
        self.head = Cell(head_x, head_y, "#")
        self.body_list = [[head_x, head_y]]
        self.last_command = "U"
        self.score = 0

    def move(self, command: chr):
        if command in ["U", "D", "L", "R"]:  # checking valid command
            self.head.shift(command)
            self.body_list.insert(0, [self.head.x, self.head.y])
            if self.length >= len(self.body_list):
                pass
            else:
                self.body_list.pop()
            self.last_command = command
        else:
            self.head.shift(self.last_command)

    def __repr__(self):
        for cell in self.body:
            print(cell, end=", ")


class Board:
    def __init__(self, size: int):
        self.grid = [[Cell(i, j, " ") for i in range(size + 1)] for j in range(size + 1)]
        self.size = size

    def change_cell(self, old_x: int, old_y: int, new_content: chr):
        self.grid[old_x][old_y].contents = new_content

    def whats_here(self, x, y):
        return self.grid[x][y].contents

    def __repr__(self):
        string = " " + " =" * (self.size - 2) + "\n"
        for row in self.grid:
            string += "| "
            for cell in row:
                string += cell.contents
            string += " |\n"
        string += " " + " =" * (self.size - 2)
        return string


class Cell:
    def __init__(self, x, y, contents: chr):
        self.x = x
        self.y = y
        self.contents = contents

    def shift(self, command):
        if command == "U":
            self.x -= 1
        if command == "D":
            self.x += 1
        if command == "L":
            self.y -= 1
        if command == "R":
            self.y += 1

    def __repr__(self):
        return self.contents


if __name__ == "__main__":
    main()
