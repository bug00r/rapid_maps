"""

This Module contains a collection of Map Datastructures

"""
from typing import Any


class MapEventEmitter(object):
    """ Map Event Emitter Interface """
    def on_paint_map(self, event: Any):
        pass

    def on_click(self, event: Any):
        pass


class MapEntityMeta(object):
    """ Metadata Interface for MapEntities """
    def get_name(self) -> str:
        pass


class MapImage(object):
    """ Image Data for drawing on the Map """
    def get_data(self) -> Any:
        pass


class MapEntity(object):
    """ Map Entity who can be add / draw on a Map """
    def get_meta(self) -> MapEntityMeta:
        pass

    def get_position(self) -> Any:
        pass

    def get_image(self) -> MapImage:
        pass


class Map(object):
    """ Map Interface """
    def set_background(self, image: MapImage):
        pass

    def add_entity(self, entity: MapEntity):
        pass
