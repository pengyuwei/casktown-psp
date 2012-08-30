#$Id: mapmanager.py,v 1.1 2007/11/20 14:22:00 ffb Exp $#
#-*- coding:utf-8 -*-
# Last Update 
# by hoker.ffb[hoker.ffb@gmail.com] 2010-5-9
# homepage: http://mutong.saveasdf.com/
# project homepage: http://gforge.osdn.net.cn/projects/rpg2/

import pygame
from xml.dom import minidom
from log import *
import os

class ImgInfo:
    id = 0
    file = ""
    frame = 1
    
class Info:
    def __init__(self):
        self.imgs = {}
        self.load()
    def load(self):
        "加载图片信息文件"
        filename = os.path.join('data/', 'info.xml')
        print 'loading info file %s' % filename
        xmldoc = minidom.parse(filename)
        root = xmldoc.firstChild
        
        # 读取符号释义
        elem_imgs = root.getElementsByTagName("img")
        self.imgs = {}
        for i in range(0, len(elem_imgs)):
            elem_img = elem_imgs[i]
            info = ImgInfo()
            info.id = int(elem_img.getAttribute("id"))
            info.file = elem_img.getAttribute("file")
            info.frame = int(elem_img.getAttribute("frame"))
            self.imgs[info.id] = info
    def get_frame_count(self, id):
            """根据ID返回图片的帧数"""
            if self.imgs.has_key(id):
                return self.imgs[id].frame
            else:
                return 0
                
def testCase():
    b = Info()
    print b.get_frame_count(1)
    print b.get_frame_count(2)

        
if __name__ == '__main__':
    testCase()
                
