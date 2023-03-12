import pygame
from sys import exit
from random import randint

#initialize
pygame.init()
screen = pygame.display.set_mode((800,450))
pygame.display.set_caption('Jungle Rush')
Icon = pygame.image.load('JR_Data/Graphics/Fire.png')
pygame.display.set_icon(Icon)
#clock
timer = pygame.time.Clock()
TextF = pygame.font.Font('JR_Data/Font/Tiger.otf',50)
#Audio
Jump = pygame.mixer.Sound('JR_Data/Audio/Jump.mp3')
Jump.set_volume(0.3)
Struck = pygame.mixer.Sound('JR_Data/Audio/Struck.mp3')
Struck.set_volume(0.3)
BGM = pygame.mixer.Sound('JR_Data/Audio/BGM.mp3')
Running = False
Runtime = 0
FirstRun = True
Speed = 7
Score = 0

#Ground scrolling
def BackdropScroll(G_rect):
    if G_rect.x <= -800:
        G_rect.x = 800
    screen.blit(Ground_surf,G_rect)
    G_rect.x -= Speed

#Enemy scrolling
def EnemyMovement(EnemyList):
    if EnemyList:
        for Enemy_rect in EnemyList:
            Enemy_rect.x -= Speed
            if Enemy_rect.y == 280:
                screen.blit(Flytrap_surf,Enemy_rect)
            else:
                screen.blit(Eagle_surf,Enemy_rect)
        EnemyList = [ Enemy for Enemy in EnemyList if Enemy.x > -100]
        return EnemyList
    else: return []

#Collision
def Collision(Char, EnemyList):
    if EnemyList:
        for Enemy_rect in EnemyList:
            if Enemy_rect.y != 280 and Char.collidepoint(Enemy_rect.bottomleft):
                BGM.stop()
                Struck.play()
                return False
            elif Char.collidepoint(Enemy_rect.center):
                BGM.stop()
                Struck.play()
                return False
            else:
                return True
    else:
        return True

#Character animations
def CharAnim():
    global Char_surf, Char_move
    if Char_rect.bottom < 370:
        Char_surf = Char_jump
    else:
        Char_move += 0.12
        if Char_move >= len(Char_run):
            Char_move = 0
        Char_surf = Char_run[int(Char_move)]
#Score Screen
def ScoreCalc():
        global Score
        Score = (int)((pygame.time.get_ticks() - Runtime)/500)
        Score_surf = TextF.render(f' Score: {Score} ', True, 'Gold').convert_alpha()
        Score_rect = Score_surf.get_rect(midtop= (400,10))
        pygame.draw.rect(screen,'#552200',Score_rect,0,10)
        pygame.draw.rect(screen,'#000000',Score_rect,3,10)
        screen.blit(Score_surf,Score_rect)


#surfaces
Ground_surf = pygame.image.load('JR_Data/Graphics/Ground.png').convert_alpha()
Backdrop_surf = pygame.image.load('JR_Data/Graphics/Backdrop.png').convert_alpha()
Fire_surf = pygame.image.load('JR_Data/Graphics/Campfire.png').convert_alpha()
Flytrap_frame1 = pygame.image.load('JR_Data/Graphics/Flytrap.png').convert_alpha()
Flytrap_frame2 = pygame.image.load('JR_Data/Graphics/Flytrap2.png').convert_alpha()
Flytrap_frame = [Flytrap_frame1,Flytrap_frame2]
Flytrap_move = 0
Flytrap_surf = Flytrap_frame[Flytrap_move]
Eagle_frame1 = pygame.image.load('JR_Data/Graphics/Eagle.png')
Eagle_frame2 = pygame.image.load('JR_Data/Graphics/Eagle2.png')
Eagle_frame = [Eagle_frame1,Eagle_frame2]
Eagle_move = 0
Eagle_surf = Eagle_frame[Eagle_move]
Char_run1 = pygame.image.load('JR_Data/Graphics/Run1.png').convert_alpha()
Char_run2 = pygame.image.load('JR_Data/Graphics/Run2.png').convert_alpha()
Char_run3 = pygame.image.load('JR_Data/Graphics/Run3.png').convert_alpha()
Char_jump = pygame.image.load('JR_Data/Graphics/Jump.png').convert_alpha()
Char_run = [Char_run1,Char_run3,Char_run2]
Char_move = 0
Char_surf = Char_run[Char_move]
#Rectangle
Ground_rect1 = pygame.Rect(0,305,800,150)
Ground_rect2 = pygame.Rect(800,305,800,150)
Flytrap_rect = pygame.Rect(800,280,100,65)
Eagle_rect = pygame.Rect(800,0,100,100)
Char_rect = pygame.Rect(80,170,100,200)
Char_grav = 0

#Enemy Animations
Flytrap_Anim_Timer = pygame.USEREVENT + 2
pygame.time.set_timer(Flytrap_Anim_Timer, 500)
Eagle_Anim_Timer = pygame.USEREVENT + 3
pygame.time.set_timer(Eagle_Anim_Timer, 200)

Enemy_rect_list = []
#timer
Enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(Enemy_timer,900)

#loop to keep screen
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            #close code
            exit()
        if Running :
            if event.type == pygame.KEYDOWN and Char_rect.bottom == 370:
                if event.key == pygame.K_SPACE:
                    Char_grav = -20
                    Jump.play()
        else :
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                Running = True
                Flytrap_rect.left=800
                Runtime = pygame.time.get_ticks()
                FirstRun = False
                BGM.play(loops = -1)
        #Enemy spawning
        if Running:
            if event.type == Enemy_timer and Running:
                if randint(0,5):
                    Enemy_rect_list.append(Eagle_surf.get_rect(topleft = (randint(1400,1500),280)))
                else:
                    Enemy_rect_list.append(Flytrap_surf.get_rect(topleft = (randint(1400,1500),0)))
            if event.type == Flytrap_Anim_Timer:
                Flytrap_move = 1 if Flytrap_move == 0 else 0
                Flytrap_surf = Flytrap_frame[Flytrap_move]
            if event.type == Eagle_Anim_Timer:
                Eagle_move = 1 if Eagle_move == 0 else 0
                Eagle_surf = Eagle_frame[Eagle_move]
    if Running :
        #Increasing Speed
        Speed = 7 + int(Score/30)
        #upload surface 
        screen.blit(Backdrop_surf,(0,0))
        screen.blit(Flytrap_surf,Flytrap_rect)
        #Character
        Char_grav += 1
        Char_rect.y += Char_grav
        if Char_rect.bottom > 370 :
            Char_rect.bottom = 370 
            Char_grav = 0
        CharAnim()
        screen.blit(Char_surf,(Char_rect.x-60,Char_rect.y))
        #Enemy scrolling
        Enemy_rect_list = EnemyMovement(Enemy_rect_list)
        #Collision
        Running = Collision(Char_rect,Enemy_rect_list)
        BackdropScroll(Ground_rect1)
        BackdropScroll(Ground_rect2)
        ScoreCalc()
    #Standby screen
    else:
        Enemy_rect_list.clear()
        if FirstRun:
            screen.fill('#110000')
            TopText = "Jungle Rush"
        else:
            pygame.time.wait(500)
            TopText = "Game Over"
            Char_rect.topleft = (80,170)
            Speed = 7
        pygame.draw.rect(screen, '#552200', (150,75,500,300),0,10)
        pygame.draw.rect(screen, '#000000', (150,75,500,300),4,10)
        screen.blit(Fire_surf,(325,150))
        TT_surf = TextF.render(TopText, True, 'Gold')
        TT_rect = TT_surf.get_rect(midtop = (400,100))
        screen.blit(TT_surf,TT_rect)
        BT_surf = TextF.render("Press SPACE to Start", True, 'Gold')
        BT_rect = BT_surf.get_rect(midtop = (400,310))
        screen.blit(BT_surf,BT_rect)
    #to update
    pygame.display.update()
    timer.tick(60)