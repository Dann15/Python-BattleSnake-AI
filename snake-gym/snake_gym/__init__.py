from gym.envs.registration import register
from snake_gym.envs.snake_env import SnakeEnv

register(
    id='snake-v0',
    entry_point='snake_gym.envs:SnakeEnv'
)