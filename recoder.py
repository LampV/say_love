#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@author: Jiawei Wu
@create time: 2022-01-04 11:13
@edit time: 2022-01-06 12:07
@file: /say_love/recoder.py
@desc: 
"""
import pygame
from ctext import Text, TextLine
from heart import Heart
from collections import deque
from enum import Enum
import numpy as np


class Status(Enum):
    FREE = 0
    BUSY = 1
    ATOMIC = 2  # 原子操作中，禁止中断


class Recoder:
    hello_voice = pygame.mixer.Sound('resources/hello.wav')
    heart_voice = pygame.mixer.Sound('resources/heart.wav')
    poem_voice = pygame.mixer.Sound('resources/poem.wav')
    # love_voice = pygame.mixer.Sound('resources/love-demo.wav')
    love_voice = pygame.mixer.Sound('resources/love.wav')
    

    def __init__(self, ticks, speaker, add_entity_func):
        self.ticks = ticks  # 一秒多少tick
        self.speaker = speaker
        # 共享实体
        self.add_entity_func = add_entity_func
        self.events = []
        # 一次只能播放一段音频
        self.cur_tick = 0
        self.status = Status.FREE

    def play_heart(self, pos):
        # 如果是原子级别，则不允许打断
        if self.status == Status.ATOMIC:
            return
        self.status = Status.BUSY
        self.speaker.speak(self.heart_voice)
        event = deque([(self.cur_tick, Heart(), pos)])
        self.events.append(event)

    def play_hello(self):
        self.status = Status.ATOMIC
        voice, chars = self.hello_voice, '你好，这里是为荔荔编写的智能小黄鸭'

        duration = voice.get_length()  # 单位: 秒
        total_ticks = duration * self.ticks
        avg_ticks = total_ticks / len(chars)

        event = deque()
        for index, char in enumerate(chars):
            entity = Text(char)
            event.append((self.cur_tick + avg_ticks *
                         index, entity, (300, 320)))
        self.events.append(event)

        self.speaker.speak(voice)
        self.dur = total_ticks

    def play_poem(self):
        self.status = Status.ATOMIC
        poem = [
            "七律·赠赵荔",
            "青空放目风物宜，佳节相思情意驰。",
            "比翼芳丛花作乐，同心木叶笑成诗。",
            "游船戏水奥森畔，绘马祈祥古北陲。",
            "问我流年曼何似，春来红豆二三枝。"
        ]
        voice = self.poem_voice
        duration = voice.get_length()
        total_ticks = duration * self.ticks
        # 暂且认为是9等分的时间
        interval = total_ticks / 10
        
        # 把诗行添加到显示中
        event = deque()
        for index, text in enumerate(poem):
            entity = TextLine(text, dur=total_ticks-2*interval, fade_out=interval)
            event.append((self.cur_tick + interval *
                         (2 * index - 1), entity, (200, 320)))
        self.events.append(event)
        
        self.speaker.speak(voice)
        self.dur = total_ticks
        
    def play_love(self):
        self.status = Status.ATOMIC
        
        voice = self.love_voice
        total_ticks = int(voice.get_length() * self.ticks)
        
        # 随机添加爱心
        event = deque()
        for tick in range(0, total_ticks, 10):
            heart = Heart()
            pos = np.random.randint(40, 600, 2)
            event.append((self.cur_tick + tick, heart, pos))
        self.events.append(event)
        
        self.speaker.speak(voice)
        self.dur = total_ticks
        
        

    def end_play(self):
        self.status = Status.FREE
        self.speaker.end_speak()

    def event_loop(self):
        for event in self.events:
            t, e, p = event[0]
            if self.cur_tick >= t:
                self.add_entity_func(e, p)
                event.popleft()
                if not event:
                    self.events.remove(event)
        self.cur_tick += 1  # cur_tick永远增加
