import pygame


class Button():
    def __init__(self,x,y,image,scale):
        width=image.get_width()
        height=image.get_height()
        self.image=pygame.transform.scale(image,(int( width * scale ), int(height * scale)))

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft =(x,y)
        self.clicked = False


    def draw(self,surface):
        action =False
        #geting mouse positions
        pos =pygame.mouse.get_pos()
        #print(pos)
        #checking if mouse is clicked
        if self.rect.collidepoint(pos):
            #print('Hover')
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                #print('clicked')
                action=True
                self.clicked=True
            
        if pygame.mouse.get_pressed()[0]==0:
            self.clicked=False

     
        surface.blit(self.image, (self.rect.x,self.rect.y))

        return action