#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame import *
import pygame, time, numpy, pygame.sndarray
import sys
import random

sample_rate = 44100


class Player(object):
    def __init__(self, surface):
        self.surface = surface
        self._clean()

    def _play_for(self, sample_array, ms, volLeft, volRight):
        sound = pygame.sndarray.make_sound(sample_array)
        beg = time.time()
        channel = sound.play(-1)
        channel.set_volume(volLeft,volRight)
        pygame.time.delay(ms)
        sound.stop()
        end = time.time()
        return beg, end

    def _sine_array_onecycle(self, hz, peak):
        length = sample_rate / float(hz)
        omega = numpy.pi * 2 / length
        xvalues = numpy.arange(int(length)) * omega
        return peak * numpy.sin(xvalues)

    def _sine_array(self, hz, peak, n_samples = sample_rate):
        return numpy.resize(self._sine_array_onecycle(hz, peak), (n_samples,))

    def _draw(self, color=None):
        randint = random.randint
        w, h = self.surface.get_size()
        x, y, radius = randint(0, w), randint(0, h), randint(10, 100)
        if not color:
            color = randint(50, 255), randint(50, 255), randint(50, 255)
        pygame.draw.circle(self.surface, color, (x, y), radius)
        pygame.display.update()

    def _clean(self):
        self.surface.fill((0, 0, 0))
        pygame.display.update()

    def play(self, freq):
        f = self._sine_array(freq, 1)
        f = numpy.array(zip(f , f))

        self._draw()
        self._play_for(f , 500, 0.5, 0.5)
        self._clean()


def main():
    pygame.mixer.pre_init(sample_rate, -16, 2) # 44.1kHz, 16-bit signed, stereo
    pygame.init()
    surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    player = Player(surface)

    random.seed(0.5)
    shuffler = range(200)
    random.shuffle(shuffler)

    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            key, mod = event.key, event.mod

            if key == 99 and mod & pygame.KMOD_CTRL:
                sys.exit()
        elif event.type == pygame.QUIT:
            sys.exit(0)
        else:
            continue

        freq = 3000 + int(shuffler[key%200] * 4000. / 200)
        player.play(freq)


if __name__ == '__main__':
    main()

