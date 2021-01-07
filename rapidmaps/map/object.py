from rapidmaps.map.meta import Map


class MapObject(object):
    """This class contains all loaded meta files.
       This should be handled lazy."""
    def __init__(self, _map: Map):
        self._map = _map


class MapToObjectTransformator(object):

    def __init__(self, _map: Map):
        self._map = _map

    def transform(self) -> MapObject:
        """TODO reading zip file from Map and fill MapObject with parameter and Background,
        shapes and so on"""
        map_obj = MapObject(self._map)
        return map_obj


class MapObjectWriter(object):

    def __init__(self, map_object: MapObject):
        self._map_object = map_object

    def write(self):
        """TODO creating zip archive and save to map path. If map path not exist
        as reason of a new map, rise an exception, catch them and edit path with dialog"""
        pass