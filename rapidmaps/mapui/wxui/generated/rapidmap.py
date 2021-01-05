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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Rapid Mapping tool", pos = wx.DefaultPosition, size = wx.Size( 1208,766 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 640,480 ), wx.DefaultSize )
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

		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )

		self.m_scrolledWindow2 = wx.ScrolledWindow( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow2.SetScrollRate( 5, 5 )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel3 = wx.Panel( self.m_scrolledWindow2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer31 = wx.BoxSizer( wx.VERTICAL )

		m_actionsChoices = [ u"Move", u"Select", u"Add" ]
		self.m_actions = wx.RadioBox( self.m_panel3, wx.ID_ANY, u"Actions", wx.DefaultPosition, wx.DefaultSize, m_actionsChoices, 1, wx.RA_SPECIFY_COLS )
		self.m_actions.SetSelection( 0 )
		bSizer31.Add( self.m_actions, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_panel311 = wx.Panel( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		colsizer = wx.StaticBoxSizer( wx.StaticBox( self.m_panel311, wx.ID_ANY, u"Shapes" ), wx.VERTICAL )

		self.m_shape_lib = wx.Panel( self.m_panel311, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		m_shape_lib_sizer = wx.BoxSizer( wx.VERTICAL )


		self.m_shape_lib.SetSizer( m_shape_lib_sizer )
		self.m_shape_lib.Layout()
		m_shape_lib_sizer.Fit( self.m_shape_lib )
		colsizer.Add( self.m_shape_lib, 1, wx.EXPAND |wx.ALL, 5 )


		self.m_panel311.SetSizer( colsizer )
		self.m_panel311.Layout()
		colsizer.Fit( self.m_panel311 )
		bSizer31.Add( self.m_panel311, 1, wx.EXPAND |wx.ALL, 5 )

		m_shapesChoices = [ u"Point", u"Quad", u"Circle", u"Woman", u"ImageQuad", u"ImageCircle" ]
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

		self.m_size = wx.Slider( self.m_panel31, wx.ID_ANY, 20, 1, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL|wx.SL_LABELS )
		bSizer4.Add( self.m_size, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_colour = wx.ColourPickerCtrl( self.m_panel31, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		bSizer4.Add( self.m_colour, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText4 = wx.StaticText( self.m_panel31, wx.ID_ANY, u"Rotation:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer4.Add( self.m_staticText4, 0, wx.ALL, 5 )

		self.m_rotation = wx.Slider( self.m_panel31, wx.ID_ANY, 0, -180, 180, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL|wx.SL_LABELS )
		bSizer4.Add( self.m_rotation, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText5 = wx.StaticText( self.m_panel31, wx.ID_ANY, u"Text Größe:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer4.Add( self.m_staticText5, 0, wx.ALL, 5 )

		self.m_text_size = wx.Slider( self.m_panel31, wx.ID_ANY, 1, 1, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL|wx.SL_LABELS )
		bSizer4.Add( self.m_text_size, 0, wx.ALL|wx.EXPAND, 5 )


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

		self.m_zoom = wx.Slider( self.m_panel3, wx.ID_ANY, 100, 1, 400, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		bSizer31.Add( self.m_zoom, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel3.SetSizer( bSizer31 )
		self.m_panel3.Layout()
		bSizer31.Fit( self.m_panel3 )
		bSizer5.Add( self.m_panel3, 0, wx.EXPAND |wx.ALL, 5 )


		self.m_scrolledWindow2.SetSizer( bSizer5 )
		self.m_scrolledWindow2.Layout()
		bSizer5.Fit( self.m_scrolledWindow2 )
		self.m_panel6 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.canvas = wx.Panel( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.canvas.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.canvas.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

		bSizer8.Add( self.canvas, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_map_hscroll = wx.ScrollBar( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SB_HORIZONTAL )
		bSizer8.Add( self.m_map_hscroll, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer6.Add( bSizer8, 1, wx.EXPAND, 5 )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		self.m_map_vscroll = wx.ScrollBar( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SB_VERTICAL )
		bSizer7.Add( self.m_map_vscroll, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer6.Add( bSizer7, 0, wx.EXPAND, 5 )


		self.m_panel6.SetSizer( bSizer6 )
		self.m_panel6.Layout()
		bSizer6.Fit( self.m_panel6 )
		self.m_splitter1.SplitVertically( self.m_scrolledWindow2, self.m_panel6, 160 )
		bSizer1.Add( self.m_splitter1, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.Bind( wx.EVT_MENU, self.OnLoadMap, id = self.m_mi_loadmap.GetId() )
		self.Bind( wx.EVT_MENU, self.OnExit, id = self.m_mi_exit.GetId() )
		self.m_actions.Bind( wx.EVT_RADIOBOX, self.on_mode_change )
		self.m_shapes.Bind( wx.EVT_RADIOBOX, self.OnShapeChange )
		self.m_name.Bind( wx.EVT_TEXT_ENTER, self.OnNameChanged )
		self.m_size.Bind( wx.EVT_SCROLL, self.OnSizeChanged )
		self.m_colour.Bind( wx.EVT_COLOURPICKER_CHANGED, self.OnColourChanged )
		self.m_rotation.Bind( wx.EVT_SCROLL, self.OnRotationChanged )
		self.m_text_size.Bind( wx.EVT_SCROLL, self.OnTextSizeChanged )
		self.m_clear.Bind( wx.EVT_BUTTON, self.OnClearMap )
		self.m_button2.Bind( wx.EVT_BUTTON, self.OnRemoveSelected )
		self.m_zoom.Bind( wx.EVT_SCROLL_CHANGED, self.OnMapZoom )
		self.canvas.Bind( wx.EVT_KEY_DOWN, self.canvasOnKeyDown )
		self.canvas.Bind( wx.EVT_KEY_UP, self.canvasOnKeyUp )
		self.canvas.Bind( wx.EVT_LEFT_DOWN, self.canvasOnLeftDown )
		self.canvas.Bind( wx.EVT_LEFT_UP, self.canvasOnLeftUp )
		self.canvas.Bind( wx.EVT_MOTION, self.canvasOnMotion )
		self.canvas.Bind( wx.EVT_MOUSEWHEEL, self.canvasOnMouseWheel )
		self.canvas.Bind( wx.EVT_PAINT, self.canvasOnPaint )
		self.canvas.Bind( wx.EVT_SIZE, self.canvasOnSize )
		self.m_map_hscroll.Bind( wx.EVT_SCROLL, self.m_map_hscrollOnScroll )
		self.m_map_hscroll.Bind( wx.EVT_SCROLL_THUMBRELEASE, self.m_map_hscrollOnScrollThumbRelease )
		self.m_map_vscroll.Bind( wx.EVT_SCROLL, self.m_map_vscrollOnScroll )
		self.m_map_vscroll.Bind( wx.EVT_SCROLL_THUMBRELEASE, self.m_map_vscrollOnScrollThumbRelease )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnClose( self, event ):
		event.Skip()

	def OnLoadMap( self, event ):
		event.Skip()

	def OnExit( self, event ):
		event.Skip()

	def on_mode_change( self, event ):
		event.Skip()

	def OnShapeChange( self, event ):
		event.Skip()

	def OnNameChanged( self, event ):
		event.Skip()

	def OnSizeChanged( self, event ):
		event.Skip()

	def OnColourChanged( self, event ):
		event.Skip()

	def OnRotationChanged( self, event ):
		event.Skip()

	def OnTextSizeChanged( self, event ):
		event.Skip()

	def OnClearMap( self, event ):
		event.Skip()

	def OnRemoveSelected( self, event ):
		event.Skip()

	def OnMapZoom( self, event ):
		event.Skip()

	def canvasOnKeyDown( self, event ):
		event.Skip()

	def canvasOnKeyUp( self, event ):
		event.Skip()

	def canvasOnLeftDown( self, event ):
		event.Skip()

	def canvasOnLeftUp( self, event ):
		event.Skip()

	def canvasOnMotion( self, event ):
		event.Skip()

	def canvasOnMouseWheel( self, event ):
		event.Skip()

	def canvasOnPaint( self, event ):
		event.Skip()

	def canvasOnSize( self, event ):
		event.Skip()

	def m_map_hscrollOnScroll( self, event ):
		event.Skip()

	def m_map_hscrollOnScrollThumbRelease( self, event ):
		event.Skip()

	def m_map_vscrollOnScroll( self, event ):
		event.Skip()

	def m_map_vscrollOnScrollThumbRelease( self, event ):
		event.Skip()

	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 160 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )


