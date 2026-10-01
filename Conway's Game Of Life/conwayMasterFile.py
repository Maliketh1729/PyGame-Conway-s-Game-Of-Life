import time, sys, os, pygame, random, pickle
from pygame.locals import *
from pygame.math import Vector2
pygame.init() #Initializes pyGame
clock = pygame.time.Clock()         #Limits FPS - once per spacebar click
#Much of this code was imported from my personal platformer project and then my battleships, so it may be a little messy

ScreenSizeObj = pygame.display.Info()
worldx, worldy = ScreenSizeObj.current_w,ScreenSizeObj.current_h
screen = pygame.display.set_mode([worldx, worldy])
pygame.display.set_caption("Conway's Game Of Life - Now with even more spaghetti!")
tx,ty = 64,64

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.alive = True

    def update(self):
        pressed_keys = pygame.key.get_pressed()               
        mousePos = pygame.mouse.get_pos() #use rect.collidepoint for detection
        if pressed_keys[K_SPACE]:
            hit = False
            for pixel in pixel_list:                                                                     
                if pixel.rect.collidepoint(mousePos) == True:    #If mouse position intersects the rect box:

                    #delete pixel
                    hit = True
                    print("Pixel will be deleted")
                    time.sleep(0.1)

            if hit == False:
                pass
                print("Pixel will be placed")
                #place pixel here


        elif pressed_keys[K_ESCAPE]:
            running = False



class Pixel(pygame.sprite.Sprite):     #reusing the basics of my ship code for this
    def __init__(self, xloc,yloc, imgw, imgh, img):
        super().__init__()
        self.image = pygame.image.load("Images/livePixel.jpg").convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.y = yloc
        self.rect.x = xloc
        imgw = 8
        imgh = 8
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        #to place on grid, have div by 8, round to full value and then multiply + place on screen

class DeadPixel(pygame.sprite.Sprite):     #reusing the basics of my ship code for this
    def __init__(self, xloc,yloc, imgw, imgh, img):
        super().__init__()
        self.image = pygame.image.load("Images/deadPixel.jpg").convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.y = yloc
        self.rect.x = xloc
        imgw = 8
        imgh = 8
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        #to place on grid, have div by 8, round to full value and then multiply + place on screen

class Level:
    def pixel(tx, ty):
        pixel_list = pygame.sprite.Group()
        hshloc = []
        vshloc = []
        i = 0
        #Place spike locations for stage 1 here
        hshloc.append((tx, ty, 4))  #5 LONG PIXEL TEST        

        while i < len(hshloc):                                    
            j = 0
            while j <= hshloc[i][2]:  #repeat as long as no exceeding index 2 (how many times it tiles)
                pix = Pixel((hshloc[i][0] + (j * (8))), hshloc[i][1], 8, 8, pygame.image.load("Images/livePixel.jpg"))  #Change distance between ships with (j*tx)
                pixel_list.add(pix)        #^move this to            ^here to flip the tiling vertically
                j = j + 1                 
            i = i + 1
        i = 0
        return pixel_list
    def clearList():
        pixel_list = []
        empty_list = []
        
    def deadPixel(tx, ty):
        dead_pixel_list = pygame.sprite.Group()
        hshloc = []
        vshloc = []
        i = 0
        #Place spike locations for stage 1 here
        hshloc.append((0, 0, 100))        

        while i < len(hshloc):                                    
            j = 0
            while j <= hshloc[i][2]:  #repeat as long as no exceeding index 2 (how many times it tiles)
                deadpix = DeadPixel((hshloc[i][0] + (j * (8))), hshloc[i][1], 8, 8, pygame.image.load("Images/deadPixel.jpg"))  #Change distance between ships with (j*tx)
                dead_pixel_list.add(deadpix)        #^move this to            ^here to flip the tiling vertically
                j = j + 1                 
            i = i + 1
        i = 0
        return dead_pixel_list
    def clearList():
        pixel_list = []
        dead_pixel_list = []
        empty_list = []

#I feel like the best approach is to have every single possible pixel location to be  a 'dead pixel' and then change it to a live pixel if it meets conditions
        
Level.clearList()
global pixel_list 
pixel_list = Level.pixel(tx, ty)
global dead_pixel_list 
dead_pixel_list = Level.deadPixel(tx, ty)

player = Player()

running, colGen = True, True
while running:
    numNeighbors = 0
#make collision detection based on if the 'large' hitbox of the pix overlaps the 'small' pixel

    for pixel in pixel_list:                                          #for every alive pixel:
        pixelBigRect = pixel.rect.inflate(4,4)                            #create a big pixel with a larger collision
        pixels = pixel_list.sprites()                                     #Turn all pixels into a sprite list
        for colPixel in pixels:                                              #compare each pixel with a particular pixel
            if pygame.sprite.collide_mask(pixelBigRect, colPixel):           #If they collide:
                numNeighbors += 1                                            #neighbors is increased by one
        if numNeighbors < 2:
            pixel_list.remove(pixel)
            dead_pixel_ships.add(pixel)
        elif numNeighbors > 3:
            pixel_list.remove(pixel)
            dead_pixel_ships.add(pixel)
#I'm going to  have to shange mask to spritecollide as its more memory-efficient + doesnt cause random crashes
    for deadPixel in dead_pixel_list:
        deadPixelBigRect = pixel.rect.inflate(4,4)
        pixels = pixel_list.sprites()
        for colPixel in pixels:
            if pygame.sprite.collide_mask(deadPixelBigRect, colPixel): #this is somehow breaking python
                numNeighbors += 1
        if numNeighbors == 3:
            #reuse deadShipAliveShip code
            dead_pixel_list.remove(deadPixel)
            pixel_ships.add(deadPixel) 

    clock.tick(60)  #later replace with only progressing when key pressed
    player.update()
    pixel_list.draw(screen)
    dead_pixel_list.draw(screen)
    

    
    pygame.display.update()
    screen.fill("blue")#blue for testing
quit()
