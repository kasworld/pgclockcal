#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import sys
import time
import datetime

import requests
from bs4 import BeautifulSoup


def getNaverWeather():
    source = requests.get('https://www.naver.com/')
    soup = BeautifulSoup(source.content, "html.parser")

    group_weather = soup.find('div', {'class': 'group_weather'})
    current_box = group_weather.find('div', {'class': 'current_box'})
    current = current_box.find('strong', {'class': 'current'}).text
    current_state = current_box.find('strong', {'class': 'state'}).text
    location = group_weather.find('span', {'class': 'location'}).text
    weatherUpdate = datetime.datetime.now()
    return current, current_state, location, weatherUpdate


success, fail = pygame.init()

# screen = pygame.display.set_mode(flags=pygame.FULLSCREEN) # not work on linux
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode()
screenW, screenH = screen.get_size()
dayW = screenW/14
dayH = screenH/12
calendarBaseY = screenH - dayH*7
calendarBaseX = screenW - dayW*7 - dayW/4

bigFt = pygame.font.SysFont(None, int(screenH/1.7))
midFt = pygame.font.SysFont(None, int(screenH/6.6))
smallFt = pygame.font.SysFont(None, int(screenH/11))

tick = pygame.time.Clock()

current, current_state, location, weatherUpdate = getNaverWeather()


def calcCenter(suf, refW=screenW):
    sufW = suf.get_width()
    return (refW-sufW)/2


def drawClockCal():
    screen.fill((0, 0, 0))

    # for x in range(0,screenW,1):
    #     pygame.draw.line(screen, (x % 256,x / 16,x% 16),(0,0),(x,screenH))

    # draw FPS
    txtSuf = smallFt.render("FPS {0:.1f}".format(
        tick.get_fps()), False, (7, 7, 7))
    screen.blit(txtSuf, (0, screenH-dayH))

    # draw Clock
    clockText = time.strftime("%H:%M:%S", time.localtime())
    txtSuf = bigFt.render(clockText, False, (255, 255, 255))
    screen.blit(txtSuf, (calcCenter(txtSuf), 0))

    # draw calendar date
    dateText = "{0:%Y-%m-%d %a}".format(datetime.datetime.now())
    txtSuf = midFt.render(dateText, False, (255, 255, 255))
    screen.blit(txtSuf, (calcCenter(txtSuf, screenW/2), screenH/2))

    # draw weather
    weatherText = current
    txtSuf = midFt.render(weatherText, False, (255, 255, 255))
    screen.blit(txtSuf, (calcCenter(txtSuf, screenW/2), screenH/2+dayH*2))

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


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()

    tick.tick(2)
    if datetime.datetime.now() - weatherUpdate > datetime.timedelta(minutes=10):
        current, current_state, location, weatherUpdate = getNaverWeather()
    drawClockCal()
