import curses
import time
import math
import random

# Function to draw a firework shot
def firework_shot(stdscr, y, x):
    stdscr.addch(y, x, '|')

# Function to draw a growing explosion with variation
def firework_explosion(stdscr, y, x, radius):
    chars = ['o', '*', '+', '.', 'x', '#', '%']  # Variety of characters for explosion
    for angle in range(0, 360, 10):  # Draw the circle with more points for prettier result
        rad_angle = math.radians(angle)
        y_offset = int(radius * math.sin(rad_angle))
        x_offset = int(radius * math.cos(rad_angle))
        if 0 < y + y_offset < curses.LINES and 0 < x + x_offset < curses.COLS:
            stdscr.addch(y + y_offset, x + x_offset, random.choice(chars))

# Function to introduce a sparkle effect for realism
def sparkle_effect(stdscr, y, x, spread):
    sparkle_chars = ['.', '*', '+']
    for _ in range(spread):
        spark_x = x + random.randint(-spread, spread)
        spark_y = y + random.randint(-spread, spread)
        if 0 < spark_y < curses.LINES and 0 < spark_x < curses.COLS:
            stdscr.addch(spark_y, spark_x, random.choice(sparkle_chars))

# Class to represent a firework
class Firework:
    def __init__(self, x, y, state='shooting', explosion_radius=0, max_explosion_radius=15):
        self.x = x
        self.y = y
        self.state = state  # 'shooting', 'exploding', or 'sparkling'
        self.explosion_radius = explosion_radius
        self.max_explosion_radius = max_explosion_radius

    def update(self, stdscr):
        if self.state == 'shooting':
            firework_shot(stdscr, self.y, self.x)
            self.y -= 1
            if self.y < curses.LINES // 3:  # Firework reaches the top 1/3 of the screen
                self.state = 'exploding'
        elif self.state == 'exploding':
            firework_explosion(stdscr, self.y, self.x, self.explosion_radius)
            self.explosion_radius += 1
            if self.explosion_radius >= self.max_explosion_radius:
                self.state = 'sparkling'
        elif self.state == 'sparkling':
            sparkle_effect(stdscr, self.y, self.x, spread=8)

        # Check if firework is finished
        return self.state != 'sparkling' or random.random() > 0.05  # Small chance to remove sparkle

# Main animation loop
def firework_animation(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(True)  # Make getch() non-blocking
    stdscr.timeout(30)  # Set a timeout of 100ms for getch()

    # Use default terminal colors
    curses.use_default_colors()

    fireworks = []
    height, width = stdscr.getmaxyx()

    # Run the fireworks animation continuously until a key is pressed
    while True:
        stdscr.clear()

        # Launch new fireworks randomly
        if len(fireworks) < 5 and random.random() < 0.2:  # Limit to 5 concurrent fireworks
            x = random.randint(2, width - 3)
            y = height - 2
            fireworks.append(Firework(x, y))

        # Update each firework
        fireworks = [fw for fw in fireworks if fw.update(stdscr)]

        stdscr.refresh()
        
        # Exit if any key is pressed
        if stdscr.getch() != -1:
            break

# Wrapper for running curses
curses.wrapper(firework_animation)

