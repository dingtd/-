import pygame,sys
from pygame.color import THECOLORS
from pygame.locals import *

def chushi(name,x,y,color):
    pygame.init()   
    screencaption = pygame.display.set_caption(name)
    screen = pygame.display.set_mode([x,y])
    screen.fill(THECOLORS[color])
    return screen 
#创建棋盘类．．．
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
        y3 = y2
        for i in range(15):
            l = []
            x3 = x2
            for j in range(15):
                l.append([x3,y3])
                x3+= length
            y3 += length
            L.append(l)
        print(L)
        #绘制九个中心点圆形
        s=[L[7][7],L[3][3],L[3][7],L[7][3],L[3][11],L[7][11],L[11][3],L[11][11],L[11][7]]        
        for i in s:
            pygame.draw.circle(screen,THECOLORS['black'],[int(i[0]),int(i[1])],6)
        return L
def up(i,j,sign):
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
                x = l[i][j]
                break
    s = [count,x]
    return s
def down(i,j,sign):
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
                x = l[i][j]
                break
    s = [count,x]
    return s
def lleft(i,j,sign):
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
                x = l[i][j]
                break
    s = [count,x]
    return s
def rright(i,j,sign):
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
                x = l[i][j]
                break
    s = [count,x]
    return s
def lup(i,j,sign):
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
                x = l[i][j]
                break
    s = [count,x]
    return s
def ldown(i,j,sign):
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
                x = l[i][j] 
                break
    s = [count,x]
    return s 
def rup(i,j,sign):
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
                x = l[i][j]
                break
    s = [count,x]
    return s 
def rdown(i,j,sign):
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
                x = l[i][j]
                break
    s =[count,x]
    return s
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
                if up(i,j,sign)[0]+down(i,j,sign)[0] >= 4:
                    win(sign)
                    return
                elif lleft(i,j,sign)[0]+rright(i,j,sign)[0] >= 4:
                    win(sign)
                    return
                elif lup(i,j,sign)[0]+ldown(i,j,sign)[0] >= 4:
                    win(sign)
                    return
                elif rup(i,j,sign)[0]+rdown(i,j,sign)[0] >= 4:
                    win(sign)
                    return
def count(l,sign):
    L = {}
    for i in range(15):
        for j in range(15):
            if l[i][j] == 0:
                crow = up(i,j,sign)+down(i,j,sign)

                cshu =lleft(i,j,sign)+rright(i,j,sign)

                cleft =lup(i,j,sign)+ldown(i,j,sign)

                cright =rup(i,j,sign)+rdown(i,j,sign)

                L[(i,j)] = [crow,cshu,cleft,cright]
    print(L)
    return L

def position(l):
    # 计算分数，白棋，黑棋
    # 生成一个用来存各位置分数的字典　　S[(i,j)] = score
    S = {}
    s1 = count(l,2)
    print(sorted(s1.items(),key = lambda x:x[0],reverse = True))
    print('----------------------------')
    s2 = count(l,1)
    print(sorted(s2.items(),key = lambda x:x[0],reverse = True))
    print('=============================')
    for i in range(15):
        
        for j in range(15):
            if l[i][j] == 0:
                score = 0
                t = 0
                w = 0
                for k in s1[(i,j)]:
                    # 白棋评分标准
                    if k[0]+k[2]+1>=5:
                        score += 200000
                    elif k[0]+k[2]+1== 4 and k[1]==0 and k[3] ==0:
                        score+= 70000
                    #不再边界上
                    elif k[0]+k[2]+1== 4 and ((k[1]==0 and  k[3]!= 0 or 1) or (k[1]!= 0 or 1 and k[3] == 0)):
                        score+=60000
                    elif k[0]+k[2]+1==3 and k[1]==0 and k[3] ==0:
                        score+=30000
                        t+=1
                if  t>=2:
                    score+=10000
                    
                    
                   
                for f in s2[(i,j)]:
                    if f[0]+f[2]+1>=5:
                        score += 150000
                    elif f[0]+f[2]+1== 4 and f[1]==0 and f[3] ==0:
                        score+=50000
                    elif f[0]+f[2]+1== 4 and ((f[1]==0 and f[3]!= 0 or 2) or (f[1]!= 0 or 2 and f[3] == 0)):
                        w += 1
                    elif f[0]+f[2]+1==3 and k[1]==0 and k[3] ==0:               
                        w +=1
                print(w,'00000000000000000++++++++++++++++++++++ ')
                if w>=2:
                    score+=35000
               
                
                S[(i,j)] = score
    s = sorted(S.items(),key = lambda x:x[1],reverse = True)
    print(s)
    print('--++++++++++++++++++++++++++++++++++++------')
    
    del s1,s2,S   
        # if s == []:
        #     return
    return s[0][0]

        

if __name__ == '__main__':
    screen = chushi('wuziqi',700,700,'white')
    qipan1 = qipan(screen,100,600,100,600)
    fpsClock = pygame.time.Clock()
    L = qipan1.drawqp()
    l = [[0 for i in range(15)] for j in range(15)]
    count1 = 0
    win1 = 0
    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            # if count%2 == 0:
            #     flag = 1
            #     color='white'
            # else:
            #     flag = 2
            #     color='black'
            if event.type == pygame.MOUSEBUTTONDOWN:
                msg =''
                #判断棋子中心点
                z1 = 0
                # if  not win(flag) :
                for i in L:
                    z2 = 0
                    for j in i:
                        
                        if win1 == 0 and l[z1][z2]==0 and j[0]-10<=event.pos[0]<=j[0]+10 and j[1]-10<=event.pos[1] <= j[1]+10:
                            #创建棋子
                            # print(l[z2][z1])
                            qizi1 = qizi(screen,'black',20)
                            qizi1.drawc(int(j[0]),int(j[1]))
                            count1 += 1
                            

                            # print(z2,z1)
                            l[z1][z2] = 1
                            # renji(l)
                         
                            # print(l)
                            judgewin(l,1)
                            
                        z2 += 1
                    z1 += 1
                
                if count1%2 == 1:
                    count1 +=1
                    qizi2 = qizi(screen,'blue',20)
                    Y =position(l)

                    qizi2.drawc(int((L[Y[0]][Y[1]])[0]),int((L[Y[0]][Y[1]])[1]))
                    l[Y[0]][Y[1]] = 2

                    judgewin(l,2)
                print(l)
                print('+*****************************************')

                    
                   


        pygame.display.update()
        fpsClock.tick(40)
