import pygame,sys
from pygame.color import THECOLORS
from pygame.locals import *
import mainmenu
#　创建　文字
def wenzi(screen,filename,size,text,x,y,color1,color2='white'):
    fontobj = pygame.font.Font(filename,size)
    textSurfaceobj = fontobj.render(text,True,THECOLORS[color1],THECOLORS[color2])
    textRectobj = textSurfaceobj.get_rect()
    textRectobj.center = (x,y)
    screen.blit(textSurfaceobj,textRectobj)
#插入图片
def tu(screen,filename,x1,y1,x2,y2):
    image =pygame.image.load(filename).convert_alpha()
    new = pygame.transform.scale(image,(x1,y1))
    screen.blit(new,(x2,y2))

#创建窗口
def window(name,x,y,color):
    #绘制主画面　棋盘　背景　图像　等一直显示的东西
    pygame.init()
    screencaption = pygame.display.set_caption(name)
    screen = pygame.display.set_mode([x,y])
    screen.fill(THECOLORS[color])
    return screen

#绘制棋盘
class qipan:
    #棋盘属性　　所在窗体，棋盘的大小位置
    def __init__(self,surface,xstart,xstop,ystart,ystop):
        self.surface = surface
        self.xstart = xstart
        self.xstop = xstop
        self.ystart = ystart
        self.ystop = ystop
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

#绘制棋子,color,r
class qizi:
    def __init__(self,surface,color,r):
        self.surface = surface
 
    def drawc(self,x,y):
        pygame.draw.circle(self.surface,THECOLORS[self.color],[x,y],self.r)

    #计步器
    def addc(self,x,y,t):
        fontobj = pygame.font.Font('1.TTF',25)
        # textSurfaceobj = fontobj.render(t,True,THECOLORS['red'],THECOLORS['green'])
        textSurfaceobj = fontobj.render(t,True,THECOLORS['red'])
        textRectobj = textSurfaceobj.get_rect()
        textRectobj.center = (x,y)
        self.surface.blit(textSurfaceobj,textRectobj)

#插入棋子
# tu(screen,'qizi.png',x1,y1,x2,y2)


#绘制主画面　棋盘　背景　图像　等一直显示的东西
def huamian(screen,w,h,x=1,y=1):
    #插入背景图
    tu(screen,'bg.png',1200,800,0,0)
    tu(screen,'log1.png',100,100,50,50)
    tu(screen,'log2.png',100,100,1100,50)
    #插入棋盘背景
    tu(screen,'bg1.png',700,700,250,100)
    #绘制棋盘,返回中心像素坐标值
    #生成棋盘对象，绘制棋盘，返回二维中心点列表，匹配　储值列表
    qipanobject = qipan(screen,350,850,200,700)
    L = qipanobject.drawqp()
    #绘制其他插件，包含可变插件
    # 右侧文字插件
    w = screen.get_width()
    h = screen.get_height()
    wenzi(screen,'t.ttf',20,'昵称',0.7*w,0.1*h,'black')
    wenzi(screen,'t.ttf',20,'个人中心',0.2*w,0.1*h,'black')
    wenzi(screen,'t.ttf',20,'模式选择',0.4*w,0.1*h,'black')
    wenzi(screen,'t.ttf',20,'好友',0.5*w,0.1*h,'black')
    wenzi(screen,'t.ttf',20,'战绩',0.6*w,0.1*h,'black')
    wenzi(screen,'t.ttf',20,'对话',0.7*w,0.1*h,'black')
    
    if x == 1:
        wenzi(screen,'t.ttf',40,'准备',0.85*w,0.4*h,'black')
    else:
        wenzi(screen,'t.ttf',40,'取消',0.85*w,0.4*h,'black')
    wenzi(screen,'t.ttf',40,'悔棋',0.85*w,0.5*h,'black')
    if y == 1:
        wenzi(screen,'t.ttf',40,'显示顺序',0.85*w,0.6*h,'black')
    else:
        wenzi(screen,'t.ttf',40,'隐藏顺序',0.85*w,0.6*h,'black')
    # wenzi(screen,'t.ttf',50,'取消',0.85*w,0.5*h,'black')

    wenzi(screen,'t.ttf',40,'返回主界面',0.85*w,0.8*h,'black')
    return L
    

def zhunbei(screen,w,h,n):
    zb = 0
    if n%2 == 1:
        huamian(screen,w,h,0,1) 
        #发送至服务器
        zb = 1
    else:
        huamian(screen,w,h,1,1)


    return zb 
def xiaqi(screen,L,l,S,win1,count,disp):
    z1 = 0
    for i in L:
        z2 = 0
        for j in i: 
            if not win1 and j[0]-15<=event.pos[0]<=j[0]+15 and j[1]-15<=event.pos[1]<=j[1]+15 and l[z1][z2] == 0:
                #创建棋子
                qizi1 = qizi(screen,color,18)
                qizi1.drawc(int(j[0]),int(j[1]))
                #计步器
                if dis1 != 1:
                    qizi1.addc(int(j[0]),int(j[1]),str(count))
                l[z1][z2] = sign
                win2 = judgewin(l,sign,screen)
                win1 = win2
                S.append(((z1,z2),(sign,count)))
                pygame.display.update()
                
                
                count += 1
            z2 += 1
        z1 += 1 
    if win1==1:
        #赢棋延迟时间1s
        
        if  330<=event.pos[0]<=370 and 530<=event.pos[1]<=570 :
            gcontinue()
        elif 580<=event.pos[0]<=620 and 530<=event.pos[1]<=570 :
            l = []
            win1 = 0
            again()

def huiqi():
    pass



def grzx(screen,w,h,x,y):
    huamian(screen,w,h,x,y)
    wenzi(screen,'t.ttf',20,'帐号',0.15*w,0.2*h,'black')
    wenzi(screen,'t.ttf',20,'ID',0.15*w,0.25*h,'black')
    wenzi(screen,'t.ttf',20,'我的好友',0.15*w,0.3*h,'black')
    wenzi(screen,'t.ttf',20,'我的战绩',0.15*w,0.35*h,'black')
    wenzi(screen,'t.ttf',20,'对战模式',0.15*w,0.4*h,'black')
    wenzi(screen,'t.ttf',20,'设置',0.15*w,0.45*h,'black')
    wenzi(screen,'t.ttf',20,'退出',0.15*w,0.5*h,'black')
    return 1

def tuichu(screen,w,h,x,y):
    screen.fill(THECOLORS['white'])
    huamian(screen,w,h,x,y)
    return 0


#等待处理的函数　　事件
def moshixuanze():
    print('模式选择')
def haoyou():
    print('好友')
def zhanji():
    print('战绩')
def zhanghao():
    print('帐号')
def ID():
    print('ID')
def myfriend():
    print('好友')
def myzhanji():
    print('战绩')
def moshi():
    print('对战模式')
def shezhi():
    print('设置')
def duihua():
    print('对话')


# 主函数
def main():
    #建立窗口
    screen = window('五子棋',1200,800,'white')
    w = screen.get_width()
    h = screen.get_height()
    L = huamian(screen,w,h)
    #生成15*15　二维列表　用于存储　棋盘值
    l = [[0 for i in range(15)] for i in range(15)]
    #准备判断
    n = 0
    #记录棋子顺序
    count = 1
    #显示顺序判断
    disp = 0
    #用于记录棋子位置的顺序的列表
    S = []
    #玩家1　准备完成信号 
    zb1 = 0
    zb2 = 1
    g = 0
    x = 1
    y = 1
    win1 = 0
    fpsClock = pygame.time.Clock()
    while 1:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            #所有的按钮事件，　每一个文字标题代表一处按钮，当涉及文本输入时，　用tkinter
            if event.type == pygame.MOUSEBUTTONDOWN:
                #下棋以外的其他事件
                if 0.2*w-40<=event.pos[0]<=0.2*w+40 and 0.1*h-20<=event.pos[1]<=0.1*h+20 :
                    g = grzx(screen,w,h,x,y)
                if 0.4*w-40<=event.pos[0]<=0.4*w+40 and 0.1*h-20<=event.pos[1]<=0.1*h+20 :
                    moshixuanze()
                if 0.5*w-20<=event.pos[0]<=0.5*w+20 and 0.1*h-10<=event.pos[1]<=0.1*h+10 :
                    haoyou()
                if 0.6*w-20<=event.pos[0]<=0.6*w+20 and 0.1*h-10<=event.pos[1]<=0.1*h+10 :
                    zhanji()
                if 0.7*w-20<=event.pos[0]<=0.7*w+20 and 0.1*h-10<=event.pos[1]<=0.1*h+10 :
                    duihua()
                if g== 1:
                    if 0.15*w-20<=event.pos[0]<=0.15*w+20 and 0.5*h-20<=event.pos[1]<=0.5*h+20 :
                        g = tuichu(screen,w,h,x,y)

                    if 0.15*w-20<=event.pos[0]<=0.15*w+20 and 0.2*h-10<=event.pos[1]<=0.2*h+10 :
                        zhanghao()
                    if 0.15*w-20<=event.pos[0]<=0.15*w+20 and 0.25*h-10<=event.pos[1]<=0.25*h+10 :
                        ID()
                    if 0.15*w-40<=event.pos[0]<=0.15*w+40 and 0.3*h-10<=event.pos[1]<=0.3*h+10 :
                        myfriend()
                    if 0.15*w-40<=event.pos[0]<=0.15*w+40 and 0.35*h-10<=event.pos[1]<=0.35*h+10 :
                        myzhanji()
                    if 0.15*w-40<=event.pos[0]<=0.15*w+40 and 0.4*h-10<=event.pos[1]<=0.4*h+10 :
                        moshi()
                    if 0.15*w-20<=event.pos[0]<=0.15*w+20 and 0.45*h-10<=event.pos[1]<=0.45*h+10 :
                        shezhi()

                                        
                if 0.85*w-40<=event.pos[0]<=0.85*w+40 and 0.8*h-20<=event.pos[1]<=0.8*h+20 :
                    mainmenu.homePage()

                # 准备　事件
                if 0.85*w-40<=event.pos[0]<=0.85*w+40 and 0.4*h-40<=event.pos[1]<=0.4*h+40 :
                    
                    zb1 = zhunbei(screen,w,h,n)
                    n += 1
                # # 下棋　事件 当玩家都准备好后　　可以进行进行下棋事件　，等待zb2 准备信号
                # if zb1 == 1 and zb2 == 1:
                #     xiaqi(screen,L,l,S,win1,count,disp)
                if count > 1:
                    if 0.85*w-40<=event.pos[0]<=0.85*w+40 and 0.5*h-40<=event.pos[1]<=0.5*h+40 :
                        huiqi()
                    if 0.85*w-40<=event.pos[0]<=0.85*w+40 and 0.4*h-40<=event.pos[1]<=0.4*h+40 :
                        display()


        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)            
        pygame.display.update()
        fpsClock.tick(30)
if __name__ == '__main__':
    main()


