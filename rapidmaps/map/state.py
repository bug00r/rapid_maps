"""
This Module containing all needed Data Structure for handling
MapState
"""
from enum import Enum, auto
from typing import Any, Union

from rapidmaps.core.type_tools import same_type


class MapStateType(Enum):
    UNKNOWN = auto()
    SELECTED_POS = auto()
    MOUSE_LEFT = auto()

    @classmethod
    def contains(cls, state) -> bool:
        return isinstance(state, cls) and state.name in MapStateType.__members__

    @staticmethod
    def get_default(state, default=None):
        used_default = default if MapStateType.contains(default) else MapStateType.UNKNOWN
        return state if MapStateType.contains(state) else used_default


class MapStateEntity(object):

    def __init__(self, _type: MapStateType, cur_value: Any, last_value=None):
        self._type = MapStateType.get_default(_type)
        self._cur_value = cur_value
        self._last_value = last_value

    @property
    def value(self):
        return self._cur_value

    @value.setter
    def value(self, value: Any):
        if not same_type(self._cur_value, value):
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

    def __init__(self):
        self._states = dict()

    def get_state(self, state_type: MapStateType) -> Union[MapStateEntity, None]:
        return self._states[state_type] if MapStateType.contains(state_type) and \
                                           state_type in self._states else None

    def set_state(self, state_type: MapStateType, value: Any, last_value=None):
        if not MapStateType.contains(state_type):
            raise ValueError("state_type invalid")

        if state_type not in self._states:
            self._states[state_type] = MapStateEntity(state_type, value, last_value)

        return self._states[state_type]
