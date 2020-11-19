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

		self.m_panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer31 = wx.BoxSizer( wx.VERTICAL )

		m_radioBox21Choices = [ u"Select", u"Add" ]
		self.m_radioBox21 = wx.RadioBox( self.m_panel3, wx.ID_ANY, u"Actions", wx.DefaultPosition, wx.DefaultSize, m_radioBox21Choices, 1, wx.RA_SPECIFY_COLS )
		self.m_radioBox21.SetSelection( 0 )
		bSizer31.Add( self.m_radioBox21, 0, wx.ALL|wx.EXPAND, 5 )

		m_radioBox2Choices = [ u"Point", u"Quad", u"Circle", u"Triangle" ]
		self.m_radioBox2 = wx.RadioBox( self.m_panel3, wx.ID_ANY, u"Shapes", wx.DefaultPosition, wx.DefaultSize, m_radioBox2Choices, 1, wx.RA_SPECIFY_COLS )
		self.m_radioBox2.SetSelection( 0 )
		self.m_radioBox2.Enable( False )

		bSizer31.Add( self.m_radioBox2, 0, wx.ALL, 5 )


		self.m_panel3.SetSizer( bSizer31 )
		self.m_panel3.Layout()
		bSizer31.Fit( self.m_panel3 )
		bSizer1.Add( self.m_panel3, 0, wx.EXPAND |wx.ALL, 5 )

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

		# Connect Events
		self.m_radioBox21.Bind( wx.EVT_RADIOBOX, self.OnActionChange )
		self.m_radioBox2.Bind( wx.EVT_RADIOBOX, self.OnShapeChange )
		self.canvas.Bind( wx.EVT_LEFT_DOWN, self.OnMouseLeftDown )
		self.canvas.Bind( wx.EVT_LEFT_UP, self.OnMouseLeftUp )
		self.canvas.Bind( wx.EVT_MOTION, self.OnMouseMotion )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnActionChange( self, event ):
		event.Skip()

	def OnShapeChange( self, event ):
		event.Skip()

	def OnMouseLeftDown( self, event ):
		event.Skip()

	def OnMouseLeftUp( self, event ):
		event.Skip()

	def OnMouseMotion( self, event ):
		event.Skip()


