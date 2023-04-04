import pygame
from pygame.locals import *
from random import randint, choice, uniform
import math, characters, cam

screen = pygame.display.set_mode((800,600))

camera = cam.Camera(4, screen)

def checkcollide(it1, it2, tolerance=115):
    
    if it1.rect.colliderect(it2.rect):
        if abs(it2.rect.top - it1.rect.bottom) < tolerance:
            return {"bottom" : True, "left" : False,"right" : False,"top" : False,}
        
        elif abs(it2.rect.bottom - it1.rect.top) < tolerance:
            return {"bottom" : False, "left" : False,"right" : False,"top" : True,}
        
        elif abs(it2.rect.right - it1.rect.left) < tolerance:
            return {"bottom" : False, "left" : True,"right" : False,"top" : False,}
        
        elif abs(it2.rect.left - it1.rect.right) < tolerance:
            return {"bottom" : False, "left" : False,"right" : True,"top" : False,}
        
        return {"bottom" : False, "left" : False,"right" : False,"top" : False,}
        
block_list = [characters.Block((400,400), (600,400), (255,255,255))]
        

def render():
    screen.fill((0,0,255))
    
    characters.plr.update(screen, camera.scroll, block_list)

    #pygame.draw.rect(screen, (25,25,25), characters.plr.rect)
    
    
    for block in block_list:
        block.update(screen, camera.scroll)
    
    camera.follow(characters.plr, 1, speed= 32,)


def collisions():
    
    pass


