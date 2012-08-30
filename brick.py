#$Id: map.py,v 1.1 2007/11/20 14:22:00 ffb Exp $#
#-*- coding:utf-8 -*-
# Last Update 
# by hoker.ffb[hoker.ffb@gmail.com] 2008-2-4
# homepage: http://mutong.saveasdf.com/
# project homepage: http://gforge.osdn.net.cn/projects/rpg2/

import pygame
from log import *
from inc import *
from ani import *
import os

# 符号
class Sym:
    def __init__(self):
        self.Code = ""
        self.Img = ""
        self.Through = True
        
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
class Brick(Ani):
    def __init__(self, imgFile, frame_count, x, y):
        Ani.__init__(self, 0, imgFile, frame_count)
        self.x = x
        self.y = y
        self.through = True
    def draw(self, view):
        Ani.draw(self, view, self.x, self.y)
    def canThrough(self):
        return self.through
        
     
def testCase():
    view = pygame.display.set_mode((480,272))
    pygame.display.set_caption('Class Map testCase.')
    
    b = Brick("data/brick1.png", 2, x=1, y=1)
    
    for i in range(1, 99):
        b.updateImg()
        b.draw(view)
        pygame.display.flip()
        pygame.time.delay(100)
        
if __name__ == '__main__':
    testCase()

