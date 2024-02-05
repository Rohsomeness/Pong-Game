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
FREQUENCY = 1/100

# Game setup
l_paddle = Paddle((-350, 0))
r_paddle = Paddle((350, 0))
DIFFICULTY = 1.2
ball = Ball(difficulty=DIFFICULTY)
scoreboard = ScoreBoard()

def perform_agent_action(agent, state):
    action = agent.choose_action(state)
    if action == pong_ai.Action.UP:
        agent.paddle.go_up()
    elif action == pong_ai.Action.DOWN:
        agent.paddle.go_down()

def play_game(l_paddle_agent, r_paddle_agent, num_games=5, end_score=3, store_output='output/game_results.txt'):

    # Player/AI setup
    agents = []
    screen.listen()
    if r_paddle_agent is None:
        screen.onkey(r_paddle.go_up, "Up")
        screen.onkey(r_paddle.go_down, "Down")
        r_paddle.speed = 40
    else:
        agents.append(r_paddle_agent)
    if l_paddle_agent is None:
        screen.onkey(l_paddle.go_up, "w")
        screen.onkey(l_paddle.go_down, "s")
        l_paddle.speed = 40
    else:
        agents.append(l_paddle_agent)

    wins = [0, 0]
    names = []
    for agent in [l_paddle_agent, r_paddle_agent]:
        try:
            names.append(agent.name)
        except:
            names.append("Human")

    with open(store_output, 'a') as f:
        f.write(f'==========Game Results for {names[0]} vs {names[1]}==========\n')

    for game in range(num_games):

        while scoreboard.l_score < end_score and scoreboard.r_score < end_score:
            for agent in agents:
                state = pong_ai.State(ball, other_paddle=r_paddle if agent.paddle == l_paddle else l_paddle, screen_dim=SCREEN_DIM)
                perform_agent_action(agent, state)

            time.sleep(FREQUENCY)
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

        if scoreboard.l_score > scoreboard.r_score:
            wins[0] += 1
        else:
            wins[1] += 1

        with open(store_output, 'a') as f:
            f.write(f'Game {game + 1} Results: {scoreboard.l_score} - {scoreboard.r_score}\n')
        
        scoreboard.reset()

    with open(store_output, 'a') as f:
        for name, win in zip(names, wins):
            f.write(f'{name} Wins: {win}\n')

    screen.bye()

play_game(pong_ai.DeltaAgent(paddle=l_paddle), None, num_games = 3)
