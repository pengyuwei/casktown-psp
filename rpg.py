#$Id: script.py,v 1.1 2007/11/20 14:22:00 ffb Exp $#
#-*- coding:utf-8 -*-
# Last Update
# by hoker.ffb[hoker.ffb@gmail.com] 2008-2-4
# homepage: http://mutong.saveasdf.com/
# project homepage: http://gforge.osdn.net.cn/projects/rpg2/

import pygame
import psp2dex
from map import Map as RpgMap
from player import *
from inc import *
from dialog import *
from datetime import datetime
from fire import *
from manager import *
from object import *
from npc import *


class Rpg:
    player1 = None
    map = None

    def __init__(self, view):
        self.player1 = None
        self.map = None

        self.map = RpgMap.getMap()
        self.map.view = view
        self.map.changeMap('map_01', 3, 3)

        self.player1 = Player.getPlayer1()
        self.player1.init('p1', self.map.bufViewMap)
        self.player1.xMax = self.map.mapWPix
        self.player1.yMax = self.map.mapHPix

        Rpg.map = self.map
        Rpg.player1 = self.player1


def play(view):

    map = Rpg.map
    player1 = Rpg.player1

    # 用于计算P1的自动Stop
    timeImgFilp = datetime.now()
    timePass = datetime.now() - timeImgFilp
    # 用于限制游戏速度
    timeSpeed = datetime.now()
    timePassSpeed = datetime.now() - timeSpeed

    fires = Fires.getFires()
    fires.view = map.bufViewMap
    while True:
        pad = psp2dex.Controller()

        if pad.circle or pad.esc:
            break
        if pad.altenter:
            view = pygame.display.set_mode((Inc.ScreenW, Inc.ScreenH), pygame.FULLSCREEN)
        if pad.left:
            timeImgFilp = datetime.now()
            for i in range(1, 8):
                if PlayerMoveLeft(player1, map):
                    break
        if pad.right:
            timeImgFilp = datetime.now()
            for i in range(1, 8):
                if PlayerMoveRight(player1, map):
                    break

        if pad.up:
            timeImgFilp = datetime.now()
            for i in range(1, 8):
                if PlayerMoveUp(player1, map):
                    break
        if pad.down:
            timeImgFilp = datetime.now()
            for i in range(1, 8):
                if PlayerMoveDown(player1, map):
                    break
        if pad.square:
            # J 开火
            fire = Fire(player1.x, player1.y, player1.direction, map)
            fires.fires.append(fire)
            pass
        if pad.space:
            Action(player1, map)
            pass

        # 1P 自动站住
        timePass = datetime.now() - timeImgFilp
        if timePass.days * 24 * 60 * 60 * 1000 + timePass.seconds * 1000 + timePass.microseconds / 1000 > 110:
            timeImgFilp = datetime.now()
            player1.stop()

        view.fill((0, 0, 0))
        map.draw()
        player1.draw()
        fires.update()
        fires.draw()
        map.present()

        # debug info
        player1.drawDebug(view)
        map.drawDebug(view)
        t = "hotMap(%d,%d), view(%d,%d in %d,%d)" % \
                (map.hotMapX, map.hotMapY, map.viewX, map.viewY, map.mapWPix, map.mapHPix)
        psp2dex.drawText(view, t, 0, 10)
        t = "view(%d,%d,%d)" % \
                        (map.viewX, Inc.ScreenW / 2, map.viewX - Inc.ScreenW / 2)
        psp2dex.drawText(view, t, 0, 20)
        # end debug info

        # 限制游戏速度
        while True:
            timePassSpeed = datetime.now() - timeSpeed
            timePassSpeedmicroseconds = timePassSpeed.days * 24 * 60 * 60 * 1000 + timePassSpeed.seconds * 1000 + timePassSpeed.microseconds / 1000
            if timePassSpeedmicroseconds > 30:
                timeSpeed = datetime.now()
                break

        pygame.display.flip()

    print "The End."


def PlayerMoveLeft(player1, map):
    player1.setDirection(Player.Left)
    x, y = player1.getNextPos()
    lstRpgXY = map.getRpgXy([ \
                              [x + 1, y + 1], \
                              [x + 1, y + Inc.FootH - 1] \
                             ])
    if map.canMove(lstRpgXY):
        player1.moveLeft()
        if -player1.x > (map.viewX - Inc.ScreenW / 2):
            map.moveView(Inc.moveStepPix, 0)
        map.raiseEventAuto(lstRpgXY, 0)
    else:
        player1.stop()
    return False


def PlayerMoveRight(player1, map):
    player1.setDirection(Player.Right)
    x, y = player1.getNextPos()
    lstRpgXY = map.getRpgXy([ \
                                  [x + Inc.PlayerW - 1, y + 1], \
                                  [x + Inc.PlayerW - 1, y + Inc.FootH - 1] \
                                 ])
    if map.canMove(lstRpgXY):
        player1.moveRight()
        if player1.x - map.viewX > Inc.ScreenW / 2:
            map.moveView(-Inc.moveStepPix, 0)
        map.raiseEventAuto(lstRpgXY, 0)
    else:
        player1.stop()
    return False


def PlayerMoveUp(player1, map):
    player1.setDirection(Player.Up)
    x, y = player1.getNextPos()
    lstRpgXY = map.getRpgXy([ \
                              [x + 1, y + 1], \
                              [x + Inc.FootW - 1, y + 1] \
                             ])
    if map.canMove(lstRpgXY):
        player1.moveUp()
        if -player1.y > (map.viewY - Inc.ScreenH / 2):
            map.moveView(0, Inc.moveStepPix)
        map.raiseEventAuto(lstRpgXY, 0)
    else:
        player1.stop()
    return False


def PlayerMoveDown(player1, map):
    player1.setDirection(Player.Down)
    x, y = player1.getNextPos()
    lstRpgXY = map.getRpgXy([ \
                              [x + 1, y + Inc.FootH - 1], \
                              [x + Inc.FootW - 1, y + Inc.FootH - 1] \
                             ])
    if map.canMove(lstRpgXY):
        player1.moveDown()
        if player1.y - map.viewY > Inc.ScreenH / 2:
            map.moveView(0, -Inc.moveStepPix)
        map.raiseEventAuto(lstRpgXY, 0)
    else:
        player1.stop()
    return False


def Action(player1, map):
    player1.setDirection(Player.Up)
    x, y = player1.getNextPos()
    lstRpgXY = map.getRpgXy([ \
                              [x + 1, y + 1], \
                              [x + Inc.FootW, y + 2] \
                             ])
    map.raiseEventAuto(lstRpgXY, 0)


if __name__ == '__main__':
    try:
        import script
        script.main()
    except:
        import traceback
        traceback.print_exc(file=file('trace.txt', 'w'))
