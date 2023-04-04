import pygame
from pygame.locals import *
from random import randint, choice, uniform
from assets import IMAGES
import math

GRAVITY = 1
GROUND_LEVEL = 300

class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, pos, asset_lib, **kwargs):
        pygame.sprite.Sprite.__init__(self)


        self.create_physics(pos,**kwargs)
        self.create_animation(asset_lib, **kwargs)
        

    def update_physics(self, update_gravity, own_movement, jump=False):
        self.next_x = self.velocity.x 
        self.next_y = self.velocity.y 

        if update_gravity:
            self.gravity_force.y += self.gravity * self.mass / 100

            if self.gravity_force.y > 9.8:
                self.gravity_force.y = 9.8


            if  not self.on_ground:
                self.position.y += self.gravity_force.y

        if own_movement:
            
            keys = pygame.key.get_pressed()

            self.velocity.x += (keys[K_d] - keys[K_a]) * self.speed
            if not jump:
                self.velocity.y += (keys[K_s] - keys[K_w]) * self.speed
            else:
                if keys[K_SPACE] and self.on_ground:
                    self.jumped = True
                    self.on_ground = False
                    self.velocity.y = -((self.speed - self.friction) * 40) 
 
        #print(self.on_ground, self.jumped)

        self.velocity = self.velocity.move_towards((0,0), self.friction)
        
        self.sum_y_vel = round(self.velocity.y + self.gravity_force.y)

        if self.velocity.x > self.max_speed:
            self.velocity.x = self.max_speed 
        if self.velocity.x < self.max_speed *-1:
            self.velocity.x = self.max_speed *-1

        if not jump:
            if self.velocity.y > self.max_speed:
                self.velocity.y = self.max_speed 
            if self.velocity.y < self.max_speed *-1:
                self.velocity.y = self.max_speed *-1

    def affect_by_scroll(self, scroll):
        self.final_pos = self.position - pygame.math.Vector2(scroll) -  pygame.math.Vector2(50,60)
        self.x, self.y = self.position
 
    def create_physics(self,pos, **kwargs):
        global GRAVITY, GROUND_LEVEL

        self.gravity = GRAVITY
        self.ground_level = GROUND_LEVEL
        self.mass = kwargs["mass"]
        self.friction = self.gravity * self.mass / 50
        self.speed = kwargs["speed"]
        self.speed_squared = self.speed * self.speed
        self.gravity_force = pygame.math.Vector2(0,0)
        self.velocity = pygame.math.Vector2(0,0)
        
        self.jumped = False

        self.max_speed =  self.mass  / (self.speed * 5)

        self.position = pygame.math.Vector2(pos)
        self.on_ground = True
        
        self.final_pos = pygame.math.Vector2()

    def animate(self):
        self.update_anim_info()
        time_now = pygame.time.get_ticks()

        if time_now > self.next_frame:
            self.index += 1 
            
            self.next_frame = time_now + self.anim_cooldown
            if self.animation == "jump" and pygame.key.get_pressed()[K_SPACE]:
                if self.index > 1:
                    self.index = 1
                
            
            if self.index > self.max_index:
            
                
            
                self.index = 0
                
                if not self.repeat_anim:
                    self.animation = self.base_anim
        

        if self.flip:
            self.image = pygame.transform.flip(self.anim_list[self.index], True, False)
        else:
            self.image = pygame.transform.flip(self.anim_list[self.index], False, False)

    def update_anim_info(self):
        self.anim_list = self.images[self.anim_path][self.animation]
        self.max_index = len(self.anim_list) -1
        self.anim_cooldown = self.animation_info[self.animation][0]
        if self.animation == "run":
            self.anim_cooldown = self.animation_info[self.animation][0] * abs(self.velocity.x /3 ) 
        
        self.repeat_anim = self.animation_info[self.animation][1]
        self.anim_done = self.index>self.max_index

    def create_animation(self, asset_lib, **kwargs):

        self.anim_path = kwargs["anim_group"]
        self.animation_info = kwargs["anim_names"]
        self.base_anim = kwargs.get("base_anim", "idle")
        self.index = 0 
        self.anim_done = False
        self.flip = False

        if "idle" in self.animation_info.keys():
            self.animation = "idle"
        else:
            raise Exception("Please set an idle animation state")

        self.images = asset_lib

        self.anim_cooldown = self.animation_info[self.animation][0]
        self.repeat_anim = self.animation_info[self.animation][1]

        self.next_frame = pygame.time.get_ticks() + self.anim_cooldown

        self.anim_list = self.images[self.anim_path][self.animation]

        self.max_index = len(self.anim_list) - 1

        self.image = self.anim_list[self.index]

    def set_animation(self, animation):
        if self.animation != animation:
            self.animation = animation
            self.index = 0 
            self.update_anim_info()
            self.next_frame = pygame.time.get_ticks() + self.anim_cooldown
            
class Block(pygame.sprite.Sprite):
    def __init__(self, pos, size, color):
        
        self.pos = pygame.math.Vector2(pos) 
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.size = size
        self.color = color
        
    def update(self, screen, scroll):
        
        self.rect.topleft = self.pos - pygame.math.Vector2(scroll)
        
        pygame.draw.rect(screen, self.color, self.rect)    
    
class Bullet():
    def __init__(self,shooter ,target_pos, speed):
        
        self.shooter = shooter
        
        
        self.position = pygame.math.Vector2(self.shooter.owner.position.x, self.shooter.owner.position.y)
        
        self.image = pygame.transform.scale(IMAGES["player"]["idle"][0], (25,25))
        
        self.rad = uniform(4.5, 8)
        
        
        angle = math.atan2(target_pos[1] - self.shooter.owner.final_pos.y -50, target_pos[0] - self.shooter.owner.final_pos.x- 50)
        self.velocity =( pygame.math.Vector2(math.cos(angle) , math.sin(angle)  ))* speed
        
        

        
        
    def affect_by_scroll(self, scroll):
        self.final_pos = self.position - pygame.math.Vector2(scroll) + pygame.math.Vector2(-50,-50)
        
        
    def update(self, scroll, screen):
        self.on_screen = pygame.Rect.colliderect(self.image.get_rect(center=self.position - scroll), screen.get_rect(topleft=(0,0)))
        
        self.position += self.velocity
        
        self.affect_by_scroll(scroll)
        
                    
class ShootController(pygame.sprite.Sprite):
    def __init__(self, owner):
        pygame.sprite.Sprite.__init__(self)

        self.owner = owner
        self.bullet_list = []
        
    def update_self(self):
        self.position = self.owner.final_pos
        
    def update_bullets(self, screen, scroll):
        
        for bullet in self.bullet_list:
            bullet.update(scroll, screen)
            if bullet.on_screen:
                #screen.blit(bullet.image, bullet.final_pos)
                pygame.draw.circle(screen, (255,0,0), bullet.final_pos + pygame.math.Vector2(20,20), bullet.rad)


            
    def shoot(self, speed=6):

        self.bullet_list.append(Bullet(self, pygame.mouse.get_pos(), speed))
        
        
        
class Player(PhysicsEntity):
    def __init__(self, pos, **kwargs):
        super().__init__(pos, kwargs.pop('asset_lib'), **kwargs)

        self.not_idled_anims = ["punch"]

        self.not_runned_anims = ["punch", "jump"]
        
        self.shooter = ShootController(self)
        
        self.shot = True
        

    def update(self, screen, scroll, block_list):
        
        self.affect_by_scroll(scroll)
        self.animate()
        self.update_physics(True, True, True)
        self.control()
        self.walls(block_list, screen)
        self.shooter.update_self()
        self.shooter.update_bullets(screen, scroll)
        
        self.position.x += self.next_x
        self.position.y += self.next_y
        
        if pygame.mouse.get_pressed()[0] :
            if not self.shot:
                self.shooter.shoot()
                self.shot = True
            
        else:
            self.shot = False

        screen.blit(self.image, self.rect.topleft)
        pygame.draw.rect(screen, (255,0,255), self.rect)
        #screen.blit(self.image, self.final_pos)
        

    def control(self):
        keys = pygame.key.get_pressed()
        
        self.rect = self.image.get_rect(center=self.final_pos + pygame.math.Vector2(20,30))
        
        

        if not self.animation in self.not_runned_anims:
            if keys[K_a]:
                self.set_animation("run")
                if not keys[K_d]:
                    self.flip = True
            elif keys[K_d]:
                self.set_animation("run")
                if not keys[K_a]:
                    self.flip = False

            else:
                if not self.animation in self.not_idled_anims:
                    self.set_animation("idle")
                
        if self.sum_y_vel > 0:
            self.set_animation("fall")
            
        if self.jumped :
            self.set_animation("jump")

    def walls(self, block_list, screen):
                        
        for block in block_list:
            if block.rect.colliderect(self.rect.x + self.next_x, self.rect.y, self.image.get_width(), self.image.get_height()):

                self.next_x = 0
                
            if block.rect.colliderect(self.rect.x , self.next_y  + self.next_y, self.image.get_width(), self.image.get_height()):
                
                if self.sum_y_vel > 0:
                    
                    self.rect.bottom = block.rect.top  
                    #self.velocity.y  = 0 
                    #self.next_y= 0
                    self.gravity_force.y = 0 
                    
                elif self.sum_y_vel < 0:
                    self.rect.top =  block.rect.bottom - 64
                    #self.on_ground = True
                    self.gravity_force.y = 0 
                    #self.next_y= 0
                    
        self.track_pos = pygame.math.Vector2(self.rect.center)
                
plr = Player(
    (200, 200),
    asset_lib=IMAGES,
    anim_group="player",
    anim_names={"idle": (150, True), "run": (125, True), "punch": (500, False), "fall": (125, True), "jump": (100, False),},
    mass=8,
    speed=.5,
)
