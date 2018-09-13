import pygame,sys
sys.path.append("/home/tarena/桌面/client/play")
import rj,jdrj,gjrj
from pygame.color import THECOLORS
from pygame.locals import *
import mainmenu
#　创建　文字
def wenzi(screen,size,text,x,y,color1,color2='white'):
    fontobj = pygame.font.Font('t.ttf',size)
    textSurfaceobj = fontobj.render(text,True,THECOLORS[color1],THECOLORS[color2])

    pygame.image.save(textSurfaceobj, "name.png")
    image =pygame.image.load('name.png')
    screen.blit(image,(x,y))
    # textRectobj = textSurfaceobj.get_rect()
    # textRectobj.center = (x,y)
    # screen.blit(textSurfaceobj,textRectobj)



#插入图片
def tu(screen,filename,x1,y1,x2,y2):
    image =pygame.image.load(filename).convert_alpha()
    new = pygame.transform.scale(image,(x1,y1))
    screen.blit(new,(x2,y2))
def tu1(screen,filename,x,y):
    image =pygame.image.load(filename).convert_alpha()
    screen.blit(image,(x,y))


#创建窗口
def window(name,x,y):
    #绘制主画面　棋盘　背景　图像　等一直显示的东西
    pygame.init()
    screencaption = pygame.display.set_caption(name)
    screen = pygame.display.set_mode([x,y])
    screen.fill(THECOLORS['white'])
    return screen

def huamian(screen,w,h,a,b,c,d):
    tu(screen,'bg3.png',500,650,0,0)
    tu1(screen,'ms.png',0.3*w,0.25*h)

    if a == 0:
        tu1(screen,'jd1.png',0.45*w,0.4*h)
    else:
        tu1(screen,'jd2.png',0.45*w,0.4*h)
    if b == 0:
        tu1(screen,'yb1.png',0.45*w,0.55*h)
    else:
        tu1(screen,'yb2.png',0.45*w,0.55*h)
    if c == 0:
        tu1(screen,'kn1.png',0.45*w,0.7*h)
    else:
        tu1(screen,'kn2.png',0.45*w,0.7*h)
    if d == 0:
        tu1(screen,'fh1.png',0.35*w,0.85*h)
    else:
        tu1(screen,'fh2.png',0.35*w,0.85*h)





        # wenzi(screen,40,'简单',0.5*w,0.3*h,'black')


        # wenzi(screen,40,'一般',0.5*w,0.5*h,'black')
        # wenzi(screen,50,'困难',0.5*w,0.7*h,'pink')
        # wenzi(screen,40,'困难',0.5*w,0.7*h,'black')

        # wenzi(screen,50,'返回主菜单',0.5*w,0.9*h,'pink')
        # wenzi(screen,40,'返回主菜单',0.5*w,0.9*h,'black')



def main():
    a = 0
    b = 0
    c = 0
    d = 0
    screen = window('模式选择',500,650)
    w = screen.get_width()
    h = screen.get_height()
    huamian(screen,w,h,a,b,c,d)

    fpsClock = pygame.time.Clock()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                
                if 225<=event.pos[0]<=290 and 260<=event.pos[1]<=300:
                    a = 1
                else:
                    a = 0
                if 225<=event.pos[0]<=290 and 360<=event.pos[1]<=390:
                    b = 1
                else:
                    b = 0
                if 225<=event.pos[0]<=290 and 460<=event.pos[1]<=490:
                    c = 1
                else:
                    c = 0
                if 150<=event.pos[0]<=450 and 560<=event.pos[1]<=590:
                    d = 1
                else:
                    d = 0


            if event.type == pygame.MOUSEBUTTONDOWN:
                if 225<=event.pos[0]<=290 and 260<=event.pos[1]<=300:
                    jdrj.p2mPage()

                if 225<=event.pos[0]<=290 and 360<=event.pos[1]<=390:
                    rj.p2mPage()

                if 225<=event.pos[0]<=290 and 460<=event.pos[1]<=490:
                    gjrj.p2mPage()


                if 150<=event.pos[0]<=450 and 560<=event.pos[1]<=590:
                    mainmenu.homePage()

        huamian(screen,w,h,a,b,c,d)
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)            
        pygame.display.update()
        fpsClock.tick(30)

# if __name__ == '__main__':
#     main()
