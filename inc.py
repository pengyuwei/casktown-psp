#-*- coding:utf-8 -*-
#!/usr/bin/env python
# Last Update 
# by hoker.ffb[hoker.ffb@gmail.com] 2008-2-4
# homepage: http://mutong.saveasdf.com/
# project homepage: http://gforge.osdn.net.cn/projects/rpg2/

class Inc:
    BrickW       = 48
    BrickH       = 48
    BoxW         = 48
    BoxH         = 48
    PlayerW      = 48
    PlayerH      = 48
    FootW        = 48 # 1P的脚的大小，用于移动判断
    FootH        = 15
    MapW         = 100
    MapH         = 100
    
    # direction
    UP           = 1 
    DOWN         = 2
    LEFT         = 3
    RIGHT        = 4
    
    # PSP is (480,272)
    ScreenW      = 480
    ScreenH      = 272
    moveStepPix  = 1
    
    # event
    EVT_ONPLAYER = 2 # 与主角接触
    EVT_CHGMAP   = 4 # 地图变换
