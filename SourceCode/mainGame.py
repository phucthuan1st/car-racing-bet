import random

import pygame

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(10)

# creat the screen
screen = pygame.display.set_mode((1280, 720))

#Title and Icon
pygame.display.set_caption("Car Racing")
icon = pygame.image.load("../image/racing.png")
pygame.display.set_icon(icon)



# Common Variables
SpriteDelay = 10

#Start and Finish
StartImg = pygame.image.load("../image/2.png")
StartX = 0
StartY = 100
FinishImg = pygame.image.load("../image/4.png")
FinishX = 1205
FinishY = 100

#You Win
WinImg = pygame.image.load("../image/YouWin.png")
RankingImg = pygame.image.load("../image/panel.jpg")
WinX = 450
WinY = 230
PanelX = 300
PanelY = 100
RacingLen = 1200


#You Lose
LoseImg = pygame.image.load("../image/YouLose.png")
LoseX = 450
LoseY = 130


#Road
RoadImg = pygame.image.load("../image/3.png")
RoadX = 20
RoadY = 100
RoadX_change = 100
num_of_road = 15

#Buff
BuffSpeedImg = pygame.image.load("../image/buff.png")
BuffSpeedX = random.randrange(350, RacingLen, 100)
BuffSpeedY = 105
BuffSpeedY_change = 85
number_of_buffspeed = 6

# Game Classes

class MyCar():
    def __init__(self, No, image):
        self.No = No
        self.image = image
        self.x = 10
        self.y = 100 + No*85
        self.buffX = 0
        self.buffCount = 0
        self.buff = None
        self.isGoBack = False
        self.isStun = False
        self.isFinish = False
        self.timer = 0
        self.rank = 0

        self.xChange = random.randrange(10, 15, 1) / 10

    def Update(self):
        # update timer for go back
        global currentRank
        global selectedCar

        if self.isGoBack:
            self.timer -= 1
        if self.timer <= 0 and self.isGoBack:
            self.isGoBack = False
            self.xChange *= -1

        if self.isStun:
            self.timer -= 1
        if self.timer <= 0 and self.isStun:
            self.isStun = False
            self.xChange = random.randrange(10, 15, 1) / 10

        if not self.isGoBack and not self.isStun:
            self.x += self.xChange

        elif self.x > 10:
            self.x += self.xChange

        if self.x <= 0:
            self.x = 10
        if self.x >= RacingLen:
            self.x = RacingLen
            if self.rank == 0:
                self.rank = currentRank
                if currentRank == 1:
                    if self.No == selectedCar:
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound('../soundFX/winner.mp3'))
                    else:
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound('../soundFX/lose.mp3'))
                currentRank += 1


        if self.buffX > 0 and self.x >= self.buffX:
            if self.buff.type == 0:
                pygame.mixer.Channel(4 + self.No).play(pygame.mixer.Sound('../soundFX/speed-up.mp3'))
            elif self.buff.type == 1:
                pygame.mixer.Channel(4 + self.No).play(pygame.mixer.Sound('../soundFX/speed-down.mp3'))
            elif self.buff.type == 2:
                self.x = 10
                pygame.mixer.Channel(4 + self.No).play(pygame.mixer.Sound('../soundFX/quaylai.mp3'))
            elif self.buff.type == 3:
                self.xChange *= -1
                self.isGoBack = True
                self.timer = 50
                pygame.mixer.Channel(4 + self.No).play(pygame.mixer.Sound('../soundFX/quayxe.mp3'))
            elif self.buff.type == 4:
                self.xChange = 0
                self.isStun = True
                self.timer = 50
                pygame.mixer.Channel(4 + self.No).play(pygame.mixer.Sound('../soundFX/broken.mp3'))
            elif self.buff.type == 5:
                self.x = RacingLen
                pygame.mixer.Channel(4 + self.No).play(pygame.mixer.Sound('../soundFX/tele.mp3'))
            else:
                self.xChange += self.buff.xChange

            self.buffX = 0
            self.buff = None

    def Draw(self, screen):
        if self.isGoBack:
            flipImage = pygame.transform.flip(self.image, True, False)
            screen.blit(flipImage, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))
        if self.x >= 200 and self.x < RacingLen and self.buffX == 0 and self.buffCount < 2:
            # random in range position X of Car + 100 => Car X + 500
            maxRange = int(self.x) + 500
            if maxRange > 1000:
                maxRange = 1000

            self.buffX = random.randrange(int(self.x) + 100, maxRange, 100)
            type = random.randint(0,5)
            self.buff = MyBuff(type, self.buffX, BuffSpeedY + self.No * BuffSpeedY_change)
            self.buffCount += 1

        if self.buffX > 0 and self.buff:
            self.buff.Draw(screen)

class MyBuff():
    def __init__(self, type, x, y):
        self.x = x
        self.y = y
        self.type = type
        self.xChange = 0
        if type == 0:
            self.image = pygame.image.load("../image/buff.png")
            self.xChange = 1
        elif type == 1:
            self.image = pygame.image.load("../image/exhaust.png")
            self.xChange = -0.5
        elif type == 2:
            self.image = pygame.image.load("../image/ve.png")
        elif type == 3:
            self.image = pygame.image.load("../image/turn.png")
        elif type == 4:
            StunImg = pygame.image.load("../image/stun.png")
            self.image = pygame.transform.scale(StunImg, (50, 50))
        elif type == 5:
            FinishLineImg = pygame.image.load("../image/bùa về đích.png")
            self.image = pygame.transform.scale(FinishLineImg, (60, 60))
        else:
            self.image = pygame.image.load("../image/buff.png")
            self.xChange = 1

    def Draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Cheer():
    def __init__(self, name, imgNum, x, y):
        self.images = []
        self.imageIndex = 0
        self.x = x
        self.y = y
        self.delay = SpriteDelay
        for i in range(imgNum):
            self.images.append(pygame.image.load("../image/{0}{1}.png".format(name, i)))

    def Draw(self, screen):
        screen.blit(self.images[self.imageIndex], (self.x, self.y))
        # delay for draw image
        self.delay -= 1
        if self.delay == 0:
            self.imageIndex += 1
            self.delay = SpriteDelay
            if self.imageIndex == len(self.images):
                self.imageIndex = 0

def DrawStart():
    screen.blit(StartImg, (StartX, StartY))

def DrawFinish():
    screen.blit(FinishImg, (FinishX, FinishY))

# draw ranking panel
def Win():
    global winDelay
    if winDelay > 0:
        screen.blit(WinImg, (WinX, WinY))
        winDelay -= 1


def Lose():
    global winDelay
    global selectedCar

    if winDelay > 0:
        screen.blit(LoseImg, (LoseX, LoseY))
        winDelay -= 1


def ShowRanking(Cars):
    # Stop background song
    pygame.mixer.Channel(0).stop()
    # Play clap sound
    global playedClap
    if not playedClap:
        pygame.mixer.Channel(3).play(pygame.mixer.Sound('../soundFX/clap.mp3'))
        playedClap = True

    # Draw panel
    rankingImg = pygame.transform.scale(RankingImg, (700, 500))
    screen.blit(rankingImg, (PanelX, PanelY))

    # init font
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)

    for i in range(len(Cars)):
        rankText = myfont.render('Rank {0}:'.format(i+1), False, (255,0,0))
        screen.blit(rankText, (PanelX + 150, PanelY+180+i*50))
        carsImg = pygame.transform.scale(Cars[i].image, (50, 50))
        screen.blit(carsImg, (PanelX + 500, PanelY+170+i*50))

def Road(RoadX, RoadY):
    i = 0
    for i in range(num_of_road):
        screen.blit(RoadImg, (RoadX, RoadY))
        RoadX += RoadX_change

def SortRanking(car):
    return car.rank

def DrawTrees(screen):
    Trees = []
    for i in range(6):
        Trees.append(pygame.image.load('../image/tree{0}.png'.format(i%2)))

    for i in range(6):
        screen.blit(Trees[i], (450+i*60, 20))

    for i in range(6):
        screen.blit(Trees[i], (450+i*60, 600))

def InitCheers(x, y):
    for i in range(6):
        if i % 2 == 0:
            Cheers.append(Cheer("cheer", 2, x + i * 60, y))
        else:
            Cheers.append(Cheer("cheerblue", 2, x + i * 60, y))

def DrawCheers(screen):
    for i in range(len(Cheers)):
        Cheers[i].Draw(screen)

def quitGame():
    # stop music
    pygame.mixer.Channel(0).stop()


    # clear all global variables
    Cars.clear()
    Cheers.clear()


def initGame(setName):
    global currentRank
    global playedClap
    global selectedCar
    global winDelay
    global youWin

    currentRank = 1
    playedClap = False
    selectedCar = -1
    winDelay = 200
    youWin = False

    for i in range(6):
        image = pygame.image.load("../image/set{0}/car{1}.png".format(setName,i+1))
        car = MyCar(i, image)
        Cars.append(car)

    InitCheers(50, 20)
    InitCheers(850, 20)
    InitCheers(50, 600)
    InitCheers(850, 600)

    # Play background song
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('../soundFX/race3.mp3'), -1)

# Global Game Variables
Cars = []
Cheers = []
# will increase when a car finish
currentRank = 1
playedClap = False
selectedCar = -1
winDelay = 200
youWin = False

#Game Loop
def runGame(selectedNumber, setName, money):
    running = True
    initGame(setName)
    global selectedCar
    global youWin

    selectedCar = selectedNumber

    while running:
        # RGB
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quitGame()
                    running = False

        i = 0
        for i in range(num_of_road):
            Road(RoadX, RoadY)

        # Cheers
        DrawCheers(screen)
        DrawTrees(screen)

        DrawStart()
        DrawFinish()
        for i in range(len(Cars)):
            Cars[i].Update()
            Cars[i].Draw(screen)

        # # Draw win panel
        if currentRank > 1:

            winner = None
            for i in range(len(Cars)):
                if Cars[i].rank == 1:
                    winner = Cars[i]
                    break
            # because Number of Car from index 0
            # selectedCar from index 1
            if winner != None and winner.No+1 == selectedCar:
                Win()
                youWin = True
            else:
                Lose()

        # Draw Ranking
        if currentRank > len(Cars):
            # sort rank for car list
            Cars.sort(key=SortRanking)
            ShowRanking(Cars)

        pygame.display.update()
    if youWin:
        money += 1160
    else:
        money -= 1000
    return money

