import pygame
import sys
import numpy as np
from dataclasses import dataclass
from collections import deque

from duck import Duck
from ctext import Text
from heart import Heart
from recoder import Recoder

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

pygame.init()  # 初始化pygame

@dataclass
class Entity:
    obj: object
    pos: tuple




class Javis:
    def __init__(self):
        # setup pygame
        size = width, height = 640, 640  # 设置窗口大小
        self.screen = pygame.display.set_mode(size)  # 显示窗口
        self.duck = Duck(size)
        # init
        self.entities = []
        self.buff = deque(maxlen=80)
        self.recoder = Recoder(60, self.duck, self.add_entity)
    

    def set_background(self):
        self.screen.fill(WHITE)  # 填充颜色(设置为0，执不执行这行代码都一样)
        # 画鸭子
        duck_bg, duck_rect = self.duck.get_style()
        self.screen.blit(duck_bg, duck_rect)
        
    def show_entities(self):
        for entity in self.entities:
            surface, rect = entity.obj.get_next()
            if surface is None:
                self.entities.remove(entity)
                continue
            x, y = entity.pos
            pos = x - rect.width / 2, y - rect.height / 2
            cur = rect.move(pos)
            self.screen.blit(surface, cur)
        
    def add_entity(self, ety, pos):
        self.entities.append(Entity(ety, pos))

    def handle_events(self, events):
        for event in events:  # 遍历所有事件
            if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                sys.exit()
            # 鼠标点击左键，则在鼠标点击的位置添加一个爱心
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                self.recoder.play_heart(pos)
            # 键盘按下，则添加到buff中
            if event.type == pygame.KEYDOWN:
                try:
                    self.buff.append(chr(event.key))
                except:
                    pass    # 保证chr正确就行了
                # bonus
                tmp = ''.join(self.buff)
                if any(word in tmp for word in ("zhaoli", u"赵荔", "lili", "lily")):
                    self.recoder.play_love()
                    self.buff.clear()
                if any(word in tmp for word in ("wjw", "wujiawei")):
                    self.recoder.play_poem()
                    self.buff.clear()
            # USEREVENT是播放器传递的，表示停止播放，需要处理
            if event.type == pygame.USEREVENT:
                self.recoder.end_play()

    def run(self, *args, **kwargs):
        clock = pygame.time.Clock()  # 设置时钟
        self.recoder.play_hello()
        while True:  # 死循环确保窗口一直显示
            clock.tick(60)
            self.handle_events(pygame.event.get())
            self.recoder.event_loop()
            self.set_background()
            self.show_entities()
            pygame.display.flip()  # 更新全部显示

        pygame.quit()  # 退出pygame


if __name__ == '__main__':
    javis = Javis()
    javis.run()
    