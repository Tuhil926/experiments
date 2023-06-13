"""
A library that holds the animations for tic tac 2.0
"""

import pygame
import time
import threading


def distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


class ButtonSlideAnim:
    def __init__(self, button, original_pos, start_pos):
        self.button = button
        self.original_pos = original_pos
        self.start_pos = start_pos
        self.dt = 0
        self.speed = 0.5
        self.prev_time = 0
        self.playing = False

    def play(self, speed):
        self.speed = speed
        #print("starting")
        self.button.pos = list(self.start_pos)
        self.playing = True
        self.prev_time = time.time_ns()

    def update(self):
        if self.playing:
            # print(self.start_pos)
            if distance(self.button.pos, self.original_pos) > 1:
                self.dt = (time.time_ns() - self.prev_time) / 1000000000
                self.prev_time = time.time_ns()
                self.button.pos[0] += (self.original_pos[0] - self.button.pos[0]) * self.speed * self.dt
                self.button.pos[1] += (self.original_pos[1] - self.button.pos[1]) * self.speed * self.dt
            else:
                self.playing = False
                self.button.pos = self.original_pos

    def start(self):
        #print("started")
        time_now = time.time_ns()
        #print(self.start_pos)
        while distance(self.button.pos, self.original_pos) > 1:
            self.dt = (time.time_ns() - time_now)/1000000000
            time_now = time.time_ns()
            self.button.pos[0] += (self.original_pos[0] - self.button.pos[0]) * self.speed * self.dt
            self.button.pos[1] += (self.original_pos[1] - self.button.pos[1]) * self.speed * self.dt
        #time.sleep(0.03)
            #rint(self.pos.pos)
        #self.pos.pos = self.original_pos
        #print("done")

