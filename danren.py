import pygame,sys
from pygame.color import THECOLORS
from pygame.locals import *
#　创建　文字
def wenzi(screen,size,text,x,y,color1,color2='white'):
    fontobj = pygame.font.Font('t.ttf',size)
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




def huamian(screen,w,h):
    tu(screen,'bg2.png',1000,800,0,0)
    qipanobject = qipan(screen,200,800,100,700)
    L = qipanobject.drawqp()
    wenzi(screen,40,'开始游戏',0.9*w,0.3*h,'black')
    wenzi(screen,40,'模式选择',0.9*w,0.4*h,'black')
    wenzi(screen,40,'结束游戏',0.9*w,0.5*h,'black')
    wenzi(screen,40,'设置',0.9*w,0.6*h,'black')
    wenzi(screen,40,'返回主界面',0.9*w,0.7*h,'black')



    return L


def main():

    screen = window('人机对战',1000,800,'white')
    w = screen.get_width()
    h = screen.get_height()
    L = huamian(screen,w,h)



    fpsClock = pygame.time.Clock()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)            
        pygame.display.update()
        fpsClock.tick(30)
if __name__ == '__main__':
    main()
