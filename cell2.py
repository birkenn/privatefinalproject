import pygame


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = None
        self.selected = False
        self.font = pygame.font.SysFont('Arial', 30)

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self, x, y, width, height):
        # Draw cell
        if self.selected:
            pygame.draw.rect(self.screen, (200, 200, 255), (x, y, width, height))

        # Draw value
        if self.value != 0:
            text = self.font.render(str(self.value), True, "black")
            self.screen.blit(text, (x + width // 2 - text.get_width() // 2,
                                    y + height // 2 - text.get_height() // 2))
        elif self.sketched_value:
            text = self.font.render(str(self.sketched_value), True, (150, 150, 150))
            self.screen.blit(text, (x + 5, y + 5))
