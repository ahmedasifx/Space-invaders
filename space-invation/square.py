import pygame

class Square:
    def __init__(self, color, x, y, width, height):
        self.rect = pygame.Rect(x,y,width,height)
        self.color = color
        self.direction = 'E'
        self.speed = 5

    def move(self):
        if self.direction == 'E':
            self.rect.x = self.rect.x+self.speed
        if self.direction == 'W':
            self.rect.x = self.rect.x-self.speed
        if self.direction == 'N':
            self.rect.y = self.rect.y-self.speed
        if self.direction == 'S':
            self.rect.y = self.rect.y+self.speed

    def collided(self, other_rect):
        #Return True if self collided with other_rect
        return self.rect.colliderect(other_rect)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
