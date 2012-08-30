#$Id: fire.py,v 1.1 2008/02/11 15:11:00 ffb Exp $#
#-*- coding:utf-8 -*-
# Last Update
# by hoker.ffb[hoker.ffb@gmail.com] 2008-2-11
# homepage: http://mutong.saveasdf.com/
# project homepage: http://gforge.osdn.net.cn/projects/rpg2/

import pygame
from inc import *
from log import *
from datetime import datetime
import random
import os


FIRE_NEW = 0
FIRE_FLY = 1
FIRE_EXPLODE = 2
FIRE_END = 3


class Fire:
    def __init__(self, x, y, direction, mapM):
        self.x = x
        self.y = y
        self.direction = direction
        self.img = pygame.image.load(os.path.join("data/", "fire.png"))
        self.flag = FIRE_FLY
        self.life = 250
        self.mapM = mapM
        pass

    def draw(self, view):
        if self.flag == FIRE_FLY:
            view.blit(self.img, (self.x, self.y))
        elif self.flag == FIRE_EXPLODE:
            #pygame.draw.rect(view, (0,0,200), (self.x, self.y, self.life, self.life),1)
            pygame.draw.circle(view, (0, 0, 200), (self.x, self.y), self.life, 1)

    def getNextPos(self):
        x = self.x
        y = self.y
        if self.direction == Inc.RIGHT:
            x += 1
        elif self.direction == Inc.LEFT:
            x -= 1
        elif self.direction == Inc.DOWN:
            y += 1
        elif self.direction == Inc.UP:
            y -= 1
        return x, y

    def update(self):
        if self.flag == FIRE_FLY:
            x, y = self.getNextPos()
            mapM = self.mapM
            rpgXY = mapM.getRpgXy([[x, y]])
            if mapM.canMove(rpgXY):
                self.x, self.y = x, y
                self.life -= 1
                if self.life < 0:
                    self.flag = FIRE_END
            else:
                self.flag = FIRE_EXPLODE
                self.life = 1 + random.randrange(0, 5)
                self.x += random.randrange(-10, 10)
                self.y += random.randrange(-10, 10)
        elif self.flag == FIRE_EXPLODE:
            self.life += 1
            if self.life > 50:
                self.flag = FIRE_END


class Fires:
    FiresManager = None

    @staticmethod
    def getFires():
        if None == Fires.FiresManager:
            Fires.FiresManager = Fires()
        return Fires.FiresManager

    def __init__(self):
        self.fires = []
        self.view = None
        pass

    def update(self):
        for i in range(0, 10):
            for f in self.fires:
                if f.flag != FIRE_END:
                    f.update()
            for f in self.fires:
                if f.flag == FIRE_END:
                    self.fires.remove(f)
                    break  # 考虑如何删除所有END标记的对象
        pass

    def draw(self):
        for f in self.fires:
            f.draw(self.view)
        pass

if __name__ == '__main__':
    import rpg
    rpg.play()
