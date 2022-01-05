#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@author: Jiawei Wu
@create time: 2022-01-03 18:43
@edit time: 2022-01-04 23:49
@file: /say_love/duck.py
@desc: 
"""
import pygame
from enum import Enum
class BillStyle(Enum):
    ClOSED = 0
    OPEN = 1

# singltone
class Duck:
    _instance = None # 无并发，仅仅是保证资源不冲突
    bill_normal = pygame.image.load('resources/yaya-normal.png')
    bill_smile = pygame.image.load('resources/yaya-speak.png')

    def __new__(self, screen_size):
        if not self._instance:
            self._instance = super().__new__(self)
        return self._instance
    
    def __init__(self, screen_size):
        # 声道
        self.channel = pygame.mixer.Channel(0)  # default channel
        self.playing = False
        # self.style = BillStyle.ClOSED
        self.speak_tick = 0
        self.screen_size = screen_size # 居中
    
    def speak(self, sound):
        if self.playing:
            self.channel.set_endevent(pygame.NOEVENT)
            self.channel.stop()
        self.channel.play(sound)
        self.playing = True
        self.channel.set_endevent(pygame.USEREVENT)
        
    def end_speak(self):
        if self.playing:
            self.channel.set_endevent(pygame.NOEVENT)
            self.channel.stop()
        self.playing = False
        
    def get_style(self):
        # 这个函数会被主函数调用，每个tick一次
        if self.playing:
            self.speak_tick += 1
            # change every 10 ticks
            if (self.speak_tick // 10) % 2 == 0:
                bg = self.bill_normal
            else:
                bg = self.bill_smile
        else:
            self.speak_tick = 0
            bg = self.bill_normal
        rect = bg.get_rect()
        w, h = rect.width, rect.height
        w_, h_ = self.screen_size
        return bg, rect.move((w_-w)/2, (h_-h)/2) # 移动到中央
    
    