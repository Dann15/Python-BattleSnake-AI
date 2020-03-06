import random as rand

jeff_did_not_kill_himself = True


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
    def __init__(self, board_size, starting_apples=5, seed, starting_length=3):
        self.board = Board(board_size)  # creates a square board of side length board_size
	self.seed = seed # sets all random values based on a seed
	self.apples_spawned = 0
	rand.seed(self.seed)
	starting_pos_x = rand.randint(7)
	rand.seed(self.seed*2)
	starting_pos_y = rand.randint(7)
        self.snake = Snake(starting_pos_x, starting_pos_y, starting_length)  # sets starting pos of the snake and
        # creates a snake instance
        self.turns = 0
        self.update_game()  # draws everything and increments turns, this is reset to zero later in init
        self.turns = 0  # resets to zero
        self.apple_list = []  # empty list to store apple coords in form [x,y]
        for apple in range(starting_apples):  # makes all the starting apples
            self.apple_list.append(self.add_apple())

    def add_apple(self):  # adds apple in a empty spot. all this does is return valid coords, so YOU have to append
        # that bad boy.
        while jeff_did_not_kill_himself:
	    rand.seed(self.seed+self.apples_spawned)
            poss_coords_x = rand.randint(0, self.board.size)
	    rand.seed((self.seed+self.apples_spawned)*2)
	    poss_coords_y = rand.randint(0, self.board.size)
	    self.apples_spawned += 1
            # generates random location in x, y
            if self.board.whats_here(poss_coords_x, poss_coords_y) == " ":
                self.board.change_cell(poss_coords_x, poss_coords_y, "A")
                return [poss_coords_x, poss_coords_y]

    def move_snake(self, command):
        reward = 1
        if self.is_hit_self(command):  # checks to see if snake committed via collision w self
            print("snake has big dumb and hit itself")
            return 0

        if self.is_hit_apple():  # checks apple collision
            self.snake.score += 1
            self.snake.length += 1
            reward += 1

        self.snake.move(command)

        if self.is_out_of_bounds():  # and finally wall collision
            print("dumbass went outta bounds")
            return 0
            
        self.render()
        self.update_game()  # this is where update is called every turn.
        return reward # live

    def is_hit_apple(self):  # does the snake hit an apple?
        return [self.snake.head.x, self.snake.head.y] in self.apple_list

    def is_hit_self(self, command):  # does the snake hit itself?
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

    def is_out_of_bounds(self):  # does the snake try to leave bounds?
        for snake_body_bit in self.snake.body_list:
            if snake_body_bit[0] > self.board.size or snake_body_bit[1] > self.board.size or snake_body_bit[0] < 0 or \
                    snake_body_bit[1] < 0:
                return True

    def update_game(self):  # this draws everything and increments turns by 1
        for row in self.board.grid:
            for cell in row:
                if self.board.whats_here(cell.x, cell.y) == "#":
                    self.board.change_cell(cell.x, cell.y, " ")
                if [cell.x, cell.y] in self.snake.body_list:
                    self.board.change_cell(cell.x, cell.y, "#")
        self.turns += 1

    def __repr__(self):  # creates a string representation of the board called on print(), more or less toString()
        return str(self.board)


class Snake:
    def __init__(self, head_x: int, head_y: int, length: int):
        self.length = length
        self.head = Cell(head_x, head_y, "#")  # head
        self.body_list = [[head_x, head_y]]  # list of all the body bits of our snake
        self.last_command = "U"  # last command, defaults to Up until first command is entered
        self.score = 0  # score, yet to be touched

    def move(self, command: chr):
        if command in ["U", "D", "L", "R"]:  # checking valid command
            self.head.shift(command)  # moves head.
            self.body_list.insert(0, [self.head.x, self.head.y])
            if self.length >= len(self.body_list):  # checks to see if apple has been eaten by seeing if length should
                # be longer than it is.
                pass
            else:  # if no apple eaten, we kill off the tail so it remains the same size.
                self.body_list.pop()
            self.last_command = command
        else:
            self.head.shift(self.last_command)  # default if invalid command entered

    def __repr__(self):
        for cell in self.body_list:
            print(cell, end=", ")


class Board:
    def __init__(self, size: int):
        self.grid = [[Cell(i, j, " ") for i in range(size + 1)] for j in range(size + 1)]  # creates a 2d array via
        # python magic
        self.size = size

    def change_cell(self, old_x: int, old_y: int, new_content: chr):  # changes whats inside a given cell
        self.grid[old_x][old_y].contents = new_content

    def whats_here(self, x, y):  # returns whats in this cell.
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

    def shift(self, command):  # do not look too closely, the numbers actually make no sense, but it works to move a
        # cell.
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


#main()
