import pygame
from setting import *

#  by the Lab6 
bling_animation = []
for i in range(1,10):
    bling_image = pygame.image.load(f"picture/bling{i}.png")
    bling_animation.append(bling_image)


class Explosion(pygame.sprite.Sprite): 
    def __init__(self, x, y, size):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.animation = [pygame.transform.scale(bling_animation[i], (self.size, self.size)) for i in range(9)]
        self.image = self.animation[0]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.frame = 0
        self.animation_time = 0
        self.animation_delay = 10
        self.sound = pygame.mixer.Sound("Sound/hit.mp3")

    def update(self):
        if self.frame == 0:
            self.sound.set_volume(0.05)  #把音量調小聲
            self.sound.play()

        now = pygame.time.get_ticks()
        if now - self.animation_time > self.animation_delay:
            self.frame += 1
            self.animation_time = pygame.time.get_ticks()
            if self.frame == len(self.animation):
                self.kill()
            else:
                self.image = self.animation[self.frame]      
