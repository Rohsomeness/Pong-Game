from turtle import Screen
from paddle import Paddle
from ball import Ball
import time
from scoreboard import ScoreBoard
import pong_ai

# GUI Definition
screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Pong Game")
screen.tracer(0)
SCREEN_DIM = {'width': 800, 'height': 600}

# Game setup
l_paddle = Paddle((-350, 0))
r_paddle = Paddle((350, 0))
DIFFICULTY = 1.2
ball = Ball(difficulty=DIFFICULTY)
scoreboard = ScoreBoard()

# AI setup
R_PADDLE_AI = pong_ai.DeltaAgent(paddle=l_paddle)
L_PADDLE_AI = pong_ai.BallAgent(paddle=r_paddle)
agents = []

# Human setup
screen.listen()
if R_PADDLE_AI is None:
    screen.onkey(r_paddle.go_up, "Up")
    screen.onkey(r_paddle.go_down, "Down")
else:
    agents.append(R_PADDLE_AI)
if L_PADDLE_AI is None:
    screen.onkey(l_paddle.go_up, "w")
    screen.onkey(l_paddle.go_down, "s")
else:
    agents.append(L_PADDLE_AI)

is_game_on = True

def perform_agent_action(agent, state):
    action = agent.choose_action(state)
    if action == pong_ai.Action.UP:
        agent.paddle.go_up()
    elif action == pong_ai.Action.DOWN:
        agent.paddle.go_down()

while is_game_on:

    for agent in agents:
        state = pong_ai.State(ball, other_paddle=r_paddle if agent.paddle == l_paddle else l_paddle, screen_dim=SCREEN_DIM)
        perform_agent_action(agent, state)

    time.sleep(1/100)
    screen.update()
    ball.move()

    # detect collision with wall
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # detect collision with paddle
    if ball.distance(r_paddle) < 50 and ball.xcor() > 320 and ball.x_move > 0 or ball.distance(l_paddle) < 50 and ball.xcor() < -320 and ball.x_move < 0:
        ball.bounce_x()

    # r paddle ball misses
    if ball.xcor() > 380:
        ball.reset_position()
        l_paddle.goto(-350, 0)
        r_paddle.goto(350, 0)
        scoreboard.l_point()

    # detect l_paddle ball misses
    if ball.xcor() < -380:
        ball.reset_position()
        l_paddle.goto(-350, 0)
        r_paddle.goto(350, 0)
        scoreboard.r_point()

screen.exitonclick()
