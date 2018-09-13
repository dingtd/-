#＿＊_ coding:utf-8 _*_
from socket import *
from threading import *
import sys,os,time
PATH = os.getcwd()
import datetime
import pygame
from pygame.color import THECOLORS
from pygame.locals import *
from queue import Queue
from time import sleep


path = PATH+'/play/'

#点击准备按钮　提交准备　服务器　收到两个客户端准备后　发送开始游戏信号　do
#uid fight do recordlist
#recordlist = uid rid aid color x y time mid
#建立全局变量　列表 qpinfo=[]　存储当前棋盘信息 每次根据列表内容绘制棋盘
#每次下棋后　qpinfo.append(aid color x y )

#定义全局的棋盘棋子信息
qpinfo = []
l = [[0 for i in range(15)] for i in range(15)]
count = 1
b = 0
# uid = 0
rid = 0
mid = 0
start = 0
flag = 0

#子线程　th1
def sendinfo(sq,fsq):
    while 1:
        a = sq.get()
        fsq.put(a)

        
#子线程　th2
def recvinfo(rq,frq):  
    while 1: 
        msg = frq.get()
        print('收到',msg)
        rq.put(msg)

#处理服务器发送的消息
def select(screen,rq,sq):
    #uid fight match fid
    # fid fight match  uid
    #match  id black_pid white_pid start_time time_counter=8
    # [uid,'fight','start']
    # [uid]+['fight','do']+record.listOutput()
    # [uid,'fight','giveup']
    # 收到 uid 开头的为自己发送的消息 不进行处理
    # uid fight cmd fid 
    global qpinfo,l,count,uid,fid,mid,start,mid,flag
    if not rq.empty():
        rinfo = rq.get()
        info = rinfo.split(' ')
        if len(info)>2:
            hand_msg = info[2]
        print(info,start)
        if info[3] == 'matching_please_wait':
            start = 1
        if start == 1:
            if len(info)>4:
                hand_msg = info[2]
                print(hand_msg)
                print(info[3],uid)
                if hand_msg == 'ok':

                    judgefirst()
                elif hand_msg == 'match' and flag == 0 :

                    fid = int(info[3])

                    flag = 1
                    matchinfo = info[5]
                    myinfo = matchinfo.split(',')
                    mid = myinfo[0]
                    black_id = myinfo[1]
                    white_id = myinfo[2]
                    time.sleep(1)
                    if uid == black_id:
                        first(screen,rq,sq)
                    elif uid == white_id:
                        second(screen,rq,sq)

                elif hand_msg == 'do' :
                    print('收到下棋消息')
                    record = info[4].split(',')
                    print(record)
                    if record[3] == 'B':
                        color1 = 1
                        qzinfo = (int(record[4]),int(record[5]),color1,int(record[2]))
                        qpinfo.append(qzinfo)
                        l[int(record[4])][int(record[5])] = 1 
                        if judgewin(l,1,screen)==1:
                            print('赢了')
                            
                            win1(screen,rq,sq)
                            msg = str(uid)+' '+'fight'+' '+'over'+' '+str(fid)+' '+'lose'
                            sq.put(msg)
                            # putcmd(sq,'Bwin') 
                        else:
                            count+=1
                            xiaqi2(screen,rq,sq)
                    if record[3] == 'W':
                        color1 = 2
                        qzinfo = (int(record[4]),int(record[5]),color1,int(record[2]))
                        qpinfo.append(qzinfo)
                        l[int(record[4])][int(record[5])] = 2 
                        if judgewin(l,2,screen)==1:
                            print('赢了')
                            
                            win2(screen,rq,sq)
                            msg = str(uid)+' '+'fight'+' '+'over'+' '+str(fid)+' '+'lose'
                            sq.put(msg)
                            # putcmd(sq,'Wwin') 
                        else:
                            count+=1
                            xiaqi1(screen,rq,sq)
                hand_msg1=info[4]
                if hand_msg == 'Bgiveup' :
                    putcmd(sq,'Wwin')
                    win2(screen,rq,sq)

                elif hand_msg == 'Wgiveup' :
                    putcmd(sq,'Bwin')
                    win1(screen,rq,sq)
                elif hand_msg == 'xiaqi1':
                    xiaqi1(screen,rq,sq)
                elif hand_msg == 'xiaqi2' :
                    xiaqi2(screen,rq,sq)
                elif hand_msg == 'tongyi1' :
                    tongyihuiqi(screen,rq,sq,1)
                elif hand_msg == 'tongyi2' :
                    tongyihuiqi(screen,rq,sq,2)


                elif hand_msg == 'Bqingqiuhuiqi' :
                    qingqiuhuiqi(screen,rq,sq,1)
                elif hand_msg == 'Wqingqiuhuiqi' :
                    qingqiuhuiqi(screen,rq,sq,2)










#创建窗口
def window(name,x,y,color):
    pygame.init()   
    screencaption = pygame.display.set_caption(name)
    screen = pygame.display.set_mode([x,y])
    screen.fill(THECOLORS[color])
    return screen 
#插入图片
def tu(screen,filename,x1,y1,x2,y2):
    image =pygame.image.load(path+filename).convert_alpha()
    new = pygame.transform.scale(image,(x1,y1))
    screen.blit(new,(x2,y2))
#添加消息到消息队列
def putmsg(sq,msg):
    dt = datetime.datetime.now()
    time = dt.strftime("%Y:%m:%d:%H:%M:%S")
    aid = msg[0]
    x = msg[1]
    y = msg[2]
    color = msg[3]
    # if sign == 1:
    #     color = 'B'
    # else:
    #     color = 'W'
    record = str(uid)+','+str(rid)+','+str(aid)+','+color+','+str(x)+','+str(y)+','+time+','+str(mid)
    send = str(uid)+' '+'fight'+' '+'do'+' '+str(fid)+' '+record
    # send = str(uid)+' '+'fight'+' '+'do'+' '+str(fid)+' '+ str(mid)+' '+record
    sq.put(send)
def putcmd(sq,msg):
    # send = str(uid)+' '+'fight'+' '+msg+' '+str(fid)
    send = str(uid)+' '+'fight'+' '+'judge'+' '+str(fid)+' '+msg
    sq.put(send)

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
        fontobj = pygame.font.Font(path+'t.ttf',25)
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
def qingqiuhuiqi(screen,rq,sq,a):
    global b
    L = huizhi(screen)
    rhuizhi(screen,L)
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20) 
    tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',80,40,0.9*w-40,0.9*h-20)
    tu(screen,'dfqqhq.png',360,80,0.5*w-180,0.4*h-40)
    tu(screen,'ty.png',80,40,0.4*w-40,0.7*h-20)
    tu(screen,'jj.png',80,40,0.6*w-40,0.7*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0.9*w-80<=event.pos[0]<=0.9*w+80  and  0.9*h-20<=event.pos[1]<=0.9*h+20:
                    sys.exit()
                if 0.4*w-80<=event.pos[0]<=0.4*w+80  and  0.7*h-20<=event.pos[1]<=0.7*h+20:
                    if a == 1:
                        putcmd(sq,'tongyi1')
                    elif a == 2:
                        putcmd(sq,'tongyi2')                    
                    tongyihuiqi(screen,rq,sq,0)
                if 0.6*w-40<=event.pos[0]<=0.6*w+40  and  0.7*h-20<=event.pos[1]<=0.7*h+20:
                    if a==1:
                        msg = 'xiaqi1'
                        putcmd(sq,msg)
                    elif a==2:
                        msg = 'xiaqi2'
                        putcmd(sq,msg)
                    sq.put(send1)
                    
                    L = huizhi(screen)
                    rhuizhi(screen,L)
                    fpsClock = pygame.time.Clock()
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        pygame.display.update()
        fpsClock.tick(30)
def tongyihuiqi(screen,rq,sq,a):
    for i in range(2):
        huiqi=info1.pop()
        l[huiqi[0]][huiqi[1]]=0
        count-=1
    if a == 1:
        xiaqi1(screen,rq,sq)
    elif a == 2:
        xiaqi2(screen,rq,sq)
    global b
    L = huizhi(screen)
    rhuizhi(screen,L)
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
    tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                qiangxingtuichu() 
            if event.type == pygame.MOUSEBUTTONDOWN:
 
                if 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.7*h-20<=event.pos[1]<=0.7*h+20:
                    if b==0:
                        b = 1
                    else:
                        b = 0
                    xianshishunxu1(screen,rq,sq)
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
       
        pygame.display.update()
        fpsClock.tick(30)




def win1(screen,rq,sq):
    global b,qpinfo,l,count

    L = huizhi(screen)
    rhuizhi(screen,L)
    w = screen.get_width()
    h = screen.get_height()
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
                    send = str(uid)+' '+'fight'+' '+'match'+' '+'p2p'
                    sq.put(send)

                    run(screen,rq,sq)
                if 0.6*w-40<=event.pos[0]<=0.6*w+40  and  0.7*h-20<=event.pos[1]<=0.7*h+20:
                    fanhui(screen,rq,sq) 
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
       
        pygame.display.update()
        fpsClock.tick(30)
def win2(screen,rq,sq):
    global b,qpinfo,l,count

    L = huizhi(screen)
    rhuizhi(screen,L)
    w = screen.get_width()
    h = screen.get_height()
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
                    send = str(uid)+' '+'fight'+' '+'match'+' '+'p2p'
                    sq.put(send)
                    run(screen,rq,sq)
                if 0.6*w-40<=event.pos[0]<=0.6*w+40  and  0.7*h-20<=event.pos[1]<=0.7*h+20:
                    fanhui(screen,rq,sq)
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)       
        pygame.display.update()
        fpsClock.tick(30)

def fanhui(screen,rq,sq):
    run(screen,rq,sq)
#等待对手接入信号
def waitlog(screen,rq,sq):
    L = huizhi(screen)
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'waitzb.png',720,80,0.5*w-360,0.4*h-40)
    tu(screen,'qxzb.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()                  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0.9*w-80<=event.pos[0]<=0.9*w+80  and  0.7*h-20<=event.pos[1]<=0.7*h+20:
                    msg = str(uid)+','+'fight'+','+'start'
                    sq.put(msg)
                    run(screen,rq,sq)
                if 0.9*w-80<=event.pos[0]<=0.9*w+80  and  0.9*h-20<=event.pos[1]<=0.9*h+20:
                    sys.exit()
        pygame.display.update()
        fpsClock.tick(30)
def huizhi(screen):
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'bg4.png',w,h,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    return L

def rhuizhi(screen,L):
    # 绘制当前盘面
    if qpinfo:
        for i in qpinfo:
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

#双方匹配好后服务器判定先手
def judgefirst(screen,rq,sq):
    L = huizhi(screen)
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'sjxs.png',640,80,0.5*w-320,0.7*h-40)
    tu(screen,'qxzb.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()                  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0.9*w-80<=event.pos[0]<=0.9*w+80  and  0.9*h-20<=event.pos[1]<=0.9*h+20:
                    sys.exit()
        pygame.display.update()
        fpsClock.tick(30)
#服务器　发送先手　　执行　先手黑
def first(screen,rq,sq):
    L = huizhi(screen)
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'zhxz.png',400,80,0.5*w-200,0.4*h-40)
    tu(screen,'qd.png',80,40,0.5*w-40,0.6*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()                  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0.9*w-80<=event.pos[0]<=0.9*w+80  and  0.9*h-20<=event.pos[1]<=0.9*h+20:
                    #游戏开始后强行退出即为负
                    qiangxingtuichu1(screen,rq,sq)
                if 0.5*w-40<=event.pos[0]<=0.5*w+40  and  0.6*h-20<=event.pos[1]<=0.6*h+20:
                    firststep(screen,rq,sq)     
        pygame.display.update()
        fpsClock.tick(30)
#白棋　等待　黑棋　完成信号
def second(screen,rq,sq):
    L = huizhi(screen)
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'wait.png',400,80,0.5*w-200,0.4*h-40)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()                  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0.9*w-80<=event.pos[0]<=0.9*w+80  and  0.9*h-20<=event.pos[1]<=0.9*h+20:
                    qiangxingtuichu2(screen,rq,sq)
        pygame.display.update()
        fpsClock.tick(30)
#黑色方　　执行下棋
def firststep(screen,rq,sq):
    global b,qpinfo,l,count
    permit = 0
    L = huizhi(screen)
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                qiangxingtuichu() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                z1 = 0
                for i in L:
                    z2 = 0
                    for j in i: 
                        if permit == 0 and j[0]-15<=event.pos[0]<=j[0]+15 and j[1]-15<=event.pos[1]<=j[1]+15 and l[z1][z2] == 0: 
                            qizi1 = qizi(screen,'black',18)
                            tu(screen,'hqz.png',40,40,int(j[0])-20,int(j[1])-20)
                            if b == 1:
                                qizi1.addc(int(j[0]),int(j[1]),str(count))
                            l[z2][z1] = 1
                            qpinfo.append((z2,z1,1,count))
                            msg = [count,z2,z1,'B']
                            putmsg(sq,msg)
                            count += 1
                            permit = 1   
                        z2 += 1
                    z1 += 1 
                if 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.7*h-20<=event.pos[1]<=0.7*h+20:
                    if b==0:
                        b = 1
                    else:
                        b = 0
                    xianshishunxu1(screen,rq,sq)
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)  
        pygame.display.update()
        fpsClock.tick(30)
def xianshishunxu1(screen,rq,sq):
    global b,qpinfo,l,count
    L = huizhi(screen)
    # 绘制当前盘面
    rhuizhi(screen,L)
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
    if b == 1: 
        tu(screen,'ycsx.png',160,40,0.9*w-80,0.7*h-20)
    elif b == 0:
        tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)

def xiaqi1(screen,rq,sq):
    global b,qpinfo,l,count
    permit = 0
    L = huizhi(screen)
    # 绘制当前盘面
    rhuizhi(screen,L)
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
    tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                qiangxingtuichu1(screen,sq) 
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
                            qpinfo.append((z2,z1,1,count))                           
                            if judgewin(l,1,screen)==1:
                                msg = [count,z2,z1,'B']
                                putmsg(sq,msg)
                                sleep(0.2)
                                msg1 = str(uid)+' '+'fight'+' '+'over'+' '+str(fid)+' '+'win'
                                sq.put(msg1)
                                win1(screen,rq,sq)

                            l[z2][z1] = 1
                            qpinfo.append((z2,z1,1,count))
                            msg = [count,z2,z1,'B']
                            putmsg(sq,msg)
                            count += 1
                            permit = 1  
                        z2 += 1
                    z1 += 1 
                if 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.7*h-20<=event.pos[1]<=0.7*h+20:
                    if b==0:
                        b = 1
                    else:
                        b = 0
                    xianshishunxu1(screen,rq,sq)
                if permit == 0 and 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.5*h-20<=event.pos[1]<=0.5*h+20: 
                    tu(screen,'fshq.png',800,80,0.5*w-400,0.4*h-40)
                    msg = 'Bqingqiuhuiqi'
                    putcmd(sq,msg)
                if permit == 0 and 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.9*h-20<=event.pos[1]<=0.9*h+20:
                    qiangxingtuichu1(screen,rq,sq)
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        pygame.display.update()
        fpsClock.tick(30)

def xiaqi2(screen,rq,sq):
    global b,qpinfo,l,count
    permit = 0
    L = huizhi(screen)
    rhuizhi(screen,L)
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
    tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                qiangxingtuichu2(screen,sq) 
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
                            qpinfo.append((z2,z1,2,count))
                            if judgewin(l,2,screen) == 1:
                                msg = [count,z2,z1,'W']
                                putmsg(sq,msg)
                                sleep(0.2)
                                msg1 = str(uid)+' '+'fight'+' '+'over'+' '+str(fid)+' '+'win'
                                sq.put(msg1)                                
                                win2(screen,rq,sq)
                            msg = [count,z2,z1,'W']
                            putmsg(sq,msg)
                            count += 1
                            permit = 1   
                        z2 += 1
                    z1 += 1 
                if 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.7*h-20<=event.pos[1]<=0.7*h+20:
                    if b==0:
                        b = 1
                    else:
                        b = 0
                    xianshishunxu1(screen,rq,sq)
                if permit == 0 and 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.5*h-20<=event.pos[1]<=0.5*h+20:
                    tu(screen,'fshq.png',800,80,0.5*w-400,0.4*h-40)
                    msg = 'Wqingqiuhuiqi'
                    putcmd(sq,msg)
                if permit == 0 and 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.9*h-20<=event.pos[1]<=0.9*h+20:
                    qiangxingtuichu2(screen,rq,sq)
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
       
        pygame.display.update()
        fpsClock.tick(30)

def qiangxingtuichu1(screen,rq,sq):
    #重新绘制棋盘根据请求是否继续强行退出游戏 是 发送强行退出到服务器 否继续游戏 发送给服务器对方胜
    global b,qpinfo,l,count
    permit = 0
    L = huizhi(screen)
    rhuizhi(screen,L)
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
    tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    tu(screen,'qxtc.png',480,80,0.5*w-240,0.4*h-40)
    tu(screen,'kid.png',240,40,0.65*w-120,0.65*h-20)
    tu(screen,'sure.png',80,40,0.4*w-40,0.65*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                qiangxingtuichu1(screen,sq) 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0.4*w-40<=event.pos[0]<=0.4*w+40 and 0.65*h-20<=event.pos[1]<=0.65*h+20:
                    msg = 'Bgiveup'                             
                    putcmd(sq,msg)
                    pygame.quit()
                    sys.exit()
                if 0.65*w-120<=event.pos[0]<=0.65*w+120 and 0.65*h-20<=event.pos[1]<=0.65*h+20:
                    xiaqi1(screen,rq,sq)
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        pygame.display.update()
        fpsClock.tick(30)

def qiangxingtuichu2(screen,rq,sq):
    global b,qpinfo,l,count
    permit = 0
    L = huizhi(screen)
    rhuizhi(screen,L)
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'hq.png',80,40,0.9*w-40,0.5*h-20)
    tu(screen,'xssx.png',160,40,0.9*w-80,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    tu(screen,'qxtc.png',480,80,0.5*w-240,0.4*h-40)
    tu(screen,'kid.png',240,40,0.65*w-120,0.65*h-20)
    tu(screen,'sure.png',80,40,0.4*w-40,0.65*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                qiangxingtuichu2(screen,rq,sq) 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0.4*w-40<=event.pos[0]<=0.4*w+40 and 0.65*h-20<=event.pos[1]<=0.65*h+20:
                    msg = 'Wgiveup'
                    putcmd(sq,msg)
                    pygame.quit()
                    sys.exit()
                if 0.65*w-120<=event.pos[0]<=0.65*w+120 and 0.65*h-20<=event.pos[1]<=0.65*h+20:
                    xiaqi2(screen,rq,sq)
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        pygame.display.update()
        fpsClock.tick(30)

#主线程
def run(screen,rq,sq):
    global b
    b = 0
    L = huizhi(screen)
    w = screen.get_width()
    h = screen.get_height()
    tu(screen,'zb.png',80,40,0.9*w-40,0.7*h-20)
    tu(screen,'tc.png',160,40,0.9*w-80,0.9*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        select(screen,rq,sq)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()                  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0.9*w-40<=event.pos[0]<=0.9*w+40  and  0.7*h-20<=event.pos[1]<=0.7*h+20:
                    send = str(uid)+' '+'fight'+' '+'start'
                    sq.put(send)
                    waitlog(screen,rq,sq)                    
                if 0.9*w-80<=event.pos[0]<=0.9*w+80  and  0.9*h-20<=event.pos[1]<=0.9*h+20:
                    sys.exit()
        pygame.display.update()
        fpsClock.tick(30)

#客户端主函数        
def double_fight(fsq,frq,uid1):
    global uid
    uid = uid1 
    windowname = 'wuziqi'
    width = 1024
    height = 800
    fillcolor = 'white'
    screen = window(windowname,width,height,fillcolor)
    sq = Queue(5)
    rq = Queue(5)
    th1 = Thread(target = sendinfo,args=(sq,fsq))
    th2 = Thread(target = recvinfo, args=(rq,frq))
    threads = [th1,th2]
    for t in threads:
        t.setDaemon(True)
        t.start()
    run(screen,rq,sq)


if __name__ == '__main__':
    double_fight()
