#$Id: mapmanager.py,v 1.1 2007/11/20 14:22:00 ffb Exp $#
#-*- coding:utf-8 -*-
# Last Update
# by hoker.ffb[hoker.ffb@gmail.com] 2008-2-4
# homepage: http://mutong.saveasdf.com/
# project homepage: http://gforge.osdn.net.cn/projects/rpg2/

import pygame
from xml.dom import minidom
from log import *
from mapbrick import *
from inc import *
from fire import *
from manager import *
#debug
import psp2dex
from dialog import *
from player import *


# 符号
class Sym:
    def __init__(self):
        self.Code = ""
        self.Img = ""
        self.Through = True


# 地图
class Map(Manager):
    MapManager = None

    @staticmethod
    def getMap():
        if None == Map.MapManager:
            Map.MapManager = Map()
        return Map.MapManager

    def __init__(self):
        self.x = 0
        self.y = 0
        self.view = None
        self.UnitW = Inc.BoxW  # 地图上一个地图元素的宽
        self.UnitH = Inc.BoxH  # 地图上一个地图元素的高

        self.viewX = 0
        self.viewY = 0
        self.mapHPix = 800
        self.mapWPix = 600

        self.hotMapBox = None
        self.hotMapX = 0
        self.hotMapY = 0

        self.preBgMusic = ""
        self.bgMusic = ""

    def load(self, file):
        "加载指定的地图文件"
        self.viewX = 0
        self.viewY = 0
        self.maps = []  # 所有的砖块对象集合
        self.hotMapBox = None
        xmldoc = minidom.parse(os.path.join('data/', file + '.xml'))
        root = xmldoc.firstChild

        # 读取符号释义
        sym = root.getElementsByTagName("sym")
        syms = {}
        for i in range(0, len(sym)):
            elemSym = sym[i]
            objSym = Sym()
            objSym.Code = elemSym.getAttribute("code")
            objSym.Img = elemSym.getAttribute("img")
            bThrough = int(elemSym.getAttribute("through"))
            if 0 == bThrough:
                objSym.Through = False
            else:
                objSym.Through = True
            syms[objSym.Code] = objSym

        # 读取事件
        # <event sym="P" flag="4" next="map_01" px="13" py="3" />
        event = root.getElementsByTagName("event")
        events = {}
        for i in range(0, len(event)):
            elemEvt = event[i]
            objEvt = Event()
            objEvt.sym = elemEvt.getAttribute("sym")
            objEvt.flag = int(elemEvt.getAttribute("flag").encode("utf-8"), 10)
            objEvt.playerx = int(elemEvt.getAttribute("px"), 10)
            objEvt.playery = int(elemEvt.getAttribute("py"), 10)
            objEvt.nextmap = elemEvt.getAttribute("next")
            events[objEvt.sym] = objEvt
            Log.info("event %d, %s" % (i, objEvt.nextmap))
        Log.info("%d events" % len(events))

        # 层
        # layer = root.firstChild
        # 按行读取地图
        line = root.getElementsByTagName("line")
        mapbuf = []
        for i in range(0, len(line)):
            m = line[i].firstChild.data
            mapbuf.append(m)
            row = []
            for j in range(0, len(m)):
                key = m[j]
                imgFile = syms[key].Img
                map = MapBrick(self.view, m[j], imgFile, j * self.UnitW, i * self.UnitH)
                if key in syms:
                    map.through = syms[key].Through
                #debug
                if key in events:
                    Log.debug("map.has key")
                    map.evt = events[key]
                    map.evt.event = self.eventCallBackNextMap
                    #map.evt.nextmap = events[key].nextmap
                    #map.evt.playerx = events[key].playerx
                    #map.evt.playery = events[key].playery
                    #map.evt.flag = events[key].flag
                    #map.evt.sym = events[key].sym
                    Log.info("applay event next=%s" % map.evt.nextmap)
                row.append(map)
            self.maps.append(row)
            Log.debug(m + str(len(self.maps)))
        Log.debug("maps=" + str(len(self.maps)))

        # 基本属性
        self.mapName = root.getAttribute("name")
        self.preBgMusic = self.bgMusic
        self.bgMusic = root.getAttribute("bgmusic")
        self.mapHeight = len(self.maps)
        self.mapWidth = len(self.maps[0])
        self.mapHPix = self.mapHeight * Inc.BrickH
        self.mapWPix = self.mapWidth * Inc.BrickW

        # 建立屏后地图缓冲
        self.bufFullMap = pygame.Surface((self.mapWPix, self.mapHPix))  # 完全大小的地图（保存原始地图）
        self.bufViewMap = pygame.Surface((self.mapWPix, self.mapHPix))  # 屏后地图缓冲（用来显示的）
        self.drawMapBuf(self.bufFullMap)

    def changeMap(self, mapName, playerx, playery):
        self.load(mapName)

        try:
            if (self.preBgMusic != self.bgMusic) and (self.bgMusic != ""):
                pygame.mixer.music.load("music/%s" % self.bgMusic)
                pygame.mixer.music.play()
        except:
            pass

        fires = Fires.getFires()
        fires.view = self.bufViewMap
        fires.fires = []

        player1 = Player.getPlayer1()
        player1.view = self.bufViewMap
        player1.x = Inc.BrickW * playerx
        player1.y = Inc.BrickH * playery + (Inc.PlayerH - Inc.FootH)
        player1.xMax = self.mapWPix
        player1.yMax = self.mapHPix

        self.centerView(player1.x, player1.y)

#debug
    def eventCallBackNextMap(self, objMapbrick):
        "切换地图的回调函数"
        self.changeMap(objMapbrick.evt.nextmap, objMapbrick.evt.playerx, objMapbrick.evt.playery)

    def eventCallBackTest(self):
        say = Dialog()
        say.init("box.png", self.view)
        player1 = Player.getPlayer1()
        while True:
            pad = psp2dex.Controller()

            if pad.space or pad.esc:
                break
            self.view.fill((0, 0, 0))
            self.draw()
            player1.draw()
            self.present()
            say.draw('对了，忘记带书包了，回家拿去...')
            pygame.display.flip()
        pygame.event.clear()

    def eventCallBackTest2(self):
        say = Dialog()
        say.init("box.png", self.view)
        player1 = Player.getPlayer1()
        while True:
            pad = psp2dex.Controller()

            if pad.space or pad.esc:
                break
            self.view.fill((0, 0, 0))
            self.draw()
            player1.draw()
            self.present()
            say.draw('表进来！人家在换衣服呢！')
            pygame.display.flip()
        pygame.event.clear()

#end debug

    def drawMapBuf(self, view):
        "绘制地图缓冲"
        Log.debug(str("draw"))
        for i in range(0, len(self.maps)):
            m = self.maps[i]
            for j in range(0, len(m)):
                b = m[j]
                b.draw(view)

    def draw(self):
        "绘制地图缓冲到屏后缓冲"
        # rect = self.bufViewMap.get_rect()
        self.bufViewMap.blit(self.bufFullMap, (0, 0))
        # debug
        # Display current position box
        if self.hotMapBox != None:
            pygame.draw.rect(self.bufViewMap, (0, 0, 200), (self.hotMapBox.x, self.hotMapBox.y, Inc.BoxW, Inc.BoxH), 1)

    def drawDebug(self, view):
        t = "hotMap(%d,%d), view(%d,%d in %d,%d)" % \
                (self.hotMapX, self.hotMapY, self.viewX, self.viewY, self.mapWPix, self.mapHPix)
        psp2dex.drawText(view, t, 0, 10)
        t = "view(%d,%d,%d)" % \
                        (self.viewX, Inc.ScreenW / 2, self.viewX - Inc.ScreenW / 2)
        psp2dex.drawText(view, t, 0, 20)
        t = ""
        if self.hotMapBox != None:
            t = "evt(f=%d,sym=%s,next=%s)" % \
                                (self.hotMapBox.evt.flag, self.hotMapBox.evt.sym, self.hotMapBox.evt.nextmap)
        psp2dex.drawText(view, t, 0, 30)

    def present(self):
        "绘制屏后缓冲到屏幕"
        rect = self.view.get_rect()
        self.view.blit(self.bufViewMap, rect.move(self.viewX, self.viewY))
        pass

    def moveView(self, ox, oy):
        "移动用户视图, x,y 是偏移量"
        self.viewX += ox
        self.viewY += oy
        if self.viewX > 0:
            self.viewX = 0
        if self.viewY > 0:
            self.viewY = 0
        if self.viewX - Inc.ScreenW < -self.mapWPix:
            self.viewX = -self.mapWPix + Inc.ScreenW
        if self.viewY - Inc.ScreenH < -self.mapHPix:
            self.viewY = -self.mapHPix + Inc.ScreenH

        pass

    def centerView(self, x, y):
        "以x,y为中心点使用户视图居中"
        self.viewX = -(x - Inc.ScreenW / 2)
        self.viewY = -(y - Inc.ScreenH / 2)
        self.moveView(0, 0)

    def getRpgXy(self, pixXYList):
        """根据制定的绝对坐标x,y集合得到对应的RPG地块坐标集合"""
        lstRet = []
        for pixXY in pixXYList:
            MapX = (pixXY[0] + 0) / self.UnitW
            MapY = (pixXY[1] + 0) / self.UnitH
            #判断地图出界
            if MapY < 0 or MapY >= len(self.maps) or MapX < 0 or MapX >= len(self.maps[MapY]):
                pass
            else:
                lstRet.append([MapX, MapY])
        return lstRet

    def canMove(self, rpgXYList):
        """判断指定的绝对坐标集合是否可以移动通过"""
        bRet = True
        for rpgXY in rpgXYList:
            # 判断地图出界
            x = rpgXY[0]
            y = rpgXY[1]
            bRet = bRet and self.canThrough(x, y)
        #if not bRet:
            #Log.info("No move.%d,%d" % (x,y))
        #else:
            #Log.info("move.%d,%d" % (x,y))
        return bRet

    def canThrough(self, rpgX, rpgY):
        """判断指定的绝对坐标x,y是否可以移动通过"""
        MapY = rpgY
        MapX = rpgX
        #判断地图出界
        if MapY < 0 or MapY >= len(self.maps) or MapX < 0 or MapX >= len(self.maps[MapY]):
            return False
        else:
            map = self.maps[MapY][MapX]
        #print map
        if map.canThrough():
            self.hotMapX = 0
            self.hotMapY = 0
            self.hotMapBox = None
        else:
            self.hotMapX = MapX
            self.hotMapY = MapY
            self.hotMapBox = map

        return map.canThrough()

    def raiseEventAuto(self, rpgXYList, caller):
        for rpgXY in rpgXYList:
            self.raiseEvent(rpgXY[0], rpgXY[1], caller)

    def raiseEvent(self, rpgX, rpgY, caller):
        if rpgY < 0 or rpgY >= len(self.maps) or rpgX < 0 or rpgX >= len(self.maps[rpgY]):
            return False

        map = self.maps[rpgY][rpgX]
        #print "rpgX,Y = ",rpgX,rpgY
        if caller == 0 and map.evt.flag != 0:
            #print "evt"
            Log.info("map.evt.flag")
            map.evt.event(map)
            return True
        else:
            return False


def testCase():
    m = Map('')
    m.load('map_01')
    print m.canThrough(22, 22)  # False
    print m.canThrough(35, 35)  # True
    print m.canThrough(128, 35)  # False
    print m.canThrough(31, 42)  # False

if __name__ == '__main__':
    import script
    script.main()
    #testCase();
