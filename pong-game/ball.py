from turtle import Turtle


class Ball(Turtle):
    def __init__(self, color: str, speed: int) -> None:
        super().__init__()
        self.color(color)
        self.shape("circle")
        self.speed(speed)
        self.penup()
        self.goto(0, 0)
        self.dx = 5
        self.dy = -5

    def move(self) -> None:
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)

    def bounce_y(self) -> None:
        self.dy *= -1

    def bounce_x(self) -> None:
        self.dx *= -1

    def reset_position(self) -> None:
        self.goto(0, 0)
        self.bounce_x()
