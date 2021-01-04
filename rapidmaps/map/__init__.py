from typing import Union

import wx

from rapidmaps.map.selection import Selections
from rapidmaps.map.state import MapStateTranslator, MapState, MapStateType
from rapidmaps.map.shape import *
from rapidmaps.map.shape_lib import ShapeLibraryLoader, ShapeLibrary


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


class ScrollbarParameter(object):
    def __init__(self):
        self._pos = 0
        self._thumbsize = 0
        self._maxpos = 0
        self._page_size = 0

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos

    @property
    def thumb_size(self):
        return self._thumbsize

    @thumb_size.setter
    def thumb_size(self, thumbsize):
        self._thumbsize = thumbsize

    @property
    def max_pos(self):
        return self._maxpos

    @max_pos.setter
    def max_pos(self, maxpos):
        self._maxpos = maxpos

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        self._page_size = page_size


class ScrollbarDimensions(object):
    def __init__(self, horizontal=None, vertical=None):
        self._vertical = vertical if vertical else ScrollbarParameter()
        self._horizontal = horizontal if horizontal else ScrollbarParameter()

    @property
    def vertical(self):
        return self._vertical

    @property
    def horizontal(self):
        return self._horizontal

    @vertical.setter
    def vertical(self, vertical=None):
        self._vertical = vertical if vertical else ScrollbarParameter()

    @horizontal.setter
    def horizontal(self, horizontal=None):
        self._horizontal = horizontal if horizontal else ScrollbarParameter()


class RapidMap(object):

    def __init__(self, canvas: wx.Panel, appconf):
        self._appconf = appconf
        self.__shape_clz = [Point, Quad, Circle, CharImage, ImageQuad, ImageCircle]
        self._shape_lib = ShapeLibraryLoader(appconf.shape_path).to_lib()
        self._selections = Selections()
        self.__sel_shape = None
        # new parts
        self._ms = MapState()
        self._mst = MapStateTranslator(self._ms, self._selections)
        self.__shape_obj = []
        self._canvas = canvas
        self._bg_bitmap = None
        self._bg_image = None
        self._view = MapView()
        self._normalized = wx.Rect(self._view.viewport.base)
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
        self._scrollbar = ScrollbarDimensions()

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
    def view(self) -> wx.Rect:
        return self._view

    @property
    def shape_lib(self) -> ShapeLibrary:
        return self._shape_lib

    def _refresh_view_state(self):
        self._view.refresh_zoomed_vport()
        zoomedview = self._view.viewport.zoomed
        self._normalized = wx.Rect(zoomedview.x, zoomedview.y,
                                 min(self._bg_image.GetSize().width if self._bg_bitmap else self._view.rsize.width,
                                     zoomedview.width),
                                 min(self._bg_image.GetSize().height if self._bg_bitmap else self._view.rsize.height,
                                     zoomedview.height))
        self._should_scale_up = (zoomedview.width < self._canvas.GetSize().width,
                                 zoomedview.height < self._canvas.GetSize().height)

    def set_background(self, image: wx.Image):
        if image:
            self._bg_image = image
            self._bg_bitmap = self._bg_image.ConvertToBitmap()
            self._view.vsize = self._bg_image.GetSize()
            self._view.viewport.base.x = 0
            self._view.viewport.base.y = 0
            self._view.viewport.base.width = self._canvas.GetSize().width
            self._view.viewport.base.height = self._canvas.GetSize().height
            self._view.zoom.factor = 1.0
            self._canvas.Refresh()

    def _realign_viewport_on_overflow(self):
        ## If scroll position + normalized screen width overflows on zoom we have to recalculate and refresh
        if self._bg_bitmap:
            scrolloverx = self._bg_bitmap.GetSize().width - (self._normalized.x + self._normalized.width)
            scrolloverx = 0.0 if scrolloverx > 0 else scrolloverx

            scrollovery = self._bg_bitmap.GetSize().height - (self._normalized.y + self._normalized.height)
            scrollovery = 0.0 if scrollovery > 0 else scrollovery

            self._view.viewport.base.x += scrolloverx
            self._view.viewport.base.y += scrollovery

    def do_zoom(self, zoom_value: int):
        if self._bg_image:
            self._view.zoom.factor = float(zoom_value) / 100.0

            self._refresh_view_state()

            self._realign_viewport_on_overflow()

            self._canvas.Refresh()

    def do_resize_viewport(self, newsize: wx.Size):
        self._view.rsize = newsize
        self._view.viewport.base.width = newsize.width
        self._view.viewport.base.height = newsize.height
        self._refresh_view_state()
        self._realign_viewport_on_overflow()

    def _draw_background(self, dc):
        if self._bg_bitmap:

            scalew = self._canvas.GetSize().width if self._should_scale_up[0] \
                else self._normalized.width * self._view.zoom.factor

            scaleh = self._canvas.GetSize().height if self._should_scale_up[1] \
                else self._normalized.height * self._view.zoom.factor

            if not self._should_scale_up[0] or not self._should_scale_up[1]:
                dc.SetBackground(wx.BLACK_BRUSH)
                dc.Clear()

            subimg = self._bg_image.GetSubImage(self._normalized).Scale(scalew, scaleh)

            dc.DrawBitmap(subimg.ConvertToBitmap(), 0, 0)
        elif not self._bg_image:
            dc.SetBackground(wx.BLACK_BRUSH)
            dc.Clear()
            self._view.viewport.base.x = 0
            self._view.viewport.base.y = 0
            self._view.viewport.base.width = self._canvas.GetSize().width
            self._view.viewport.base.height = self._canvas.GetSize().height

    def _draw_objects(self, dc):
        for shape in self.__shape_obj:
            zoomedview = self._view.viewport.zoomed
            zoom = self._view.zoom.factor
            if shape.get_bbox().Intersects(zoomedview):
                if zoom > 0:
                    temppos = shape.get_pos()
                    tempsize = shape.get_size()
                    shape.set_pos(wx.Point((temppos.x - zoomedview.x) * zoom,
                                           (temppos.y - zoomedview.y) * zoom))
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
        self._refresh_view_state()
        self._draw_background(dc)
        self._draw_objects(dc)
        self._draw_selection_outline(dc)

    def single_select_at(self, x: int, y: int) -> Union[Shape, None]:
        anyselected = False
        for shape in self.__shape_obj:
            zoomedview = self._view.viewport.zoomed
            sel_pos = wx.Point(zoomedview.x + (x * self._view.zoom.reciprocal),
                               zoomedview.y + (y * self._view.zoom.reciprocal))

            if shape.intersect_by(sel_pos):
                self.__sel_shape = shape
                anyselected = True
                if self._mst.should_add_selection:
                    if self._selections.contains(shape):
                        self._selections.remove(shape)
                    else:
                        self._selections.add(shape)
                else:
                    self._selections.clear()
                    self._selections.add(shape)
            #if not self._selections.is_empty():
                #self.__edit_enabled(True)
                #self.__set_edit_by(shape)
        if not self._mst.should_add_selection and not anyselected:
            self._selections.clear()
        self._canvas.Refresh()
        return self.__sel_shape

    def area_selection_at(self, selected_area: wx.Rect):

        if selected_area.width < 0:
            selected_area.x = selected_area.x + selected_area.width
            selected_area.width = abs(selected_area.width)
        if selected_area.height < 0:
            selected_area.y = selected_area.y + selected_area.height
            selected_area.height = abs(selected_area.height)

        if selected_area.width > 0 and selected_area.height > 0:
            zoomedview = self._view.viewport.zoomed
            zoom = self._view.zoom.reciprocal
            selected_area.x = zoomedview.x + (selected_area.x * zoom)
            selected_area.y = zoomedview.y + (selected_area.y * zoom)
            selected_area.width *= zoom
            selected_area.height *= zoom

            for shape in self.__shape_obj:

                if selected_area.Contains(shape.get_bbox()):
                    self._selections.add(shape)
                elif self._mst.should_add_selection:
                    if not self._selections.contains(shape):
                        self._selections.remove(shape)
                else:
                    self._selections.remove(shape)

            self._canvas.Refresh()

    def add_shape(self, shape_type: int, pos_x: int, pos_y: int):
        new_obj = self.__shape_clz[shape_type]()
        zoomedview = self._view.viewport.zoomed
        zoom = self._view.zoom.reciprocal
        newpos = wx.Point(zoomedview.x + (pos_x * zoom),
                          zoomedview.y + (pos_y * zoom))

        new_obj.set_pos(position=newpos)

        self.__shape_obj.append(new_obj)
        self._canvas.Refresh()

    def move_selected_shapes(self):
        self._selections.action_on('add_to_pos', [self._mst.mouse_move_diff * self._view.zoom.reciprocal])
        self._canvas.Refresh()

    def get_update_scrollbar_dimensions(self) -> ScrollbarDimensions:
        self._scrollbar = ScrollbarDimensions()
        if self._bg_image:
            newvize = self._bg_image.GetSize()
            realsize = self._canvas.GetSize()

            self._scrollbar.horizontal.pos = self._view.viewport.base.x
            self._scrollbar.horizontal.thumb_size = realsize.width * self._view.zoom.reciprocal
            self._scrollbar.horizontal.max_pos = newvize.width
            self._scrollbar.horizontal.page_size = realsize.width
            self._scrollbar.vertical.pos = self._view.viewport.base.y
            self._scrollbar.vertical.thumb_size = realsize.height * self._view.zoom.reciprocal
            self._scrollbar.vertical.max_pos = newvize.height
            self._scrollbar.vertical.page_size = realsize.height
        else:
            width, height = self._canvas.GetSize().width, self._canvas.GetSize().height
            self._scrollbar.horizontal.max_pos = width
            self._scrollbar.horizontal.thumb_size = width
            self._scrollbar.horizontal.page_size = width
            self._scrollbar.vertical.max_pos = height
            self._scrollbar.vertical.thumb_size = height
            self._scrollbar.vertical.page_size = height

        return self._scrollbar
