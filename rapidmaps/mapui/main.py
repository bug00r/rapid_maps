from wx import BG_STYLE_PAINT, Exit, AutoBufferedPaintDC as abDC

from rapidmaps.mapui.wxui.generated.rapidmap import MainFrame
from rapidmaps.map.state import MapStateType
from rapidmaps.map.shape import *
from rapidmaps.map import RapidMap


def remove_from_list(shape, a_list: list):
    a_list.remove(shape)


class RapidMapFrame(MainFrame):

    def __init__(self):
        super().__init__(None)
        self._appconfig = wx.GetApp().app_conf
        self.canvas.SetBackgroundStyle(BG_STYLE_PAINT)
        self._map = RapidMap(self.canvas, self._appconfig)
        self._shape_lib = self._map.shape_lib
        self.__shape_obj = self._map.map_objects
        self._selections = self._map.selections
        self._ms = self._map.mapstate
        self._mst = self._map.mapstatetranslator
        self._shape_lib_groups = {}
        self._cur_shape_btn = None
        self._all_shape_btns = {}
        self._init_shapes()

    def _init_shapes(self):
        for shape_entry in self._shape_lib.get_shapes():

            if not shape_entry.group in self._shape_lib_groups:
                colpane = self._add_new_shape_group(shape_entry.group)
                self._shape_lib_groups[shape_entry.group] = colpane
            else:
                colpane = self._shape_lib_groups[shape_entry.group]

            c_btn = wx.BitmapToggleButton(colpane.GetPane())
            c_btn.SetBitmapMargins(0,0)
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

        if self._cur_shape_btn:
            self._cur_shape_btn.SetValue(False)

        self._cur_shape_btn = event.EventObject

    def _add_new_shape_group(self, group_name) -> wx.CollapsiblePane:
        new_cpane = wx.CollapsiblePane(self.m_shape_lib, wx.ID_ANY, f"{group_name}:", style=wx.CP_NO_TLW_RESIZE)
        new_cpane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.on_shape_group_collapse)
        grid_sizer = wx.GridSizer(rows=0, cols=3, gap=wx.Size(2,2))
        new_cpane.GetPane().SetSizer(grid_sizer)
        grid_sizer.SetSizeHints(new_cpane.GetPane())
        self.m_shape_lib.GetSizer().Add(new_cpane, 0, wx.GROW | wx.ALL, 5)
        return new_cpane

    def on_shape_group_collapse(self, event):
        self.m_panel3.GetSizer().Layout()
        self.m_panel3.Refresh()
        #This is for redrawing leftpanel, little bit hacky
        b_pos = self.m_splitter1.GetSashPosition()
        self.m_splitter1.SetSashPosition(b_pos + 1)
        self.m_splitter1.SetSashPosition(b_pos)

    def on_mode_change(self, event):
        # event.Skip()
        self._ms.set(MapStateType.MOVING_MODE_UI, event.Selection == 0)
        self._ms.set(MapStateType.SELECTION_MODE_UI, event.Selection == 1)
        self._ms.set(MapStateType.ADDITION_MODE_UI, event.Selection == 2)
        self.m_shape_lib.Enable(enable=self.should_add_entity())

    def OnShapeChange(self, event):
        event.Skip()

    def canvasOnLeftDown(self, event):
        self._ms.set(MapStateType.MOUSE_LEFT, event.EventType)
        self._ms.set(MapStateType.MOUSE_LEFT_POS, event.Position)

        if not self._mst.is_moving_mode_active and self._mst.is_selection_mode_active:
            foundShape = self._map.single_select_at(event.Position.x, event.Position.y)
            if foundShape:
                self.__edit_enabled(True)
                self.__set_edit_by(foundShape)
        event.Skip()

    def canvasOnMotion(self, event):
        self._ms.set(MapStateType.MOUSE_POS, event.Position)
        if self._mst.is_selection_area_active:
            self.canvas.Refresh()
        elif self._mst.selection_is_moving:
            self._ms.set(MapStateType.SELECTION_IS_MOVING, True)

            self._map.move_selected_shapes()
        else:
            self._ms.set(MapStateType.SELECTION_IS_MOVING, False)

    def canvasOnLeftUp(self, event):
        self._ms.set(MapStateType.MOUSE_LEFT, event.EventType)
        self._ms.set(MapStateType.MOUSE_LEFT_RELEASE_POS, event.Position)

        if self._mst.was_selection_area_active:
            self._map.area_selection_at(self._mst.current_selected_area)
        if self.should_add_entity() and self._cur_shape_btn is not None:
            self._map.add_shape_obj(self._all_shape_btns.get(self._cur_shape_btn, 'unknown'),
                                    event.Position.x, event.Position.y)

        event.Skip()

    def _canvas_set_key(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_CONTROL:
            self._ms.set(MapStateType.KB_CTRL, event.EventType)
        elif keycode == wx.WXK_ALT:
            self._ms.set(MapStateType.KB_ALT, event.EventType)
        elif keycode == wx.WXK_SHIFT:
            self._ms.set(MapStateType.KB_SHIFT, event.EventType)

    def canvasOnKeyDown(self, event):
        self._canvas_set_key(event)
        event.Skip()

    def canvasOnKeyUp(self, event):
        self._canvas_set_key(event)
        event.Skip()

    def canvasOnPaint(self, event):
        dc = abDC(self.canvas)
        self._map.update(dc)

    def _adjust_scrollbars(self):
        scroll = self._map.get_update_scrollbar_dimensions()
        hsbar, vsbar = scroll.horizontal, scroll.vertical
        self.m_map_hscroll.SetScrollbar(hsbar.pos, hsbar.thumb_size, hsbar.max_pos, hsbar.page_size, True)
        self.m_map_vscroll.SetScrollbar(vsbar.pos, vsbar.thumb_size, vsbar.max_pos, vsbar.page_size, True)

    def should_add_entity(self):
        return self._ms.get(MapStateType.ADDITION_MODE_UI).value

    def OnLoadMap(self, event):
        if self._map.bg_image and wx.MessageBox("Do you really want to reload the Map?", "Please confirm",
                                             wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
            event.Skip()
        else:
            with wx.FileDialog(self, "Open Map file",
                               wildcard="PNG,JPEG,JPG files (*.png;*.jpeg;*.jpg)|*.png;*.jpeg;*.jpg",
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    event.Skip()
                else:
                    try:
                        pathname = fileDialog.GetPath()
                        self._map.set_background(wx.Image(pathname, wx.BITMAP_TYPE_ANY))
                        self._adjust_scrollbars()
                        self.m_zoom.Value = 100
                    except IOError:
                        wx.LogError("Cannot open file '%s'." % pathname)

    def OnClose(self, event):
        self.__process_exit()

    def OnExit(self, event):
        self.__process_exit()

    def __process_exit(self):
        dlg = wx.MessageDialog(self,
                               "Do you want to close the Editor?",
                               'Closing Rapid Map Editor',
                               wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            Exit()

    def canvasOnSize(self, event):
        self._map.do_resize_viewport(event.Size)
        self._adjust_scrollbars()

    def OnClearMap(self, event):
        if self.__shape_obj:
            self.__shape_obj.clear()
            self.canvas.Refresh()

    def OnRemoveSelected(self, event):
        if not self._selections.is_empty():
            self._selections.action(remove_from_list, [self.__shape_obj])
            self._selections.clear()
            self.canvas.Refresh()

    def OnNameChanged(self, event):
        if not self._selections.is_empty():
            self._selections.action_on('set_name', [event.String])
            self.canvas.Refresh()

    def OnSizeChanged(self, event):
        if not self._selections.is_empty():
            self._selections.action_on('set_size', [Size(event.Int, event.Int)])
            self.canvas.Refresh()

    def OnTextSizeChanged(self, event):
        if not self._selections.is_empty():
            self._selections.action_on('set_text_size', [event.Int])
            self.canvas.Refresh()

    def OnRotationChanged(self, event):
        if not self._selections.is_empty():
            self._selections.action_on('set_angle', [event.Int])
            self.canvas.Refresh()

    def OnColourChanged(self, event):
        if not self._selections.is_empty():
            self._selections.action_on('set_color', [event.Colour])
            self.canvas.Refresh()

    def __edit_enabled(self, enabled: bool):
        self.m_name.Enable(enabled)
        self.m_size.Enable(enabled)
        self.m_colour.Enable(enabled)
        self.m_rotation.Enable(enabled)
        self.m_text_size.Enable(enabled)

    def __set_edit_by(self, shape: Shape):
        self.m_name.SetValue(shape.get_name())
        self.m_size.SetValue(shape.get_size().x)
        self.m_colour.SetColour(shape.get_color())
        self.m_rotation.SetValue(shape.get_angle())
        self.m_text_size.SetValue(shape.get_text_size())

    def _do_zoom(self, zoom_value: int):
        if self._map.bg_image:
            self._map.do_zoom(zoom_value)
            self._adjust_scrollbars()

    def OnMapZoom(self, event):
        self._do_zoom(event.Int)

    def m_map_hscrollOnScroll(self, event):
        # todo only repaint until realtim scroll is enabled(should be added)
        self._map.view.viewport.base.x = event.Position
        self.canvas.Refresh()

    def m_map_vscrollOnScroll(self, event):
        #todo only repaint until realtim scroll is enabled(should be added)
        self._map.view.viewport.base.y = event.Position
        self.canvas.Refresh()

    def canvasOnMouseWheel(self, event):
        if event.controlDown:
            wheeldiff = 0.1 if event.shiftDown else 0.01
            new_val = self.m_zoom.Value + (event.WheelRotation*wheeldiff)
            self.m_zoom.Value = min(max(new_val, self.m_zoom.Min), self.m_zoom.Max)
            self._do_zoom(self.m_zoom.Value)
