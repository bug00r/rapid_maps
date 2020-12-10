from typing import Union

import wx

from rapidmaps.map.selection import Selections
from rapidmaps.map.state import MapStateTranslator, MapState, MapStateType
from rapidmaps.map.shape import *


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

    def __init__(self, canvas: wx.Panel):
        self.__shape_clz = [Point, Quad, Circle, CharImage, ImageQuad, ImageCircle]
        self._selections = Selections()
        self.__sel_shape = None
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

    def _refresh_view_state(self):
        self._zoomedview = wx.Rect(self._view.viewport) 
        self._zoomedview.width *= self._zoom[1]
        self._zoomedview.height *= self._zoom[1]
        self._normalized = wx.Rect(self._zoomedview.x, self._zoomedview.y,
                                 min(self._bg_image.GetSize().width if self._bg_bitmap else self._view.rsize.width,
                                     self._zoomedview.width),
                                 min(self._bg_image.GetSize().height if self._bg_bitmap else self._view.rsize.height,
                                     self._zoomedview.height))
        self._should_scale_up = (self._zoomedview.width < self._canvas.GetSize().width,
                                 self._zoomedview.height < self._canvas.GetSize().height)
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

    def _realign_viewport_on_overflow(self):
        ## If scroll position + normalized screen width overflows on zoom we have to recalculate and refresh
        scrolloverx = self._bg_bitmap.GetSize().width - (self._normalized.x + self._normalized.width)
        scrolloverx = 0.0 if scrolloverx > 0 else scrolloverx

        scrollovery = self._bg_bitmap.GetSize().height - (self._normalized.y + self._normalized.height)
        scrollovery = 0.0 if scrollovery > 0 else scrollovery

        self._view.viewport.x += scrolloverx
        self._view.viewport.y += scrollovery

    def do_zoom(self, zoom_value: int):
        if self._bg_image:
            zoom_factor = float(zoom_value) / 100.0
            self._zoom = (zoom_factor, 1.0 / zoom_factor)

            self._refresh_view_state()

            self._realign_viewport_on_overflow()

            self._canvas.Refresh()

    def do_resize_viewport(self, newsize: wx.Size):
        self._view.rsize = newsize
        self._view.viewport.width = newsize.width
        self._view.viewport.height = newsize.height
        self._refresh_view_state()
        self._realign_viewport_on_overflow()

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
        self._refresh_view_state()
        self._draw_background(dc)
        self._draw_objects(dc)
        self._draw_selection_outline(dc)

    def single_select_at(self, x: int, y: int) -> Union[Shape, None]:
        anyselected = False
        for shape in self.__shape_obj:

            zoom = self._map_zoom_factor if self._should_scale_up[0] else self._object_zoom_factor

            sel_pos = wx.Point(self._zoomedview.x + (x * zoom), self._zoomedview.y + (y * zoom))

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

            zoom = self._map_zoom_factor if self._should_scale_up[0] else self._object_zoom_factor

            selected_area.x = self._zoomedview.x + (selected_area.x * zoom)
            selected_area.y = self._zoomedview.y + (selected_area.y * zoom)
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

        zoom = self._map_zoom_factor if self._should_scale_up[0] else self._object_zoom_factor

        newpos = wx.Point(self._zoomedview.x + (pos_x * zoom), self._zoomedview.y + (pos_y * zoom))

        new_obj.set_pos(position=newpos)

        self.__shape_obj.append(new_obj)
        self._canvas.Refresh()

    def move_selected_shapes(self):
        zoom = self._map_zoom_factor if self._should_scale_up[0] else self._object_zoom_factor
        self._selections.action_on('add_to_pos', [self._mst.mouse_move_diff * zoom])
        self._canvas.Refresh()

    def get_update_scrollbar_dimensions(self) -> ScrollbarDimensions:
        self._scrollbar = ScrollbarDimensions()
        if self._bg_image:
            newvize = self._bg_image.GetSize()
            realsize = self._canvas.GetSize()

            zoom = self._map_zoom_factor if self._should_scale_up[0] else self._object_zoom_factor

            self._scrollbar.horizontal.pos = self._view.viewport.x
            self._scrollbar.horizontal.thumb_size = realsize.width * zoom
            self._scrollbar.horizontal.max_pos = newvize.width
            self._scrollbar.horizontal.page_size = realsize.width
            self._scrollbar.vertical.pos = self._view.viewport.y
            self._scrollbar.vertical.thumb_size = realsize.height * zoom
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
