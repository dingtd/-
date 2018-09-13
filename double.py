import pygame,sys,os
from pygame.color import THECOLORS
from pygame.locals import *
import mainmenu

PATH = os.getcwd()
# path = PATH + '/play/'

#初始化窗口
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
    # def last(self,x,y,t):
    #     fontobj = pygame.font.Font('t.ttf',25)
    #     # textSurfaceobj = fontobj.render(t,True,THECOLORS['red'],THECOLORS['green'])
    #     textSurfaceobj = fontobj.render(t,True,THECOLORS['blue'])
    #     textRectobj = textSurfaceobj.get_rect()
    #     textRectobj.center = (x,y)
    #     self.surface.blit(textSurfaceobj,textRectobj)


   
def xiaqi(screen,w,h,a,b,L,l,S,count,win1,flag1):
    fpsClock = pygame.time.Clock()

    while 1:
        for event in pygame.event.get():
            if count%2 == 1:
                sign = 1
                color = 'black'
                file ='hqz.png'
            elif count%2 ==0:
                sign = 2
                color = 'white'
                file ='bqz.png'
            if event.type == pygame.QUIT:
                sys.exit()                  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if a ==0 and 0.9*w-100<=event.pos[0]<=0.9*w+100 and 0.9*h-20<=event.pos[1]<=0.9*h+20: 
                    mainmenu.homePage()

                if a ==0 and 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.7*h-20<=event.pos[1]<=0.7*h+20:              
                    a = 1
                elif a == 1:
                    if 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.7*h-20<=event.pos[1]<=0.7*h+20:
                        jieshu(screen,w,h,a,b,L,l,S,count,win1,flag1)
                if b == 0 and 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.5*h-20<=event.pos[1]<=0.5*h+20:
                    b=1
                elif b == 1 and 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.5*h-20<=event.pos[1]<=0.5*h+20:
                    b=0
                if len(S)>0 and 0.9*w-80<=event.pos[0]<=0.9*w+80 and 0.3*h-20<=event.pos[1]<=0.3*h+20:
                    huiqi(screen,w,h,a,b,L,l,S,count,win1,flag1)
                if a == 1:
                    z1 = 0
                    for i in L:
                        z2 = 0
                        for j in i: 
                            if not win1 and j[0]-15<=event.pos[0]<=j[0]+15 and j[1]-15<=event.pos[1]<=j[1]+15 and l[z1][z2] == 0:
                                
                                qizi1 = qizi(screen,color,18)
                                tu(screen,file,40,40,int(j[0])-20,int(j[1])-20)
                                # qizi1.drawc(int(j[0]),int(j[1]))
                                #计步器
                                # qizi1.addc(int(j[0]),int(j[1]),str(count))
                                l[z1][z2] = sign
                                win1 = judgewin(l,sign,screen)
                               
                                S.append(((z1,z2),(sign,count)))
                                pygame.display.update()
                                
                                
                                count += 1
                            z2 += 1
                        z1 += 1 
                    if win1==1:

                        
                        if  0.4*w-40<=event.pos[0]<=0.4*w+40 and 0.6*h-20<=event.pos[1]<=0.6*h+20 :
                            #关闭文字，显示棋盘
                            main()
                        elif 0.6*w-40<=event.pos[0]<=0.6*w+40 and 0.6*h-20<=event.pos[1]<=0.6*w+20 :
                            
                            
                            again(screen,w,h,a,b,L,l,S,count,win1,flag1)
                    
                        if 0.85*w-50<=event.pos[0]<=0.85*w+50 and 0.3*h-50<=event.pos[1]<=0.3*h+50 :
                            pass
            
        
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






def jieshu(screen,w,h,a,b,L,l,S,count,win1,flag1):
    screen = window('wuziqi',1024,800,'white')
    huamian(screen,w,h,a,b,l,S,win1)
    tu1(screen,'qdjs.png',0.5*w-500,0.4*h-40)
    # wenzi(screen,60,'对局还没有结束，确定结束游戏？',0.5*w,0.3*h,'red')
    # wenzi(screen,40,'确定',0.4*w,0.6*h,'green')
    tu1(screen,'rjqd.png',0.4*w-120,0.6*h-20)
    # wenzi(screen,40,'取消',0.6*w,0.6*h,'green')
    tu1(screen,'rjqx.png',0.6*w-120,0.6*h-20)
    fpsClock = pygame.time.Clock()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()                  
            if event.type == pygame.MOUSEBUTTONDOWN:

                if 0.4*w-40<=event.pos[0]<=0.4*w+40  and  0.6*h-40<=event.pos[1]<=0.6*h+40:
                    
                    main()
                    
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
    huamian(screen,w,h,a,b,l,S,win1)
    xiaqi(screen,w,h,a,b,L,l,S,count,win1,flag1)





def huamian(screen,w,h,a,b,l,S,win1):
    tu(screen,'bg4.png',1024,800,0,0)
    s = qipan(screen,200,800,100,700)
    L = s.drawqp()
    if a == 0:
        tu1(screen,'rjks.png',0.9*w-120,0.7*h-20)
        # wenzi(screen,40,'开始游戏',0.9*w,0.7*h,'black')
    elif a == 1:
        # wenzi(screen,40,'结束游戏',0.9*w,0.7*h,'black')
        tu1(screen,'rjjs.png',0.9*w-120,0.7*h-20)
        # wenzi(screen,40,'悔棋',0.9*w,0.3*h,'black')
        tu1(screen,'rjhq.png',0.9*w-120,0.3*h-20)

        
        if b == 0:
            tu1(screen,'rjyc.png',0.9*w-120,0.5*h-20)
            # wenzi(screen,40,'隐藏顺序',0.9*w,0.5*h,'black')
        else:
            tu1(screen,'rjxs.png',0.9*w-120,0.5*h-20)
            # wenzi(screen,40,'显示顺序',0.9*w,0.5*h,'black')
    # wenzi(screen,40,'返回主界面',0.9*w,0.9*h,'black')
    # tu1(screen,'fhzjm.png',0.9*w-120,0.9*h-20)
    tu(screen,'fhzjm.png',250,50,0.9*w-125,0.9*h-20)
    


    if not S is True:
        for i in S:
            if i[1][0] == 1:
                color='black'
                file ='hqz.png'
            else:
                color ='white'
                file ='bqz.png'
            n = L[i[0][0]][i[0][1]]
            qizi1 = qizi(screen,color,18)
            qizi1.drawc(int(n[0]),int(n[1]))
            tu(screen,file,40,40,int(n[0])-20,int(n[1])-20)
            if b == 0:

                qizi1.addc(int(n[0]),int(n[1]),str(i[1][1]))
    if win1 == 1:
        win = S[-1][1][0]
        if win == 1:
            # wenzi(screen,100,'黑棋胜！',0.5*w,0.3*h,'red')
            tu1(screen,'hwin.png',0.5*w-220,0.4*h-40)

        elif win == 2:
            # wenzi(screen,100,'白棋胜！',0.5*w,0.3*h,'red')
            tu1(screen,'bwin.png',0.5*w-220,0.4*h-40)

        # wenzi(screen,40,'结束',0.4*w,0.6*h,'green')
        tu1(screen,'rjjs1.png',0.4*w-120,0.6*h-20)
        # wenzi(screen,40,'再来一局',0.6*w,0.6*h,'green')
        tu1(screen,'rjzlyj.png',0.6*w-120,0.6*h-20)
        # wenzi(screen,40,'确定',0.4*w,0.6*h,'green')



    return L


def main():
    
    
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
    
    xiaqi(screen,w,h,a,b,L,l,S,count,win1,flag1)

if __name__ == '__main__':
    main()
