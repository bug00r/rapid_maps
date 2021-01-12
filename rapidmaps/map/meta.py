from pathlib import Path
from lxml import etree


class MapExistException(Exception):
    pass


class MapNotExistException(Exception):
    pass


class InvalidMapDataException(Exception):
    pass


class MissingMapNameException(Exception):
    pass


class Map(object):
    def __init__(self, name: str, archive: Path):
        if not name or len(name) == 0:
            raise MissingMapNameException(f"No Map name found")
        self._name = name
        self._ar_path = archive

    @property
    def name(self) -> str:
        return self._name

    @property
    def archive_path(self) -> Path:
        return self._ar_path

    @archive_path.setter
    def archive_path(self, archive_path: Path):
        self._ar_path = archive_path

    def is_new(self):
        return self._ar_path is None


class MapWrapper(object):

    def __init__(self, _map: Map):
        self._map = _map

    @property
    def name(self) -> str:
        return self._map.name


class MapHistory(object):

    def __init__(self):
        self._map_cache = {}
        self._map_meta = None

    def get(self, map_name):
        if map_name in self._map_cache:
            return self._map_cache[map_name]
        else:
            raise MapNotExistException(f"map \'{map_name}\' not exist.")

    def add(self, new_map: Map):
        if new_map.name not in self._map_cache:
            self._map_cache[new_map.name] = new_map
        else:
            raise MapExistException(f"map \'{new_map.name}\' already exist.")

    def remove_by_name(self, map_name: str):
        if map_name in self._map_cache:
            del self._map_cache[map_name]
        else:
            raise MapNotExistException(f"map \'{map_name}\' not exist.")

    def remove_by_obj(self, to_rem_map: Map):
        self.remove_by_name(to_rem_map.name)

    def clear(self):
        self._map_cache.clear()

    def get_maps(self):
        #if not self._map_meta:
        #    self._map_meta = [MapWrapper(_map) for _map in self._map_cache.values()]
        #return self._map_meta
        return [MapWrapper(_map) for _map in self._map_cache.values()]


class MapHistoryLoader(object):
    """Loading last used and saved maps"""
    def __init__(self, map_history_path: Path):
        self._mh_path = map_history_path / 'maps.history'

    def _xml_element_to_map(self, xml_element) -> Map:
        map_name = xml_element.get('name')
        map_file = xml_element.get('file')

        if not (map_name and map_file):
            raise InvalidMapDataException(f"map: {map_name} file: {map_file}")

        return Map(map_name, Path(map_file))

    def load(self) -> MapHistory:
        map_history = MapHistory()

        tree = etree.parse(str(self._mh_path))
        for child in tree.getroot().xpath('//map'):
            map_history.add(self._xml_element_to_map(child))

        return map_history


class MapHistoryWriter(object):

    file_skeleton = b'<?xml version="1.0" encoding="UTF-8"?><history></history>'

    def __init__(self, map_history_path: Path):
        self._mh_path = map_history_path.joinpath('maps.history')

    def write(self, history: MapHistory):
        root = etree.XML(self.file_skeleton)
        h_tree = etree.ElementTree(root)
        for map_meta in history.get_maps():
            _map = history.get(map_meta.name)
            etree.SubElement(root, 'map', attrib={ 'name': _map.name, 'file': str(_map.archive_path)})
        h_tree.write(str(self._mh_path), standalone=True, encoding='utf-8',pretty_print=True)
