import wx


class MapZoom(object):

    def __init__(self):
        self._factor = 1.0
        self._factor_reciprocal = 1.0

    @property
    def factor(self):
        return self._factor

    @factor.setter
    def factor(self, newfactor: float):
        self._factor = newfactor
        self._factor_reciprocal = 1.0 / newfactor

    @property
    def reciprocal(self):
        return self._factor_reciprocal


class MapViewport(object):

    def __init__(self):
        self._base = wx.Rect()
        self._zoomed = wx.Rect()

    @property
    def base(self):
        return self._base

    @property
    def zoomed(self):
        return self._zoomed

    @zoomed.setter
    def zoomed(self, zoomed: wx.Rect):
        self._zoomed = zoomed


class MapView(object):
    def __init__(self):
        self._vsize = wx.Size()         #virtual map Size
        self._rsize = wx.Size()         #real map Size
        self._viewport = MapViewport()  #current map viewport
        self._zoom = MapZoom()          #

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
        return self._viewport

    @viewport.setter
    def viewport(self, viewport: wx.Rect):
        self._viewport = viewport

    @property
    def zoom(self):
        return self._zoom

    def refresh_zoomed_vport(self):
        self._viewport.zoomed = wx.Rect(self._viewport.base)
        self._viewport.zoomed.width *= self._zoom.reciprocal
        self._viewport.zoomed.height *= self._zoom.reciprocal
