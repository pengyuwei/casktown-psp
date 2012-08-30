#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Last Update
# by hoker.ffb[hoker.ffb@gmail.com] 2008-2-4
# homepage: http://mutong.saveasdf.com/
# project homepage: http://gforge.osdn.net.cn/projects/rpg2/

import pygame
from inc import *
import os


class Dialog:
    def __init__(self):
        pass

    def init(self, imgFile, view):
        self.view = view
        self.img = pygame.image.load(os.path.join("data/" + imgFile))
        self.img.set_alpha(150)

    def draw(self, text):
        # debug
        strText = unicode(text, 'utf-8')
        #try:
        # m_font = pygame.font.Font(os.path.join(os.getenv('WinDir'), 'Fonts', 'simsun.ttc'), 19)
        m_font = pygame.font.Font(os.path.join('./fonts', 'simsun.ttc'), 19)
        image = m_font.render(strText, True, (255, 255, 255))
        rect = image.get_rect()
        # 背景
        self.view.blit(self.img, rect.move(50, 190))
        # 文本
        self.view.blit(image, rect.move(110, 200))
        #except:
        #    pass
