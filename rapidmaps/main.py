#!/usr/bin/python
# -*- coding: <<encoding>> -*-
# -------------------------------------------------------------------------------
#   <<project>>
#
# -------------------------------------------------------------------------------

import wx

from rapidmaps.mapui.main import RapidMapFrame

app = wx.App(redirect=False)  # Error messages go to popup window
top = RapidMapFrame()
top.Show()
app.MainLoop()
