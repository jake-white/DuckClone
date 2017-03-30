import pygame, sys, time, random
from gametime import GameTimer
from duck import Duck


class Game():
    playerX = 0
    playerY = 0
    screenX = 600
    screenY = 600
    playerSpeed = 4
    score = 0
    maxDucks = 7
    duckList = []
    lastDuckSpawn = 0
    randomDuckTimer = 1000
    randomDuckMin = 500
    randomDuckMax = 1000
    duckSpeedMin = -2
    duckSpeedMax = 2
    duckSize = 40
    crossHairSize = 30
    startTime = 0
    timeLimit = 10000
    def __init__(self):
        self.loop = GameTimer(self.tick, 10)
        self.screen = self.configureScreen()

    def start(self):
        self.startTime = self.timeInMillis()
        self.loop.start()

    def tick(self):
        self.generateDucks()
        self.eventCatcher()
        self.physics()
        self.draw()
        pygame.display.update()

    def draw(self):
        self.screen.fill((150, 220, 235))
        grass = pygame.Rect(0, self.screenY - self.screenY/5, self.screenX, self.screenY)
        pygame.draw.rect(self.screen, (50, 175, 50), grass, 0)
        upcross = pygame.Rect(self.playerX - 2, self.playerY - self.crossHairSize, 4, self.crossHairSize*2)
        sidecross = pygame.Rect(self.playerX - self.crossHairSize, self.playerY - 2, self.crossHairSize*2, 4)
        pygame.draw.rect(self.screen, (255, 50, 0), upcross, 0)
        pygame.draw.rect(self.screen, (255, 50, 0), sidecross, 0)

        crosssquare = pygame.Rect(self.playerX - self.crossHairSize/2, self.playerY - self.crossHairSize/2, self.crossHairSize, self.crossHairSize)
        pygame.draw.circle(self.screen, (255, 0, 0), (self.playerX, self.playerY),  self.crossHairSize-6, 3)

        crosshair = pygame.Rect(self.playerX, self.playerY, 1, 1)
        print(len(self.duckList))
        for duck in self.duckList:
            duckDraw = pygame.Rect(duck.getX(), duck.getY(), self.duckSize, self.duckSize)
            pygame.draw.rect(self.screen, (255, 255, 100), duckDraw, 0)
            if(self.KEY_SHOOT):
                if(duckDraw.colliderect(crosshair)):
                    self.duckList.remove(duck)
                    self.score+=1

        myfont = pygame.font.SysFont("monospace", 20)
        # render text
        self.timeLeft = self.timeLimit - (self.timeInMillis() - self.startTime)
        secondsTotal = self.timeLeft / 1000
        seconds = str(int(secondsTotal %60))
        minutes = str(int(secondsTotal/60))
        scoreLabel = myfont.render("Score: {}".format(self.score), 1, (255,0,0))
        timeLabel = myfont.render("{} : {}".format(minutes, seconds.zfill(2)), 1, (255,0,0))
        self.screen.blit(scoreLabel, (10, 10))
        self.screen.blit(timeLabel, (10, 40))

    def configureScreen(self):
        #this creates and returns a pygame screen
        pygame.init()
        screen = pygame.display.set_mode((self.screenX, self.screenY), pygame.RESIZABLE)
        pygame.display.set_caption("Duck Hunt")
        return screen

    def adjustScreen(self, eventDict):
        self.screenX = eventDict[0]
        self.screenY = eventDict[1]
        self.screen = pygame.display.set_mode(eventDict)

    def physics(self):
        if(self.KEY_SLOW):
            self.effectiveSpeed = int(self.playerSpeed/3)
        else:
            self.effectiveSpeed = self.playerSpeed

        self.playerX -= self.KEY_LEFT*self.effectiveSpeed
        self.playerX += self.KEY_RIGHT*self.effectiveSpeed
        self.playerY -= self.KEY_UP*self.effectiveSpeed
        self.playerY += self.KEY_DOWN*self.effectiveSpeed
        for duck in self.duckList:
            duck.fly()
            if(duck.getX() > self.screenX or duck.getX() < -self.duckSize or duck.getY() + self.duckSize > self.screenY - self.screenY/5 or duck.getY() < -self.duckSize):
                self.duckList.remove(duck)


    def generateDucks(self):
        if(len(self.duckList) < self.maxDucks):
            if(self.timeInMillis() - self.lastDuckSpawn > self.randomDuckTimer):
                self.lastDuckSpawn = self.timeInMillis()
                self.randomDuckTimer = random.randint(self.randomDuckMin, self.randomDuckMax)
                duckSpeedX = random.randint(self.duckSpeedMin, self.duckSpeedMax)
                duckSpeedY = random.randint(self.duckSpeedMin, -1)
                randomPosX = random.randint(self.duckSize, self.screenX-self.duckSize)
                posY  = self.screenY - self.screenY/5 - self.duckSize - 2
                self.duckList.append(Duck(randomPosX, posY, duckSpeedX, duckSpeedY))

    def eventCatcher(self):
        #catching pygame generated events
        for event in pygame.event.get():
            #closes both the pygame module and forces the program to end
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                self.adjustScreen(event.dict['size'])

        self.KEY_UP = pygame.key.get_pressed()[eval("pygame.K_w")]
        self.KEY_DOWN = pygame.key.get_pressed()[eval("pygame.K_s")]
        self.KEY_LEFT  = pygame.key.get_pressed()[eval("pygame.K_a")]
        self.KEY_RIGHT = pygame.key.get_pressed()[eval("pygame.K_d")]
        self.KEY_SHOOT = pygame.key.get_pressed()[eval("pygame.K_SPACE")]
        self.KEY_SLOW = pygame.key.get_pressed()[eval("pygame.K_LSHIFT")]

    def timeInMillis(self):
        #returns the current time in milliseconds
        return time.time() * 1000