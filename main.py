from graphics import Canvas
import time
import random

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 600
PADDLE_Y = CANVAS_HEIGHT - 30
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 15
BALL_RADIUS = 10
BALL_VELOCITY = 5

DELAY = 0.001

BRICK_GAP = 5
BRICK_WIDTH = (CANVAS_WIDTH - BRICK_GAP * 9) / 10
BRICK_HEIGHT = 10


def colorpicker():
    colors = ["pink", "aqua", "lime", "skyblue", "orange", "turquoise", "cyan", "silver", "wheat", "lavender", "violet"]
    return random.choice(colors)


def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    bricks = []  # Store all bricks

    # Create bricks
    for i in range(10):
        for j in range(10):
            x1 = (j * BRICK_WIDTH) + (BRICK_GAP * j)
            y1 = i * BRICK_HEIGHT + ((i + 1) * BRICK_GAP)
            x2 = x1 + BRICK_WIDTH
            y2 = y1 + BRICK_HEIGHT
            brick = canvas.create_rectangle(x1, y1, x2, y2, colorpicker(), "black")
            bricks.append(brick)  # Store the brick ID

    # Ball
    ball_x = CANVAS_WIDTH / 2 - BALL_RADIUS
    ball_y = CANVAS_HEIGHT / 2 - BALL_RADIUS
    ball = canvas.create_oval(ball_x, ball_y, ball_x + 2 * BALL_RADIUS, ball_y + 2 * BALL_RADIUS, "thistle", "black")

    # Paddle
    paddle_x = CANVAS_WIDTH / 2 - PADDLE_WIDTH / 2
    paddle_y = CANVAS_HEIGHT - 20 - PADDLE_HEIGHT
    paddle = canvas.create_rectangle(paddle_x, paddle_y, paddle_x + PADDLE_WIDTH, paddle_y + PADDLE_HEIGHT, "tan", "black")



    # Run the game loop
    game_loop(canvas, paddle, paddle_y, ball, ball_x, ball_y, bricks)


def game_loop(canvas, paddle, paddle_y, ball, ball_x, ball_y, bricks):
    count = 0
    score = canvas.create_text(
                    CANVAS_WIDTH/2-10, 
                    CANVAS_HEIGHT/2-10, 
                    text = str(count),
                    font = 'Arial', 
                    font_size = 50, 
                    color ='lavender'
                )
                
    """Main game loop for handling both paddle movement and ball movement."""
    x_velocity = BALL_VELOCITY
    y_velocity = BALL_VELOCITY

    while True:
        # Move paddle
        mouse_x = canvas.get_mouse_x()

        # Constrain paddle within the canvas width
        if mouse_x > CANVAS_WIDTH - PADDLE_WIDTH / 2:
            mouse_x = CANVAS_WIDTH - PADDLE_WIDTH / 2
        if mouse_x < PADDLE_WIDTH / 2:
            mouse_x = PADDLE_WIDTH / 2

        canvas.moveto(paddle, mouse_x - PADDLE_WIDTH / 2, paddle_y)

        # Move ball
        if ball_x <= 0 or ball_x + (2 * BALL_RADIUS) >= CANVAS_WIDTH:
            x_velocity = -x_velocity

        if (ball_y) >= CANVAS_HEIGHT:
            canvas.create_text(
                CANVAS_WIDTH/2-110, 
                CANVAS_HEIGHT/2-50, 
                text = "Game Over! Your score is",
                font = 'Arial', 
                font_size = 20, 
                color ='grey'
            )


            canvas.delete(score)
            score = canvas.create_text(
                    CANVAS_WIDTH/2-10, 
                    CANVAS_HEIGHT/2-10, 
                    text = str(count),
                    font = 'Arial', 
                    font_size = 50, 
                    color ='grey'
                )

            

            break

        # Check collisions
        colliding_list = canvas.find_overlapping(ball_x, ball_y, ball_x + (2 * BALL_RADIUS), ball_y + (2 * BALL_RADIUS))

        paddle_coords = canvas.coords(paddle)
        if len(paddle_coords) == 4:
            paddle_x1, _, paddle_x2, _ = paddle_coords
        else:
            paddle_x1, paddle_x2 = paddle_coords[0], paddle_coords[0] + PADDLE_WIDTH  # Safe fallback

        if paddle in colliding_list:
            ball_center_x = ball_x + BALL_RADIUS

            # Ball hits the **left side** of the paddle
            if ball_center_x < paddle_x1 + PADDLE_WIDTH / 4:
                x_velocity = -abs(x_velocity)  # Ensure ball moves left
                y_velocity = -abs(y_velocity)  # Bounce up

            # Ball hits the **right side** of the paddle
            elif ball_center_x > paddle_x2 - PADDLE_WIDTH / 4:
                x_velocity = abs(x_velocity)  # Ensure ball moves right
                y_velocity = -abs(y_velocity)  # Bounce up

            else:
                y_velocity = -abs(y_velocity)  # Normal bounce straight up

        # Check for collision with bricks
        for brick in bricks:
            if brick in colliding_list:
                y_velocity = -y_velocity  # Bounce the ball
                canvas.delete(brick)  # Remove the brick
                bricks.remove(brick)  # Remove from the list
                canvas.delete(score)
                count += 1
                score = canvas.create_text(
                    CANVAS_WIDTH/2-10, 
                    CANVAS_HEIGHT/2-10, 
                    text = str(count),
                    font = 'Arial', 
                    font_size = 50, 
                    color ='lavender'
                )

                break  # Stop checking multiple collisions at once

        if count == 100:
            print("Congratulations! You have completed the game.")

            canvas.create_text(
                CANVAS_WIDTH/2-120, 
                CANVAS_HEIGHT/2-50, 
                text = "Congratulations! Your score is",
                font = 'Arial', 
                font_size = 20, 
                color ='skyblue'
            )
            break


        if ball_y <= 0:
            y_velocity = -y_velocity

        ball_x += x_velocity
        ball_y += y_velocity
        canvas.moveto(ball, ball_x, ball_y)

        # Pause to control speed
        time.sleep(DELAY)


if __name__ == '__main__':
    main()
