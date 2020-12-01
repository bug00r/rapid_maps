from rapidmaps.mapui.wxui.generated.rapidmap import MainFrame
from rapidmaps.map.state import MapStateTranslator, MapState, MapStateType
from wx import AutoBufferedPaintDC as abDC
from wx import BG_STYLE_PAINT, Exit

from rapidmaps.map.shape import *
from rapidmaps.map.selection import Selections


def remove_from_list(shape, aList: list):
    aList.remove(shape)


class RapidMapFrame(MainFrame):

    def __init__(self):
        super().__init__(None)
        self.canvas.SetBackgroundStyle(BG_STYLE_PAINT)
        self.m_scrolled_map.SetAutoLayout(True)
        self.__shape_clz = [Point, Quad, Circle, Triangle, CharImage]
        self.__shape_obj = []
        self.__bg_image = None
        self.__bg_bitmap = None
        self.__sel_shape = None
        self.__scaled_image = None
        self.__scalefactor = (1.0, 1.0)
        self.__last_scalefactor = tuple(self.__scalefactor)
        self._selections = Selections()
        # new parts
        self._ms = MapState()
        self._mst = MapStateTranslator(self._ms, self._selections)
        self._ms.set(MapStateType.MOVING_MODE_UI, True)
        self._ms.set(MapStateType.SELECTION_MODE_UI, False)
        self._ms.set(MapStateType.ADDITION_MODE_UI, False)
        self._ms.set(MapStateType.SELECTION_IS_MOVING, False)
        self._ms.set(MapStateType.KB_CTRL, wx.wxEVT_KEY_UP)
        self._ms.set(MapStateType.KB_SHIFT, wx.wxEVT_KEY_UP)
        self._ms.set(MapStateType.KB_ALT, wx.wxEVT_KEY_UP)
        self._ms.set(MapStateType.MOUSE_LEFT, wx.wxEVT_LEFT_UP)
        self._ms.set(MapStateType.MOUSE_LEFT_POS, wxPoint(-1, -1))
        self._ms.set(MapStateType.MOUSE_LEFT_RELEASE_POS, wxPoint(-1, -1))

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
            self.__edit_enabled(False)
            anyselected = False
            for shape in self.__shape_obj:
                if shape.intersect_by(event.Position):
                    self.__sel_shape = shape
                    anyselected = True
                    if self._mst.should_add_selection:
                        if self._selections.contains(shape):
                            self._selections.remove(shape)
                        else:
                            self._selections.add(shape)
                    else:
                        self._selections.clear()
                        self._selections.add(shape)
                if not self._selections.is_empty():
                    self.__edit_enabled(True)
                    self.__set_edit_by(shape)
            if not self._mst.should_add_selection and not anyselected:
                self._selections.clear()

        self.canvas.Refresh()
        event.Skip()

    def canvasOnMotion(self, event):
        self._ms.set(MapStateType.MOUSE_POS, event.Position)
        if self._mst.is_selection_area_active:
            self.canvas.Refresh()
        elif self._mst.selection_is_moving:
            self._ms.set(MapStateType.SELECTION_IS_MOVING, True)
            self._selections.action_on('add_to_pos', [self._mst.mouse_move_diff])
            self.canvas.Refresh()
        else:
            self._ms.set(MapStateType.SELECTION_IS_MOVING, False)

    def canvasOnLeftUp(self, event):
        was_area_sel = self._mst.is_selection_area_active
        selected_area = self._mst.current_selected_area

        self._ms.set(MapStateType.MOUSE_LEFT, event.EventType)
        self._ms.set(MapStateType.MOUSE_LEFT_RELEASE_POS, event.Position)

        if was_area_sel:
            if selected_area.width < 0:
                selected_area.x = selected_area.x + selected_area.width
                selected_area.width = abs(selected_area.width)
            if selected_area.height < 0:
                selected_area.y = selected_area.y + selected_area.height
                selected_area.height = abs(selected_area.height)
            for shape in self.__shape_obj:
                if selected_area.Contains(shape.get_bbox()):
                    self._selections.add(shape)
                elif self._mst.should_add_selection:
                    if not self._selections.contains(shape):
                        self._selections.remove(shape)
                else:
                    self._selections.remove(shape)
        if self.should_add_entity():
            self.__sel_shape = self.m_shapes.Selection
            new_obj = self.__shape_clz[self.__sel_shape]()
            new_obj.set_pos(position=event.Position)
            new_obj.scale_size(self.__scalefactor[0])
            self.__shape_obj.append(new_obj)
            # self.canvas.Refresh()
        else:
            self.__sel_shape = None
        self.canvas.Refresh()
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
        if self.__bg_bitmap:
            dc.DrawBitmap(self.__bg_bitmap, 0, 0)
        elif not self.__bg_image:
            dc.SetBackground(Brush(Colour(0, 0, 0)))
            dc.Clear()
        for shape in self.__shape_obj:
            shape.draw_by_dc(dc)
        if self._mst.is_selection_area_active:
            oldpen = dc.GetPen()
            oldbrush = dc.GetBrush()
            dc.SetPen(wx.Pen(GREEN, 2))
            dc.SetBrush(wx.Brush(GREEN, wx.TRANSPARENT))
            dc.DrawRectangle(self._mst.current_selected_area)
            dc.SetPen(oldpen)
            dc.SetBrush(oldbrush)


    def should_add_entity(self):
        return self._ms.get(MapStateType.ADDITION_MODE_UI).value

    def OnLoadMap(self, event):
        if self.__bg_image and wx.MessageBox("Do you really want to reload the Map?", "Please confirm",
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
                        self.__bg_image = wx.Image(pathname, wx.BITMAP_TYPE_ANY)
                        self.__bg_bitmap = self.__bg_image.ConvertToBitmap();
                        self.canvas.SetSize(self.__bg_image.GetSize())
                        self.canvas.Refresh()
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
        if self.__bg_bitmap:
            size = self.__scaled_image.GetSize() if self.__scaled_image else self.__bg_image.GetSize()
            if self.m_scrolled_map.GetVirtualSize() != size:
                self.m_scrolled_map.SetVirtualSize(size)
            else:
                event.Skip()
        else:
            event.Skip()

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

    def OnMapZoom(self, event):
        if self.__bg_image and self.__bg_image:
            scale_factor = 1.0 + (float(event.Int) / 100.0)
            self.__last_scalefactor = tuple(self.__scalefactor)
            self.__scalefactor = (scale_factor, 1.0 / scale_factor)
            self.__scaled_image = self.__bg_image.Scale(self.__bg_image.Width * scale_factor,
                                                        self.__bg_image.Height * scale_factor)
            self.__bg_bitmap = self.__scaled_image.ConvertToBitmap()
            self.canvas.SetSize(self.__scaled_image.GetSize())
            self.canvas.Refresh()
            self.m_scrolled_map.SetVirtualSize(self.__scaled_image.GetSize())
            new_scale = self.__scalefactor[0] * self.__last_scalefactor[1]
            for shape in self.__shape_obj:
                shape.scale(new_scale)
