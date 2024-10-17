from time import sleep
from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard


def main() -> None:
    screen = Screen()
    screen.title("Pong Game")
    screen.bgcolor("white")
    screen.setup(width=1000, height=600)
    screen.tracer(0)

    left_paddle = Paddle(position=(-400, 0), color="black")
    right_paddle = Paddle(position=(400, 0), color="black")
    ball = Ball(color="blue", speed=4)
    scoreboard = Scoreboard(color="blue")

    screen.listen()
    screen.onkeypress(left_paddle.move_up, "w")
    screen.onkeypress(left_paddle.move_down, "s")
    screen.onkeypress(right_paddle.move_up, "Up")
    screen.onkeypress(right_paddle.move_down, "Down")

    while True:
        screen.update()
        sleep(0.01)
        ball.move()

        # checks if ball touches the sides of the screen

        if ball.ycor() > 280 or ball.ycor() < -280:
            ball.bounce_y()

        if ball.xcor() > 500:
            ball.reset_position()
            scoreboard.left_point()

        if ball.xcor() < -500:
            ball.reset_position()
            scoreboard.right_point()

        # checks if ball touches the paddles

        if (ball.xcor() > 360 and ball.xcor() < 370) and \
            (
                ball.ycor() < right_paddle.ycor() + 50
                and ball.ycor() > right_paddle.ycor() - 50
        ):
            ball.bounce_x()

        if (ball.xcor() < -360 and ball.xcor() > -370) and \
            (
                ball.ycor() < left_paddle.ycor() + 50
                and ball.ycor() > left_paddle.ycor() - 50
        ):
            ball.bounce_x()


if __name__ == "__main__":
    main()
