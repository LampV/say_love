#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@author: Jiawei Wu
@create time: 2022-01-03 19:12
@edit time: 2022-01-03 19:16
@file: /say_love/heart.py
@desc: 
"""
import pygame
pygame.init()

class Heart:
    # cls properties
    heart = pygame.image.load('resources/heart_2_mini.png')

    def __init__(self):
        self.cur_heart = 0
        self.max_heart = 60 # ticks
        self.idx = 0

    def get_next(self):
        # 每个tick变化一次
        if self.cur_heart >= self.max_heart:
            return None, None # 表示可以删掉
        self.cur_heart += 1

        # 不透明度，最开始是255，最后是0
        alpha = 255 - self.cur_heart/self.max_heart*255
        # 逐渐变大
        width = self.heart.get_width() * (1 - alpha / 255)
        height = self.heart.get_height() * (1 - alpha / 255)
        cpy = pygame.transform.scale(self.heart, (width, height))
        cpy.set_alpha(alpha)
        return cpy, cpy.get_rect()

