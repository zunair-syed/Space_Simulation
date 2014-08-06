"""
Space Simulation
By: Zunair Syed
Framework/Library: Pygame
Language: Python

Features:
1) Approximate size of each planet correctly scaled to fit our screen
2) Mathematical Gravity calulations aqquired from detailed gravitational pull calculations, involving distance and size of planet variables
3) Acceleration of our Spaceship, and any moons floating around is very accurate

Concepts Utilized:
-Object Oriented Concepts Applied --> Classes, Objects, Instantiation etc
-Basic Programming Concepts --> While/For loops, Conditional Statements, methods etc
-Pygame Library utilized --> Events, Canvas, window Handling etc

Project Not Finished.
-Need to add: Sprites for each planet, so there is a animation of the planet revolving on it's self
-Collisions: Collision, when spacehip collides with an object
-Add more planets, and pluto
"""



# 1 - Import library
import pygame, sys, math
from pygame.locals import *


"""
Class for Astrioids: Right now this is used for Moon objects
eg, earth's moon, mars's moons
"""
class Astroid:
    xPos=0
    yPos=0
    width=0
    height=0
    velX=0
    velY=0

    def __init__(self,  name,  xPos2,  yPos2,  width,  height, startingVelX ):
        self.xPos=xPos2
        self.yPos=yPos2
        self.width=width
        self.height=height
        self.velX=startingVelX

    def getX(self):
        return self.xPos

    def getY(self):
        return self.yPos


     
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def updatePos(self, boundingPlanetAccX,boundingPlanetAccY):
        self.velX+=boundingPlanetAccX
        self.velY+=boundingPlanetAccY                      
        self.xPos+=self.velX
        self.yPos-=self.velY
        
        

"""
Planet Class:Utilized for all planets and sun
"""
class Planet:
    xPos=0
    yPos=0
    width=0
    height=0
    planAccX=0
    planAccY=0
    gravityConst=0
    
    def __init__(self,  name,  xPos2,  yPos2,  width,  height ):
        self.xPos=xPos2
        self.yPos=yPos2
        self.width=width
        self.height=height
        self.gravityConst=width*height*.044444444444444 #0.4444 is a constant that I mathematically calculated by scaling down the real gravitiational constant
    
    def getX(self):
        return self.xPos

    def getY(self):
        return self.yPos
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height

    def getGravity(self):
        return self.gravityConst



    def getAccelarationToPlanX(self, playerX,playerY,playerWidth,playerHeight):
        disPlanToX=math.fabs((playerX + (playerWidth/2)) - (self.xPos + (self.width/2)))
        disPlanToY=math.fabs((playerY + (playerHeight/2)) - (self.yPos + (self.height/2)))
        disPlan= math.sqrt((disPlanToX**2) + (disPlanToY**2))
        planAccX=0
        if disPlan<500:
            if playerX + (playerWidth/2)<= self.xPos + (self.width/2):
                    #if disPlanToX>75:
                        planAccX=self.gravityConst/(disPlan**2)
            if playerX + (playerWidth/2)>= self.xPos +(self.width/2):
                    #if disPlanToX>75:
                        planAccX=-self.gravityConst/(disPlan**2)
        return planAccX



    def getAccelarationToPlanY(self, playerX, playerY, playerWidth, playerHeight):
        disPlanToX=math.fabs((playerX + (playerWidth/2)) - (self.xPos + (self.width/2)))
        disPlanToY=math.fabs((playerY + (playerHeight/2)) - (self.yPos + (self.height/2)))
        disPlan= math.sqrt((disPlanToX**2) + (disPlanToY**2)) 
        planAccY=0
        if disPlan<500:
            if playerY + (playerHeight/2)<= self.yPos+(self.height/2):
                    #if disPlanToY>75:
                        planAccY=-self.gravityConst/(disPlan**2)
            if playerY + (playerHeight/2)>= self.yPos +(self.height/2):
                    #if disPlanToY>75:
                        planAccY=+self.gravityConst/(disPlan**2)

        return planAccY






 
# 2 - Initialize the game
pygame.init()
width, height = 1200, 500
screen=pygame.display.set_mode((width, height))

# 3 - Load images
player = pygame.image.load("spaceship.png")
playerWidth=70
playerHeight=80

player= pygame.transform.scale(player, (playerWidth, playerHeight))

bg = pygame.image.load("background.png")

earth = pygame.image.load("earth.png")
earth= pygame.transform.scale(earth, (150, 150))

mars = pygame.image.load("mars.png")
mars= pygame.transform.scale(mars, (80, 80))

venus = pygame.image.load("venus.png")
venus= pygame.transform.scale(venus, (140, 140))

mercury = pygame.image.load("mercury.png")
mercury= pygame.transform.scale(mercury, (57, 57))

sun = pygame.image.load("sun.png")
sun= pygame.transform.scale(sun, (500, 500))


earthmoonpic = pygame.image.load("rock.png")
earthmoonpic= pygame.transform.scale(earthmoonpic, (50, 50))

marsmoonpic = pygame.image.load("rock.png")
marsmoonpic= pygame.transform.scale(marsmoonpic, (20, 20))


boostleft= pygame.image.load("boostleft.png")
boostleft= pygame.transform.scale(boostleft, (30, 15))
boostright= pygame.image.load("boostright.png")
boostright= pygame.transform.scale(boostright, (30, 15))
boostdown= pygame.image.load("boostdown.png")
boostdown= pygame.transform.scale(boostdown, (15, 30))
boostup= pygame.image.load("boostup.png")
boostup= pygame.transform.scale(boostup, (15, 30))

whichboost="nothing"

playerX=600
playerY=100
velX=0
velY=0
accX=0
accY=0

disPlanToX=0
disPlanToY=0


mercuryPlanet =Planet("mercury",250 ,221, 57, 57)
venusPlanet =Planet("venus",420 ,180, 140, 140)

earthPlanet =Planet("earth",775 ,175, 150, 150)
earthMoon=Astroid("earthMoon",  850,  60,  50,  50, 3.1)

marsPlanet =Planet("mars",1100 ,210, 80, 80)#250
marsMoon1=Astroid("marsMoon1",  1129,  140,  20,  20, 2.0)
marsMoon2=Astroid("marsMoon2",  1129,  340,  20,  20,2.0)#320

sunPlanet =Planet("sun",-350 ,0, 500, 500)


TotalGravityAccX=0
TotalGravityAccY=0

# 4 - keep looping through
while True:
        # 5 - clear the screen before drawing it again
        screen.fill(0)
        for event in pygame.event.get():
                if event.type==pygame.QUIT:
                        # if it is quit the game
                        pygame.quit() 
                        sys.exit()
                if event.type==KEYDOWN:
                        if event.key==K_LEFT:
                                accX=-0.15
                                whichboost="left"
                        if event.key==K_RIGHT:
                                accX=0.15
                                whichboost="right"
                        if event.key==K_UP:
                                accY=0.15
                                whichboost="up"
                        if event.key==K_DOWN:
                                accY=-0.15
                                whichboost="down"
                        if event.key==K_SPACE:
                                whichboost="brake"
                                                      
                if event.type==KEYUP:
                        if event.key==K_LEFT:
                                accX=0
                                whichboost="nothing"
                        if event.key==K_RIGHT:
                                accX=0
                                whichboost="nothing"
                        if event.key==K_UP:
                                accY=0
                                whichboost="nothing"
                        if event.key==K_DOWN:
                                accY=0
                                whichboost="nothing"
                        if event.key==K_SPACE:
                                accY=0
                                accX=0
                                whichboost="nothing"       

      
       
        earthMoon.updatePos(  earthPlanet.getAccelarationToPlanX(earthMoon.getX(),earthMoon.getY(),earthMoon.getWidth(),earthMoon.getHeight())   ,    earthPlanet.getAccelarationToPlanY(earthMoon.getX(),earthMoon.getY(),earthMoon.getWidth(),earthMoon.getHeight()) )

        marsMoon1.updatePos(  marsPlanet.getAccelarationToPlanX(marsMoon1.getX(),marsMoon1.getY(),marsMoon1.getWidth(),marsMoon1.getHeight())   ,    marsPlanet.getAccelarationToPlanY(marsMoon1.getX(),marsMoon1.getY(),marsMoon1.getWidth(),marsMoon1.getHeight()) )
        marsMoon2.updatePos(  marsPlanet.getAccelarationToPlanX(marsMoon2.getX(),marsMoon2.getY(),marsMoon2.getWidth(),marsMoon2.getHeight())   ,    marsPlanet.getAccelarationToPlanY(marsMoon2.getX(),marsMoon2.getY(),marsMoon2.getWidth(),marsMoon2.getHeight()) )


        TotalGravityAccX=sunPlanet.getAccelarationToPlanX(playerX,playerY,70,80)+mercuryPlanet.getAccelarationToPlanX(playerX,playerY,70,80)+venusPlanet.getAccelarationToPlanX(playerX,playerY,70,80)+earthPlanet.getAccelarationToPlanX(playerX,playerY,70,80)+marsPlanet.getAccelarationToPlanX(playerX,playerY,70,80)
        TotalGravityAccY=sunPlanet.getAccelarationToPlanY(playerX,playerY,70,80)+mercuryPlanet.getAccelarationToPlanY(playerX,playerY,70,80)+venusPlanet.getAccelarationToPlanY(playerX,playerY,70,80)+earthPlanet.getAccelarationToPlanY(playerX,playerY,70,80)+marsPlanet.getAccelarationToPlanY(playerX,playerY,70,80)
        velX+=accX+TotalGravityAccX
        velY+=accY+TotalGravityAccY                      
        playerX+=velX
        playerY-=velY
        
 

                
        #color = (255,255,255)
        #planetX,planetY = pygame.mouse.get_pos()
        #planetX, planetY=275,275
        screen.blit(bg, (0,0))        
        screen.blit(earth, (earthPlanet.getX(),earthPlanet.getY()))
        screen.blit(mars, (marsPlanet.getX(),marsPlanet.getY()))
        screen.blit(venus, (venusPlanet.getX(),venusPlanet.getY()))
        screen.blit(mercury, (mercuryPlanet.getX(),mercuryPlanet.getY()))
        screen.blit(sun, (sunPlanet.getX(),sunPlanet.getY()))


        screen.blit(earthmoonpic, (earthMoon.getX(),earthMoon.getY()))
        screen.blit(marsmoonpic, (marsMoon1.getX(),marsMoon1.getY()))        
        screen.blit(marsmoonpic, (marsMoon2.getX(),marsMoon2.getY()))        

         
        screen.blit(player, (playerX,playerY))
        if whichboost!="nothing":
                if whichboost=="up":
                        screen.blit(boostup, (playerX+28,playerY+69))
                if whichboost=="down":
                        screen.blit(boostdown, (playerX+28,playerY-20))
                if whichboost=="right":
                        screen.blit(boostright, (playerX-30,playerY+23))
                        screen.blit(boostright, (playerX-30,playerY+53))                       
                if whichboost=="left":
                        screen.blit(boostleft, (playerX+70,playerY+23))
                        screen.blit(boostleft, (playerX+70,playerY+53))
                if whichboost=="brake":
                        if velX >0:
                            accX=-0.5
                        elif velX < 0:
                            accX=+0.5

                        if (velX<0.5 and velX>0) or (velX>-0.5 and velX<0):
                            velX=0
                        if (velY<0.5 and velY>0) or (velY>-0.5 and velY<0):
                            velX=0

                        if velY >0:
                            accY=-0.5
                        elif velY < 0:
                            accY=+0.5 
        pygame.display.update()#creates smotheness
        pygame.time.delay(30)





   
