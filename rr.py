import pygame,sys
from pygame.color import THECOLORS
from pygame.locals import *
import tkinter as tk 
from tkinter import messagebox
#初始化窗口
def chushi(name,x,y,color):   
    screencaption = pygame.display.set_caption(name)
    screen = pygame.display.set_mode([x,y])
    screen.fill(THECOLORS[color])
    return screen 
#创建棋盘类
class qipan:
    #棋盘属性　　所在窗体，棋盘的大小位置
    def __init__(self,surface,xstart,xstop,ystart,ystop):
        self.surface = surface
        self.xstart = xstart
        self.xstop = xstop
        self.ystart = ystart
        self.ystop = ystop
    #棋盘的背景设置
    def bg(self,filename,x,y):
        img = pygame.image.load(filename)   
        self.surface.blit(img,[x,y])
    #绘制棋盘，返回中心点像素坐标
    def drawqp(self):
        x,x1 = self.xstart,self.xstop
        y,y1 = self.ystart,self.ystop
        x2,y2 = x,y
        z = y
        length = (x1 - x)/14
        # 绘制线条
        for i in range(15):
            # 边界加宽
            if i ==0 or i == 14:
                pygame.draw.lines(screen,THECOLORS['black'],False,[[x,y],[x1,y]],4)           
            pygame.draw.lines(screen,THECOLORS['black'],False,[[x,y],[x1,y]],2)
            y +=length
        for i in range(15):
            if i ==0 or i == 14:
                pygame.draw.lines(screen,THECOLORS['black'],False,[[x,z],[x,y1]],4)
            pygame.draw.lines(screen,THECOLORS['black'],False,[[x,z],[x,y1]],2)
            x +=length                                 
        #中心点列表　L = [[x,y]]
        L = []
        x3 = x2
        for i in range(15):
            l = []
            y3 = y2
            for j in range(15):
                l.append([x3,y3])
                y3+= length
            x3 += length
            L.append(l)
        #绘制九个中心点圆形
        s=[L[7][7],L[3][3],L[3][7],L[7][3],L[3][11],L[7][11],L[11][3],L[11][11],L[11][7]]        
        for i in s:
            pygame.draw.circle(screen,THECOLORS['black'],[int(i[0]),int(i[1])],6)
        return L
def up(i,j,sign):
    count = 0
    while 1:
        if i >= 0:
            i -= 1
            if l[i][j] == sign:
                count += 1
            else:
                break
    return count 
def down(i,j,sign):
    count = 0
    while 1:
        if i <= 14:
            i += 1
            if l[i][j] == sign:
                count += 1
            else:
                break
    return count 
def left(i,j,sign):
    count = 0
    while 1:
        if j >= 0:
            j -= 1
            if l[i][j] == sign:
                count += 1
            else:
                break
    return count 
def right(i,j,sign):
    count = 0
    while 1:
        if j <= 14:
            j += 1
            if l[i][j] == sign:
                count += 1
            else:
                break
    return count 
def lup(i,j,sign):
    count = 0
    while 1:
        if i >= 0 and j <= 14:
            i -= 1
            j += 1
            if l[i][j] == sign:
                count += 1
            else:
                break
    return count 
def ldown(i,j,sign):
    count = 0
    while 1:
        if i <= 14 and j >= 0:
            i += 1
            j -= 1
            if l[i][j] == sign:
                count += 1
            else:
                break
    return count 
def rup(i,j,sign):
    count = 0
    while 1:
        if j >= 0 and i >= 0:
            i -= 1
            j -= 1
            if l[i][j] == sign:
                count += 1
            else:
                break
    return count 
def rdown(i,j,sign):
    count = 0
    while 1:
        if i <= 14 and j <= 14:
            i += 1
            j += 1
            if l[i][j] == sign:
                count += 1
            else:
                break
    return count
#创建棋子类
class qizi:
    def __init__(self,surface,color,r):
        self.surface = surface
        self.color = color
        self.r = r 
    def drawc(self,x,y):
        pygame.draw.circle(self.surface,THECOLORS[self.color],[x,y],self.r)
    #计步器
    def addc(self,x,y,t):
        fontobj = pygame.font.Font('1.TTF',25)
        # textSurfaceobj = fontobj.render(t,True,THECOLORS['red'],THECOLORS['green'])
        textSurfaceobj = fontobj.render(t,True,THECOLORS['red'])
        textRectobj = textSurfaceobj.get_rect()
        textRectobj.center = (x,y)
        screen.blit(textSurfaceobj,textRectobj)
def wenzi(size,text,color1,color2,x,y):
    fontobj = pygame.font.Font('1.TTF',size)
    textSurfaceobj = fontobj.render(text,True,THECOLORS[color1],THECOLORS[color2])
    textRectobj = textSurfaceobj.get_rect()
    textRectobj.center = (x,y)
    screen.blit(textSurfaceobj,textRectobj)
# 胜负处理
def win(sign):
    global win1
    if sign == 1:
        msg = '黑棋胜利！'
    elif sign == 2:
        msg = '白棋胜利！'
    win1 = 1
    fontobj = pygame.font.Font('1.TTF',100)
    textSurfaceobj = fontobj.render(msg,True,THECOLORS['red'],THECOLORS['green'])
    textRectobj = textSurfaceobj.get_rect()
    textRectobj.center = (500,320)
    screen.blit(textSurfaceobj,textRectobj)
    fontobj = pygame.font.Font('1.TTF',40)
    textSurfaceobj = fontobj.render('继续',True,THECOLORS['black'],THECOLORS['yellow'])
    textRectobj = textSurfaceobj.get_rect()
    textRectobj.center = (350,550)
    screen.blit(textSurfaceobj,textRectobj)
    wenzi(40,'再来一局','black','yellow',600,550)   
def judgewin(l,sign):
    flag = 0
    for i in range(15):
        for j in range(15):
            #判断每个位置是否五连棋
            if l[i][j] == sign:
                # while 1:
                if up(i,j,sign)+down(i,j,sign) >= 4:
                    win(sign)
                    return
                elif left(i,j,sign)+right(i,j,sign) >= 4:
                    win(sign)
                    return
                elif lup(i,j,sign)+ldown(i,j,sign) >= 4:
                    win(sign)
                    return
                elif rup(i,j,sign)+rdown(i,j,sign) >= 4:
                    win(sign)
                    return
def gcontinue():
    sys.exit()

def again():
    global l
    l = [[0 for i in range(15)] for i in range(15)]
    pygame.init()
    screen = chushi('wuziqi',1024,800,'white')
    fpsClock = pygame.time.Clock()
    a = qipan(screen,200,800,100,700)
    l = [[0 for i in range(15)] for i in range(15)]
    win1 = 0
    
    renren()  
def renren():
    global win1,l
    a = qipan(screen,200,800,100,700)
    # a.bg('log1.png',0,0)
    L = a.drawqp()
    l = [[0 for i in range(15)] for i in range(15)]
    count = 1
    
    while 1:
        for event in pygame.event.get():
            if count%2 == 1:
                sign = 1
                color = 'black'
            elif count%2 ==0:
                sign = 2
                color = 'blue'
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #判断棋子中心点
                z1 = 0
                for i in L:
                    z2 = 0
                    for j in i: 
                        if win1 == 0 and j[0]-25<=event.pos[0]<=j[0]+25 and j[1]-25<=event.pos[1]<=j[1]+25 and l[z1][z2] == 0:
                            #创建棋子
                            qizi1 = qizi(screen,color,20)
                            qizi1.drawc(int(j[0]),int(j[1]))
                            # #计步器
                            # qizi1.addc(int(j[0]),int(j[1]),str(count))
                            l[z1][z2] = sign
                            judgewin(l,sign)
                            
                            count += 1
                        z2 += 1
                    z1 += 1 
                if  330<=event.pos[0]<=370 and 530<=event.pos[1]<=570 :
                    gcontinue()
                elif 580<=event.pos[0]<=620 and 530<=event.pos[1]<=570 :
                    l = []
                    win1 = 0
                    again()

                    
               
        pygame.display.update()
        fpsClock.tick(30)

if __name__ == '__main__':
    pygame.init()
    screen = chushi('wuziqi',1024,800,'white')
    fpsClock = pygame.time.Clock()
    a = qipan(screen,200,800,100,700)
    
    win1 = 0
    # a.bg('log1.png',0,0)
    renren()

