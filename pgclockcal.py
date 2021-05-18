#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import sys
import time
import datetime

success, fail = pygame.init()
if fail > 0 :
    print("success, fail", success, fail)
    sys.exit()

screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
screenW, screenH = screen.get_size()

bigFt = pygame.font.SysFont(None, int(screenH/2))
midFt = pygame.font.SysFont(None, int(screenH/4))
smallFt = pygame.font.SysFont(None, int(screenH/12))

tick = pygame.time.Clock()


def calcCenter(suf):
    sufW = suf.get_width()
    return (screenW-sufW)/2


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    tick.tick(60)

    screen.fill((0, 0, 0))

    # for x in range(0,screenW,1):
    #     pygame.draw.line(screen, (x % 256,x / 16,x% 16),(0,0),(x,screenH))

    # draw FPS
    txtSuf = smallFt.render("FPS {0:.1f}".format(
        tick.get_fps()), False, (63, 63, 63))
    screen.blit(txtSuf, (0, 0))

    # draw Clock
    clockText = time.strftime("%H:%M:%S", time.localtime())
    txtSuf = bigFt.render(clockText, False, (255, 255, 255))
    screen.blit(txtSuf, (calcCenter(txtSuf), 0))

    # draw calendar date
    dateText = "{0:%Y-%m-%d %a}".format(datetime.datetime.now())
    txtSuf = midFt.render(dateText, False, (255, 255, 255))
    screen.blit(txtSuf, (calcCenter(txtSuf), screenH/3))

    # draw 6 week
    today = datetime.datetime.now()
    dayIndex = today + datetime.timedelta(days=(-today.weekday() - 7))

    # draw weed day
    dayW = screenW/16
    dayH = screenH/16
    for wd in range(7):
        wdStr = "{0:%a}".format((dayIndex + datetime.timedelta(days=wd)))
        txtSuf = smallFt.render(wdStr, False, (255, 255, 255))
        screen.blit(txtSuf, (wd*dayW + calcCenter(txtSuf), screenH/2))

    for week in range(6):
        for wd in range(7):
            dStr = "{0:%d}".format(dayIndex)
            if dayIndex.month != today.month:
                txtSuf = smallFt.render(dStr, False, (127, 127, 127))
            else:
                if dayIndex.day == today.day:
                    txtSuf = smallFt.render(dStr, False, (255, 255, 0))
                elif dayIndex.weekday() == 5:  # saturday
                    txtSuf = smallFt.render(dStr, False, (0, 0, 255))
                elif dayIndex.weekday() == 6:  # sunday
                    txtSuf = smallFt.render(dStr, False, (255, 0, 0))
                else:
                    txtSuf = smallFt.render(dStr, False, (255, 255, 255))

            screen.blit(txtSuf, (wd*dayW + calcCenter(txtSuf),
                        screenH/2 + dayH*(week+1)))

            dayIndex += datetime.timedelta(days=1)

    pygame.display.flip()
