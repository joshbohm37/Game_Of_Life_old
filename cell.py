import pygame

class Cell(pygame.sprite.Sprite):
    def __init__(self, start_pos, state, cell_size):
        super().__init__()
        color = ()
        if state == 1:
            color = (255, 255, 255)
        else:
            color = (0, 0, 0)

        self.surf = pygame.Surface((cell_size, cell_size))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(topleft = start_pos)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True

#This is another test
