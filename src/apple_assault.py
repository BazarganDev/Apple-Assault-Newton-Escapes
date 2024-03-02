# Import modules
import curses
import random
import time



# Initialize the curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(False)
stdscr.nodelay(True)
stdscr.keypad(True)

# Determine the size of the screen
max_lines = curses.LINES - 1
max_columns = curses.COLS - 1

# Define everything necessary
ground = []
apples = []
newton_character = "🙂"
apple_character = "🍎"
newton_x = 0
newton_y = 0
score = 0

# Functions
def set_coordinates():
    """
    Set coordinates to apples.
    They begin to fall from the first line.

    Returns:
        x, y (int): The X axis and Y axis.
    """
    x = 1
    y = random.randint(5, max_columns - 5)

    return x, y

def init():
    """
    Initialize.
    The world and other objects in the game needs to be initialized before drawing them.
    """
    global newton_x, newton_y

    # Initialize the environment
    for i in range(0, max_lines - 7):
        ground.append([])
        for j in range(max_columns):
            ground[i].append(' ')

    # Initialize the ground
    for i in range(max_lines - 7, max_lines + 1):
        ground.append([])
        for j in range(max_columns):
            ground[i].append('+')
    
    # Initialize apples
    for i in range(30):
        apple_x, apple_y = set_coordinates()
        apples.append((apple_x, apple_y))
   
    # Initialize the Newton
    newton_x = max_lines - 8
    newton_y = random.randint(0, max_columns)

def draw():
    """
    Draw the world.
    """
    # Draw the initialized environment and the ground
    for i in range(max_lines):
        for j in range(max_columns):
            stdscr.addch(i, j, ground[i][j])
    
    # Show the number of evaded apples
    stdscr.addstr(0, 0, f"Apples Evaded: {score}", curses.A_BOLD)
    
    # Draw the initialized apples
    for a in apples:
        apple_x, apple_y = a
        stdscr.addch(apple_x, apple_y, apple_character)
    
    # Place Newton on the ground with given coordinates
    stdscr.addch(newton_x, newton_y, newton_character)
    stdscr.refresh()

def border(position, minimum, maximum):
    """
    Newton should not be able to get pass beyond the sides of the screen.
    
    Args:
        position (int): Current position
        minimum (int): Lowest position possible
        maximum (int): Highest position possible

    Returns:
        position (int)
    """
    if position > maximum:
        return maximum
    if position < minimum:
        return minimum
    return position

def move_newton(keystroke):
    """
    Newton can dodge the apples by moving to the left or to the right.
    Remember that Newton should not be able to get pass beyond the sides of the screen.
    So we should define the border to him.
    A --> Move to the left
    D --> Move to the right
    
    Args:
        keystroke (str): Takes the pressed key.
    """

    global newton_y
    
    if keystroke == 'a':
        newton_y -= 1
    elif keystroke == 'd':
        newton_y += 1

    newton_y = border(newton_y, 0, max_columns - 1)

def physics():
    """
    The physics of the game such as gravity and fall damage.
    """
    global playing, score
    
    # Simulate gravity
    for i in range(len(apples)):
        x, y = apples[i]
        if random.random() > 0.95:
            x += 1
            apples[i] = x, y
        
        # If apple hits Newton's head, You know what will happen ;)
        # He will discover gravity and the game will come to an end!
        if x == newton_x and y == newton_y:
            stdscr.addstr(max_lines // 2, max_columns // 2 - 13, "NEWTON DISCOVERED GRAVITY!")
            stdscr.refresh()
            time.sleep(3)
            playing = False
        
        # If the apple hits the ground, it will take fall damage.
        # It means that the apple is crushed. Then we have to replace it with a new apple.
        # Add a one score when an apple is evaded.
        elif ground[x][y] == '+':
            score += 1
            new_apple_x, new_apple_y = set_coordinates()
            apples[i] = (new_apple_x, new_apple_y)

def main():
    """
    The main loop of the game.
    Everything happens here.
    """
    init()
    
    global playing
    
    playing = True
    while playing:
        try:
            key = stdscr.getkey()
        except:
            key = ''
        if key in 'ad':
            move_newton(key)
        elif key == 'q':
            playing = False
        physics()
        time.sleep(0.01)
        draw()

main()

stdscr.addstr(max_lines // 2, max_columns // 2 - 9, "THANKS FOR PLAYING!")
stdscr.refresh()
time.sleep(3)

curses.curs_set(True)
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
