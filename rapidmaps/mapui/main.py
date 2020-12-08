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
        self.canvas.SetBackgroundStyle(BG_STYLE_PAINT)
        self.__shape_clz = [Point, Quad, Circle, Triangle, CharImage]
        self.__sel_shape = None
        self.__scaled_image = None
        self._map = RapidMap(self.canvas)
        self.__shape_obj = self._map.map_objects
        self._selections = self._map.selections
        self._ms = self._map.mapstate
        self._mst = self._map.mapstatetranslator

    def on_mode_change(self, event):
        # event.Skip()
        self._ms.set(MapStateType.MOVING_MODE_UI, event.Selection == 0)
        self._ms.set(MapStateType.SELECTION_MODE_UI, event.Selection == 1)
        self._ms.set(MapStateType.ADDITION_MODE_UI, event.Selection == 2)
        self.m_shapes.Enable(enable=self.should_add_entity())

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

            zoom = self._map.map_zoom_factor if self._map.should_scale_up[0] else self._map.object_zoom_factor

            self._selections.action_on('add_to_pos', [self._mst.mouse_move_diff * zoom])
            self.canvas.Refresh()
        else:
            self._ms.set(MapStateType.SELECTION_IS_MOVING, False)

    def canvasOnLeftUp(self, event):
        self._ms.set(MapStateType.MOUSE_LEFT, event.EventType)
        self._ms.set(MapStateType.MOUSE_LEFT_RELEASE_POS, event.Position)

        if self._mst.was_selection_area_active:
            self._map.area_selection_at(self._mst.current_selected_area)
        if self.should_add_entity():
            self._map.add_shape(self.m_shapes.Selection, event.Position.x, event.Position.y)
        else:
            self.__sel_shape = None

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
        if self._map.bg_image:
            newvize = self._map.bg_image.GetSize()
            realsize = self.canvas.GetSize()

            zoom = self._map.map_zoom_factor if self._map.should_scale_up[0] else self._map.object_zoom_factor

            self.m_map_hscroll.SetScrollbar(self._map.view.viewport.x,
                                            realsize.width * zoom, newvize.width, realsize.width, True)
            self.m_map_vscroll.SetScrollbar(self._map.view.viewport.y,
                                            realsize.height * zoom, newvize.height, realsize.height, True)

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
        self._map.view.rsize = event.Size
        self._map.view.viewport.width = event.Size.width
        self._map.view.viewport.height = event.Size.height
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
        self._map.view.viewport.x = event.Position
        self.canvas.Refresh()

    def m_map_hscrollOnScrollThumbRelease(self, event):
        self.canvas.Refresh()

    def m_map_vscrollOnScroll(self, event):
        #todo only repaint until realtim scroll is enabled(should be added)
        self._map.view.viewport.y = event.Position
        self.canvas.Refresh()

    def m_map_vscrollOnScrollThumbRelease(self, event):
        self.canvas.Refresh()

    def canvasOnMouseWheel(self, event):
        if event.controlDown:
            new_val = self.m_zoom.Value + ((event.WheelRotation/100) * 4)
            if new_val > self.m_zoom.Max:
                new_val = self.m_zoom.Max
            elif new_val < self.m_zoom.Min:
                new_val = self.m_zoom.Min
            self.m_zoom.Value = new_val
            self._do_zoom(self.m_zoom.Value)
