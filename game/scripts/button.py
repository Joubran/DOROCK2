import pygame

class Button():
    def __init__(self, x, y, image, scale=1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.hovered = False



    def draw(self, surface, activity='left_click'):
        action = False

        #get mouse pos
        pos = pygame.mouse.get_pos()

            #check mouseover and clicked condotions
        if activity == 'left_click':
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] and not self.clicked:
                    self.clicked = True
                    action = True
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False

            #draw button on screen
            surface.blit(self.image, (self.rect.x, self.rect.y))

        elif activity == 'hover':
            if self.rect.collidepoint(pos):
                surface.blit(self.image, (self.rect.x, self.rect.y))
                action = True
            else:
                action = False



        return action