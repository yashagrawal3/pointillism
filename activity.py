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
import pygame
import olpcgames
from olpcgames import activity
from sugar.datastore import datastore
from sugar.graphics.toolbutton import ToolButton
from gettext import gettext as _

class Activity(activity.PyGameActivity):
    
    game_name = 'run'
    game_title = _('Pointillism')
    game_size = (1200, 900)

    def build_toolbar(self):
        toolbar = super( Activity, self).build_toolbar()
        toolbar.keep.props.visible = False
        savebutton = ToolButton('filesave')
        savebutton.set_tooltip(_('Save Image'))
        savebutton.connect('clicked',self._savebutton_cb)
        toolbar.insert(savebutton, 2)
        savebutton.show()
        
        return toolbar

    def _savebutton_cb(self,button):
        pygame.event.post(olpcgames.eventwrap.Event(pygame.USEREVENT, action='savebutton'))

    def save_image(self,image):
        journalobj = datastore.create()
        journalobj.metadata['title'] = 'Pointillism'
        journalobj.metadata['mime_type'] = 'image/jpeg'
        
        file_path = os.path.join(olpcgames.ACTIVITY.get_activity_root(),'instance','pointillism.jpg')

        pygame.image.save(image,file_path)
        journalobj.set_file_path(file_path)
        datastore.write(journalobj)

        journalobj.destroy()
