from rapidmaps.mapui.wxui.generated.rapidmap import MainFrame
from typing import Any
import wx
from wx import Point as wxPoint
from wx import AutoBufferedPaintDC as abDC
from wx import Size, BG_STYLE_PAINT, Brush, Colour, Exit


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
        self.m_scrolled_map.SetAutoLayout(True)
        self.__shape_clz = [Point, Quad, Circle, Triangle]
        self.__shape_obj = []
        self.__sel_action = 0
        self.__lm_release = None
        self.__sel_shape = None
        self.__bg_image = None
        self.__bg_isnew = False

    def OnActionChange(self, event):
        # event.Skip()
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
            new_obj.set_position(position=self.__lm_release)
            self.__shape_obj.append(new_obj)
            print(f"x: {self.__lm_release[0]} y: {self.__lm_release[1]} shape: {self.__sel_shape}")
            self.canvas.Refresh()

    def OnMouseMotion(self, event):
        event.Skip()

    def OnPaint(self, event):
        dc = abDC(self.canvas)
        if self.__bg_image:
            print("draw bg")
            dc.DrawBitmap(self.__bg_image.ConvertToBitmap(), 0, 0)
            self.__bg_isnew = False
            self.m_scrolled_map.Layout()
            #self.canvas.Refresh()
        elif not self.__bg_image:
            print("draw bg color")
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
                    pathname = fileDialog.GetPath()
                    try:
                        self.__bg_image = wx.Image(pathname, wx.BITMAP_TYPE_ANY)
                        self.__bg_isnew = True
                        self.canvas.SetSize(self.__bg_image.GetSize())
                        self.canvas.Refresh()
                        self.m_scrolled_map.SetVirtualSize(self.__bg_image.GetSize())
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
        if self.__bg_image:
            self.m_scrolled_map.SetVirtualSize(self.__bg_image.GetSize())
