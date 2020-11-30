import wx
from wx import Point as wxPoint
from wx import Size, Brush, Colour, BLACK, GREEN
from typing import Any


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
        self._selected = False

    def set_selected(self, selected: bool):
        self._selected = selected

    def get_selected(self):
        return self._selected

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

    def add_to_pos(self, delta: wxPoint):
        self._pos += delta

    def set_name(self, name: str):
        self._name = name

    def draw_by_dc(self, dc: Any):
        pass

    def _draw_outline(self, dc: Any):
        if self._selected:
            oldpen = dc.GetPen()
            oldbrush = dc.GetBrush()
            dc.SetPen(wx.Pen(GREEN, 2))
            dc.SetBrush(wx.Brush(GREEN, wx.TRANSPARENT))
            dc.DrawRoundedRectangle(self._pos.x, self._pos.y, self._size.width, self._size.height, 5)
            dc.SetPen(oldpen)
            dc.SetBrush(oldbrush)

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
        self._path = "./../test/examplemaps/woman.png"
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

        self._draw_outline(dc)

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
