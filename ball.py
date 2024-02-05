from turtle import Turtle
import random

class Ball(Turtle):
    def __init__(self, difficulty):
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.speed("slow")
        self.penup()
        self.x_move = 5
        self.y_move = 5
        self.difficulty = difficulty

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1 * self.difficulty
        self.y_move *= self.difficulty

    def reset_position(self):
        self.goto(0, 0)
        self.x_move = 5 * random.choice([1, -1])
        self.y_move = 5
