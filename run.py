#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Pointillism
# Copyright (C) 2011, 2012
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information:
# Alan Aguiar <alanjas@gmail.com>
#

import os
import sys
sys.path.insert(0, "lib")
import olpcgames
import logging
import random
import pygame
from pygame import camera

log = logging.getLogger( 'Pointillism run' )
log.setLevel( logging.ERROR )

def main():
    size = (1200,900)
    pygame.init()
    camera.init()
    if olpcgames.ACTIVITY:
        size = olpcgames.ACTIVITY.game_size
    screen = pygame.display.set_mode(size)
    
    screen.fill((0,0,0))
    pygame.display.flip()
    clock = pygame.time.Clock()
    
    cam = camera.Camera("/dev/video0", (640, 480), "RGB")
    cam.start()
    cam.set_controls(True, False)
    cap = pygame.surface.Surface((640, 480), 0, screen)
    frames = 0

    running = True
    while running:
        cap = cam.get_image(cap)
        rect = []
        for z in range(max(20, int(frames)*10)):
            x = random.random()
            y = random.random()
            rect.append(pygame.draw.circle(screen, cap.get_at((int(x * 640), int(y * 480))), (int(x * 1200), int(y * 900)), random.randrange(2, 12, 1), 0))
        pygame.display.update(rect)

        clock.tick()
        frames = clock.get_fps() 

        events = pygame.event.get()       
        if events:
            for event in events:
                #log.debug( "Event: %s", event )
                if event.type == pygame.QUIT:
                    cam.stop()
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        cam.stop()
                        running = False
                    elif event.key == pygame.K_s:
                        olpcgames.ACTIVITY.save_image(screen)
                elif event.type == pygame.USEREVENT:
                    if hasattr(event,'action'):
                        if event.action == 'savebutton':
                            olpcgames.ACTIVITY.save_image(screen)
            pygame.display.flip()

if __name__ == "__main__":
    logging.basicConfig()
    main()
