import pygame
from pygame.locals import *
class Camera:
    def __init__(self, speed, screen):
        self.scroll = [0,0]
        self.speed = speed
        self.screen = screen
        self.zoom = 1

    def move_on_command(self, dt):

        keys = pygame.key.get_pressed()
        
        if keys[K_w]:
            self.scroll[1] -= self.speed  *dt
        if keys[K_s]:
            self.scroll[1] += self.speed *dt
        if keys[K_d]:
            self.scroll[0] += self.speed *dt
        if keys[K_a]:
            self.scroll[0] -= self.speed *dt
            
    def follow(self, obj, dt ,speed=320):
        screen_center_x = self.screen.get_width()/2    
        screen_center_y = self.screen.get_height()/2
        
        if obj.rect.x  - self.scroll[0] != screen_center_x:
            self.scroll[0] += ((obj.x - (self.scroll[0]+screen_center_x))/speed) * dt
            
        if obj.rect.y  - self.scroll[1] != screen_center_y:
            self.scroll[1] += ((obj.y - (self.scroll[1]+screen_center_x))/speed) * dt


    def zoom_game(self, zoom):
        self.zoom = zoom

    def center_obj(self, obj):
        self.scroll = [obj.rect.x,obj.rect.y]

