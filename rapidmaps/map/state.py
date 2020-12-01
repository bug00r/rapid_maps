"""
This Module containing all needed Data Structure for handling
MapState
"""
from enum import Enum, auto
from typing import Any, Union

import wx

from rapidmaps.core.type_tools import same_type
from rapidmaps.map.selection import Selections


class MapStateType(Enum):
    """
    This Class holds the summary of all possible Map States.
    """
    UNKNOWN = auto()
    MOUSE_LEFT_POS = auto()             # mouse left down position
    MOUSE_LEFT_RELEASE_POS = auto()     # mouse left up position
    MOUSE_POS = auto()                  # mouse move position
    MOUSE_LEFT = auto()                 # mouse left click state (up/down)
    KB_CTRL = auto()                    # Keyboard CTRL State
    KB_SHIFT = auto()                   # Keyboard SHIFT State
    KB_ALT = auto()                     # Keyboard ALT State
    SELECTION_MODE_UI = auto()          # UI Element, selection active
    ADDITION_MODE_UI = auto()           # UI Element, addition active
    MOVING_MODE_UI = auto()             # UI Element, moving active
    # combined states
    SELECTION_IS_MOVING = auto()        # selected item woving around

    @classmethod
    def contains(cls, state) -> bool:
        return isinstance(state, cls) and state.name in MapStateType.__members__

    @staticmethod
    def get_default(state, default=None):
        used_default = default if MapStateType.contains(default) else MapStateType.UNKNOWN
        return state if MapStateType.contains(state) else used_default


class MapStateEntity(object):
    """
    This Class represents a MapStateEntity for holding a single
    State Instance. There could be a value and a last value. If
    the current value will be set then the actual current value
    will be moved into the last value. With these simple mechanism
    you ca examine simple state changes like:

        * Rectangle grows/shrinks
        * Button was pressed/released
    """
    def __init__(self, _type: MapStateType, cur_value: Any, last_value=None):
        self._type = MapStateType.get_default(_type)
        self._cur_value = cur_value
        self._last_value = last_value

    @property
    def value(self):
        return self._cur_value

    @value.setter
    def value(self, value: Any):
        if self._cur_value is not None and not same_type(self._cur_value, value):
            raise ValueError(f"Set type {type(value)} ne {type(self._cur_value)}")
        self._last_value = self._cur_value
        self._cur_value = value

    @property
    def last_value(self) -> Any:
        return self._last_value

    @property
    def type(self) -> MapStateType:
        return self._type

    def is_type(self, check_type: MapStateType) -> bool:
        return MapStateType.contains(check_type) and check_type == self._type


class MapState(object):
    """
    This class represents a simple dict based MapStateEntity
    Collection with some predefined check against plausibility
    """
    def __init__(self):
        self._states = dict()

    def get(self, state_type: MapStateType) -> Union[MapStateEntity, None]:
        return self._states[state_type] if MapStateType.contains(state_type) and \
                                           state_type in self._states else None

    def set(self, state_type: MapStateType, value: Any):
        if not MapStateType.contains(state_type):
            raise ValueError("state_type invalid")

        if state_type not in self._states:
            self._states[state_type] = MapStateEntity(state_type, value, value)
        else:
            self._states[state_type].value = value

        return self._states[state_type]


class MapStateTranslator(object):
    """
    This class offers combined MapStates translated to
    User Interactions.
    """
    def __init__(self, maps_state: MapState, selections: Selections):
        if not maps_state or not isinstance(maps_state, MapState):
            raise ValueError("expecting MapState Object")
        if not selections or not isinstance(selections, Selections):
            raise ValueError("expecting Selections Object")

        self._sel = selections
        self._ms = maps_state

    @property
    def is_selection_mode_active(self):
        return self._ms.get(MapStateType.SELECTION_MODE_UI).value

    @property
    def is_selection_area_active(self):
        return not self.is_moving_mode_active and self.is_selection_mode_active \
                and self._ms.get(MapStateType.MOUSE_LEFT).value == wx.wxEVT_LEFT_DOWN

    @property
    def is_addition_mode_active(self):
        return self._ms.get(MapStateType.ADDITION_MODE_UI).value or \
                self._ms.get(MapStateType.KB_ALT).value == wx.wxEVT_KEY_DOWN

    @property
    def is_moving_mode_active(self):
        return self._ms.get(MapStateType.MOVING_MODE_UI).value or \
                self._ms.get(MapStateType.KB_SHIFT).value == wx.wxEVT_KEY_DOWN

    @property
    def should_add_selection(self) -> bool:
        lc = self._ms.get(MapStateType.KB_CTRL)
        return lc and lc.value == wx.wxEVT_KEY_DOWN and self.is_selection_mode_active

    @property
    def selection_is_moving(self) -> bool:
        return not self._sel.is_empty() and self.mouse_move_diff != wx.Point(0, 0) \
            and self.is_moving_mode_active \
            and self._ms.get(MapStateType.MOUSE_LEFT).value == wx.wxEVT_LEFT_DOWN

    @property
    def mouse_move_diff(self) -> wx.Point:
        mp = self._ms.get(MapStateType.MOUSE_POS)
        return mp.value - mp.last_value

    @property
    def current_selected_area(self) -> wx.Rect:
        startpos = self._ms.get(MapStateType.MOUSE_LEFT_POS).value
        area = self._ms.get(MapStateType.MOUSE_POS).value - startpos
        return wx.Rect(startpos.x, startpos.y, area.x, area.y)