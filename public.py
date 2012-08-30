#$Id: script.py,v 1.1 2007/11/20 14:22:00 ffb Exp $#
#-*- coding:utf-8 -*-

# Last Update
# by hoker.ffb[hoker.ffb@gmail.com] 2008-2-15
# homepage: http://mutong.saveasdf.com/
# project homepage: http://gforge.osdn.net.cn/projects/rpg2/

import pygame
from inc import *
from log import *
import os


class Pub:
    @staticmethod
    def getImgList(imgName, nFramePixW):
        imglst = []
        strFile = os.path.join("data/", imgName + ".png")
        img = pygame.image.load(strFile)
        nWidth = img.get_width()
        nHeight = img.get_height()
        for i in range(0, nWidth, nFramePixW):
            imgFrame = pygame.Surface((nFramePixW, nHeight))
            imgFrame.set_colorkey((0, 0, 0))
            rect = pygame.Rect(-i, 0, nFramePixW, nHeight)
            imgFrame.blit(img, rect)
            imglst.append(imgFrame)

        return imglst

if __name__ == '__main__':
    import rpg
    rpg.play()
