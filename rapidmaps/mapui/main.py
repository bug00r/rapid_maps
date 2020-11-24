from rapidmaps.mapui.wxui.generated.rapidmap import MainFrame
from typing import Any
import wx
from wx import Point as wxPoint
from wx import AutoBufferedPaintDC as abDC
from wx import Size, BG_STYLE_PAINT, Brush, Colour, Exit, BLACK


class Shape(object):

    def __init__(self):
        self._pos = wxPoint(0, 0)
        self._size = Size(20, 20)
        self._color = BLACK
        self._name = ""
        self._text_size = 12
        self._scale = 1.0
        self._angle = 0
        self._angle_changed = False

    def set_text_size(self, text_size):
        self._text_size = text_size

    def set_angle(self, angle: int):
        self._angle = angle
        self._angle_changed = True

    def get_angle(self):
        return self._angle

    def get_text_size(self):
        return self._text_size

    def scale(self, scale):
        self._scale = scale
        self.scale_pos(self._scale)
        self.scale_size(self._scale)

    def scale_pos(self, scale):
        self._pos = wxPoint(self._pos.x * scale, self._pos.y * scale)

    def scale_size(self, scale):
        self._size = Size(self._size.x * scale, self._size.y * scale)

    def get_color(self) -> Colour:
        return self._color

    def get_size(self):
        return self._size

    def get_name(self) -> str:
        return self._name

    def get_pos(self):
        return self._pos

    def set_color(self, color: Colour):
        self._color = color

    def set_size(self, size: Size):
        self._size = size

    def set_pos(self, position: wxPoint):
        self._pos = position

    def set_name(self, name: str):
        self._name = name

    def draw_by_dc(self, dc: Any):
        pass

    def intersect_by(self, point: wxPoint):
        pass

    def get_scaled_pos(self) -> wxPoint:
        return self._pos

    def get_scaled_size(self) -> Size:
        return self._size


class CharImage(Shape):
    def __init__(self):
        super().__init__()
        self._name = "Char"
        self._path = "/home/bug0r/dev/python/rapid_maps/test/examplemaps/woman.png"
        self._orig_image = wx.Image(self._path, wx.BITMAP_TYPE_ANY)
        self._image = self._orig_image.Copy()
        self._bitmap = self._image.ConvertToBitmap()
        self._size = self._bitmap.GetSize()

    def draw_by_dc(self, dc: Any):
        pos = self.get_scaled_pos()
        size = self.get_scaled_size()
        imagechanged = False
        rotimg = None

        if size != self._bitmap.GetSize():
            self._image = self._orig_image.Scale(size.width, size.height)
            self._angle_changed = True
            imagechanged = True

        if self._angle_changed:
            rotimg = self._image.Rotate(self._angle * 0.017453293, wxPoint(size.x * 0.5, size.y * 0.5))
            self._angle_changed = False
            imagechanged = True

        if imagechanged:
            usedimg = rotimg if rotimg else self._image
            self._bitmap = usedimg.ConvertToBitmap()

        font = dc.GetFont()
        font.SetPointSize(self._text_size )
        dc.SetFont(font)
        txtw, txth = dc.GetTextExtent(self._name)
        dc.DrawRoundedRectangle(pos.x, pos.y - (txth+6), txtw+6, txth+5, 2)
        dc.DrawText(self._name, pos.x+3, pos.y - txth-2)
        dc.DrawBitmap(self._bitmap, pos.x, pos.y)


    def intersect_by(self, point: wxPoint):
        pos = self.get_scaled_pos()
        size = self.get_scaled_size()
        return pos.x <= point.x <= (pos.x + size.x) and pos.y <= point.y <= (pos.y + size.y)


class Point(Shape):
    def __init__(self):
        super().__init__()

    def draw_by_dc(self, dc: Any):
        dc.DrawPoint(self._pos)

    def intersect_by(self, point: wxPoint):
        return self._pos == point


class Circle(Shape):
    def __init__(self):
        super().__init__()
        self._name = "Circle"

    def draw_by_dc(self, dc: Any):
        pos = self.get_scaled_pos()
        size = self.get_scaled_size()
        dc.DrawText(self._name, pos.x-size.x, pos.y-(size.y+15))
        dc.SetBrush(Brush(self._color))
        dc.DrawCircle(pos, size.x)

    def intersect_by(self, point: wxPoint):
        pos = self.get_scaled_pos()
        size = self.get_scaled_size()
        return (pos.x-size.x) <= point.x <= (pos.x + size.x) and (pos.y-size.y) <= point.y <= (pos.y + size.y)


class Quad(Shape):
    def __init__(self):
        super().__init__()
        self._name = "Quadrat"

    def draw_by_dc(self, dc: Any):
        pos = self.get_scaled_pos()
        size = self.get_scaled_size()
        dc.DrawText(self._name, pos.x, pos.y - 20)
        dc.SetBrush(Brush(self._color))
        dc.DrawRectangle(pt=pos, sz=size)

    def intersect_by(self, point: wxPoint):
        pos = self.get_scaled_pos()
        size = self.get_scaled_size()
        return pos.x <= point.x <= (pos.x + size.x) and pos.y <= point.y <= (pos.y + size.y)


class Triangle(Shape):
    def __init__(self):
        super().__init__()
        self._name = "Triangle"

    def draw_by_dc(self, dc: Any):
        print(f"Triangle: {self._pos}")

    def intersect_by(self, point: wxPoint):
        return self._pos.x <= point.x <= (self._pos.x + 20) and self._pos.y <= point.y <= (self._pos.y + 20)


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

    def OnActionChange(self, event):
        # event.Skip()
        self.__sel_action = event.Selection
        self.m_shapes.Enable(enable=self.should_add_entity())

    def OnShapeChange(self, event):
        event.Skip()

    def OnMouseLeftDown(self, event):
        self.__sel_shape_point = event.Position
        self.__edit_enabled(False)
        for shape in self.__shape_obj:
            if shape.intersect_by(self.__sel_shape_point):
                self.__sel_shape = shape
                self.__last_sel_shape = shape
                self.__edit_enabled(True)
                self.__set_edit_by(shape)
                self.__last_move_pt = self.__sel_shape_point

    def OnMouseMotion(self, event):
        if self.__sel_shape and isinstance(self.__sel_shape, Shape):
            newpos = self.__sel_shape.get_pos() + (event.Position - self.__last_move_pt)
            self.__sel_shape.set_pos(newpos)
            self.__last_move_pt = event.Position
            self.canvas.Refresh()

    def OnMouseLeftUp(self, event):
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

    def OnPaint(self, event):
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

    def OnCanvasSize(self, event):
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
        if self.__last_sel_shape:
            self.__shape_obj.remove(self.__last_sel_shape)
            self.__last_sel_shape = None
            self.__edit_enabled(False)
            self.canvas.Refresh()

    def OnNameChanged(self, event):
        if self.__last_sel_shape:
            self.__last_sel_shape.set_name(event.String)
            self.canvas.Refresh()

    def OnSizeChanged(self, event):
        if self.__last_sel_shape:
            self.__last_sel_shape.set_size(Size(event.Int, event.Int))
            self.canvas.Refresh()

    def OnTextSizeChanged(self, event):
        if self.__last_sel_shape:
            self.__last_sel_shape.set_text_size(event.Int)
            self.canvas.Refresh()

    def OnRotationChanged(self, event):
        if self.__last_sel_shape:
            self.__last_sel_shape.set_angle(event.Int)
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
