#五子棋棋盘绘制
import pygame,sys
from pygame.color import THECOLORS
pygame.init()
screencaption = pygame.display.set_caption('wuziqi')
screen = pygame.display.set_mode([1080,800])
screen.fill(THECOLORS['yellow'])
def qipan(start,stop,start1,stop1): #横
    global l
    x = start
    length = (stop - start)/14
    for i in range(15):
        pygame.draw.lines(screen,[0,255,255],False,[[start1,x],[stop1,x]],1)
        x +=length
# def shu(start,stop):  #数
    y = start1
    length1 = (stop1 - start1)/14
    for i in range(15):
        pygame.draw.lines(screen,[0,255,255],False,[[y,start],[y,stop]],1)
        y +=length


#生成焦点坐标即棋子中心坐标
    l = [[x,y] for y in range(start,stop+1,int(length)) for x in range(start1,stop1+1,int(length1))]
qipan(80,570,155,645)
def circle(x,y,color='black'):
    pygame.draw.circle(screen,THECOLORS[color],[x,y],10)
count = 0 
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if count%2 == 0:
            color='white'
        else:
            color='black'


        if event.type == pygame.MOUSEBUTTONDOWN:

            #判断棋子中心点
           
            for i in l:
                if i[0]-15<=event.pos[0]<=i[0]+15 and i[1]-15<=event.pos[1]<=i[1]+15:
                    circle(i[0],i[1],color)
                    count+=1
                    l.remove(i)

    pygame.display.update()