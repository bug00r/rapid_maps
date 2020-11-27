"""
This Module containing all needed Data Structure for handling
MapState
"""
from enum import Enum, auto
from typing import Any, Union

import wx

from rapidmaps.core.type_tools import same_type


class MapStateType(Enum):
    """
    This Class holds the summary of all possible Map States.
    """
    UNKNOWN = auto()
    SELECTED_POS = auto()
    MOUSE_LEFT = auto()
    LEFT_CTRL = auto()
    SELECTION_UI = auto()

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
    def __init__(self, maps_state: MapState):
        if not maps_state or not isinstance(maps_state, MapState):
            raise ValueError("expecting MapState Object")

        self._ms = maps_state

    @property
    def is_single_selection(self) -> bool:
        """
        true: (SELECTION_UI) or LEFT_CTRL(keyboard) pressed)
                and
              (MOUSE_LEFT(Mouse) was clicked(down followed by UP) )
        :return: True or False
        """
        ms = self._ms
        mst = MapStateType
        ml = ms.get(mst.MOUSE_LEFT)
        sl = ms.get(mst.SELECTION_UI)
        lc = ms.get(mst.LEFT_CTRL)
        return ml and sl and lc and (sl.value or lc.value == wx.wxEVT_KEY_DOWN) \
               and ml.last_value == wx.wxEVT_LEFT_DOWN \
               and ml.value == wx.wxEVT_LEFT_UP


    @property
    def is_area_selection(self) -> bool:
        return False

    @property
    def selection_ends(self) -> bool:
        return not (self.is_single_selection or self.is_area_selection)
