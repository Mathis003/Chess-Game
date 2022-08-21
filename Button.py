import math
import pygame
from Configs import *

class SoundButton():

    def __init__(self, screen, image_sound_on, image_sound_off, rect):
        self.screen = screen
        self.image_sound_on = image_sound_on
        self.image_sound_off = image_sound_off
        self.rect = rect
        self.sound_on = True # Variable to know if the sound is on or off

    def checkCollision(self, pos_mouse):
        if math.sqrt((pos_mouse[0] - (2 + self.image_sound_on.get_width() / 2)) ** 2 + (
                      pos_mouse[1] - (2 + self.image_sound_on.get_width() / 2)) ** 2) <= SQUARE / 4:
            return True
        return False

    def changeButton(self):
        if self.sound_on:
            self.sound_on = False
        else:
            self.sound_on = True

    def displayButton(self):
        if self.sound_on:
            pygame.draw.circle(self.screen, (255, 255, 255), (2 + self.image_sound_on.get_width() / 2,
                                                              2 + self.image_sound_on.get_width() / 2), SQUARE / 4)
            self.screen.blit(self.image_sound_on, self.rect)
        else:
            pygame.draw.circle(self.screen, (255, 255, 255), (2 + self.image_sound_off.get_width() / 2,
                                                              2 + self.image_sound_off.get_width() / 2), SQUARE / 4)
            self.screen.blit(self.image_sound_off, self.rect)

class BoardColorButton:

    def __init__(self, screen, image, rect):
        self.screen = screen
        self.image= image
        self.rect = rect
        self.mod_board = "blue_mod" # Variable to know in which color board mod we are.

    def checkCollision(self, pos_mouse):
        if math.sqrt((pos_mouse[0] - (self.screen.get_width() - self.image.get_width() / 2 - 2))
                     ** 2 + (pos_mouse[1] - 2) ** 2) <= SQUARE / 4:  # If the mouse is on the circle of the button
            return True
        return False

    def changeColorBoard(self):
        if self.mod_board == "brown_mod":
            self.mod_board = "blue_mod"
        elif self.mod_board == "blue_mod":
            self.mod_board = "green_mod"
        elif self.mod_board == "green_mod":
            self.mod_board = "brown_mod"

    def displayButton(self):
        pygame.draw.circle(self.screen, (255, 255, 255), (self.screen.get_width() - 2
                           - self.image.get_width() / 2, 2 + self.image.get_height()
                           / 2), SQUARE / 4)
        self.screen.blit(self.image, self.rect)