#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@author: Jiawei Wu
@create time: 2022-01-02 16:35
@edit time: 2022-01-02 18:12
@file: /say_love/show_pygame.py
@desc: 
"""


import pygame
from pygame.color import Color
import sys
import time
import numpy as np

start = time.time()

pygame.init()  # 初始化pygame
size = width, height = 640, 480  # 设置窗口大小
screen = pygame.display.set_mode(size)  # 显示窗口
WHITE = Color(255, 255, 255)  # 设置颜色
BLACK = Color(0, 0, 0)

clock = pygame.time.Clock()  # 设置时钟

def draw_lines(sur, s):
    # 每一行之间的偏移量是1tick
    unit = 20
    # for line in range(1, height//unit):
    #     draw_line(sur, s, bias=line, h=line*unit)
    for line in range(1, height//unit):
        pygame.draw.line(sur, BLACK, (0, line*unit), ((s-line+1)*unit, line*unit))
    # starts = [(0, h*unit) for h in range(height//unit)]
    # ends = [((s-h+1)*unit, h*unit) for h in range(height//unit)]
    # pygame.draw.lines(sur, BLACK, starts, ends)

def draw_line(sur, s, bias=0, h=0):
    # 每10像素绘制一段
    # 希望每段都用20tick绘制然后用20tick消失
    # 不同段之间的间隔是1tick
    # sl = 40
    # ss = -100
    # colors = [
    #     BLACK.lerp(WHITE, np.clip((abs(sn+50)-30)/20, 0, 1))
    #     for sn in range(ss, 1)
    # ]
    # for index, color in enumerate(colors):
    #     cur = s + index + ss - bias
    #     if 0 <= cur < width//sl:
            # pygame.draw.line(sur, color, (cur*sl, h), ((cur+1)*sl, h))
    pygame.draw.line(sur, BLACK, (0, h), ((s-bias+1)*10, h))

        
    
step = 0
while True:  # 死循环确保窗口一直显示
    # clock.tick(60)  # 每秒执行60次
    for event in pygame.event.get():  # 遍历所有事件
        if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
            sys.exit()
            
    screen.fill(WHITE)  # 填充颜色(设置为0，执不执行这行代码都一样)
    draw_lines(screen, step)
    pygame.display.flip()  # 更新全部显示
    step += 1
    
    