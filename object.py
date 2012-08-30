#$Id: object.py,v 1.1 2007/11/20 14:22:00 ffb Exp $#
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

# 所有对象基类
class Object:
    def __init__(self):
        self.x = 0
        self.y = 0
