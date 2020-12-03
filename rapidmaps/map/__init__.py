import wx


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

    def __init__(self):
        self._bg_bitmap = None
        self._bg_image = None
        self._zoom = (1.0, 1.0)    # zoom factor and 1./scale (for mul)
        self._view = MapView()
        self._zoomedview = wx.Rect(self._view.viewport)
        self._normalized = wx.Rect(self._view.viewport)  
        self._object_zoom_factor = self._zoom[0]
        self._map_zoom_factor = self._zoom[1]
        self._should_scale_up = (False, False)

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
