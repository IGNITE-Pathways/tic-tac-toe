import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
FONT = pygame.font.SysFont('arial', 40)
WINNER_FONT = pygame.font.SysFont('arial', 60)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BG_COLOR)

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Draw lines
def draw_lines():
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, BLUE, (int(col * SQUARE_SIZE + SQUARE_SIZE//2), int(row * SQUARE_SIZE + SQUARE_SIZE//2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

# Check win
def check_win(player):
    for row in range(BOARD_ROWS):
        if all([spot == player for spot in board[row]]):
            return True
    for col in range(BOARD_COLS):
        if all([board[row][col] == player for row in range(BOARD_ROWS)]):
            return True
    if all([board[i][i] == player for i in range(BOARD_COLS)]):
        return True
    if all([board[i][BOARD_COLS - i - 1] == player for i in range(BOARD_COLS)]):
        return True
    return False

# Display winner
def display_winner(player_name):
    winner_text = f"{player_name} Wins!"
    winner_label = WINNER_FONT.render(winner_text, True, (255, 255, 255))
    screen.blit(winner_label, (WIDTH//4, HEIGHT//2 - 30))
    pygame.display.update()
    pygame.time.wait(3000)

# Restart the game
def restart_game():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None

# Capture player names
def get_player_names():
    player1_name = input("Enter Player 1 (X) name: ")
    player2_name = input("Enter Player 2 (O) name: ")
    return player1_name, player2_name

# Main loop
player1_name, player2_name = get_player_names()
player = 'X'
player_name = player1_name
game_over = False
draw_lines()
pygame.display.set_caption(f"{player_name}'s Turn")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX, mouseY = event.pos
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE
            if board[clicked_row][clicked_col] is None:
                board[clicked_row][clicked_col] = player
                if check_win(player):
                    game_over = True
                    display_winner(player_name)
                else:
                    player = 'O' if player == 'X' else 'X'
                    player_name = player2_name if player == 'O' else player1_name
                    pygame.display.set_caption(f"{player_name}'s Turn")
                draw_figures()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 'X'
                player_name = player1_name
                pygame.display.set_caption(f"{player_name}'s Turn")
    pygame.display.update()
