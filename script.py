#$Id: script.py,v 1.1 2007/11/20 14:22:00 ffb Exp $#
#-*- coding:utf-8 -*-

# Last Update
# by hoker.ffb[hoker.ffb@gmail.com] 2008-1-7

import pygame
import rpg
import psp2dex
from inc import *
from dialog import *
import os


def movie1(view):
    img = pygame.image.load(os.path.join("data/", "logo.jpg"))
    rect = view.get_rect()
    alpha = 0
    while alpha < 250:
        img.set_alpha(alpha)
        view.blit(img, rect)
        alpha += 2
        pygame.display.flip()
        pygame.time.delay(10)

    pygame.time.delay(2000)


def movie2(view, map, player1):
    say = Dialog()
    say.init("box.png", view)

    while True:
        pad = psp2dex.Controller()

        if pad.space or pad.esc:
            break
        view.fill((0, 0, 0))
        map.draw()
        player1.draw()
        map.present()
        player1.drawDebug(view)
        say.draw('木桶镇')
        pygame.display.flip()
    pygame.event.clear()


def main():
    pygame.init()
    #view = pygame.display.set_mode((Inc.ScreenW, Inc.ScreenH), pygame.FULLSCREEN)
    view = pygame.display.set_mode((Inc.ScreenW, Inc.ScreenH))
    pygame.display.set_caption('CaskTown2 - http://mutong.saveasdf.com')
    view.fill((0, 0, 0))

    rpggame = rpg.Rpg(view)

    # logo
    #movie1(view)

    movie2(view, rpggame.map, rpggame.player1)

    rpg.play(view)

if __name__ == '__main__':
    try:
        main()
    except:
        import traceback
        traceback.print_exc(file=file('trace.txt', 'w'))
