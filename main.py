import pygame
import os
pygame.init()

#Colors
white = (255,255,255)
red = (255,0,0)
gold = (255,215,0)
silver = (155,20,20)
black = (0,0,0)
green = (0,255,0)
blue = (0,0,255)
brown = (210,105,30)

#Initial Setup
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300,100)
directory = os.getcwd()
screenWidth = 800
screenHeight = 800
win = pygame.display.set_mode((screenWidth,screenHeight), pygame.RESIZABLE)
pygame.display.set_caption("Orbits")
clock = pygame.time.Clock()
planets = pygame.image.load(directory + r"/img/planets2.png")
pygame.mixer.music.load(directory + r"\sounds\buttonPush.mp3")

#Global variables
bodyList = []
run = True

class Center(object):
    def __init__(self, massMult):
        self.x = int(screenWidth / 2)
        self.y = int(screenHeight / 2)
        #Figure out how to scale the mass
        self.mass = 100 * massMult
        self.radius = self.mass
        self.color = red

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

class Orbital(object):
    def __init__(self, x, y, massMult):
        #self.surf = pygame.Surface((20, 20))
        self.x = x
        self.y = y
        self.mass = 15 * massMult
        self.radius = self.mass
        self.color = blue
    
    def draw(self):
        #pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        
        #A and B are the location it will be placed
        #C and D are the cropped part of the image from the top left corner
        #E and F define the image size
        #For testing with just a red circle, comment out this line and uncomment line 51
        win.blit(planets, (self.x, self.y), (25, 5, 120, 120))

class Button(object):
    def __init__(self, x, y, width, height, text =""):
        self.color = silver
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
    
    def draw(self, outline = None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != "":
            font = pygame.font.SysFont('Calibri', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

but = Button(10, 10, 150, 60, "Reset")
sun = Center(1)
origRadius = sun.radius

def clear():
    bodyList.clear()
    sun.radius = origRadius
    redrawGameWindow()

def redrawGameWindow():
    win.fill(black)
    x = 0
    for x in range(len(bodyList)):
        bodyList[x].draw()
    sun.draw()
    but.draw()
    pygame.display.update()

mouse = pygame.mouse.get_pos()
click = pygame.mouse.get_pressed()

while run:
    clock.tick(144)
    for event in pygame.event.get():
        if pygame.mouse.get_pressed()[0]:
            pygame.mixer.music.play(0)
            clickPos = pygame.mouse.get_pos()
            clickColor = win.get_at(clickPos)
            if but.isOver(clickPos):
                clear()
            elif clickColor == black: #Don't allow multiple objects to spawn ontop of each other
                bodyList.append(Orbital(clickPos[0] - 60, clickPos[1] - 60, 1)) #Append a planet object to list of bodies
        if event.type == pygame.VIDEORESIZE: #Allow for resizing
            screenHeight = event.h
            screenWidth = event.w
            surface = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
            #Update the sun's position when the video is resized
            sun.x = int(screenWidth / 2)
            sun.y = int(screenHeight / 2)
        if event.type == pygame.MOUSEBUTTONDOWN: #Scrolling in and out
            if event.button == 4: #Mouse wheel down
                if sun.radius > 0: #If the radius becomes negative it crashes
                    sun.radius -= 5
            if event.button == 5: #Mouse wheel up
                  sun.radius += 5
        if event.type == pygame.QUIT:
            run = False
    redrawGameWindow()