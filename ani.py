#$Id: ani.py,v 1.1 2010/4/21 14:22:00 ffb Exp $#
#-*- coding:utf-8 -*-
# Last Update 
# by hoker.ffb[hoker.ffb@gmail.com] 2010-4-25
# homepage: http://www.hoker.org/MUTONG/index.html
# project homepage: https://sourceforge.net/projects/casktown2/

import pygame
import os
from datetime import datetime
from log import *

class Ani:
    "描述物体的动画"
    MULTI_IN_ONE = 0
    ONE_IN_ONE = 1
    
    def __init__(self, mode, name, frame_count):
        self.mode = mode;
        self.timeImgFilp = datetime.now() # 计算图片切换时间间隔
        if self.mode == Ani.MULTI_IN_ONE:
            self.init(name, frame_count)
        else:
            self.init2(name, frame_count)
    def init(self, name, frame_count):
        """初始化为单图模式，多个帧包含在一张图片中
        name:图片文件名
        frame_count:帧数"""
        strFile = os.path.join("./", name)
        if not os.path.exists(strFile):
            Log.error("file not found: %s" % strFile)
            return
        self.ani_img = pygame.image.load(strFile)
        self.rect = pygame.Rect(0, 0, self.ani_img.get_width() / frame_count, self.ani_img.get_height())
        self.img_index = 0
        self.frame_count = frame_count
        self.frame_width = self.ani_img.get_width()/frame_count
        print "self.frame_width = %s" % self.frame_width
        self.rect = pygame.Rect(0, 0, self.frame_width, self.ani_img.get_height())
    def init2(self, name, frame_count):
        """初始化为多个连续文件方式，每个帧一个文件
        name:图片文件前缀
        frame_count:帧数"""
        self.img_index = 0
        self.img = []

        for i in range(1, frame_count + 1):
            strFile = os.path.join("./", name + "_" + str(i) + ".png")
            if os.path.exists(strFile):
                img = pygame.image.load(strFile)
                self.img.append( img )
                Log.debug(strFile)
        self.frame_count = len(self.img)
        
        Log.debug("acutal frames == %d." % self.frame_count)
        
    def updateImg(self):
        timePass = datetime.now() - self.timeImgFilp
        if timePass.days * 24 * 60 * 60 * 1000 + timePass.seconds * 1000 + timePass.microseconds / 1000 >200:
            self.img_index = self.img_index + 1
            if self.img_index > self.frame_count - 1:
                self.img_index = 0
            self.timeImgFilp = datetime.now()
            
    def getImg(self):
        return self.img[self.img_index]
    def draw(self, view, x, y):
        if self.mode == Ani.ONE_IN_ONE:
            view.blit(self.getImg(), (x, y))
        else:
            view.blit(self.ani_img, (x, y), self.rect.move(self.frame_width * self.img_index, 0))
                    
def testCase():
    Log.setDebugLevel(Log.DebugLevel_Debug)
    view = pygame.display.set_mode((480,272))
    pygame.display.set_caption('Class Ani testCase.')
    
    player = []
    for i in range(1, 5):
        name= "data/p1_%d" % i
        player.append( Ani(1, name, 4) )
    fish = Ani(0, "data/wanda.png", 8)
    
    timePass = datetime.now()
    i = 0
    while True:
        for event in pygame.event.get():
            if event.type == 0:  
                return  
        view.fill((222,222,222))
        for i in range(0, 4):
            p = player[i]
            p.draw(view, 10 + 50 * i, 10)
            p.updateImg()
        fish.updateImg()
        fish.draw(view, 10, 70)
        pygame.display.flip()
        pygame.time.delay(1)
        i = i + 1
        if i > 5:
            break;
     
if __name__ == '__main__':
    testCase()                      
