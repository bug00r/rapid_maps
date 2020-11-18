# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Nov 18 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Rapid Mapping tool", pos = wx.DefaultPosition, size = wx.Size( 1208,728 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.m_statusmain = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menu1 = wx.Menu()
		self.m_mi_loadmap = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Load Map", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_mi_loadmap )

		self.m_menu1.AppendSeparator()

		self.m_mi_exit = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_mi_exit )

		self.m_menubar1.Append( self.m_menu1, u"File" )

		self.SetMenuBar( self.m_menubar1 )

		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_scrolledWindow1 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow1.SetScrollRate( 5, 5 )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.canvas = wx.Panel( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.canvas.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

		bSizer3.Add( self.canvas, 1, wx.EXPAND |wx.ALL, 5 )


		self.m_scrolledWindow1.SetSizer( bSizer3 )
		self.m_scrolledWindow1.Layout()
		bSizer3.Fit( self.m_scrolledWindow1 )
		bSizer1.Add( self.m_scrolledWindow1, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


