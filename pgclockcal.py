#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import sys
import time
import datetime

import requests
from bs4 import BeautifulSoup


def getNaverWeather():
    try:
        source = requests.get('https://www.naver.com/')
        soup = BeautifulSoup(source.content, "html.parser")

        group_weather = soup.find('div', {'class': 'group_weather'})
        # print(group_weather)
        current_box = group_weather.find('div', {'class': 'current_box'})
        current = current_box.find('strong', {'class': 'current'}).text
        current_state = current_box.find('strong', {'class': 'state'}).text
        location = group_weather.find('span', {'class': 'location'}).text

        # <ul class="list_air">
        # <li class="air_item">미세<strong class="state state_good">좋음</strong></li>
        # <li class="air_item">초미세<strong class="state state_normal">보통</strong></li>
        # </ul>
        listair = group_weather.find('ul', {'class': 'list_air'})
        airlist = listair.find_all('li', {'class': 'air_item'})
        air_fine, air_fine2 = airlist[0].text, airlist[1].text

        weatherUpdate = datetime.datetime.now()
        return current, current_state, location, air_fine, air_fine2, weatherUpdate
    except:
        # return err info and retry after 1 min
        return "internet", "connection",  "no",   "retry", "in 1 min", datetime.datetime.now() - datetime.timedelta(minutes=9)


def printUsage():
    print("""
    use system font
        python pgclockcal.py
    use custom font 
        python pgclockcal.py fontfilename bigfontrate midfontrate smallfontrate 
    example 
        python pgclockcal.py NanumGothicBold.ttf 5.0 1.0 0.9
    """)


success, fail = pygame.init()

# screen = pygame.display.set_mode(flags=pygame.FULLSCREEN) # not work on linux
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode()
screenW, screenH = screen.get_size()
dayW = screenW/14
dayH = screenH/12
calendarBaseY = screenH - dayH*7
calendarBaseX = screenW - dayW*7 - dayW/4


if len(sys.argv) == 5:
    # ftfilename = "NanumGothicBold.ttf" 5.0, 1.0 0.9
    ftfilename = sys.argv[1]
    bigRate = float(sys.argv[2])
    midRate = float(sys.argv[3])
    smallRate = float(sys.argv[4])
    bigFt = pygame.font.Font(ftfilename, int(dayH*bigRate))
    midFt = pygame.font.Font(ftfilename, int(dayH*midRate))
    smallFt = pygame.font.Font(ftfilename, int(dayH*smallRate))
else:
    printUsage()
    bigFt = pygame.font.SysFont(None, int(dayH*7))
    midFt = pygame.font.SysFont(None, int(dayH*1.7))
    smallFt = pygame.font.SysFont(None, int(dayH*1.0))

tick = pygame.time.Clock()

current, current_state, location, air_fine, air_fine2, weatherUpdate = getNaverWeather()


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

    # draw weather1
    weatherText = f"{location} {current}"
    txtSuf = midFt.render(weatherText, False, (255, 255, 255))
    screen.blit(txtSuf, (calcCenter(txtSuf, screenW/2), screenH/2+dayH*1.3))

    # draw weather2
    weatherText = f"{current_state}"
    txtSuf = midFt.render(weatherText, False, (255, 255, 255))
    screen.blit(txtSuf, (calcCenter(txtSuf, screenW/2), screenH/2+dayH*2.6))

    # draw weather3
    weatherText = f"{air_fine} {air_fine2}"
    txtSuf = midFt.render(weatherText, False, (255, 255, 255))
    screen.blit(txtSuf, (calcCenter(txtSuf, screenW/2), screenH/2+dayH*3.9))

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
        current, current_state, location, air_fine, air_fine2, weatherUpdate = getNaverWeather()
    drawClockCal()
