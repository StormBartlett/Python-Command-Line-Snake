import copy
import time
import threading
import emoji

def getChar():
    try:
        # for Windows-based systems
        import msvcrt # If successful, we are on Windows
        return msvcrt.getch()

    except ImportError:
        # for POSIX-based systems (with termios & tty support)
        import tty, sys, termios  # raises ImportError if unsupported

        fd = sys.stdin.fileno()
        oldSettings = termios.tcgetattr(fd)

        try:
            tty.setcbreak(fd)
            answer = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

        return answer

class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            self.input_cbk(getChar()) #waits to get input (without Return)

def move_callback(move):
    #evaluate the keyboard input
    # print('You Entered:', move)
    global direction
    if move == "a" and direction != [1,0]:
        direction = [-1,0]
    elif move == "d" and direction != [-1,0]:
        direction = [1,0]
    elif move == "w" and direction != [0,1]:
        direction = [0,-1]
    elif move == "s" and direction != [0,-1]:
        direction = [0,1]

#start the Keyboard thread
kthread = KeyboardThread(move_callback)

BOARD_WIDTH = BOARD_HEIGHT = 15

player = [[2,3]]
apples = [[3,4]]

def print_board():
    board =[copy.deepcopy([":rainbow:"] * BOARD_WIDTH) for i in range(BOARD_HEIGHT)]
    for a in apples:
        board[a[1]][a[0]] = ":cookie:"

    for p in player:
        board[p[1]][p[0]] = ":snake:"

    display = ""

    for r in range(BOARD_HEIGHT):
        for c in range(BOARD_WIDTH):
            display += board[r][c] + " "
        display += "\n"

    print(emoji.emojize(display))

def is_head_on_apple(player, apples):
    return player[0] in apples

def make_new_apple():
    import random
    return [random.randint(0,BOARD_WIDTH-1), random.randint(0,BOARD_HEIGHT-1)]

def check_bounds(player):
    if player[0][0] < 0 or player[0][0] >= BOARD_WIDTH \
        or player[0][1] < 0 or player[0][1] >= BOARD_HEIGHT:
        print("Died as left board")
        quit() 

def check_body_collision(player):
    if player[0] in player[1:]:
        print("Died as hit body")
        quit() 

global direction
direction = [1,0]
score = 0
while True:
    time.sleep(0.2)

    player = [copy.deepcopy(player[0])] + player
    player[0][0] += direction[0]
    player[0][1] += direction[1]
    
    if not is_head_on_apple(player, apples):
        del player[-1]
    else:
        score += 1
        apples[0] = make_new_apple()
    
    check_bounds(player)
    check_body_collision(player)

    #print(player)
    print_board()
    print("Score: " + str(score))