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

    def get_color(self):
        return self._color

    def get_size(self):
        return self._size

    def get_name(self):
        return self._name

    def get_pos(self):
        return self._pos

    def set_color(self, color: Colour):
        self._color = color

    def set_size(self, size: Size):
        self._size = size

    def set_name(self, name: str):
        self._name = name

    def set_position(self, position: wxPoint):
        self._pos = position

    def draw_by_dc(self, dc: Any):
        pass

    def intersect_by(self, point: wxPoint):
        pass


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
        self._name = "Kreis"

    def draw_by_dc(self, dc: Any):
        dc.DrawText(self._name, self._pos.x-self._size.x, self._pos.y-(self._size.y+15))
        dc.SetBrush(Brush(self._color))
        dc.DrawCircle(self._pos, self._size.x)

    def intersect_by(self, point: wxPoint):
        return (self._pos.x-self._size.x) <= point.x <= (self._pos.x + self._size.x) and (self._pos.y-self._size.y) <= point.y <= (self._pos.y + self._size.y)


class Quad(Shape):
    def __init__(self):
        super().__init__()
        self._name = "Quadrat"

    def draw_by_dc(self, dc: Any):
        dc.DrawText(self._name, self._pos.x, self._pos.y - 20)
        dc.SetBrush(Brush(self._color))
        dc.DrawRectangle(pt=self._pos, sz=self._size)

    def intersect_by(self, point: wxPoint):
        return self._pos.x <= point.x <= (self._pos.x + self._size.x) and self._pos.y <= point.y <= (self._pos.y + self._size.y)


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
        self.__shape_clz = [Point, Quad, Circle, Triangle]
        self.__shape_obj = []
        self.__sel_action = 0
        self.__lm_release = None
        self.__sel_shape = None
        self.__bg_image = None
        self.__bg_bitmap = None
        self.__bg_isnew = False
        self.__sel_shape = None
        self.__last_sel_shape = None
        self.__sel_shape_point = None
        self.__last_move_pt = None
        self.__scaled_image = None

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
            self.__sel_shape.set_position(self.__sel_shape.get_pos() + (event.Position-self.__last_move_pt))
            self.__last_move_pt = event.Position
            self.canvas.Refresh()

    def OnMouseLeftUp(self, event):
        if self.should_add_entity():
            self.__lm_release = event.Position
            self.__sel_shape = self.m_shapes.Selection
            new_obj = self.__shape_clz[self.__sel_shape]()
            new_obj.set_position(position=self.__lm_release)
            self.__shape_obj.append(new_obj)
            print(f"x: {self.__lm_release[0]} y: {self.__lm_release[1]} shape: {self.__sel_shape}")
            self.canvas.Refresh()
        else:
            self.__sel_shape = None
            self.__sel_shape_point = None

    def OnPaint(self, event):
        dc = abDC(self.canvas)
        if self.__bg_bitmap:
            dc.DrawBitmap(self.__bg_bitmap, 0, 0)
            self.__bg_isnew = False
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
                        self.__bg_isnew = True
                        self.canvas.SetSize(self.__bg_image.GetSize())
                        self.canvas.Refresh()
                        #self.m_scrolled_map.SetVirtualSize(self.__bg_image.GetSize())
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
            self.m_scrolled_map.SetVirtualSize(size)

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

    def OnColourChanged(self, event):
        if self.__last_sel_shape:
            self.__last_sel_shape.set_color(event.Colour)
            self.canvas.Refresh()

    def __edit_enabled(self, enabled: bool):
        self.m_name.Enable(enabled)
        self.m_size.Enable(enabled)
        self.m_colour.Enable(enabled)

    def __set_edit_by(self, shape: Shape):
        self.m_name.SetValue(shape.get_name())
        self.m_size.SetValue(shape.get_size().x)
        self.m_colour.SetColour(shape.get_color())

    def OnMapZoom(self, event):
        if self.__bg_image and self.__bg_image:
            viewx, viewy = self.m_scrolled_map.GetViewStart()
            scalefactor = 1.0 + (float(event.Int) / 100.0)
            self.__scaled_image = self.__bg_image.Scale(self.__bg_image.Width*scalefactor, self.__bg_image.Height*scalefactor)
            self.__bg_bitmap = self.__scaled_image.ConvertToBitmap()
            print(f"old size: {self.__bg_image.GetSize()} new Size {self.__scaled_image.GetSize()} scale factorr: {scalefactor}")
            print(f"tg {self.m_scrolled_map.GetTargetRect()}")
            self.canvas.SetSize(self.__scaled_image.GetSize())
            self.canvas.Refresh()
            self.m_scrolled_map.SetVirtualSize(self.__scaled_image.GetSize())
            self.m_scrolled_map.Scroll(viewx+(self.m_scrolled_map.GetSize().x/2), viewy+(self.m_scrolled_map.GetSize().y/2))
