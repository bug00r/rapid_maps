import wx


class ShapeInitWF(object):

    def __init__(self, main_frame):
        self._frame = main_frame
        self._shape_lib = self._frame.shape_lib
        self._shape_lib_groups = self._frame.shape_lib_groups
        self._all_shape_btns = self._frame.all_shape_btns
        self.m_shape_lib = self._frame.m_shape_lib

    def _init_shapes(self):
        for shape_entry in self._shape_lib.get_shapes():

            if not shape_entry.group in self._shape_lib_groups:
                colpane = self._add_new_shape_group(shape_entry.group)
                self._shape_lib_groups[shape_entry.group] = colpane
            else:
                colpane = self._shape_lib_groups[shape_entry.group]

            c_btn = wx.BitmapToggleButton(colpane.GetPane())

            c_btn.Bind(wx.EVT_TOGGLEBUTTON, self.on_shape_btn_pressed)
            self._all_shape_btns[c_btn] = shape_entry.name
            colpane.GetPane().GetSizer().Add(c_btn, 1, wx.ALL, 2)

            if shape_entry.shape:
                size = shape_entry.shape.get_size()
                thumb = wx.Bitmap.FromRGBA(size.width, size.height, alpha=1)
                thumb_dc = wx.MemoryDC(thumb)
                shape_entry.shape.show_label(False)
                shape_entry.shape.draw_by_dc(thumb_dc)
                shape_entry.shape.show_label(True)
                thumb_img = thumb.ConvertToImage().Rescale(32, 32)
                c_btn.SetBitmap(thumb_img.ConvertToBitmap())

    def on_shape_btn_pressed(self, event):

        if self._frame.cur_shape_btn:
            self._frame.cur_shape_btn.SetValue(False)

        if event.EventObject == self._frame.cur_shape_btn and event.Int == 0:
            self._frame.cur_shape_btn = None
        else:
            self._frame.cur_shape_btn = event.EventObject

    def _add_new_shape_group(self, group_name) -> wx.CollapsiblePane:
        new_cpane = wx.CollapsiblePane(self.m_shape_lib, wx.ID_ANY, f"{group_name}:", style=wx.CP_NO_TLW_RESIZE)
        new_cpane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.on_shape_group_collapse)
        grid_sizer = wx.GridSizer(rows=0, cols=3, gap=wx.Size(2, 2))
        new_cpane.GetPane().SetSizer(grid_sizer)
        grid_sizer.SetSizeHints(new_cpane.GetPane())
        self.m_shape_lib.GetSizer().Add(new_cpane, 0, wx.GROW | wx.ALL, 5)
        return new_cpane

    def on_shape_group_collapse(self, event):
        self._frame.m_panel3.GetSizer().Layout()
        self._frame.m_panel3.Refresh()
        #This is for redrawing leftpanel, little bit hacky
        self._frame.redraw_left_navigation_pane_complete()

    def process(self):
        self._init_shapes()


class IconInitWF(object):

    def __init__(self, main_frame):
        self._frame = main_frame

    def _init_icons(self, element_list):
        for element, icon in element_list:
            element.SetBitmap(wx.Image(f"./resource/icon/{icon}.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap())

    def process(self):
        self._init_icons([(self._frame.m_add_btn, 'add'), (self._frame.m_move_btn, 'move'),
                          (self._frame.m_select_btn, 'select'), (self._frame.m_map_del_btn, 'delete'),
                          (self._frame.m_map_edit_btn, 'edit'), (self._frame.m_map_add_btn, 'add'),
                          (self._frame.m_map_save_btn, 'save'), (self._frame.m_map_import_btn, 'import')])


class HistoryInitWF(object):

    def __init__(self, main_frame):
        self._frame = main_frame

    def _init_map_history(self):
        for index, map in enumerate(self._frame.map_history.get_maps()):
            self._frame.m_map_history_list.InsertItem(index, map.name)

    def process(self):
        self._frame.m_map_history_list.InsertColumn(0, "Name")
        self._frame.recalc_map_list_size()
        self._init_map_history()
        self._frame.redraw_left_navigation_pane_complete()
