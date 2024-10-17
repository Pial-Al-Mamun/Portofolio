from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):
    def __init__(self, color: str) -> None:
        super().__init__()
        self.color(color)
        self.penup()
        self.hideturtle()
        self.goto(0, 260)
        self.left_score = 0
        self.right_score = 0
        self.update_scoreboard()

    def update_scoreboard(self) -> None:
        self.clear()
        self.write(f"Left Player: {self.left_score}    Right Player: {
            self.right_score}", align=ALIGNMENT, font=FONT)

    def left_point(self) -> None:
        self.left_score += 1
        self.update_scoreboard()

    def right_point(self) -> None:
        self.right_score += 1
        self.update_scoreboard()
