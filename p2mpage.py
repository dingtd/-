import pygame,sys,os
# import sys,pygame,os
PATH = os.getcwd()
from pygame.color import THECOLORS
from pygame.locals import *



path = PATH + '/play/'
#初始化窗口
def window(name,x,y,color):
    pygame.init()   
    screencaption = pygame.display.set_caption(name)
    screen = pygame.display.set_mode([x,y])
    screen.fill(THECOLORS[color])
    return screen 
def wenzi(screen,size,text,x,y,color1):
    fontobj = pygame.font.Font(path+'t.ttf',size)
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
# 胜负处理
    # def win(screen,sign):
    #     global win1
    #     if sign == 1:
    #         msg = '黑棋胜利！'
    #     elif sign == 2:
    #         msg = '白棋胜利！'
        
    #     wenzi(screen,100,msg,600,350,'red')
    #     # fontobj = pygame.font.Font('t.ttf',100)
    #     # textSurfaceobj = fontobj.render(msg,True,THECOLORS['red'],THECOLORS['green'])
    #     # textRectobj = textSurfaceobj.get_rect()
    #     # textRectobj.center = (500,320)
    #     # screen.blit(textSurfaceobj,textRectobj)
    #     wenzi(screen,100,'再来一局',350,500,'red')
    #     wenzi(screen,100,'继续',550,500,'red')
    #     # fontobj = pygame.font.Font('t.ttf',40)
    #     # textSurfaceobj = fontobj.render('继续',True,THECOLORS['black'],THECOLORS['yellow'])
    #     # textRectobj = textSurfaceobj.get_rect()
    #     # textRectobj.center = (350,550)
    #     # screen.blit(textSurfaceobj,textRectobj)
    #     # wenzi(screen,40,'再来一局','black','yellow',600,550)
    #     win1 = 1  
    #     return win1
def judgewin(l,sign,screen):

    for i in range(15):
        for j in range(15):
            #判断每个位置是否五连棋
            if l[i][j] == sign:
                # while 1:
                if up(l,i,j,sign)+down(l,i,j,sign) >= 4:
                    
                    return sign
                elif left(l,i,j,sign)+right(l,i,j,sign) >= 4:
                    
                    return sign
                elif lup(l,i,j,sign)+ldown(l,i,j,sign) >= 4:
                    
                    return sign
                elif rup(l,i,j,sign)+rdown(l,i,j,sign) >= 4:
                    
                    return sign 
# def huiqi(l,count,L,S):
    #     m =S.pop()
        
    #     count -= 1
    #     x=m[0][0]
    #     y=m[0][1]
    #     l[x][y]=0
    #     pygame.init()
    #     screen = window('wuziqi',1024,800,'white')
    #     a = qipan(screen,200,800,100,700)
    #     win1 = 0

    #     bg = tu('bg1.png',700,700)
    #     screen.blit(bg,(100,50))
    #     a = qipan(screen,200,700,150,650)

    #     L = a.drawqp()
    #     print(L)
    #     for i in S:
    #         if i[1] == 1:
    #             color='black'
    #         else:
    #             color ='white'
    #         n = L[i[0][0]][i[0][1]]
    #         qizi1 = qizi(screen,color,18)
    #         qizi1.drawc(int(n[0]),int(n[1]))



    #     xiaqi(screen,w,h,a,b,L,l,S,count,win1,flag1)
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
def xiaqi(screen,w,h,a,b,L,l,S,count,win1,flag1):
    fpsClock = pygame.time.Clock()

    while 1:
        for event in pygame.event.get():
            # if count%2 == 1:
            #     sign = 1
            #     color = 'black'
            # elif count%2 ==0:
            #     sign = 2
            #     color = 'white'
            if event.type == pygame.QUIT:
                sys.exit()                  
            if event.type == pygame.MOUSEBUTTONDOWN:

                # if a ==0 and 0.9*w-100<=event.pos[0]<=0.9*w+100 and 0.9*h-20<=event.pos[1]<=0.9*h+20: 
                #     mod.main()

                if a ==0 and 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.7*h-20<=event.pos[1]<=0.7*h+20:              
                    a = 1
                elif a ==0 and 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.85*h-20<=event.pos[1]<=0.85*h+20:              
                    sys.exit()
                elif a == 1:
                    if 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.7*h-20<=event.pos[1]<=0.7*h+20:
                        result = jieshu(screen,w,h,a,b,L,l,S,count,win1,flag1)
                        if result == 'exit':
                            return 'exit'
                if b == 0 and 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.5*h-20<=event.pos[1]<=0.5*h+20:
                    b=1
                elif b == 1 and 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.5*h-20<=event.pos[1]<=0.5*h+20:
                    b=0
                if len(S)>0 and 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.3*h-20<=event.pos[1]<=0.3*h+20:
                    huiqi(screen,w,h,a,b,L,l,S,count,win1,flag1)
                if a == 1 and count%2!=0:
                    z1 = 0
                    for i in L:
                        z2 = 0
                        for j in i: 
                            if not win1 and j[0]-15<=event.pos[0]<=j[0]+15 and j[1]-15<=event.pos[1]<=j[1]+15 and l[z1][z2] == 0:
                                
                                qizi1 = qizi(screen,'black',18)
                                qizi1.drawc(int(j[0]),int(j[1]))
                                #计步器
                                # qizi1.addc(int(j[0]),int(j[1]),str(count))
                                l[z1][z2] = 1
                                S.append(((z1,z2),(1,count)))
                                win1 = judgewin(l,1,screen)
                               
                               
                                
                                pygame.display.update()
                                
                                
                                count += 1
                            z2 += 1
                        z1 += 1 
                    if count%2 == 0 and win1 !=1:
                        
                        qizi2 = qizi(screen,'blue',20)
                        Y =position(l)

                        qizi2.drawc(int((L[Y[0]][Y[1]])[0]),int((L[Y[0]][Y[1]])[1]))
                        l[Y[0]][Y[1]] = 2
                        S.append(((Y[0],Y[1]),(2,count)))
                        win1 = judgewin(l,2,screen)
                        
                        count +=1

                        

                    if win1==1 or win1 == 2:

                        
                        if  0.4*w-40<=event.pos[0]<=0.4*w+40 and 0.6*h-20<=event.pos[1]<=0.6*h+20 :
                            #关闭文字，显示棋盘
                            p2mPage()
                        elif 0.6*w-40<=event.pos[0]<=0.6*w+40 and 0.6*h-20<=event.pos[1]<=0.6*w+20 :
                            
                            
                            again(screen,w,h,a,b,L,l,S,count,win1,flag1)
                    
                        if 0.9*w-50<=event.pos[0]<=0.85*w+50 and 0.3*h-50<=event.pos[1]<=0.3*h+50 :
                            pass
            
        position(l)
        screen.fill(THECOLORS['white'])
        huamian(screen,w,h,a,b,l,S,win1)   
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
       
        pygame.display.update()
        fpsClock.tick(30)
def again(screen,w,h,a,b,L,l,S,count,win1,flag1):
    a = 1
    b = 0
    S = []
    count = 1
    win1 = 0
    flag1 = 0
    l = [[0 for i in range(15)] for i in range(15)]
    huamian(screen,w,h,a,b,l,S,win1)
    xiaqi(screen,w,h,a,b,L,l,S,count,win1,flag1)
    return 'exit'
def jieshu(screen,w,h,a,b,L,l,S,count,win1,flag1):
    screen = window('wuziqi',1024,800,'white')
    huamian(screen,w,h,a,b,l,S,win1)
    wenzi(screen,60,'对局还没有结束，确定结束游戏？',0.5*w,0.3*h,'red')
    wenzi(screen,40,'确定',0.4*w,0.6*h,'green')
    wenzi(screen,40,'取消',0.6*w,0.6*h,'green')
    fpsClock = pygame.time.Clock()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() 
                return 'exit'

            if event.type == pygame.MOUSEBUTTONDOWN:

                if 0.4*w-40<=event.pos[0]<=0.4*w+40  and  0.6*h-40<=event.pos[1]<=0.6*h+40:
                    
                    p2mPage()
                    
                if 0.6*w-40<=event.pos[0]<=0.6*w+40  and  0.6*h-40<=event.pos[1]<=0.6*h+40:
                    xiaqi(screen,w,h,a,b,L,l,S,count,win1,flag1)
        pygame.display.update()
        fpsClock.tick(30)
def huiqi(screen,w,h,a,b,L,l,S,count,win1,flag1):
    s = S.pop()
    x = s[0][0]
    y = s[0][1]
    l[x][y] = 0
    count -= 1
    s = S.pop()
    x = s[0][0]
    y = s[0][1]
    l[x][y] = 0
    count -= 1
    huamian(screen,w,h,a,b,l,S,win1)
    xiaqi(screen,w,h,a,b,L,l,S,count,win1,flag1)
    return 'exit'
def huamian(screen,w,h,a,b,l,S,win1):
    tu(screen,path+'bg4.png',1024,800,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    if a == 0:
        wenzi(screen,40,'开始游戏',0.9*w,0.7*h,'black')
        wenzi(screen,40,'退出游戏',0.9*w,0.85*h,'black')
    elif a == 1:
        wenzi(screen,40,'结束游戏',0.9*w,0.7*h,'black')
        wenzi(screen,40,'悔棋',0.9*w,0.3*h,'black')

        if b == 0:
            wenzi(screen,40,'隐藏顺序',0.9*w,0.5*h,'black')
        else:
            wenzi(screen,40,'显示顺序',0.9*w,0.5*h,'black')
    # wenzi(screen,40,'选择模式',0.9*w,0.9*h,'black')
    if win1 == 1 or win1 == 2:
        win = S[-1][1][0]
        # print(win)
        if win == 1:
            wenzi(screen,100,'黑棋胜！',0.5*w,0.3*h,'red')

        elif win == 2:
            wenzi(screen,100,'白棋胜！',0.5*w,0.3*h,'red')

        wenzi(screen,40,'结束',0.4*w,0.6*h,'green')
        wenzi(screen,40,'再来一局',0.6*w,0.6*h,'green')
        # wenzi(screen,40,'确定',0.4*w,0.6*h,'green')

    if not S is True:
        for i in S:
            if i[1][0] == 1:
                color='black'
            else:
                color ='blue'
            n = L[i[0][0]][i[0][1]]
            qizi1 = qizi(screen,color,18)
            qizi1.drawc(int(n[0]),int(n[1]))
            if b == 0:
                qizi1.addc(int(n[0]),int(n[1]),str(i[1][1]))

    return L
def p2mPage():  
    screen = window('wuziqi',1024,800,'white')
    w = screen.get_width()
    h = screen.get_height()
    #开始游戏标志
    a = 0
    #显示顺序标志
    b = 0
    # #
    # c = 0
    win1 = 0
    l = [[0 for i in range(15)] for i in range(15)]
    count = 1
    S = []
    flag1 = 0
    L = huamian(screen,w,h,a,b,l,S,win1)
    if L == 'exit':
        return
    xiaqi(screen,w,h,a,b,L,l,S,count,win1,flag1)
def up1(l,i,j,sign):
    s = []
    count = 0
    x = 3
    if i == 0:
        count =0
    else:
        while 1:
            if i >= 1:
                i -= 1
                if l[i][j] == sign:
                    count += 1
                else:
                    x = l[i][j]
                    break
            else:
                x = 3
                break
    s = [count,x]
    return s
def down1(l,i,j,sign):
    s = []
    count = 0
    x = 3
    if i == 14:
        count = 0
    else:
        while 1:
            if i <= 13:
                i += 1
                if l[i][j] == sign:
                    count += 1
                else:
                    x = l[i][j]
                    break
            else:
                x = 3
                break
    s = [count,x]
    return s
def lleft1(l,i,j,sign):
    s = []
    count = 0
    x = 3
    if j == 0:
        count = 0
    else:
        while 1:
            if j >= 1:
                j -= 1
                if l[i][j] == sign:
                    count += 1
                else:
                    x = l[i][j]
                    break
            else:
                x = 3
                break
    s = [count,x]
    return s
def rright1(l,i,j,sign):
    s = []
    count = 0
    x = 3
    if j == 14:
        count = 0
    else :
        while 1:
            if j <= 13:
                j += 1
                if l[i][j] == sign:
                    count += 1
                else:
                    x = l[i][j]
                    break
            else:
                x = 3
                break
    s = [count,x]
    return s
def lup1(l,i,j,sign):
    s = []
    count = 0
    x = 3
    if i == 0 or j == 14:
        count = 0
    else :
        while 1:
            if i >= 1 and j <= 13:
                i -= 1
                j += 1
                if l[i][j] == sign:
                    count += 1
                else:
                    x = l[i][j]
                    break
            else:
                x = 3
                break
    s = [count,x]
    return s
def ldown1(l,i,j,sign):
    s = []
    count = 0
    x = 3
    if i == 14 or j == 0:
        count = 0
    else:
        while 1:
            if i <= 13 and j >= 1:
                i += 1
                j -= 1
                if l[i][j] == sign:
                    count += 1
                else:
                    x = l[i][j]
                    break
            else:
                x = 3 
                break
    s = [count,x]
    return s 
def rup1(l,i,j,sign):
    s = []
    count = 0
    x = 3
    if i == 0 or j ==0:
        count = 0
    else:
        while 1:
            if j >= 1 and i >= 1:
                i -= 1
                j -= 1
                if l[i][j] == sign:
                    count += 1
                else:
                    x = l[i][j]
                    break
            else:
                x = 3
                break
    s = [count,x]
    return s 
def rdown1(l,i,j,sign):
    s = []
    count = 0
    x = 3
    if i == 14 or j ==14:
        count = 0
    else:
        while 1:
            if i <= 13 and j <= 13:
                i += 1
                j += 1
                if l[i][j] == sign:
                    count += 1
                else:
                    x = l[i][j]
                    break
            else:
                x = 3
                break
    s =[count,x]
    return s
def count(l,sign):
    L = {}
    for i in range(15):
        for j in range(15):
            if l[i][j] == 0:
                crow1 = up1(l,i,j,sign)+down1(l,i,j,sign)

                cshu1 =lleft1(l,i,j,sign)+rright1(l,i,j,sign)

                cleft1 =lup1(l,i,j,sign)+ldown1(l,i,j,sign)

                cright1 =rup1(l,i,j,sign)+rdown1(l,i,j,sign)

                L[(i,j)] = [crow1,cshu1,cleft1,cright1]
    return L
def position(l):
    # 计算分数，白棋，黑棋
    # 生成一个用来存各位置分数的字典　　S[(i,j)] = score
    D2={}
    D1={}
    for i in range(15):
        for j in range(15):
            D2[(i,j)] = (0,0)
            D1[(i,j)] = (0,0)
    S = {}
    s1 = count(l,2)

    s2 = count(l,1)
    # print(s1,'白棋')
    # sleep(2)
    # print(s2,'黑棋')
    # sleep(2)


    for i in range(15):        
        for j in range(15):
            if l[i][j] == 0:
                score = 0
                
                biaoji2=0
                c2 = 1
                for k in s1[(i,j)]:  #[c1,a,c2,b]  (6, 7): [[0, 0, 0, 1], [1, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0]]
                    
                #白棋先计算棋子数 5 4 3情况  3 再判定
                    if k[0] + k[2] + 1 >=5:
                        score += 1000000
                    elif k[0] + k[2] + 1 ==4:
                        if k[1] == 0 and k[3] == 0:
                            score += 500000
                        elif k[1] == 0 and k[3] != 0:
                            biaoji2 = 1
                            D2[(i,j)] =(D2[(i,j)][0] + 1,biaoji2)

                        elif k[1] != 0 and k[3] == 0:
                            biaoji2 = 1 
                            D2[(i,j)] =(D2[(i,j)][0] + 1,biaoji2)


                    elif k[0] + k[2] + 1 == 3 and k[1] == 0 and k[3] == 0:
                        score += 40000
                        # D2[(i,j)] =(D2[(i,j)][0] + 1,biaoji2)
                        

                        # 横方向
                        # 竖方向
                        #左斜方向
                        #右斜方向
                        # if k[0] == 2:
                        #     if i+2 <= 14 and l[i+2][j] == 0:
                        #         D2[(i+1,j)] =D2[(i+1,j)] + 1
                        #     elif j+2 <= 14 and l[i][j+2] == 0:
                        #         D2[(i,j+1)] =D2[(i,j+1)] + 1
                        #     elif i+2 <= 14 and j-2 >=0 and l[i+2][j-2] == 0:
                        #         D2[(i+1,j-1)] =D2[(i+1,j-1)] + 1
                        #     elif i-2>=0 and j-2 >=0 and l[i-2][j-2]==0:
                        #         D2[(i-1,j-1)] = D2[(i-1,j-1)] +1
                        #     # i+1 为空 i+2 也为空时 (i+2,j) 伪三+1
                        # elif k[2] == 2:
                        #     if i-2 >= 0 and l[i-2][j] == 0:
                        #         D2[(i-1,j)] =D2[(i-1,j)] + 1
                        #     elif j-2 >= 0 and l[i][j-2] ==0 :
                        #         D2[(i,j-1)] = D2[(i,j-1)] +1
                        #     elif i-2>=0 and j+2<=14 and l[i-2][j+2] == 0:
                        #         D2[(i-1,j+1)] = D2[(i-1,j+1)] +1
                        #     elif i+2<=14 and j+2 <=14 and l[i+2][j+2]==0:
                        #         D2[(i-1,j-1)] =D2[(i-1,j-1)] + 1
                        #     # i-1 为空 i-2 也为空时 (i-2,j) 伪三+1
                        # elif k[0] == 1 and k[2] == 1:
                        #     if i-3 >= 0 and l[i-3][j] == 0:
                        #         D2[(i-2,j)] =D2[(i-2,j)] + 1
                        #     elif i+3 <= 14 and l[i+3][j] == 0:
                        #         D2[(i+2,j)] =D2[(i+2,j)] + 1
                        #     elif j-3 >= 0 and l[i-3][j] == 0:
                        #         D2[(i,j-2)] =D2[(i,j-2)]+ 1
                        #     elif j+3 <= 14 and l[i+3][j] == 0:
                        #         D2[(i,j+2)] =D2[(i,j+2)] + 1
                        #     elif i-3 >= 0 and j+3<= 14 and l[i-3][j+3] == 0:
                        #         D2[(i-2,j+2)] =D2[(i-2,j+2)] + 1
                        #     elif j-3 >=0 and i +3<=14 and l[i+3][j-3] == 0:
                        #         D2[(i+2,j-2)] =D2[(i+2,j-2)] + 1
                        #     elif i-3 >= 0 and j-3>=0 and l[i-3][j-3] == 0:
                        #         D2[(i-2,j-2)] =D2[(i-2,j-2)] + 1
                        #     elif j+3 <=14 and i +3<=14 and l[i+3][j+3] == 0:
                        #         D2[(i+2,j+2)] =D2[(i+2,j+2)] + 1

                    #活二
                    elif k[0] + k[2] + 1 ==2 and k[1] == 0 and k[3] == 0:
                        score += 1000
                        if k[0] == 1:
                            if c2==1 and j+3<=14 and l[i][j+2]==2 and l[i][j+3]==0:
                                D2[(i,j)] =(D2[(i,j)][0] + 1,biaoji2)
                            if c2==2 and i+3<=14 and l[i+2][j]==2 and l[i+3][j]==0:
                                D2[(i,j)] =(D2[(i,j)][0] + 1,biaoji2)
                            if c2 == 3 and i+3<=14 and j-3>=0 and l[i+2][j-2]==2 and l[i+3][j-3]==0:
                                D2[(i,j)] =(D2[(i,j)][0] + 1,biaoji2)
                            if c2 ==4 and i+3<=14 and j+3<=14 and l[i+2][j+2]==2 and l[i+3][j+3]==0:
                                D2[(i,j)] =(D2[(i,j)][0] + 1,biaoji2)
                        elif k[2] == 1:
                            if c2 ==1 and j-3>=0 and l[i][j-2]==2 and l[i][j-3]==0:
                                D2[(i,j)] =(D2[(i,j)][0] + 1,biaoji2)
                            if c2==2 and i-3>=0 and l[i-2][j]==2 and l[i-3][j]==0:
                                D2[(i,j)] =(D2[(i,j)][0] + 1,biaoji2)
                            if c2 == 3 and j+3<=14 and i-3>=0 and l[i-2][j+2]==2 and l[i-3][j+3]==0:
                                D2[(i,j)] =(D2[(i,j)][0] + 1,biaoji2)
                            if c2 == 4 and i-3>=0 and j-3>=0 and l[i-2][j-2]==2 and l[i-3][j-3]==0:
                                D2[(i,j)] =(D2[(i,j)][0] + 1,biaoji2)
                    # if k[0] + k[2] + 1 == 3 and (k[1] == 0 and k[3] != 0) or (k[3] == 0 and k[1] != 0):
                    elif k[0]+k[2]==0:
                        if i==7 and j == 7:
                            score +=21
                        else:
                            if c2 ==1 and j-4>=0 and j+1 <=14 and l[i][j-4]==0 and l[i][j-3]==2 and l[i][j-2]==2 and l[i][j-1]==0 and j+1<=14 and l[i][j+1]==0:

                                D2[(i,j)] = (D2[(i,j)][0] +1,biaoji2)
                            elif c2 ==1 and j+4<=14 and j-1>=0 and l[i][j+4]==0 and l[i][j+3]==2 and l[i][j+2]==2 and l[i][j+1]==0 and j+4<=14 and l[i][j-1]==0:
                                D2[(i,j)] = (D2[(i,j)][0] +1,biaoji2)
                            if c2 ==2 and i-4>=0 and i+1<= 14 and l[i-4][j]==0 and l[i-3][j]==2 and l[i-2][j]==2 and l[i-1][j]==0 and i+1<=14 and l[i+1][j]==0:
                                D2[(i,j)] = (D2[(i,j)][0] +1,biaoji2)
                            elif c2 ==2 and i+4<=14 and i-1 >=0 and l[i+4][j]==0 and l[i+3][j]==2 and l[i+2][j]==2 and l[i+1][j]==0 and i+4<=14 and l[i-1][j]==0:
                                D2[(i,j)] = (D2[(i,j)][0] +1,biaoji2)
                            if c2 ==3 and i-4>=0 and j+4<=14 and i+1<=14 and j-1>=0 and l[i-4][j+4]==0 and l[i-3][j+3]==2 and l[i-2][j+2]==2 and l[i-1][j+1]==0 and l[i+1][j-1]==0:
                                D2[(i,j)] = (D2[(i,j)][0] +1,biaoji2)
                            elif c2 ==3 and j-4>=0 and i+4<=14 and i-1>=0 and j+1 <=14 and l[i+4][j-4]==0 and l[i+3][j-3]==2 and l[i+2][j-2]==2 and l[i+1][j-1]==0 and l[i-1][j+1]==0:
                                D2[(i,j)] = (D2[(i,j)][0] +1,biaoji2)
                            if c2 ==4 and i-4>=0 and j-4>=0 and i+1<=14 and j+1<=14 and l[i-4][j-4]==0 and l[i-3][j-3]==2 and l[i-2][j-2]==2 and l[i-1][j-1]==0 and l[i+1][j+1]==0:
                                D2[(i,j)] = (D2[(i,j)][0] +1,biaoji2)
                            elif c2 ==4 and j+4<=14 and i+4<=14 and i-1>=0 and j-1>=0 and l[i+4][j+4]==0 and l[i+3][j+3]==2 and l[i+2][j+2]==2 and l[i+1][j+1]==0 and l[i-1][j-1]==0:
                                D2[(i,j)] = (D2[(i,j)][0] +1,biaoji2)
                    c2+=1
                    #     score += 50
                biaoji = 0
                c1 = 1
                for k in s2[(i,j)]:  #[c1,a,c2,b]
                #白棋先计算棋子数 5 4 3情况  3 再判定
                    if k[0] + k[2] + 1 >=5:
                        score += 700000
                    elif k[0] + k[2] + 1 ==4:
                        if k[1] == 0 and k[3] == 0:
                            score += 60000
                        elif k[1] == 0 and k[3] != 0:
                            biaoji = 1
                            D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)
                            
                        elif k[1] != 0 and k[3] == 0:
                            biaoji = 1
                            D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)
                            
                    elif k[0] + k[2] + 1 == 3 and k[1] == 0 and k[3] == 0:
                        score += 1200
                        D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)



                        # 横方向
                        # 竖方向
                        #左斜方向
                        #右斜方向
                        # if k[0] == 2:
                        #     if i+2 <= 14 and l[i+2][j] == 0:
                        #         D1[(i+1,j)] = (D1[(i+1,j)][0] +1,biaoji)
                        #     elif j+2 <= 14 and l[i][j+2] == 0:
                        #         D1[(i,j+1)] =(D1[(i,j+1)][0] + 1,biaoji)
                        #     elif i+2 <= 14 and j-2 >=0 and l[i+2][j-2] == 0:
                        #         D1[(i+1,j-1)] =(D1[(i+1,j-1)] +1,biaoji)
                        #     elif i-2>=0 and j-2 >=0 and l[i-2][j-2]==0:
                        #         D1[(i-1,j-1)] =(D1[(i-1,j-1)][0] + 1,biaoji)
                        #     # i+1 为空 i+2 也为空时 (i+2,j) 伪三+1
                        # elif k[2] == 2:
                        #     if i-2 >= 0 and l[i-2][j] == 0:
                        #         D1[(i-1,j)] =(D1[(i-1,j)][0] + 1,biaoji)
                        #     elif j-2 >= 0 and l[i][j-2] ==0 :
                        #         D1[(i,j-1)] =(D1[(i,j-1)][0]+ 1,biaoji)
                        #     elif i-2>=0 and j+2<=14 and l[i-2][j+2] == 0:
                        #         D1[(i-1,j+1)] = (D1[(i-1,j+1)][0] +1,biaoji)
                        #     elif i+2<=14 and j+2 <=14 and l[i+2][j+2]==0:
                        #         D1[(i+1,j+1)] = (D1[(i+1,j+1)][0] +1,biaoji)
                        #     # i-1 为空 i-2 也为空时 (i-2,j) 伪三+1
                        # elif k[0] == 1 and k[2] == 1:
                        #     if i-3 >= 0 and l[i-3][j] == 0:
                        #         D1[(i-2,j)] = (D1[(i-2,j)][0] +1,biaoji)
                        #     elif i+3 <= 14 and l[i+3][j] == 0:
                        #         D1[(i+2,j)] =(D1[(i+2,j)][0] + 1,biaoji)
                        #     elif j-3 >= 0 and l[i-3][j] == 0:
                        #         D1[(i,j-2)] =  (D1[(i,j-2)][0] +1,biaoji)
                        #     elif j+3 <= 14 and l[i+3][j] == 0:
                        #         D1[(i,j+2)] = (D1[(i,j+2)][0] +1,biaoji)
                        #     elif i-3 >= 0 and j+3<= 14 and l[i-3][j+3] == 0:
                        #         D1[(i-2,j+2)] =(D1[(i-2,j+2)][0] + 1,biaoji)
                        #     elif j-3 >=0 and i +3<=14 and l[i+3][j-3] == 0:
                        #         D1[(i+2,j-2)] = (D1[(i+2,j-2)][0] +1,biaoji)
                        #     elif i-3 >= 0 and j-3>=0 and l[i-3][j-3] == 0:
                        #         D1[(i-2,j-2)] = (D1[(i-2,j-2)][0] +1,biaoji)
                        #     elif j+3 <=14 and i +3<=14 and l[i+3][j+3] == 0:
                        #         D1[(i+2,j+2)] = (D1[(i+2,j+2)][0]+1,biaoji)



                    #活二  还需要为其他位置的活三计数
                    elif k[0] + k[2] + 1 ==2 and k[1] == 0 and k[3] == 0:
                        score += 80
                        if k[0] == 1:
                            if c1 ==1 and j+3<=14 and l[i][j+2]==1 and l[i][j+3]==0:
                                D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)
                            if c1 ==2 and i+3<=14 and l[i+2][j]==1 and l[i+3][j]==0:
                                D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)
                            if c1 == 3 and i+3<=14 and j-3>=0 and l[i+2][j-2]==1 and l[i+3][j-3]==0:
                                D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)
                            if c1 ==4 and i+3<=14 and j+3<=14 and l[i+2][j+2]==1 and l[i+3][j+3]==0:
                                D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)
                        elif k[2] == 1:
                            if c1 ==1 and j-3>=0 and l[i][j-2]==1 and l[i][j-3]==0:
                                D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)
                            if c1==2 and i-3>=0 and l[i-2][j]==1 and l[i-3][j]==0:
                                D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)
                            if c1==3 and j+3<=14 and i-3>=0 and l[i-2][j+2]==1 and l[i-3][j+3]==0:
                                D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)
                            if c1 == 4 and i-3>=0 and j-3>=0 and l[i-2][j-2]==1 and l[i-3][j-3]==0:
                                D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)
                    # elif k[0] + k[2] + 1 == 3 and (k[1] == 0 and k[3] != 0) or (k[3] == 0 and k[1] != 0):
                    #     score += 80
                    elif k[0]+k[2]==0:
                        if i==7 and j == 7:
                            score +=21
                        else:
                            if c1==1 and j-4>=0 and j+1<=14 and l[i][j-4]==0 and l[i][j-3]==1 and l[i][j-2]==1 and l[i][j-1]==0 and j+1<=14 and l[i][j+1]==0:

                                D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)
                            elif c1==1 and j+4<=14 and j-1>=0 and l[i][j+4]==0 and l[i][j+3]==1 and l[i][j+2]==1 and l[i][j+1]==0 and j+4<=14 and l[i][j-1]==0:
                                D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)
                            if c1==2 and  i-4>=0 and i+1 <=14 and l[i-4][j]==0 and l[i-3][j]==1 and l[i-2][j]==1 and l[i-1][j]==0 and i+1<=14 and l[i+1][j]==0:
                                D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)
                            elif c1==2 and i+4<=14 and i-1>=0 and l[i+4][j]==0 and l[i+3][j]==1 and l[i+2][j]==1 and l[i+1][j]==0 and i+4<=14 and l[i-1][j]==0:
                                D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)
                            if  c1==3 and i-4>=0 and j+4<=14 and i+1<=14 and j-1>=0 and l[i-4][j+4]==0 and l[i-3][j+3]==1 and l[i-2][j+2]==1 and l[i-1][j+1]==0 and l[i+1][j-1]==0:
                                D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)
                            elif  c1==3 and j-4>=0 and i+4<=14 and i-1>=14 and j+1<=14 and l[i+4][j-4]==0 and l[i+3][j-3]==1 and l[i+2][j-2]==1 and l[i+1][j-1]==0 and l[i-1][j+1]==0:
                                D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)
                            if c1==4 and  i-4>=0 and j-4>=0 and i+1<=14 and j+1<=14 and l[i-4][j-4]==0 and l[i-3][j-3]==1 and l[i-2][j-2]==1 and l[i-1][j-1]==0 and l[i+1][j+1]==0:
                                D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)
                            elif c1==4 and  j+4<=14 and i+4<=14 and i-1>=0 and j-1>=0 and l[i+4][j+4]==0 and l[i+3][j+3]==1 and l[i+2][j+2]==1 and l[i+1][j+1]==0 and l[i-1][j-1]==0:
                                D1[(i,j)] = (D1[(i,j)][0] +1,biaoji)
                        c1+=1




                
                S[(i,j)] = score


    for i in S:
        
        if D2[i][0] ==1:
            S[i] = S[i]+35000 
        if D2[i][0] >=2 :
            if D2[i][1]==1:
                S[i]=S[i]+200000
            else:
                S[i]=S[i]+100000
        if D1[i][0] >= 2:
            if D1[i][1] == 1:
                S[i]=S[i]+150000
            else:
                S[i]=S[i]+75000
               
                
        # S[(i,j)] = score
    s = sorted(S.items(),key = lambda x:x[1],reverse = True)



    

    position1 = s[0][0]
    return position1

if __name__ == '__main__':
    p2mPage()
