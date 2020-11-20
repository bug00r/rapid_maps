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
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		self.m_statusmain = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menue_file = wx.Menu()
		self.m_mi_loadmap = wx.MenuItem( self.m_menue_file, wx.ID_ANY, u"Load Map", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menue_file.Append( self.m_mi_loadmap )

		self.m_menue_file.AppendSeparator()

		self.m_mi_exit = wx.MenuItem( self.m_menue_file, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menue_file.Append( self.m_mi_exit )

		self.m_menubar1.Append( self.m_menue_file, u"File" )

		self.SetMenuBar( self.m_menubar1 )

		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer31 = wx.BoxSizer( wx.VERTICAL )

		m_actionsChoices = [ u"Select", u"Add" ]
		self.m_actions = wx.RadioBox( self.m_panel3, wx.ID_ANY, u"Actions", wx.DefaultPosition, wx.DefaultSize, m_actionsChoices, 1, wx.RA_SPECIFY_COLS )
		self.m_actions.SetSelection( 0 )
		bSizer31.Add( self.m_actions, 0, wx.ALL|wx.EXPAND, 5 )

		m_shapesChoices = [ u"Point", u"Quad", u"Circle", u"Triangle" ]
		self.m_shapes = wx.RadioBox( self.m_panel3, wx.ID_ANY, u"Shapes", wx.DefaultPosition, wx.DefaultSize, m_shapesChoices, 1, wx.RA_SPECIFY_COLS )
		self.m_shapes.SetSelection( 0 )
		self.m_shapes.Enable( False )

		bSizer31.Add( self.m_shapes, 0, wx.ALL, 5 )


		self.m_panel3.SetSizer( bSizer31 )
		self.m_panel3.Layout()
		bSizer31.Fit( self.m_panel3 )
		bSizer1.Add( self.m_panel3, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_scrolled_map = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolled_map.SetScrollRate( 5, 5 )
		canvas_sizer = wx.BoxSizer( wx.VERTICAL )

		self.canvas = wx.Panel( self.m_scrolled_map, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TAB_TRAVERSAL|wx.VSCROLL )
		self.canvas.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.canvas.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

		canvas_sizer.Add( self.canvas, 1, wx.EXPAND |wx.ALL, 5 )


		self.m_scrolled_map.SetSizer( canvas_sizer )
		self.m_scrolled_map.Layout()
		canvas_sizer.Fit( self.m_scrolled_map )
		bSizer1.Add( self.m_scrolled_map, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.Bind( wx.EVT_MENU, self.OnLoadMap, id = self.m_mi_loadmap.GetId() )
		self.Bind( wx.EVT_MENU, self.OnExit, id = self.m_mi_exit.GetId() )
		self.m_actions.Bind( wx.EVT_RADIOBOX, self.OnActionChange )
		self.m_shapes.Bind( wx.EVT_RADIOBOX, self.OnShapeChange )
		self.canvas.Bind( wx.EVT_LEFT_DOWN, self.OnMouseLeftDown )
		self.canvas.Bind( wx.EVT_LEFT_UP, self.OnMouseLeftUp )
		self.canvas.Bind( wx.EVT_MOTION, self.OnMouseMotion )
		self.canvas.Bind( wx.EVT_PAINT, self.OnPaint )
		self.canvas.Bind( wx.EVT_SIZE, self.OnCanvasSize )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnClose( self, event ):
		event.Skip()

	def OnLoadMap( self, event ):
		event.Skip()

	def OnExit( self, event ):
		event.Skip()

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

	def OnPaint( self, event ):
		event.Skip()

	def OnCanvasSize( self, event ):
		event.Skip()


