#$Id: manager.py,v 1.1 2007/11/20 14:22:00 ffb Exp $#
#-*- coding:utf-8 -*-
# Last Update 
# by hoker.ffb[hoker.ffb@gmail.com] 2008-2-23
# homepage: http://mutong.saveasdf.com/
# project homepage: http://gforge.osdn.net.cn/projects/rpg2/

import pygame
from inc import *
from log import *
from datetime import datetime
from public import *

# 各类对象管理基类
class Manager:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.objects = []
    def update(self):
        for o in self.objects:
            pass
        pass
