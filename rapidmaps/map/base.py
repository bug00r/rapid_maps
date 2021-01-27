from typing import Union
from pathlib import Path

from rapidmaps.map.selection import Selections
from rapidmaps.map.state import MapStateTranslator, MapState, MapStateType
from rapidmaps.map.shape import *
from rapidmaps.map.shape_lib import ShapeLibraryLoader, ShapeLibrary, ShapeFactory, ShapeNotExistException
from rapidmaps.map.scrolling import ScrollbarDimensions, ScrollbarParameter
from rapidmaps.map.view import MapView, MapViewport, MapZoom
from rapidmaps.map.object import MapObject


class RapidMap(object):

    def __init__(self, canvas: wx.Panel, appconf):
        self._appconf = appconf
        self._shape_lib = ShapeLibraryLoader(appconf.shape_path).to_lib()
        self._selections = Selections()
        self.__sel_shape = None
        self._map_object = None
        # new parts
        self._ms = MapState()
        self._mst = MapStateTranslator(self._ms, self._selections)
        #self.__shape_obj = []
        #self._bg_bitmap = None
        #self._bg_image = None
        self._canvas = canvas
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

    #@property
    #def map_objects(self):
    #    return self.__shape_obj

    @property
    def mapstate(self) -> MapState:
        return self._ms

    @property
    def mapstatetranslator(self) -> MapStateTranslator:
        return self._mst

    @property
    def selections(self) -> Selections:
        return self._selections

    #@property
    #def bg_bitmap(self):
    #    return self._bg_bitmap

    #@bg_bitmap.setter
    #def bg_bitmap(self, bg_bitmap: wx.Image):
    #    self._bg_bitmap = bg_bitmap

    #@property
    #def bg_image(self):
    #    return self._bg_image

    #@bg_image.setter
    #def bg_image(self, new_bg_image: wx.Image):
    #    self._bg_image = new_bg_image

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

    @property
    def map_object(self):
        return self._map_object

    @map_object.setter
    def map_object(self, map_obj: MapObject):
        self._map_object = map_obj
        self._canvas.Refresh()

    def set_background(self, image_path: Path):
        if self._map_object and image_path:
            image = wx.Image(str(image_path), wx.BITMAP_TYPE_ANY)
            self._map_object.background.image = image
            self._map_object.background.path = image_path
            self._map_object.background.file_size = image_path.stat().st_size
            #self._bg_image = image
            #self._bg_bitmap = self._bg_image.ConvertToBitmap()
            self._view.vsize = image.GetSize()
            self._view.viewport.base.x = 0
            self._view.viewport.base.y = 0
            self._view.viewport.base.width = self._canvas.GetSize().width
            self._view.viewport.base.height = self._canvas.GetSize().height
            self._view.zoom.factor = 1.0

            self._canvas.Refresh()

    def _realign_viewport_on_overflow(self):
        ## If scroll position + normalized screen width overflows on zoom we have to recalculate and refresh
        #if self._bg_bitmap:
        if self._map_object and self._map_object.background.bitmap:
            bg_bitmap = self._map_object.background.bitmap
            scrolloverx = bg_bitmap.GetSize().width - (self._normalized.x + self._normalized.width)
            scrolloverx = 0.0 if scrolloverx > 0 else scrolloverx

            scrollovery = bg_bitmap.GetSize().height - (self._normalized.y + self._normalized.height)
            scrollovery = 0.0 if scrollovery > 0 else scrollovery

            self._view.viewport.base.x += scrolloverx
            self._view.viewport.base.y += scrollovery

    def do_zoom(self, zoom_value: int):
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

    def _refresh_view_state(self):
        self._view.refresh_zoomed_vport()
        zoomedview = self._view.viewport.zoomed

        if self._map_object:
            bg_bitmap = self._map_object.background.bitmap
            bg_image = self._map_object.background.image

            limit_width = bg_image.GetSize().width if bg_bitmap else self._view.rsize.width
            limit_height = bg_image.GetSize().height if bg_bitmap else self._view.rsize.height
        else:
            limit_width = self._view.rsize.width
            limit_height = self._view.rsize.height

        self._normalized = wx.Rect(zoomedview.x, zoomedview.y, min(limit_width, zoomedview.width),
                                   min(limit_height, zoomedview.height))

        self._should_scale_up = (zoomedview.width < self._canvas.GetSize().width and zoomedview.width < limit_width,
                                 zoomedview.height < self._canvas.GetSize().height and zoomedview.height < limit_height)

    def _draw_background(self, dc):
        if self._map_object and self._map_object.background.bitmap:

            scalew = self._canvas.GetSize().width if self._should_scale_up[0] \
                else self._normalized.width * self._view.zoom.factor

            scaleh = self._canvas.GetSize().height if self._should_scale_up[1] \
                else self._normalized.height * self._view.zoom.factor

            if not self._should_scale_up[0] or not self._should_scale_up[1]:
                dc.SetBackground(wx.BLACK_BRUSH)
                dc.Clear()

            subimg = self._map_object.background.image.GetSubImage(self._normalized).Scale(scalew, scaleh)

            dc.DrawBitmap(subimg.ConvertToBitmap(), 0, 0)
        elif self._map_object is None or self._map_object.background.image is None:
            dc.SetBackground(wx.BLACK_BRUSH)
            dc.Clear()
            self._view.viewport.base.x = 0
            self._view.viewport.base.y = 0
            self._view.viewport.base.width = self._canvas.GetSize().width
            self._view.viewport.base.height = self._canvas.GetSize().height

    def _draw_objects(self, dc):
        if self._map_object:
            for shape in self._map_object.shape_obj:
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
        for shape in self._map_object.shape_obj:
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

            for shape in self._map_object.shape_obj:

                if selected_area.Contains(shape.get_bbox()):
                    self._selections.add(shape)
                elif self._mst.should_add_selection:
                    if not self._selections.contains(shape):
                        self._selections.remove(shape)
                else:
                    self._selections.remove(shape)

            self._canvas.Refresh()

    def add_shape_obj(self, shape_name: str, pos_x: int, pos_y: int):
        if self._map_object:
            try:
                shape = self.shape_lib.get(shape_name)
                new_obj = shape.shape_factory.create(shape.param)
                if new_obj:
                    zoomedview = self._view.viewport.zoomed
                    zoom = self._view.zoom.reciprocal
                    newpos = wx.Point(zoomedview.x + (pos_x * zoom),
                                      zoomedview.y + (pos_y * zoom))

                    new_obj.set_pos(position=newpos)

                    self._map_object.shape_obj.append(new_obj)
                    self._canvas.Refresh()
                else:
                    print(f"shape: {shape_name} creates null Object")

            except ShapeNotExistException as e:
                print(f"no shape found: {shape_name}")

    def move_selected_shapes(self):
        self._selections.action_on('add_to_pos', [self._mst.mouse_move_diff * self._view.zoom.reciprocal])
        self._canvas.Refresh()

    def get_update_scrollbar_dimensions(self) -> ScrollbarDimensions:
        self._scrollbar = ScrollbarDimensions()

        if self._map_object and self._map_object.background.image:
            newvize = self._map_object.background.image.GetSize()
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
