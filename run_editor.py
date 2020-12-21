#!/usr/bin/python
# -*- coding: <<encoding>> -*-
# -------------------------------------------------------------------------------
#   <<project>>
#
# -------------------------------------------------------------------------------

import wx
from rapidmaps.mapui.main import RapidMapFrame
from pathlib import Path


class AppConfig(object):
    def __init__(self):
        self._app_path = Path()
        self._app_shape_path = self._app_path / 'shapes'

    @property
    def path(self):
        return self._app_path

    @property
    def shape_path(self):
        return self._app_shape_path


app = wx.App(redirect=False)  # Error messages go to popup window
setattr(app, "app_conf", AppConfig())
top = RapidMapFrame()
top.Show()
app.MainLoop()