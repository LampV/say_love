#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@author: Jiawei Wu
@create time: 2022-01-03 19:11
@edit time: 2022-01-04 23:44
@file: /say_love/ctext.py
@desc: 
"""
import pygame
pygame.init()
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)


class Text:
    # f1 = pygame.font.SysFont("Fira Code", 20)
    f1 = pygame.font.Font("resources/Serfi.otf", 20)

    def __init__(self, char, wait=0, fade_out=60):
        self.fsur = self.f1.render(char, True, BLACK)
        self.cur = 0
        self.wait = wait
        self.fade_out = fade_out  # fade in fade_out ticks

    def get_next(self):
        if self.cur >= self.fade_out:
            return None, None
        self.cur += 1

        alpha = 255 - self.cur/self.fade_out*255
        dx = -1 * int(100 * (1 - alpha / 255))
        cpy = self.fsur.copy()
        # add move
        rect = cpy.get_rect()
        rect.move_ip(dx, 0)
        cpy.scroll(dx, 0)
        cpy.set_alpha(alpha)
        return cpy, rect



class TextLine:
    # f1 = pygame.font.SysFont("Fira Code", 20)
    f1 = pygame.font.Font("resources/Serfi.otf", 20)

    def __init__(self, sen, wait=0, dur=60, fade_out=60):
        self.fsur = self.f1.render(sen, True, BLACK)
        self.cur = 0
        self.wait = wait
        self.dur = dur 
        self.fade_out = fade_out  # fade in fade_out ticks

    def get_next(self):
        if self.cur >= self.dur + self.fade_out:
            return None, None
        self.cur += 1
        
        cpy = self.fsur.copy()
        rect = cpy.get_rect()
        width, height = cpy.get_size()
        
        delta = self.cur - self.dur
        if delta < 0:
            alpha = 255
        else:
            alpha = 255 - delta/self.fade_out*255
        dy = 0.15 * self.cur # 一个tick移动一个像素

        rect.move_ip(0, -dy)
        # cpy.scroll(dx, 0)
        cpy.set_alpha(alpha)
        return cpy, rect