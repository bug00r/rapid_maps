import wx

from rapidmaps.map.selection import Selections
from rapidmaps.map.state import MapStateTranslator, MapState, MapStateType


class MapView(object):
    def __init__(self):
        self._vsize = wx.Size()     #virtual map Size
        self._rsize = wx.Size()     #real map Size
        self._view = wx.Rect()      #current map viewport

    @property
    def rsize(self) -> wx.Size:
        return self._rsize

    @rsize.setter
    def rsize(self, rsize: wx.Size):
        self._rsize = rsize

    @property
    def vsize(self) -> wx.Size:
        return self._vsize

    @vsize.setter
    def vsize(self, vsize: wx.Size):
        self._vsize = vsize

    @property
    def viewport(self) -> wx.Rect:
        return self._view

    @viewport.setter
    def viewport(self, viewport: wx.Rect):
        self._view = viewport


class RapidMap(object):

    def __init__(self, canvas: wx.Panel):
        self._selections = Selections()
        # new parts
        self._ms = MapState()
        self._mst = MapStateTranslator(self._ms, self._selections)
        self.__shape_obj = []
        self._canvas = canvas
        self._bg_bitmap = None
        self._bg_image = None
        self._zoom = (1.0, 1.0)    # zoom factor and 1./scale (for mul)
        self._view = MapView()
        self._zoomedview = wx.Rect(self._view.viewport)
        self._normalized = wx.Rect(self._view.viewport)  
        self._object_zoom_factor = self._zoom[0]
        self._map_zoom_factor = self._zoom[1]
        self._should_scale_up = (False, False)
        self._ms.set(MapStateType.MOVING_MODE_UI, True)
        self._ms.set(MapStateType.SELECTION_MODE_UI, False)
        self._ms.set(MapStateType.ADDITION_MODE_UI, False)
        self._ms.set(MapStateType.SELECTION_IS_MOVING, False)
        self._ms.set(MapStateType.KB_CTRL, wx.wxEVT_KEY_UP)
        self._ms.set(MapStateType.KB_SHIFT, wx.wxEVT_KEY_UP)
        self._ms.set(MapStateType.KB_ALT, wx.wxEVT_KEY_UP)
        self._ms.set(MapStateType.MOUSE_LEFT, wx.wxEVT_LEFT_UP)
        self._ms.set(MapStateType.MOUSE_LEFT_POS, wx.Point(-1, -1))
        self._ms.set(MapStateType.MOUSE_LEFT_RELEASE_POS, wx.Point(-1, -1))

    @property
    def map_objects(self):
        return self.__shape_obj

    @property
    def mapstate(self) -> MapState:
        return self._ms

    @property
    def mapstatetranslator(self) -> MapStateTranslator:
        return self._mst

    @property
    def selections(self) -> Selections:
        return self._selections

    @property
    def bg_bitmap(self):
        return self._bg_bitmap

    @bg_bitmap.setter
    def bg_bitmap(self, bg_bitmap: wx.Image):
        self._bg_bitmap = bg_bitmap

    @property
    def bg_image(self):
        return self._bg_image

    @bg_image.setter
    def bg_image(self, new_bg_image: wx.Image):
        self._bg_image = new_bg_image

    @property
    def normalized(self):
        return self._normalized

    @property
    def should_scale_up(self):
        return self._should_scale_up
    
    @property
    def object_zoom_factor(self):
        return self._object_zoom_factor

    @property
    def map_zoom_factor(self):
        return self._map_zoom_factor

    @property
    def view(self) -> wx.Rect:
        return self._view

    @property
    def zoom(self):
        return self._zoom

    @property
    def zoomedview(self):
        return self._zoomedview

    @zoom.setter
    def zoom(self, zoom: tuple):
        self._zoom = zoom

    def refresh_view_state(self):
        self._zoomedview = wx.Rect(self._view.viewport) 
        self._zoomedview.width *= self._zoom[1]
        self._zoomedview.height *= self._zoom[1]
        self._normalized = wx.Rect(self._view.viewport.x, self._view.viewport.y,
                                 min(self._bg_image.GetSize().width if self._bg_bitmap else self._view.rsize.width,
                                     self._zoomedview.width),
                                 min(self._bg_image.GetSize().height if self._bg_bitmap else self._view.rsize.height,
                                     self._zoomedview.height))
        self._should_scale_up = (self._zoomedview.width == self._normalized.width, self._zoomedview.height == self._normalized.height)
        self._object_zoom_factor = self._zoom[0] if self._should_scale_up[0] else self._zoom[1]
        self._map_zoom_factor = self._zoom[1] if self._should_scale_up[0] else self._zoom[0]

    def set_background(self, image: wx.Image):
        if image:
            self._bg_image = image
            self._bg_bitmap = self._bg_image.ConvertToBitmap()
            self._view.vsize = self._bg_image.GetSize()
            self._view.viewport.x = 0
            self._view.viewport.y = 0
            self._view.viewport.width = self._canvas.GetSize().width
            self._view.viewport.height = self._canvas.GetSize().height
            self._zoom = (1.0, 1.0)
            self._canvas.Refresh()

    def do_zoom(self, zoom_value: int):
        if self._bg_image:
            zoom_factor = float(zoom_value) / 100.0
            self._zoom = (zoom_factor, 1.0 / zoom_factor)

            self.refresh_view_state()

            ## If scroll position + normalized screen width overflows on zoom we have to recalculate and refresh
            scrolloverx = self._bg_bitmap.GetSize().width - (self._normalized.x + self._normalized.width)
            scrolloverx = 0.0 if scrolloverx > 0 else scrolloverx

            scrollovery = self._bg_bitmap.GetSize().height - (self._normalized.y + self._normalized.height)
            scrollovery = 0.0 if scrollovery > 0 else scrollovery

            self._view.viewport.x += scrolloverx
            self._view.viewport.y += scrollovery

            self._canvas.Refresh()

    def _draw_background(self, dc):
        if self._bg_bitmap:

            scalew = self._canvas.GetSize().width if self._should_scale_up[0] \
                else self._normalized.width * self._map_zoom_factor
            scaleh = self._canvas.GetSize().height if self._should_scale_up[1] \
                else self._normalized.height * self._map_zoom_factor

            if not self._should_scale_up[0] or not self._should_scale_up[1]:
                dc.SetBackground(wx.BLACK_BRUSH)
                dc.Clear()

            subimg = self._bg_image.GetSubImage(self._normalized).Scale(scalew, scaleh)

            dc.DrawBitmap(subimg.ConvertToBitmap(), 0, 0)
        elif not self._bg_image:
            dc.SetBackground(wx.BLACK_BRUSH)
            dc.Clear()
            self._view.viewport.x = 0
            self._view.viewport.y = 0
            self._view.viewport.width = self._canvas.GetSize().width
            self._view.viewport.height = self._canvas.GetSize().height

    def _draw_objects(self, dc):
        for shape in self.__shape_obj:
            if shape.get_bbox().Intersects(self._zoomedview):
                if self._object_zoom_factor > 0:
                    temppos = shape.get_pos()
                    tempsize = shape.get_size()
                    zoom = self._object_zoom_factor if self._should_scale_up[0] else self._map_zoom_factor
                    shape.set_pos(wx.Point((temppos.x - self._zoomedview.x) * zoom,
                                           (temppos.y - self._zoomedview.y) * zoom))
                    shape.set_size(wx.Size(tempsize.width * zoom,
                                           tempsize.height * zoom))

                    shape.draw_by_dc(dc)
                    shape.set_pos(temppos)
                    shape.set_size(tempsize)

    def _draw_selection_outline(self, dc):
        if self._mst.is_selection_area_active:
            oldpen = dc.GetPen()
            oldbrush = dc.GetBrush()
            dc.SetPen(wx.GREEN_PEN)
            dc.SetBrush(wx.Brush(wx.GREEN, wx.TRANSPARENT))
            dc.DrawRectangle(self._mst.current_selected_area)
            dc.SetPen(oldpen)
            dc.SetBrush(oldbrush)

    def update(self, dc: wx.DC):
        self.refresh_view_state()
        self._draw_background(dc)
        self._draw_objects(dc)
        self._draw_selection_outline(dc)
