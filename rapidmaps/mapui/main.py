from rapidmaps.mapui.wxui.generated.rapidmap import MainFrame
from typing import Any
from wx import Point as wxPoint
from wx import AutoBufferedPaintDC as abDC
from wx import Size, BG_STYLE_PAINT, Brush, Colour, BG_STYLE_COLOUR

class Shape(object):

    def __init__(self):
        self._pos = wxPoint(0, 0)

    def set_position(self, position: wxPoint):
        self._pos = position

    def draw_by_dc(self, dc: Any):
        pass


class Point(Shape):
    def __init__(self):
        super().__init__()

    def draw_by_dc(self, dc: Any):
        dc.DrawPoint(self._pos)
        print(f"Point: {self._pos}")


class Circle(Shape):
    def __init__(self):
        super().__init__()

    def draw_by_dc(self, dc: Any):
        dc.DrawCircle(self._pos, 5)
        print(f"Circle: {self._pos}")


class Quad(Shape):
    def __init__(self):
        super().__init__()

    def draw_by_dc(self, dc: Any):
        dc.DrawRectangle(pt=self._pos, sz=Size(20, 20))
        print(f"Quad: {self._pos}")


class Triangle(Shape):
    def __init__(self):
        super().__init__()

    def draw_by_dc(self, dc: Any):
        print(f"Triangle: {self._pos}")


class RapidMapFrame(MainFrame):

    def __init__(self):
        super().__init__(None)
        self.canvas.SetBackgroundStyle(BG_STYLE_PAINT)
        self.__shape_clz = [Point, Quad, Circle, Triangle]
        self.__shape_obj = []
        self.__sel_action = 0
        self.__lm_release = None
        self.__sel_shape = None

    def OnActionChange(self, event):
        #event.Skip()
        self.__sel_action = event.Selection
        self.m_shapes.Enable(enable=self.should_add_entity())

    def OnShapeChange(self, event):
        event.Skip()

    def OnMouseLeftDown(self, event):
        event.Skip()

    def OnMouseLeftUp(self, event):
        if self.should_add_entity():
            self.__lm_release = event.Position
            self.__sel_shape = self.m_shapes.Selection
            new_obj = self.__shape_clz[self.__sel_shape]()
            new_obj.set_position(position=self.__lm_release )
            self.__shape_obj.append(new_obj)
            print(f"x: {self.__lm_release[0]} y: {self.__lm_release[1]} shape: {self.__sel_shape}")
            self.canvas.Refresh()

    def OnMouseMotion(self, event):
        event.Skip()

    def OnPaint(self, event):
        dc = abDC(self.canvas)
        dc.SetBackground(Brush(Colour(255, 255, 255)))
        for shape in self.__shape_obj:
            shape.draw_by_dc(dc)

    def should_add_entity(self):
        return self.__sel_action == 1
