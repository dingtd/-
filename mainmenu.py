# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import pygame
import os
PATH = os.getcwd()
from pygame.color import THECOLORS
from pygame import *
import modd
import double
import net
path = PATH + '/play/'


#　创建　文字
def wenzi(screen, size, text, x, y, color1, color2='white'):
    fontobj = pygame.font.Font(path + 't.ttf', size)
    textSurfaceobj = fontobj.render(
        text, True, THECOLORS[color1], THECOLORS[color2])
    textRectobj = textSurfaceobj.get_rect()
    textRectobj.center = (x, y)
    screen.blit(textSurfaceobj, textRectobj)
# 插入图片


def tu(screen, filename, x1, y1, x2, y2):
    image = pygame.image.load(path + filename).convert_alpha()
    new = pygame.transform.scale(image, (x1, y1))
    screen.blit(new, (x2, y2))


def tu1(screen, filename, x, y):
    image = pygame.image.load(path + filename).convert_alpha()
    screen.blit(image, (x, y))

# 创建窗口


def window(name, x, y, color):
    # 绘制主画面　棋盘　背景　图像　等一直显示的东西
    pygame.init()
    screencaption = pygame.display.set_caption(name)
    screen = pygame.display.set_mode([x, y])
    screen.fill(THECOLORS[color])
    return screen


def huamian(screen, w, h, a, b, c, d, e):
    screen.fill(THECOLORS['white'])
    tu(screen, 'bg8.png', 1200, 800, 0, 0)
    tu1(screen, 'bt1.png', 0.2 * w, 0.2 * h)

    if a == 0:
        # tu1(screen,'dan.png',0.7*w-80,0.5*h-20)
        tu(screen, 'dan1.png', 250, 40, 0.7 * w - 125, 0.5 * h - 20)
    else:
        tu1(screen, 'dan2.png', 0.7 * w - 80, 0.5 * h - 20)

    if b == 0:
        # tu1(screen,'doub.png',0.7*w-80,0.6*h-20)
        tu(screen, 'doub1.png', 250, 40, 0.7 * w - 125, 0.6 * h - 20)
    else:
        tu1(screen, 'db2.png', 0.7 * w - 80, 0.6 * h - 20)
    if c == 0:
        # tu1(screen,'wl.png',0.7*w-80,0.7*h-20)
        tu(screen, 'net.png', 250, 40, 0.7 * w - 125, 0.7 * h - 20)
    else:
        tu1(screen, 'wl2.png', 0.7 * w - 80, 0.7 * h - 20)
    if d == 0:
        tu1(screen, 'sz.png', 0.7 * w - 40, 0.8 * h - 20)
    else:
        tu1(screen, 'sz2.png', 0.7 * w - 40, 0.8 * h - 20)
    if e == 0:
        tu1(screen, 'tc1.png', 0.7 * w - 80, 0.9 * h - 20)
    else:
        tu1(screen, 'tc2.png', 0.7 * w - 80, 0.9 * h - 20)

    tu1(screen, 'cp.png', w - 100, h - 20)


def homePage():
    screen = window('大闸蟹五子棋', 1200, 800, 'white')
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    w = screen.get_width()
    h = screen.get_height()
    w1 = w
    w2 = w
    w3 = 0
    huamian(screen, w, h, a, b, c, d, e)
    fpsClock = pygame.time.Clock()

    while 1:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                if 0.7 * w - 80 <= event.pos[0] <= 0.7 * w + 80 and 0.5 * h - 20 <= event.pos[1] <= 0.5 * h + 20:
                    a = 1
                else:
                    a = 0
                if 0.7 * w - 80 <= event.pos[0] <= 0.7 * w + 80 and 0.6 * h - 20 <= event.pos[1] <= 0.6 * h + 20:
                    b = 1
                else:
                    b = 0
                if 0.7 * w - 80 <= event.pos[0] <= 0.7 * w + 80 and 0.7 * h - 20 <= event.pos[1] <= 0.7 * h + 20:
                    c = 1
                else:
                    c = 0
                if 0.7 * w - 80 <= event.pos[0] <= 0.7 * w + 80 and 0.8 * h - 20 <= event.pos[1] <= 0.8 * h + 20:
                    d = 1
                else:
                    d = 0
                if 0.7 * w - 80 <= event.pos[0] <= 0.7 * w + 80 and 0.9 * h - 20 <= event.pos[1] <= 0.9 * h + 20:
                    e = 1
                else:
                    e = 0
            if event.type == MOUSEBUTTONDOWN:
                if 0.7 * w - 80 <= event.pos[0] <= 0.7 * w + 80 and 0.5 * h - 20 <= event.pos[1] <= 0.5 * h + 20:
                    modd.main()

                if 0.7 * w - 80 <= event.pos[0] <= 0.7 * w + 80 and 0.6 * h - 20 <= event.pos[1] <= 0.6 * h + 20:
                    double.main()

                if 0.7 * w - 80 <= event.pos[0] <= 0.7 * w + 80 and 0.7 * h - 20 <= event.pos[1] <= 0.7 * h + 20:
                    net.main()

                if 0.7 * w - 80 <= event.pos[0] <= 0.7 * w + 80 and 0.8 * h - 20 <= event.pos[1] <= 0.8 * h + 20:
                    shezhi.main()

                if 0.7 * w - 80 <= event.pos[0] <= 0.7 * w + 80 and 0.9 * h - 20 <= event.pos[1] <= 0.9 * h + 20:
                    tuichu()

        w1 -= 5

        huamian(screen, w, h, a, b, c, d, e)
        tu1(screen, 'tit.png', w1, 0)
        if w1 == 0:
            w3 = 1
            w2 = w
        if w3 == 1:
            w2 -= 5

            tu1(screen, 'tit.png', w2, 0)

        if w2 == 0:
            w1 = w

        x, y = pygame.mouse.get_pos()
        tu(screen, 'log2.png', 40, 40, x - 20, y - 10)
        pygame.mouse.set_visible(False)
        pygame.display.update()
        fpsClock.tick(30)


def shezhi():
    pass
    # 字体颜色
    # 背景图片
    # 背景音乐
    # 广告关闭
    #


def tuichu():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    homePage()
