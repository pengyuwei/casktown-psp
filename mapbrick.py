#$Id: map.py,v 1.1 2007/11/20 14:22:00 ffb Exp $#
#-*- coding:utf-8 -*-
# Last Update
# by hoker.ffb[hoker.ffb@gmail.com] 2008-2-4
# homepage: http://mutong.saveasdf.com/
# project homepage: http://gforge.osdn.net.cn/projects/rpg2/

import pygame
from log import *
from inc import *
import os


# 事件
class Event:
    def __init__(self):
        self.flag = 0
        self.event = None
        self.nextmap = ""
        self.playerx = 1
        self.playery = 1
        self.sym = ""


# 组成地图的元素（砖块）
class MapBrick:
    def __init__(self, view, sym, imgFile, x, y):
        self.img = pygame.image.load(os.path.join("data/", imgFile))
        self.x = x
        self.y = y
        self.through = True
        self.sym = sym
        self.view = view
        self.evt = Event()

    def canThrough(self):
        return self.through

    def draw(self):
        self.view.blit(self.img, (self.x, self.y))
        #debug
        if self.evt.event != None:
            pygame.draw.rect(self.view, (0, 0, 200), \
                    (self.x, self.y, Inc.BoxW, Inc.BoxH), 1)
        #end debug

    def draw(self, view):
        view.blit(self.img, (self.x, self.y))
        #debug
        if self.evt.event != None:
            self.img = None
            pygame.draw.rect(self.view, (0, 0, 200), \
                   (self.x, self.y, Inc.BoxW, Inc.BoxH), 1)
        #end debug


def testCase():
    pass

if __name__ == '__main__':
    testCase()
