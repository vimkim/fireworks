import curses
import time
import math
import random

# Function to draw a firework shot
def firework_shot(stdscr, y, x):
    stdscr.addch(y, x, '|')
    stdscr.refresh()

# Function to draw a growing explosion with variation
def firework_explosion(stdscr, y, x, radius, char):
    chars = ['o', '*', '+', '.', 'x', '#', '%']  # Variety of characters for explosion
    for angle in range(0, 360, 5):  # Draw the circle with more points for prettier result
        rad_angle = math.radians(angle)
        y_offset = int(radius * math.sin(rad_angle))
        x_offset = int(radius * math.cos(rad_angle))
        if 0 < y + y_offset < curses.LINES and 0 < x + x_offset < curses.COLS:
            stdscr.addch(y + y_offset, x + x_offset, random.choice(chars))
    stdscr.refresh()

# Function to introduce a sparkle effect for realism
def sparkle_effect(stdscr, y, x, spread):
    sparkle_chars = ['.', '*', '+']
    for _ in range(spread):
        spark_x = x + random.randint(-spread, spread)
        spark_y = y + random.randint(-spread, spread)
        if 0 < spark_y < curses.LINES and 0 < spark_x < curses.COLS:
            stdscr.addch(spark_y, spark_x, random.choice(sparkle_chars))
    stdscr.refresh()

# Function for multiple fireworks
def multiple_fireworks(stdscr, num_fireworks):
    height, width = stdscr.getmaxyx()
    
    for _ in range(num_fireworks):
        x = random.randint(1, width - 2)
        y = height - 2
        
        # Firework shot animation (moving upwards)
        while y > height // 3:
            stdscr.clear()
            firework_shot(stdscr, y, x)
            y -= 1
            time.sleep(0.05)

        # Explosion with expanding circle
        for radius in range(1, 15):  # Expanding circle radius
            stdscr.clear()
            firework_explosion(stdscr, y, x, radius, '*')
            sparkle_effect(stdscr, y, x, spread=radius // 2)  # Add random sparkles during explosion
            time.sleep(0.1)

        # After the explosion, some fading sparkles remain
        for _ in range(3):
            sparkle_effect(stdscr, y, x, spread=8)  # Wider area for random sparkles
            time.sleep(0.2)

# Main animation loop
def firework_animation(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(True)  # Make getch() non-blocking
    stdscr.timeout(100)  # Set a timeout of 100ms for getch()

     # Use default terminal colors
    curses.use_default_colors()

    # Run the fireworks animation continuously until a key is pressed
    while True:
        stdscr.clear()
        multiple_fireworks(stdscr, num_fireworks=random.randint(1, 3))  # Random number of fireworks
        
        if stdscr.getch() != -1:  # Exit if any key is pressed
            break

# Wrapper for running curses
curses.wrapper(firework_animation)

