from turtle import Turtle


class Paddle(Turtle):
    def __init__(self, position: tuple[int, int], color: str) -> None:
        super().__init__()
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_wid=6, stretch_len=2)
        self.penup()
        self.goto(position)

    def move_up(self) -> None:
        if self.ycor() < 250:
            self.sety(self.ycor() + 20)

    def move_down(self) -> None:
        if self.ycor() > -240:
            self.sety(self.ycor() - 20)
