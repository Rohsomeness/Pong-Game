# Code a Q learning agent to play the pong game
import random
import numpy as np
from enum import Enum

# Define the statespace as position of ball and paddles
class State():
    def __init__(self, ball, other_paddle, screen_dim):
        self.ball = ball
        self.other_paddle = other_paddle
        self.screen_dim = screen_dim


# Let's first start off with making an agent that moves up and down randomly
class Action(Enum):
    UP = 0
    DOWN = 1
    NOOP = 2

class Agent():
    '''
    Dumb agent that chooses randomly
    Here, we don't care about position of ball or paddle
    '''
    name = "Random Agent"

    def __init__(self, paddle):
        self.action_space = Action
        self.paddle = paddle

    def choose_action(self, state: State):
        return random.choice(list(self.action_space))
    
class BallAgent(Agent):
    '''
    This agent only uses the direction of the ball to move it's paddle
    '''
    name = "Ball Agent"

    def choose_action(self, state: State):
        if state.ball.y_move > 0:
            return Action.UP
        elif state.ball.y_move < 0:
            return Action.DOWN
        else:
            return Action.NOOP
    
# Now, an agent that moves up or down based on the height of the ball compared to the paddle
class DeltaAgent(Agent):
    '''
    Delta agent
    This agent cares about position of ball and it's own paddle
    '''
    name = "Delta Agent"

    def choose_action(self, state):
        if state.ball.ycor() > self.paddle.ycor():
            return Action.UP
        elif state.ball.ycor() < self.paddle.ycor():
            return Action.DOWN
        else:
            return Action.NOOP
    



