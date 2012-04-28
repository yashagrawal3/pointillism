#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Pointillism
# Copyright (C) 2008, Nirav Patel
# Copyright (C) 2011, 2012, Alan Aguiar
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
# Nirav Patel <sugarlabs@spongezone.net>

import os
import sys
import gtk
sys.path.insert(0, "lib")
import pygame
import sugargame
import sugargame.canvas
from sugar.activity import activity
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityToolbarButton
from sugar.activity.widgets import StopButton
from sugar.graphics.toolbutton import ToolButton
from sugar.datastore import datastore
from gettext import gettext as _

import puntillism

class Activity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.radio_uno = 2
        self.radio_dos = 12

        self.actividad = puntillism.Puntillism(self)

        self.build_toolbar()
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self)
        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.run_pygame(self.actividad.run)

    def build_toolbar(self):

        self.max_participants = 1
        
        toolbox = ToolbarBox()
        activity_button = ActivityToolbarButton(self)
        toolbox.toolbar.insert(activity_button, -1)
        activity_button.show()

        barra = toolbox.toolbar

        """toolbar = caja.get_activity_toolbar()
        toolbar.remove(toolbar.keep)
        toolbar.keep = None
        toolbar.remove(toolbar.share)
        toolbar.share = None"""

        separador1 = gtk.SeparatorToolItem()
        separador1.props.draw = True
        barra.insert(separador1, 1)

        item1 = gtk.ToolItem()
        self.label_radio1 = gtk.Label()
        self.label_radio1.set_text(_('Circles between') + ' ')
        item1.add(self.label_radio1)
        barra.insert(item1, 2)

        item2 = gtk.ToolItem()
        self.cradio1 = gtk.SpinButton()
        self.cradio1.set_range(1, 20)
        self.cradio1.set_increments(1, 2)
        self.cradio1.props.value = self.radio_uno
        self.cradio1_handler = self.cradio1.connect('notify::value', self.cradio1_valor)
        item2.add(self.cradio1)
        barra.insert(item2, 3)

        item3 = gtk.ToolItem()
        self.label_and = gtk.Label()
        self.label_and.set_text(' ' + _('and') + ' ')
        item3.add(self.label_and)
        barra.insert(item3, 4)

        item4 = gtk.ToolItem()
        self.cradio2 = gtk.SpinButton()
        self.cradio2.set_range(1, 20)
        self.cradio2.set_increments(1, 2)
        self.cradio2.props.value = self.radio_dos
        self.cradio2_handler = self.cradio2.connect('notify::value', self.cradio2_valor)
        item4.add(self.cradio2)
        barra.insert(item4, 5)

        """
        save_button = ToolButton('filesave')
        save_button.set_tooltip(_('Save Image'))
        save_button.connect('clicked', self._savebutton_cb)
        barra.insert(save_button, 7)
        save_button.show()"""

        self.set_toolbar_box(toolbox)

        toolbox.show()

    def cradio1_valor(self, radio, value):
        self.radio_uno = int(radio.props.value)
        self.actividad.poner_radio1(self.radio_uno)

    def cradio2_valor(self, radio, value):
        self.radio_dos = int(radio.props.value)
        self.actividad.poner_radio2(self.radio_dos)

    def _savebutton_cb(self,button):
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, action='savebutton'))

    def save_image(self,image):
        journalobj = datastore.create()
        journalobj.metadata['title'] = _('Pointillism')
        journalobj.metadata['mime_type'] = 'image/jpeg'

        file_path = os.path.join(os.environ['SUGAR_ACTIVITY_ROOT'], 'data', 'pointillism.jpg')

        pygame.image.save(image,file_path)
        journalobj.set_file_path(file_path)
        datastore.write(journalobj)

        journalobj.destroy()

