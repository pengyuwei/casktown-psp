#$Id: player.py,v 1.1 2007/11/20 14:22:00 ffb Exp $#
#-*- coding:utf-8 -*-
# Last Update
# by hoker.ffb[hoker.ffb@gmail.com] 2008-2-4
# homepage: http://mutong.saveasdf.com/
# project homepage: http://gforge.osdn.net.cn/projects/rpg2/

import pygame
from inc import *
from log import *
from datetime import datetime
from public import *
import os


class Player:
    TotalImgCount = 3  # 每个朝向的图片的总帧数
    DefImgIndex = 0
    Up = 1
    Down = Up + TotalImgCount
    Left = Down + TotalImgCount
    Right = Left + TotalImgCount
    Player1 = None

    Inc.UP = Up
    Inc.DOWN = Down
    Inc.LEFT = Left
    Inc.RIGHT = Right

    @staticmethod
    def getPlayer1():
        if None == Player.Player1:
            Player.Player1 = Player()
        return Player.Player1

    def __init__(self):
        self.life = 3
        # x,y是Player 脚 的左上角坐标
        self.x = Inc.ScreenW / 2
        self.y = Inc.ScreenH / 2

        self.moveStep = Inc.moveStepPix
        self.xMax = Inc.ScreenW
        self.yMax = Inc.ScreenH
        self.direction = 4  # up1 down2 left3 right4
        self.width = 48
        self.height = 48

        # 绘制偏移量，用于绘制大于一个地图Box单位的Player
        self.drawOffsetX = -(self.width - Inc.FootW)
        self.drawOffsetY = -(self.height - Inc.FootH)

        self.img = []
        self.imgIndex = Player.DefImgIndex

    def init(self, playerName, view):
        self.view = view
        for i in range(1, 5):
            strFile = os.path.join("data/", playerName + "_" + str(i) + ".png")
            Log.debug(strFile)
            self.img.append(pygame.image.load(strFile))
            for j in range(1, Player.TotalImgCount):
                strFile = os.path.join("data/", playerName + "_" + str(i) + "_" + str(j) + ".png")
                Log.debug(strFile)
                self.img.append(pygame.image.load(strFile))
        #self.img = Pub.getImgList("p1", 48)

        self.xOffset = self.width + self.moveStep  # 就是Player图片的宽+移动单位
        self.yOffset = self.height + self.moveStep
        self.timeImgFilp = datetime.now()  # 计算主角图片切换时间间隔

    def getRect():
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def setDirection(self, d):
        self.direction = d

    def getNextPos(self):
        x = self.x
        y = self.y
        if self.direction == Player.Up:
            if self.y - self.moveStep > 0:
                y -= self.moveStep
        elif self.direction == Player.Down:
            if self.y + self.yOffset < self.yMax:
                y += self.moveStep
        elif self.direction == Player.Left:
            if self.x - self.moveStep > 0:
                x -= self.moveStep
        elif self.direction == Player.Right:
            if self.x + self.xOffset < self.xMax:
                x += self.moveStep

        return x, y

    def stop(self):
        self.imgIndex = Player.DefImgIndex

    def moveLeft(self):
        if self.direction != Player.Left:
            self.imgIndex = Player.DefImgIndex
            self.direction = Player.Left
        self.updateImg()
        self.x, self.y = self.getNextPos()

    def moveRight(self):
        if self.direction != Player.Right:
            self.imgIndex = Player.DefImgIndex
            self.direction = Player.Right
        self.updateImg()
        self.x, self.y = self.getNextPos()

    def moveUp(self):
        if self.direction != Player.Up:
            self.imgIndex = Player.DefImgIndex
            self.direction = Player.Up
        self.updateImg()
        self.x, self.y = self.getNextPos()

    def moveDown(self):
        if self.direction != Player.Down:
            self.imgIndex = Player.DefImgIndex
            self.direction = Player.Down
        self.updateImg()
        self.x, self.y = self.getNextPos()

    def updateImg(self):
        timePass = datetime.now() - self.timeImgFilp
        if timePass.days * 24 * 60 * 60 * 1000 + timePass.seconds * 1000 + timePass.microseconds / 1000 > 100:
            self.imgIndex = self.imgIndex + 1
            if self.imgIndex >= Player.TotalImgCount:
                self.imgIndex = 1
            self.timeImgFilp = datetime.now()

    def getImg(self):
        return self.img[self.direction - 1 + self.imgIndex]

    def draw(self):
        self.view.blit(self.getImg(), (self.x + self.drawOffsetX, self.y + self.drawOffsetY))

    def drawDebug(self, view):
        #debug:
        strD = "O"
        if self.direction == 1:
            strD = "Up"
        elif self.direction == 2:
            strD = "Down"
        elif self.direction == 3:
            strD = "Left"
        elif self.direction == 4:
            strD = "Right"

        nx, ny = self.getNextPos()

        strText = u"www.hoker.org x=%d,y=%d,nx=%d,ny=%d %s" % (self.x, self.y, nx, ny, strD)
        strText = u"www.hoker.org imgIndex=%d" % (self.imgIndex)
        m_font = pygame.font.Font(None, 19)
        image = m_font.render(strText, True, (255, 255, 255))
        rect = image.get_rect()
        view.blit(image, rect)


def testCase():
    view = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Class Player testCase.')
    view.fill((0, 0, 0))

    p1 = Player()
    p1.init('p1.png', view)
    p1.moveRight()
    p1.moveDown()
    p1.moveLeft()
    p1.moveUp()
    p1.draw()

if __name__ == '__main__':
    import rpg
    rpg.play()
    #testCase();
