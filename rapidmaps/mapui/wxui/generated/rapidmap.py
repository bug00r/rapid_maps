# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
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

		bSizer31.Add( self.m_shapes, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_panel31 = wx.Panel( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText2 = wx.StaticText( self.m_panel31, wx.ID_ANY, u"Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer4.Add( self.m_staticText2, 0, wx.ALL, 5 )

		self.m_name = wx.TextCtrl( self.m_panel31, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer4.Add( self.m_name, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText1 = wx.StaticText( self.m_panel31, wx.ID_ANY, u"Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		bSizer4.Add( self.m_staticText1, 0, wx.ALL, 5 )

		self.m_size = wx.Slider( self.m_panel31, wx.ID_ANY, 20, 1, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		bSizer4.Add( self.m_size, 0, wx.ALL, 5 )

		self.m_colour = wx.ColourPickerCtrl( self.m_panel31, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		bSizer4.Add( self.m_colour, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel31.SetSizer( bSizer4 )
		self.m_panel31.Layout()
		bSizer4.Fit( self.m_panel31 )
		bSizer31.Add( self.m_panel31, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_clear = wx.Button( self.m_panel3, wx.ID_ANY, u"Clear Map", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.m_clear, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button2 = wx.Button( self.m_panel3, wx.ID_ANY, u"Del Selected", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.m_button2, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText3 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"Map Zoom", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer31.Add( self.m_staticText3, 0, wx.ALL, 5 )

		self.m_zoom = wx.Slider( self.m_panel3, wx.ID_ANY, 0, 0, 300, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		bSizer31.Add( self.m_zoom, 0, wx.ALL, 5 )


		self.m_panel3.SetSizer( bSizer31 )
		self.m_panel3.Layout()
		bSizer31.Fit( self.m_panel3 )
		bSizer1.Add( self.m_panel3, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_scrolled_map = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolled_map.SetScrollRate( 5, 5 )
		canvas_sizer = wx.BoxSizer( wx.VERTICAL )

		self.canvas = wx.Panel( self.m_scrolled_map, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.canvas.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.canvas.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

		canvas_sizer.Add( self.canvas, 1, wx.EXPAND |wx.ALL, 5 )


		self.m_scrolled_map.SetSizer( canvas_sizer )
		self.m_scrolled_map.Layout()
		canvas_sizer.Fit( self.m_scrolled_map )
		bSizer1.Add( self.m_scrolled_map, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.Bind( wx.EVT_MENU, self.OnLoadMap, id = self.m_mi_loadmap.GetId() )
		self.Bind( wx.EVT_MENU, self.OnExit, id = self.m_mi_exit.GetId() )
		self.m_actions.Bind( wx.EVT_RADIOBOX, self.OnActionChange )
		self.m_shapes.Bind( wx.EVT_RADIOBOX, self.OnShapeChange )
		self.m_name.Bind( wx.EVT_TEXT_ENTER, self.OnNameChanged )
		self.m_size.Bind( wx.EVT_SCROLL, self.OnSizeChanged )
		self.m_colour.Bind( wx.EVT_COLOURPICKER_CHANGED, self.OnColourChanged )
		self.m_clear.Bind( wx.EVT_BUTTON, self.OnClearMap )
		self.m_button2.Bind( wx.EVT_BUTTON, self.OnRemoveSelected )
		self.m_zoom.Bind( wx.EVT_SCROLL_CHANGED, self.OnMapZoom )
		self.m_scrolled_map.Bind( wx.EVT_SIZE, self.OnScrollMapSize )
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

	def OnNameChanged( self, event ):
		event.Skip()

	def OnSizeChanged( self, event ):
		event.Skip()

	def OnColourChanged( self, event ):
		event.Skip()

	def OnClearMap( self, event ):
		event.Skip()

	def OnRemoveSelected( self, event ):
		event.Skip()

	def OnMapZoom( self, event ):
		event.Skip()

	def OnScrollMapSize( self, event ):
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


