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
        self._zoom = (1.0, 1.0)    # zoom factor and 1./scale (for mul)
        self._view = MapView()

    @property
    def view(self) -> wx.Rect:
        return self._view

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, zoom: tuple):
        self._zoom = zoom

