import gym
from battlesnake import Game
from gym import spaces, error, utils
from gym.utils import seeding

class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
    POINT_ON_APPLE = 5
    POINT_ON_SURVIVE = 1
    POINT_ON_DEATH = -50
    POINT_ON_WIN = 0
    MAX_TURNS = int(1e+10)

    # TODO make a seed generation thing for starting position
    # Seed generation would involve randomly placing the snake AND apples


    def __init__(self):
        super(SnakeEnv, self).__init__()
        self.game = Game(board_size=7, starting_apples=5, starting_pos_x=3, starting_pos_y=3, starting_length=3)
        self.state = game.board.grid
        self.counter = 0
        self.action_space = spaces.Discrete(4)
        self.done = 0
        self.add = UP # by default snake starts moving up
        self.reward = 0

    def step(self, action):
        result = self.game.move_snake(action)
        self.state = self.game.grid
        self.counter += 1
        self.render()

        if result == 0: # snake dies
            self.reward += POINT_ON_DEATH
            self.done = 1
        elif result == 2: # snake got an apple
            self.reward += POINT_ON_APPLE+POINT_ON_SURVIVE
        elif result == 1: # snake is still alive, no apple
            self.reward += POINT_ON_SURVIVE
            
        if self.counter >= MAX_TURNS: # win
            self.done = 1
            self.reward += POINT_ON_WIN
    
        return [self.state, self.reward, self.done, self.add]




    def reset(self):
        self.__init__()
        return self.state
    
    def render(self, mode="human", close=False):
        print(self.game)