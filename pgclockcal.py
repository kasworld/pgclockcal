#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import sys
import time
import datetime

success, fail = pygame.init()
if not pygame.get_init():
    print("init success, fail", success, fail)
    pygame.quit()

# screen = pygame.display.set_mode(flags=pygame.FULLSCREEN) # not work on linux
screen = pygame.display.set_mode()
screenW, screenH = screen.get_size()
dayW = screenW/14
dayH = screenH/12
calendarBaseY = screenH - dayH*7
calendarBaseX = screenW - dayW*7

bigFt = pygame.font.SysFont(None, int(screenH/1.7))
midFt = pygame.font.SysFont(None, int(screenH/6.6))
smallFt = pygame.font.SysFont(None, int(screenH/11))

tick = pygame.time.Clock()


def calcCenter(suf, refW=screenW):
    sufW = suf.get_width()
    return (refW-sufW)/2


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
    screen.blit(txtSuf, (0, screenH-dayH))

    # draw Clock
    clockText = time.strftime("%H:%M:%S", time.localtime())
    txtSuf = bigFt.render(clockText, False, (255, 255, 255))
    screen.blit(txtSuf, (calcCenter(txtSuf), 0))

    # draw calendar date
    dateText = "{0:%Y-%m-%d %a}".format(datetime.datetime.now())
    txtSuf = midFt.render(dateText, False, (255, 255, 255))
    screen.blit(txtSuf, ( calcCenter(txtSuf, screenW/2) , screenH/2))

    # draw 6 week calendar
    today = datetime.datetime.now()
    dayIndex = today + datetime.timedelta(days=(-today.weekday() - 7))

    # draw week day
    for wd in range(7):
        wdStr = "{0:%a}".format((dayIndex + datetime.timedelta(days=wd)))
        txtSuf = smallFt.render(wdStr, False, (255, 255, 255))
        screen.blit(txtSuf, (calendarBaseX + wd*dayW +
                    calcCenter(txtSuf, dayW), calendarBaseY))

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

            screen.blit(txtSuf, (calendarBaseX + wd*dayW + calcCenter(txtSuf, dayW),
                        calendarBaseY + dayH*(week+1)))

            dayIndex += datetime.timedelta(days=1)

    pygame.display.flip()
