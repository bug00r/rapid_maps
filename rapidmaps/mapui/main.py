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
        self.__sel_action = 0
        self.__lm_release = None
        self.__sel_shape = None
        self.__bg_image = None
        self.__bg_bitmap = None
        self.__sel_shape = None
        self.__last_sel_shape = None
        self.__sel_shape_point = None
        self.__last_move_pt = None
        self.__scaled_image = None
        self.__scalefactor = (1.0, 1.0)
        self.__last_scalefactor = tuple(self.__scalefactor)
        self._selections = Selections()
        # new parts
        self._ms = MapState()
        self._mst = MapStateTranslator(self._ms)
        self._ms.set(MapStateType.SELECTION_UI, True)
        self._ms.set(MapStateType.KB_CTRL, wx.wxEVT_KEY_UP)
        self._ms.set(MapStateType.MOUSE_LEFT, wx.wxEVT_LEFT_UP)
        self._ms.set(MapStateType.MOUSE_LEFT_POS, wxPoint(-1, -1))
        self._ms.set(MapStateType.MOUSE_LEFT_RELEASE_POS, wxPoint(-1, -1))


    def m_actionsOnRadioBox(self, event):
        # event.Skip()
        self._ms.set(MapStateType.SELECTION_UI, event.Selection == 0)
        self.__sel_action = event.Selection
        self.m_shapes.Enable(enable=self.should_add_entity())

    def OnShapeChange(self, event):
        event.Skip()

    def canvasOnLeftDown(self, event):
        self._ms.set(MapStateType.MOUSE_LEFT, event.EventType)
        self._ms.set(MapStateType.MOUSE_LEFT_POS, event.Position)
        self._mst.is_single_selection
        self.__sel_shape_point = event.Position
        self.__edit_enabled(False)
        for shape in self.__shape_obj:
            if shape.intersect_by(self.__sel_shape_point):
                self.__sel_shape = shape
                self.__last_sel_shape = shape
                self.__last_move_pt = self.__sel_shape_point
                if event.controlDown:
                    if self._selections.contains(shape) and (self.__last_move_pt != event.Position):
                        self._selections.remove(shape)
                    else:
                        self._selections.add(shape)
        if not self._selections.is_empty():
            self.__edit_enabled(True)
            self.__set_edit_by(shape)
        self.canvas.Refresh()
        event.Skip()

    def canvasOnMotion(self, event):
        self._ms.set(MapStateType.MOUSE_POS, event.Position)
        if not self._selections.is_empty():
            if event.leftIsDown and self._selections.intersect_any(event.Position):
                self._selections.action_on('add_to_pos', [(event.Position - self.__last_move_pt)])
                self.__last_move_pt = event.Position
                self.canvas.Refresh()

    def canvasOnLeftUp(self, event):
        self._ms.set(MapStateType.MOUSE_LEFT, event.EventType)
        self._ms.set(MapStateType.MOUSE_LEFT_RELEASE_POS, event.Position)
        self._mst.is_single_selection
        if not event.controlDown:
            self._selections.clear()
            self.canvas.Refresh()
        if self.should_add_entity():
            self.__lm_release = event.Position
            self.__sel_shape = self.m_shapes.Selection
            new_obj = self.__shape_clz[self.__sel_shape]()
            new_obj.set_pos(position=self.__lm_release)
            new_obj.scale_size(self.__scalefactor[0])
            self.__shape_obj.append(new_obj)
            self.canvas.Refresh()
        else:
            self.__sel_shape = None
            self.__sel_shape_point = None
        event.Skip()

    def canvasOnKeyDown(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_CONTROL:
            self._ms.set(MapStateType.KB_CTRL, event.EventType)
        event.Skip()

    def canvasOnKeyUp(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_CONTROL:
            self._ms.set(MapStateType.KB_CTRL, event.EventType)
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

    def should_add_entity(self):
        return self.__sel_action == 1

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

    def canvasOnSize( self, event):
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
        if self.__last_sel_shape:
            self.__last_sel_shape.set_color(event.Colour)
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
            self.__scalefactor = (scale_factor, 1.0/scale_factor)
            self.__scaled_image = self.__bg_image.Scale(self.__bg_image.Width*scale_factor, self.__bg_image.Height*scale_factor)
            self.__bg_bitmap = self.__scaled_image.ConvertToBitmap()
            self.canvas.SetSize(self.__scaled_image.GetSize())
            self.canvas.Refresh()
            self.m_scrolled_map.SetVirtualSize(self.__scaled_image.GetSize())
            new_scale = self.__scalefactor[0] * self.__last_scalefactor[1]
            for shape in self.__shape_obj:
                shape.scale(new_scale)
