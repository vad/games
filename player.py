#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame import *
import pygame, time, numpy, pygame.sndarray
import sys
import random
from glob import glob

sample_rate = 44100


class Player(object):
    def __init__(self, surface):
        self.surface = surface
        self.clean()

    def _draw(self, color=None):
        randint = random.randint
        w, h = self.surface.get_size()
        x, y, radius = randint(0, w), randint(0, h), randint(10, 100)
        if not color:
            color = randint(50, 255), randint(50, 255), randint(50, 255)
        pygame.draw.circle(self.surface, color, (x, y), radius)
        pygame.display.update()

    def clean(self):
        self.surface.fill((0, 0, 0))
        pygame.display.update()

    def play(self, sound):
        self._draw()
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()


def main():
    pygame.mixer.pre_init(sample_rate, -16, 2) # 44.1kHz, 16-bit signed, stereo
    pygame.init()
    surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    player = Player(surface)

    random.seed(0.5)
    shuffler = glob("Samples/*/*.wav")
    random.shuffle(shuffler)
    shuffler = shuffler[:200]

    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            key, mod = event.key, event.mod

            if key == 99 and mod & pygame.KMOD_CTRL:
                sys.exit()

            sound = shuffler[key%200]
            player.play(sound)
        elif event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.USEREVENT:
            #player.clean()
            pass




if __name__ == '__main__':
    main()

