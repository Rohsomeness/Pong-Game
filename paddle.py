from turtle import Turtle


class Paddle(Turtle):
    def __init__(self, position, speed=5):
        super().__init__()
        self.color("white")
        self.shape("square")
        self.penup()
        self.turtlesize(stretch_wid=5, stretch_len=1)
        self.goto(position)
        self.speed = speed

    def go_up(self):
        new_y = self.ycor() + self.speed
        self.goto(self.xcor(), new_y)

    def go_down(self):
        new_y = self.ycor() - self.speed
        self.goto(self.xcor(), new_y)
