import pygame
from board import Board

pygame.init()
pygame.display.set_caption("Sudoku")

# Constants
WIDTH, HEIGHT = 540, 600
BOARD_SIZE = 540
BOARD_OFFSET_Y = 20
BEIGE = (245, 245, 220)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
BUTTON_HEIGHT = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont('Arial', 30)

def draw_start_screen():
    screen.fill(BEIGE)
    title = font.render("Welcome to Sudoku", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

    subtitle = font.render("Select Difficulty:", True, BLACK)
    screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 200))

    btn_y = 300
    pygame.draw.rect(screen, GRAY, (50, btn_y, 120, BUTTON_HEIGHT))
    easy = font.render("Easy", True, BLACK)
    screen.blit(easy, (110 - easy.get_width()//2, btn_y + 15))

    pygame.draw.rect(screen, GRAY, (210, btn_y, 120, BUTTON_HEIGHT))
    medium = font.render("Medium", True, BLACK)
    screen.blit(medium, (270 - medium.get_width()//2, btn_y + 15))

    pygame.draw.rect(screen, GRAY, (370, btn_y, 120, BUTTON_HEIGHT))
    hard = font.render("Hard", True, BLACK)
    screen.blit(hard, (430 - hard.get_width()//2, btn_y + 15))

def draw_game_buttons():
    btn_y = HEIGHT - BUTTON_HEIGHT - 10
    pygame.draw.rect(screen, GRAY, (50, btn_y, 120, BUTTON_HEIGHT))
    reset = font.render("Reset", True, BLACK)
    screen.blit(reset, (110 - reset.get_width()//2, btn_y + 15))

    pygame.draw.rect(screen, GRAY, (210, btn_y, 120, BUTTON_HEIGHT))
    restart = font.render("Restart", True, BLACK)
    screen.blit(restart, (270 - restart.get_width()//2, btn_y + 15))

    pygame.draw.rect(screen, GRAY, (370, btn_y, 120, BUTTON_HEIGHT))
    exit_btn = font.render("Exit", True, BLACK)
    screen.blit(exit_btn, (430 - exit_btn.get_width()//2, btn_y + 15))

def draw_end_screen(message):
    screen.fill(BEIGE)
    end_text = font.render(message, True, BLACK)
    screen.blit(end_text, (WIDTH//2 - end_text.get_width()//2, 200))

    btn_text = "Exit" if message == "Game Won!" else "Restart"
    pygame.draw.rect(screen, GRAY, (WIDTH//2 - 60, 300, 120, BUTTON_HEIGHT))
    text = font.render(btn_text, True, BLACK)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, 315))

def main():
    running = True
    game_start = True
    game_over = False
    game_won = False
    board = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_start:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 300 <= y <= 350:
                        if 50 <= x <= 170:
                            board = Board(BOARD_SIZE, BOARD_SIZE, screen, "easy", BOARD_OFFSET_Y)
                            game_start = False
                        elif 210 <= x <= 330:
                            board = Board(BOARD_SIZE, BOARD_SIZE, screen, "medium", BOARD_OFFSET_Y)
                            game_start = False
                        elif 370 <= x <= 490:
                            board = Board(BOARD_SIZE, BOARD_SIZE, screen, "hard", BOARD_OFFSET_Y)
                            game_start = False

            elif game_over or game_won:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 300 <= y <= 350 and WIDTH//2 - 60 <= x <= WIDTH//2 + 60:
                        if game_won:
                            running = False
                        else:
                            game_start = True
                            game_over = False

            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if y < BOARD_SIZE + BOARD_OFFSET_Y:
                        cell = board.click(x, y - BOARD_OFFSET_Y)
                        if cell:
                            board.select(cell[0], cell[1])
                    elif HEIGHT - BUTTON_HEIGHT - 10 <= y <= HEIGHT:
                        if 50 <= x <= 170:
                            board.reset_to_original()
                        elif 210 <= x <= 330:
                            game_start = True
                        elif 370 <= x <= 490:
                            running = False

                elif event.type == pygame.KEYDOWN:
                    if board.selected:
                        if pygame.K_1 <= event.key <= pygame.K_9:
                            board.sketch(event.key - pygame.K_0)
                        elif event.key == pygame.K_RETURN:
                            row, col = board.selected
                            if board.cells[row][col].sketched_value is not None:
                                board.place_number(board.cells[row][col].sketched_value)
                                if board.is_full():
                                    if board.check_board():
                                        game_won = True
                                    else:
                                        game_over = True
                        elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                            board.clear()


        if game_start:
            draw_start_screen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 300 <= y <= 350:
                    if 50 <= x <= 170:
                        difficulty = "easy"
                        board = Board(WIDTH, HEIGHT, screen, difficulty)
                        game_start = False
                    elif 210 <= x <= 330:
                        difficulty = "medium"
                        board = Board(WIDTH, HEIGHT, screen, difficulty)
                        game_start = False
                    elif 370 <= x <= 490:
                        difficulty = "hard"
                        board = Board(WIDTH, HEIGHT, screen, difficulty)
                        game_start = False
        elif game_over:
            draw_end_screen("Game Over :(")
        elif game_won:
            draw_end_screen("Game Won!")
        else:
            screen.fill(BEIGE)
            board.draw()
            draw_game_buttons()

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()