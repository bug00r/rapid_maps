from enum import Enum, auto

import wx

from rapidmaps.map.state import MapStateType


class WFCanvasClickEventType(Enum):
    LEFT_MOUSE_DOWN = auto()
    LEFT_MOUSE_UP = auto()


class WFCanvasClickEvent(object):
    def __init__(self, wf_event_type: WFCanvasClickEventType, wx_event: wx.Event):
        self._wf_evt_type = wf_event_type
        self._wx_evt = wx_event

    @property
    def type(self):
        return self._wf_evt_type

    @property
    def wx_event(self):
        return self._wx_evt


class CanvasClickWF(object):

    def __init__(self, main_frame):
        self._frame = main_frame
        self._map = main_frame.map
        self._ms = main_frame.map.mapstate
        self._mst = main_frame.map.mapstatetranslator
        self._handler = { WFCanvasClickEventType.LEFT_MOUSE_DOWN: self._handle_left_down,
                          WFCanvasClickEventType.LEFT_MOUSE_UP: self._handle_left_up
                          }

    def _handle_left_down(self, wf_event: WFCanvasClickEvent):
        event = wf_event.wx_event
        self._ms.set(MapStateType.MOUSE_LEFT, event.EventType)
        self._ms.set(MapStateType.MOUSE_LEFT_POS, event.Position)

        if not self._mst.is_moving_mode_active and self._mst.is_selection_mode_active:
            foundShape = self._map.single_select_at(event.Position.x, event.Position.y)
            if foundShape:
                self._frame.edit_enabled(True)
                self._frame.set_edit_by(foundShape)
        event.Skip()

    def _handle_left_up(self, wf_event: WFCanvasClickEvent):
        event = wf_event.wx_event
        self._ms.set(MapStateType.MOUSE_LEFT, event.EventType)
        self._ms.set(MapStateType.MOUSE_LEFT_RELEASE_POS, event.Position)

        if self._mst.was_selection_area_active:
            self._map.area_selection_at(self._mst.current_selected_area)
        if self._frame.should_add_entity() and self._frame.cur_shape_btn is not None:
            self._map.add_shape_obj(self._frame.all_shape_btns.get(self._frame.cur_shape_btn, 'unknown'),
                                    event.Position.x, event.Position.y)
        event.Skip()

    def process(self, wf_event: WFCanvasClickEvent):
        if wf_event.type in self._handler:
            self._handler[wf_event.type](wf_event)
