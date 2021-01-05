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
        self._show_label = True

    def show_label(self, show: bool):
        self._show_label = show

    def get_bbox(self):
        return wx.Rect(self._pos, self._size)

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
            dc.SetPen(wx.GREEN_PEN)
            dc.SetBrush(wx.Brush(GREEN, wx.TRANSPARENT))
            dc.DrawRoundedRectangle(self._pos.x, self._pos.y, self._size.width, self._size.height, 5)
            dc.SetPen(oldpen)
            dc.SetBrush(oldbrush)

    def intersect_by(self, point: wxPoint):
        pass


class Circle(Shape):
    def __init__(self):
        super().__init__()
        self._name = "Circle"

    def draw_by_dc(self, dc: Any):
        dc.DrawText(self._name, self._pos.x - self._size.x, self._pos.y - (self._size.y+15))
        tBrush = dc.GetBrush()
        dc.SetBrush(Brush(self._color))
        dc.DrawCircle(self._pos, self._size.x)
        dc.SetBrush(tBrush)

        self._draw_outline(dc)

    def intersect_by(self, point: wxPoint):
        return (self._pos.x - self._size.x) <= point.x <= (self._pos.x + self._size.x) and \
               (self._pos.y - self._size.y) <= point.y <= (self._pos.y + self._size.y)


class Quad(Shape):
    def __init__(self):
        super().__init__()
        self._name = "Quadrat"

    def draw_by_dc(self, dc: Any):
        dc.DrawText(self._name, self._pos.x, self._pos.y - 20)
        tBrush = dc.GetBrush()
        dc.SetBrush(Brush(self._color))
        dc.DrawRectangle(pt=self._pos, sz=self._size)
        dc.SetBrush(tBrush)

        self._draw_outline(dc)

    def intersect_by(self, point: wxPoint):
        return self._pos.x <= point.x <= (self._pos.x + self._size.x) and \
               self._pos.y <= point.y <= (self._pos.y + self._size.y)


class Point(Shape):
    def __init__(self):
        super().__init__()

    def draw_by_dc(self, dc: Any):
        dc.DrawPoint(self._pos)

    def intersect_by(self, point: wxPoint):
        return self._pos == point


class ImageShape(Shape):

    def __init__(self, image: wx.Image = None):
        super().__init__()
        self._orig_image = image
        self._image = image
        self._bitmap = None

    def set_image(self, image: wx.Image):
        if not image or not isinstance(image, wx.Image):
            raise ValueError('image should and wx.Image and not None')
        self._orig_image = image
        self._image = self._orig_image.Copy()
        self._bitmap = self._image.ConvertToBitmap()
        self._size = self._bitmap.GetSize()

    def draw_by_dc(self, dc: Any):
        if self._bitmap:
            imagechanged = False
            rotimg = None

            if self._size != self._bitmap.GetSize():
                self._image = self._orig_image.Scale(1 if self._size.width < 1 else self._size.width,
                                                     1 if self._size.height < 1 else self._size.height)
                self._angle_changed = True
                imagechanged = True

            if self._angle_changed:
                rotimg = self._image.Rotate(self._angle * 0.017453293,
                                            wxPoint(self._size.x * 0.5, self._size.y * 0.5))
                self._angle_changed = False
                imagechanged = True

            if imagechanged:
                usedimg = rotimg if rotimg else self._image
                self._bitmap = usedimg.ConvertToBitmap()
                self._size = self._bitmap.GetSize()

            if self._show_label:
                font = dc.GetFont()
                font.SetPointSize(self._text_size)
                dc.SetFont(font)
                txtw, txth = dc.GetTextExtent(self._name)
                dc.DrawRoundedRectangle(self._pos.x, self._pos.y - (txth+6), txtw+6, txth+5, 2)
                dc.DrawText(self._name, self._pos.x+3, self._pos.y - txth-2)
            dc.DrawBitmap(self._bitmap, self._pos.x, self._pos.y)

            self._draw_outline(dc)

    def intersect_by(self, point: wxPoint):
        return self._pos.x <= point.x <= (self._pos.x + self._size.width) and \
               self._pos.y <= point.y <= (self._pos.y + self._size.height)


class CharImage(ImageShape):
    def __init__(self):
        super().__init__()
        self._name = "Char"
        self.set_image(wx.Image("./test/examplemaps/woman.png", wx.BITMAP_TYPE_ANY))


class ImageCircle(ImageShape):
    def __init__(self):
        super().__init__()
        self._size = wx.Size(23, 23)
        self._name = "ImageCircle"
        self._create_circle()
        self._changed = False

    def _create_circle(self):
        bitmap = wx.Bitmap.FromRGBA(1 if self._size.width < 1 else self._size.width,
                                    1 if self._size.height < 1 else self._size.height)
        dc = wx.MemoryDC(bitmap)
        dc.SetBrush(Brush(super().get_color()))
        dc.DrawCircle((wx.Point() + self._size*0.5) - wx.Point(1,1), (self._size.width*0.5)-1)
        self._angle_changed = True
        self.set_image(bitmap.ConvertToImage())

    def draw_by_dc(self, dc: Any):
        self._create_circle()
        super().draw_by_dc(dc)


class ImageQuad(ImageShape):
    def __init__(self):
        super().__init__()
        self._name = "ImageQuad"
        self._create_quad()

    def _create_quad(self):
        bitmap = wx.Bitmap.FromRGBA(1 if self._size.width < 1 else self._size.width,
                                    1 if self._size.height < 1 else self._size.height)
        dc = wx.MemoryDC(bitmap)
        dc.SetBrush(Brush(super().get_color()))
        dc.DrawRectangle(pt=wx.Point(), sz=self._size)
        self._angle_changed = True
        self.set_image(bitmap.ConvertToImage())

    def draw_by_dc(self, dc: Any):
        self._create_quad()
        super().draw_by_dc(dc)

