#Імпортування бібліотек
import pygame
import os
from pygame.constants import MOUSEBUTTONDOWN
from pygame.constants import FINGERDOWN


#Клас базових кнопок
class ImageButton:

    def __init__(self, x, y, width, height, text, image_path, disabled):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.disabled = disabled

    def draw(self, screen):
        current_image = self.image
        screen.blit(current_image, self.rect.topleft)

        font = pygame.font.Font(None, 26)
        text_surface = font.render(self.text, True, (255,255,255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def disable(self):
        self.image = pygame.image.load("images/disabled.jpg")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.disabled = True

    def reset(self):
        self.image = pygame.image.load("images/play_empty.jpg")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.disabled = False

    def handle_event(self, event):
        if (event.type == MOUSEBUTTONDOWN
                and event.button == 1 and self.is_hovered):
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))