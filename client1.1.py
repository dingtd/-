# -*- coding:utf-8 -*-
from socket import *
from threading import *
import sys 
from time import sleep
import pygame,sys
from pygame.color import THECOLORS
from pygame.locals import *
from queue import Queue 

#获取事件的反馈信息，将信息返回给发送给 服务器端
def sendinfo(sockfd,sq):
    while 1:
        a = sq.get()
        if a!='judgefirst'and a!='first'and a!='second'and a!=' ':
            sockfd.send(a.encode())
#循环接收服务器 消息 ，当接收到不同指令时 则 进行 不同的指令
def recvinfo(sockfd,screen,rq,sq):  
    rec =[]
    jg1=[]
    while 1: 
        disfind = 0
        msg = sockfd.recv(4096).decode()
        jg = msg.split('#')
        if jg[0]=='xiaqi1'or jg[0]=='xiaqi2'or jg[0]=='qingqiuhuiqi1' or jg[0]=='qingqiuhuiqi2':
            for i in jg:
                if i=='$':
                    for i in rec:
                        msg +=i
                    rq.put(msg)
                    rec=[]
                else:
                    disfind = 1
            if disfind ==1:
                rec.append(msg)
                continue
        else:
            if msg:
                rq.put(msg)
                rec=[]
        # if msg:
        #     print('1收到消息',msg)
def select(sockfd,screen,rq,sq):
    global b
    b=0
    if not rq.empty():
        rinfo = rq.get()
        info = rinfo.split('#')
        hand_msg = info[0]
        if hand_msg == 'judgefirst':

            judgefirst(sockfd,screen,sq,rq)
        elif hand_msg == 'first':
            first(sockfd,screen,sq,rq)
        elif hand_msg == 'second':
            second(sockfd,screen,sq,rq)
        elif hand_msg == 'qiangxingtuichu':
            qiangxingtuichu()
        elif hand_msg == 'xiaqi1':
            info1 = eval(info[1])
            count = eval(info[3])
            l = eval(info[2])
            if judgewin(l,2,screen)==1:
                sq.put('win2')
                win2(sockfd,screen,sq,rq,info1,l,count)
                
            else:
                xiaqi1(sockfd,screen,sq,rq,info)
        elif hand_msg == 'xiaqi2':
            info1 = eval(info[1])
            count = eval(info[3])
            l = eval(info[2])
            if judgewin(l,1,screen)==1:
                sq.put('win1')
                win1(sockfd,screen,sq,rq,info1,l,count)
                
            else:
                xiaqi2(sockfd,screen,sq,rq,info)
        elif hand_msg == 'qingqiuhuiqi1':

            info1 = eval(info[1])
            count = eval(info[3])
            l = eval(info[2])
            qingqiuhuiqi(sockfd,screen,sq,rq,info1,l,count,1)
        elif hand_msg == 'qingqiuhuiqi2':

            info1 = eval(info[1])
            count = eval(info[3])
            l = eval(info[2])
            qingqiuhuiqi(sockfd,screen,sq,rq,info1,l,count,2)
        elif hand_msg == 'win1':
            info1 = eval(info[1])
            count = eval(info[3])
            l = eval(info[2])
            win1(sockfd,screen,sq,rq,info1,l,count)
        elif hand_msg == 'win2':
            info1 = eval(info[1])
            count = eval(info[3])
            l = eval(info[2])
            win2(sockfd,screen,sq,rq,info1,l,count)


    #     elif hand_msg == 'tuichu':
    #         tuichu()
    # else:
        pass
def qingqiuhuiqi(sockfd,screen,sq,rq,info1,l,count,a):
    global b
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'bg4.png',w,h,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    # 绘制当前盘面

    for i in info1:
        y = i[0]
        x = i[1]
        color = i[2]
        count = i[3]
        if color == 1:
            sign = 'black'
            file = 'hqz.png'
        elif color == 2:
            sign = 'white'
            file = 'bqz.png'
        qizi1 = qizi(screen,sign,18)
        tu(screen,file,40,40,int(L[x][y][0])-20,int(L[x][y][1])-20)
        #b==1 显示棋子顺序
        if b == 1:
            qizi1.addc(int(L[x][y][0]),int(L[x][y][1]),str(count))
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)	
    tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',80,40,0.9*w-40,0.9*h-20)
    tu(screen,'dfqqhq.png',360,80,0.5*w-180,0.4*h-40)
    tu(screen,'ty.png',80,40,0.4*w-40,0.7*h-20)
    tu(screen,'jj.png',80,40,0.6*w-40,0.7*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(sockfd,screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0.9*w-80<=event.pos[0]<=0.9*w+80  and  0.9*h-20<=event.pos[1]<=0.9*h+20:
                    sys.exit()
                if 0.4*w-80<=event.pos[0]<=0.4*w+80  and  0.7*h-20<=event.pos[1]<=0.7*h+20:                    
                    tongyihuiqi(sockfd,screen,sq,rq,info1,l,count,a)
                if 0.6*w-40<=event.pos[0]<=0.6*w+40  and  0.7*h-20<=event.pos[1]<=0.7*h+20:
                    if a==1:
                        count+=1
                        send1 = 'xiaqi1'+'#'+str(info1)+'#'+str(l)+'#'+str(count)+'#'+'$#'
                    else:
                        count+=1
                        send1 = 'xiaqi2'+'#'+str(info1)+'#'+str(l)+'#'+str(count)+'#'+'$#'
                    sq.put(send1)
                    w = screen.get_width()
                    h = screen.get_height()
                    tu(screen,'bg4.png',w,h,0,0)
                    s = qipan(screen,200,800,100,700)
                    L = s.drawqp()
                    # 绘制当前盘面

                    for i in info1:
                        y = i[0]
                        x = i[1]
                        color = i[2]
                        count = i[3]
                        if color == 1:
                            sign = 'black'
                        elif color == 2:
                            sign = 'white'
                        qizi1 = qizi(screen,sign,18)
                        qizi1.drawc(int(L[x][y][0]),int(L[x][y][1]))
                        #b==1 显示棋子顺序
                        if b == 1:
                            qizi1.addc(int(L[x][y][0]),int(L[x][y][1]),str(count)) 
                    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
                    tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
                    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20) 
                    tu(screen,'jjfsz.png',320,80,0.5*w-160,0.4*h-40)
                    fpsClock = pygame.time.Clock()
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        pygame.display.update()
        fpsClock.tick(30)
def tongyihuiqi(sockfd,screen,sq,rq,info1,l,count,a):
    for i in range(2):
        huiqi=info1.pop()
        l[huiqi[0]][huiqi[1]]=0
    count-=1
    if a==1:
        send1 = 'xiaqi1'+'#'+str(info1)+'#'+str(l)+'#'+str(count)+'#'+'$#'
    else:
        send1 = 'xiaqi2'+'#'+str(info1)+'#'+str(l)+'#'+str(count)+'#'+'$#'
    sq.put(send1)
    global b
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'bg4.png',w,h,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    if len(info1)>0:
        for i in info1:
            y = i[0]
            x = i[1]
            color = i[2]
            count = i[3]
            if color == 1:
                sign = 'black'
                file = 'hqz.png'
            elif color == 2:
                sign = 'white'
                file = 'bqz.png'
            qizi1 = qizi(screen,sign,18)
            tu(screen,file,40,40,int(L[x][y][0])-20,int(L[x][y][1])-20)
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
    tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(sockfd,screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                qiangxingtuichu() 
            if event.type == pygame.MOUSEBUTTONDOWN:
 
                if 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.7*h-20<=event.pos[1]<=0.7*h+20:
                    if b==0:
                        b = 1
                    else:
                        b = 0
                    xianshishunxu1(sockfd,screen,sq,rq,info1,l,count,b)
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
       
        pygame.display.update()
        fpsClock.tick(30)

def win1(sockfd,screen,sq,rq,info1,l,count):
    global b
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'bg4.png',w,h,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    # 绘制当前盘面
    for i in info1:
        y = i[0]
        x = i[1]
        color = i[2]
        count = i[3]
        if color == 1:
            sign = 'black'
            file = 'hqz.png'
        elif color == 2:
            sign = 'white'
            file = 'bqz.png'
        qizi1 = qizi(screen,sign,18)
        tu(screen,file,40,40,int(L[x][y][0])-20,int(L[x][y][1])-20)
        #b==1 显示棋子顺序
        if b == 1:
            qizi1.addc(int(L[x][y][0]),int(L[x][y][1]),str(count))
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
    tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    tu(screen,'hwin.png',320,80,0.5*w-160,0.4*h-20)
    tu(screen,'zlyj.png',160,40,0.4*w-80,0.7*h-20)
    tu(screen,'fh.png',80,40,0.6*w-40,0.7*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0.9*w-80<=event.pos[0]<=0.9*w+80  and  0.9*h-20<=event.pos[1]<=0.9*h+20:
                    sys.exit()
                if 0.4*w-80<=event.pos[0]<=0.4*w+80  and  0.7*h-20<=event.pos[1]<=0.7*h+20:

                    run(sockfd,screen,rq,sq)
                if 0.6*w-40<=event.pos[0]<=0.6*w+40  and  0.7*h-20<=event.pos[1]<=0.7*h+20:
                    fanhui(sockfd,screen,rq,sq) 
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
       
        pygame.display.update()
        fpsClock.tick(30)
def win2(sockfd,screen,sq,rq,info1,l,count):
    global b
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'bg4.png',w,h,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    # 绘制当前盘面
    for i in info1:
        y = i[0]
        x = i[1]
        color = i[2]
        count = i[3]
        if color == 1:
            sign = 'black'
            file = 'hqz.png'
        elif color == 2:
            sign = 'white'
            file = 'bqz.png'
        qizi1 = qizi(screen,sign,18)
        tu(screen,file,40,40,int(L[x][y][0])-20,int(L[x][y][1])-20)
        #b==1 显示棋子顺序
        if b == 1:
            qizi1.addc(int(L[x][y][0]),int(L[x][y][1]),str(count))
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
    tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    tu(screen,'bwin.png',320,80,0.5*w-160,0.4*h-20)
    tu(screen,'zlyj.png',160,40,0.4*w-80,0.7*h-20)
    tu(screen,'fh.png',80,40,0.6*w-40,0.7*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0.9*w-80<=event.pos[0]<=0.9*w+80  and  0.9*h-20<=event.pos[1]<=0.9*h+20:
                    sys.exit()
                if 0.4*w-80<=event.pos[0]<=0.4*w+80  and  0.7*h-20<=event.pos[1]<=0.7*h+20:
                    run(sockfd,screen,rq,sq)
                if 0.6*w-40<=event.pos[0]<=0.6*w+40  and  0.7*h-20<=event.pos[1]<=0.7*h+20:
                    fanhui(sockfd,screen,rq,sq)
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)       
        pygame.display.update()
        fpsClock.tick(30)

def fanhui(sockfd,screen,rq,sq):
    run(sockfd,screen,rq,sq)

def window(name,x,y,color):
    pygame.init()   
    screencaption = pygame.display.set_caption(name)
    screen = pygame.display.set_mode([x,y])
    screen.fill(THECOLORS[color])
    return screen 
def wenzi(screen,size,text,x,y,color1):
    fontobj = pygame.font.Font('t.ttf',size)
    textSurfaceobj = fontobj.render(text,True,THECOLORS[color1],THECOLORS['white'])
    textRectobj = textSurfaceobj.get_rect()
    textRectobj.center = (x,y)
    screen.blit(textSurfaceobj,textRectobj)

def tu(screen,filename,x1,y1,x2,y2):
    image =pygame.image.load(filename).convert_alpha()
    new = pygame.transform.scale(image,(x1,y1))
    screen.blit(new,(x2,y2))
def tu1(screen,filename,x,y):
    image =pygame.image.load(filename).convert_alpha()
    screen.blit(image,(x,y))
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
                pygame.draw.lines(self.surface,THECOLORS['black'],False,[[x,y],[x1,y]],4)           
            pygame.draw.lines(self.surface,THECOLORS['black'],False,[[x,y],[x1,y]],2)
            y +=length
        for i in range(15):
            if i ==0 or i == 14:
                pygame.draw.lines(self.surface,THECOLORS['black'],False,[[x,z],[x,y1]],4)
            pygame.draw.lines(self.surface,THECOLORS['black'],False,[[x,z],[x,y1]],2)
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
            pygame.draw.circle(self.surface,THECOLORS['black'],[int(i[0]),int(i[1])],6)
        return L
class qizi:
    def __init__(self,surface,color,r):
        self.surface = surface
        self.color = color
        self.r = r
 
    def drawc(self,x,y):
        pygame.draw.circle(self.surface,THECOLORS[self.color],[x,y],self.r)


    #计步器
    def addc(self,x,y,t):
        fontobj = pygame.font.Font('t.ttf',25)
        # textSurfaceobj = fontobj.render(t,True,THECOLORS['red'],THECOLORS['green'])
        textSurfaceobj = fontobj.render(t,True,THECOLORS['red'])
        textRectobj = textSurfaceobj.get_rect()
        textRectobj.center = (x,y)
        self.surface.blit(textSurfaceobj,textRectobj)
def up(l,i,j,sign):
    count = 0
    while 1:
        if i > 0:
            i -= 1
            if l[i][j] == sign:
                count += 1
            else:
                break
        else:
            break
    return count 
def down(l,i,j,sign):
    count = 0
    while 1:
        if i < 14:
            i += 1
            if l[i][j] == sign:
                count += 1
            else:
                break
        else:
            break
    return count 
def left(l,i,j,sign):
    count = 0
    while 1:
        if j > 0:
            j -= 1
            if l[i][j] == sign:
                count += 1
            else:
                break
        else:
            break
    return count 
def right(l,i,j,sign):
    count = 0
    while 1:
        if j <= 13:
            j += 1
            if l[i][j] == sign:
                count += 1
            else:
                break
        else:
            break
    return count 
def lup(l,i,j,sign):
    count = 0
    while 1:
        if i > 0 and j <= 13:
            i -= 1
            j += 1
            if l[i][j] == sign:
                count += 1
            else:
                break
        else:
            break
    return count 
def ldown(l,i,j,sign):
    count = 0
    while 1:
        if i <= 13 and j > 0:
            i += 1
            j -= 1
            if l[i][j] == sign:
                count += 1
            else:
                break
        else:
            break
    return count 
def rup(l,i,j,sign):
    count = 0
    while 1:
        if j > 0 and i > 0:
            i -= 1
            j -= 1
            if l[i][j] == sign:
                count += 1
            else:
                break
        else:
            break
    return count 
def rdown(l,i,j,sign):
    count = 0
    while 1:
        if i <= 13 and j <= 13:
            i += 1
            j += 1
            if l[i][j] == sign:
                count += 1
            else:
                break
        else:
            break
    return count
def judgewin(l,sign,screen):

    for i in range(15):
        for j in range(15):
            #判断每个位置是否五连棋
            if l[i][j] == sign:
                # while 1:
                if up(l,i,j,sign)+down(l,i,j,sign) >= 4:
                    
                    return 1
                elif left(l,i,j,sign)+right(l,i,j,sign) >= 4:
                    
                    return 1
                elif lup(l,i,j,sign)+ldown(l,i,j,sign) >= 4:
                    
                    return 1 
                elif rup(l,i,j,sign)+rdown(l,i,j,sign) >= 4:
                    
                    return 1 
def chushihua(sockfd,sq,rq):

    screen = window('wuziqi',1024,800,'white')
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'bg4.png',w,h,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    tu(screen,'zb.png',80,40,0.9*w-40,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(sockfd,screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()                  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0.9*w-40<=event.pos[0]<=0.9*w+40  and  0.7*h-20<=event.pos[1]<=0.7*h+20:
                    sq.put('zhunbei')
                    waitlog(sockfd,screen,sq,rq)
                    
                if 0.9*w-80<=event.pos[0]<=0.9*w+80  and  0.9*h-20<=event.pos[1]<=0.9*h+20:
                    sys.exit()
        
        pygame.display.update()
        fpsClock.tick(30)
#等待对手接入信号
def waitlog(sockfd,screen,sq,rq):
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'bg4.png',w,h,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    tu(screen,'waitzb.png',720,80,0.5*w-360,0.4*h-40)
    tu(screen,'qxzb.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(sockfd,screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()                  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0.9*w-80<=event.pos[0]<=0.9*w+80  and  0.7*h-20<=event.pos[1]<=0.7*h+20:
                    sq.put('quxiao')

                    chushihua(sockfd,sq,rq)
                if 0.9*w-80<=event.pos[0]<=0.9*w+80  and  0.9*h-20<=event.pos[1]<=0.9*h+20:
                    sys.exit()
        pygame.display.update()
        fpsClock.tick(30)

def judgefirst(sockfd,screen,sq,rq):
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'bg4.png',w,h,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    #tu1(screen,'sjxs.png',0.5*w-160,0.7*h-20)
    tu(screen,'sjxs.png',640,80,0.5*w-320,0.7*h-40)
    # wenzi(screen,40,'正在随机产生先手',0.5*w,0.7*h,'black')
    # wenzi(screen,40,'取消准备',0.9*w,0.7*h,'black')
    tu(screen,'qxzb.png',160,40,0.9*w-80,0.7*h-20)
    #tu1(screen,'tc.png',0.9*w-80,0.9*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(sockfd,screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()                  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0.9*w-80<=event.pos[0]<=0.9*w+80  and  0.9*h-20<=event.pos[1]<=0.9*h+20:
                    #游戏开始后强行退出即为负
                    sys.exit()
        # 服务器端发送盘面信息  info=[[x1,y1,color1,count1],[x2,y2,color2,count2]...]      
 
        
        pygame.display.update()
        fpsClock.tick(30)
#首先接收当前棋盘信息，然后执行一次下棋事件，返回服务器棋盘信息,执行一次下棋动作之后　，不能在操作棋盘，每次接收服务器信息中包含下棋　条件
# 先手　黑棋子
def first(sockfd,screen,sq,rq):
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'bg4.png',w,h,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    tu(screen,'zhxz.png',400,80,0.5*w-200,0.4*h-40)
    tu(screen,'qd.png',80,40,0.5*w-40,0.6*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    l =[[0 for i in range(15)]for i in range(15)]
    info = []
    count = 1
    fpsClock = pygame.time.Clock()
    while 1:
        select(sockfd,screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()                  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0.9*w-80<=event.pos[0]<=0.9*w+80  and  0.9*h-20<=event.pos[1]<=0.9*h+20:
                    #游戏开始后强行退出即为负
                    qiangxingtuichu()
                if 0.5*w-40<=event.pos[0]<=0.5*w+40  and  0.6*h-20<=event.pos[1]<=0.6*h+20:
                    
                    # sq.put('firsrstep')
                    firststep(sockfd,screen,sq,rq,info,l,count)
        # 服务器端发送盘面信息  info=[[x1,y1,color1,count1],[x2,y2,color2,count2]...]      
 

        pygame.display.update()
        fpsClock.tick(30)

def second(sockfd,screen,sq,rq):
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'bg4.png',w,h,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    tu(screen,'wait.png',400,80,0.5*w-200,0.4*h-40)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(sockfd,screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()                  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0.9*w-80<=event.pos[0]<=0.9*w+80  and  0.9*h-20<=event.pos[1]<=0.9*h+20:
                    qiangxingtuichu()
        pygame.display.update()
        fpsClock.tick(30)
def firststep(sockfd,screen,sq,rq,info,l,count):
    global b
    permit = 0
    b = 0
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'bg4.png',w,h,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    # 绘制当前盘面
    if len(info)>0:
        for i in info:
            y = i[0]
            x = i[1]
            color = i[2]
            count = i[3]
            if color == 1:
                sign = 'black'
            elif color == 2:
                sign = 'white'
            qizi1 = qizi(screen,sign,18)
            qizi1.drawc(int(L[x][y][0]),int(L[x][y][1]))
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(sockfd,screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                qiangxingtuichu() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                z1 = 0
                for i in L:
                    z2 = 0
                    for j in i: 
                        #接收到服务器信息，其中包含有　　执行1次　的　标记　？　点击后　标记状态变化　，继续点击失效
                        if permit == 0 and j[0]-15<=event.pos[0]<=j[0]+15 and j[1]-15<=event.pos[1]<=j[1]+15 and l[z1][z2] == 0: 
                            qizi1 = qizi(screen,'black',18)
                            tu(screen,'hqz.png',40,40,int(j[0])-20,int(j[1])-20)
                            if b == 1:
                                qizi1.addc(int(j[0]),int(j[1]),str(count))
                            l[z2][z1] = 1
                            judgewin(l,1,screen)
                            info.append((z2,z1,1,count))
                            count += 1
                            send1 = 'xiaqi2'+'#'+str(info)+'#'+str(l)+'#'+str(count)+'#'+'$#'
                            sq.put(send1)
                            permit = 1   
                        z2 += 1
                    z1 += 1 
                if 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.7*h-20<=event.pos[1]<=0.7*h+20:
                    if b==0:
                        b = 1
                    else:
                        b = 0
                    xianshishunxu1(sockfd,screen,sq,rq,info,l,count,b)
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)  
        pygame.display.update()
        fpsClock.tick(30)

def xianshishunxu1(sockfd,screen,sq,rq,info,l,count,b):
    info1 = info
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'bg4.png',w,h,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    # 绘制当前盘面
    if info1:
        for i in info1:
            y = i[0]
            x = i[1]
            color = i[2]
            count1 = i[3]
            if color == 1:
                sign = 'black'
                file = 'hqz.png'
            elif color == 2:
                sign = 'white'
                file = 'bqz.png'
            qizi1 = qizi(screen,sign,18)
            tu(screen,file,40,40,int(L[x][y][0])-20,int(L[x][y][1])-20)
            #b==0 显示棋子顺序
            if b == 1:
                qizi1.addc(int(L[x][y][0]),int(L[x][y][1]),str(count1))
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
    if b==1: 
        tu(screen,'ycsx.png',160,40,0.9*w-80,0.7*h-20)
    else:
        tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    # fpsClock = pygame.time.Clock()

def xiaqi1(sockfd,screen,sq,rq,info):
    global b
    permit = 0
    info1 = eval(info[1])
    # print(info1)
    l = eval(info[2])
    count = eval(info[3])
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'bg4.png',w,h,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    # 绘制当前盘面
    if info1:
        for i in info1:

            y = i[0]
            x = i[1]
            color = i[2]
            count1 = i[3]
            if color == 1:
                sign = 'black'
                file = 'hqz.png'
            elif color == 2:
                sign = 'white'
                file = 'bqz.png'
            qizi1 = qizi(screen,sign,18)
            tu(screen,file,40,40,int(L[x][y][0])-20,int(L[x][y][1])-20)
            if b == 1:
                qizi1.addc(int(L[x][y][0]),int(L[x][y][1]),str(count1))
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
    tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(sockfd,screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                qiangxingtuichu1(sockfd,screen,sq,rq,info) 
            if event.type == pygame.MOUSEBUTTONDOWN:
                z1 = 0
                for i in L:
                    z2 = 0
                    for j in i: 
                        if permit == 0 and j[0]-15<=event.pos[0]<=j[0]+15 and j[1]-15<=event.pos[1]<=j[1]+15 and l[z2][z1] == 0:
                            qizi1 = qizi(screen,'black',18)
                            tu(screen,'hqz.png',40,40,int(j[0])-20,int(j[1])-20)
                            l[z2][z1] = 1
                            if b == 1:
                                qizi1.addc(int(j[0]),int(j[1]),str(count))
                            info1.append((z2,z1,1,count))
                            count += 1
                            if judgewin(l,1,screen)==1:
                                send1 = 'xiaqi2'+'#'+str(info1)+'#'+str(l)+'#'+str(count)+'#'+'$#'
                                sq.put(send1)
                                win1(sockfd,screen,sq,rq,info1,l,count)
                            send1 = 'xiaqi2'+'#'+str(info1)+'#'+str(l)+'#'+str(count)+'#'+'$#'                             
                            sq.put(send1)
                            permit = 1  
                        z2 += 1
                    z1 += 1 
                if 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.7*h-20<=event.pos[1]<=0.7*h+20:
                    if b==0:
                        b = 1
                    else:
                        b = 0
                    xianshishunxu1(sockfd,screen,sq,rq,info1,l,count,b)
                if permit == 0 and 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.5*h-20<=event.pos[1]<=0.5*h+20: 
                    tu(screen,'fshq.png',800,80,0.5*w-400,0.4*h-40)
                    send2 = 'qingqiuhuiqi1'+'#'+str(info1)+'#'+str(l)+'#'+str(count)+'#'+'$#'              
                    sq.put(send2)
                if permit == 0 and 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.9*h-20<=event.pos[1]<=0.9*h+20:
                    qiangxingtuichu1(sockfd,screen,sq,rq,info)
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        pygame.display.update()
        fpsClock.tick(30)

def xiaqi2(sockfd,screen,sq,rq,info):
    global b
    permit = 0
    info1 = eval(info[1])
    # print(info1)
    l = eval(info[2])
    count = eval(info[3])
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'bg4.png',w,h,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    # 绘制当前盘面
    if info1:
        for i in info1:
            y = i[0]
            x = i[1]
            color = i[2]
            count1 = i[3]
            if color == 1:
                sign = 'black'
                file = 'hqz.png'
            elif color == 2:
                sign = 'white'
                file = 'bqz.png'
            qizi1 = qizi(screen,sign,18)
            tu(screen,file,40,40,int(L[x][y][0])-20,int(L[x][y][1])-20)
            if b == 1:
                qizi1.addc(int(L[x][y][0]),int(L[x][y][1]),str(count1))
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
    tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(sockfd,screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                qiangxingtuichu2(sockfd,screen,sq,rq,info) 
            if event.type == pygame.MOUSEBUTTONDOWN:
                z1 = 0
                for i in L:
                    z2 = 0
                    for j in i: 
                        if permit == 0 and j[0]-15<=event.pos[0]<=j[0]+15 and j[1]-15<=event.pos[1]<=j[1]+15 and l[z2][z1] == 0:
                            
                            qizi1 = qizi(screen,'white',18)
                            tu(screen,'bqz.png',40,40,int(j[0])-20,int(j[1])-20)
                            if b == 1:
                                qizi1.addc(int(j[0]),int(j[1]),str(count))
                            l[z2][z1] = 2
                            info1.append((z2,z1,2,count))
                            count += 1
                            if judgewin(l,2,screen)==1:
                                send2 = 'xiaqi1'+'#'+str(info1)+'#'+str(l)+'#'+str(count)+'#'+'$#'
                                sq.put(send2)
                                win2(sockfd,screen,sq,rq,info1,l,count)
                            send2 = 'xiaqi1'+'#'+str(info1)+'#'+str(l)+'#'+str(count)+'#'+'$#'
                            sq.put(send2)
                            permit = 1   
                        z2 += 1
                    z1 += 1 
                if 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.7*h-20<=event.pos[1]<=0.7*h+20:
                    if b==0:
                        b = 1
                    else:
                        b = 0
                    xianshishunxu1(sockfd,screen,sq,rq,info1,l,count,b)
                if permit == 0 and 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.5*h-20<=event.pos[1]<=0.5*h+20:
                    tu(screen,'fshq.png',800,80,0.5*w-400,0.4*h-40)
                    send2 = 'qingqiuhuiqi2'+'#'+str(info1)+'#'+str(l)+'#'+str(count)+'#'+'$#'          
                    sq.put(send2)
                if permit == 0 and 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.9*h-20<=event.pos[1]<=0.9*h+20:
                    qiangxingtuichu2(sockfd,screen,sq,rq,info)
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
       
        pygame.display.update()
        fpsClock.tick(30)

def qiangxingtuichu1(sockfd,screen,sq,rq,info):
    #重新绘制棋盘根据请求是否继续强行退出游戏 是 发送强行退出到服务器 否继续游戏 发送给服务器对方胜
    global b
    permit = 0
    info1 = eval(info[1])
    # print(info1)
    l = eval(info[2])
    count = eval(info[3])
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'bg4.png',w,h,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    # 绘制当前盘面
    if info1:
        for i in info1:
            y = i[0]
            x = i[1]
            color = i[2]
            count1 = i[3]
            if color == 1:
                sign = 'black'
                file = 'hqz.png'
            elif color == 2:
                sign = 'white'
                file = 'bqz.png'
            qizi1 = qizi(screen,sign,18)
            tu(screen,file,40,40,int(L[x][y][0])-20,int(L[x][y][1])-20)
            if b == 1:
                qizi1.addc(int(L[x][y][0]),int(L[x][y][1]),str(count1))
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
    tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    tu(screen,'qxtc.png',480,80,0.5*w-240,0.4*h-40)
    tu(screen,'kid.png',240,40,0.65*w-120,0.65*h-20)
    tu(screen,'sure.png',80,40,0.4*w-40,0.65*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(sockfd,screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                qiangxingtuichu1(sockfd,screen,sq,rq,info) 
            if event.type == pygame.MOUSEBUTTONDOWN:
                

                if 0.4*w-40<=event.pos[0]<=0.4*w+40 and 0.65*h-20<=event.pos[1]<=0.65*h+20:
                    send1 = 'win2'+'#'+str(info1)+'#'+str(l)+'#'+str(count)+'#'+'$#'                             
                    sq.put(send1)
                    pygame.quit()
                    sys.exit()
                if 0.65*w-120<=event.pos[0]<=0.65*w+120 and 0.65*h-20<=event.pos[1]<=0.65*h+20:
                    xiaqi1(sockfd,screen,sq,rq,info)
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
       
        pygame.display.update()
        fpsClock.tick(30)

def qiangxingtuichu2(sockfd,screen,sq,rq,info):
    global b
    permit = 0
    info1 = eval(info[1])
    # print(info1)
    l = eval(info[2])
    count = eval(info[3])
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'bg4.png',w,h,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    # 绘制当前盘面
    if info1:
        for i in info1:
            y = i[0]
            x = i[1]
            color = i[2]
            count1 = i[3]
            if color == 1:
                sign = 'black'
                file = 'hqz.png'
            elif color == 2:
                sign = 'white'
                file = 'bqz.png'
            qizi1 = qizi(screen,sign,18)
            tu(screen,file,40,40,int(L[x][y][0])-20,int(L[x][y][1])-20)
            if b == 1:
                qizi1.addc(int(L[x][y][0]),int(L[x][y][1]),str(count1))
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
    tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    tu(screen,'qxtc.png',480,80,0.5*w-240,0.4*h-40)
    tu(screen,'kid.png',240,40,0.65*w-120,0.65*h-20)
    tu(screen,'sure.png',80,40,0.4*w-40,0.65*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(sockfd,screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                qiangxingtuichu1(sockfd,screen,sq,rq,info) 
            if event.type == pygame.MOUSEBUTTONDOWN:
                

                if 0.4*w-40<=event.pos[0]<=0.4*w+40 and 0.65*h-20<=event.pos[1]<=0.65*h+20:
                    send1 = 'win1'+'#'+str(info1)+'#'+str(l)+'#'+str(count)+'#'+'$#'                             
                    sq.put(send1)
                    pygame.quit()
                    sys.exit()
                if 0.65*w-120<=event.pos[0]<=0.65*w+120 and 0.65*h-20<=event.pos[1]<=0.65*h+20:
                    xiaqi1(sockfd,screen,sq,rq,info)
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
       
        pygame.display.update()
        fpsClock.tick(30)



def people():
    
    sockfd = socket()
    sockfd.connect(('176.234.86.7',8888))
    screen = window('wuziqi',1024,800,'white')
    sq = Queue(5)
    rq = Queue(5)
    th1 = Thread(target = sendinfo,args=(sockfd,sq))
    th2 = Thread(target = recvinfo, args=(sockfd,screen,rq,sq))
    threads = [th1,th2]
    for t in threads:
        t.setDaemon(True)
        t.start()
    run(sockfd,screen,rq,sq)

def run(sockfd,screen,rq,sq):
    w = screen.get_width()
    h = screen.get_height()
    b = 0
    tu(screen,'bg4.png',w,h,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    tu(screen,'zb.png',80,40,0.9*w-40,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()                  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0.9*w-40<=event.pos[0]<=0.9*w+40  and  0.7*h-20<=event.pos[1]<=0.7*h+20:
                    sq.put('zhunbei')
                    waitlog(sockfd,screen,sq,rq)                    
                if 0.9*w-80<=event.pos[0]<=0.9*w+80  and  0.9*h-20<=event.pos[1]<=0.9*h+20:
                    sys.exit()
        pygame.display.update()
        fpsClock.tick(30)



people()


