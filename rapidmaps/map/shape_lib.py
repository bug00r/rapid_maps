from pathlib import Path
from lxml import etree

from rapidmaps.map.shape import Shape


class ShapeExistException(Exception):
    pass


class ShapeNotExistException(Exception):
    pass


class ShapeParameter(object):
    pass


class ShapeEntry(object):
    def __init__(self, name: str, param: ShapeParameter):
        self._param = param
        self._name = name
        self._shape = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def param(self) -> ShapeParameter:
        return self._param

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, new_shape: Shape):
        self._shape = new_shape


class ShapeLibrary(object):

    def __init__(self):
        self._shape_cache = {}
        self._shape_groups = {}

    def get(self, shape_name):
        if shape_name in self._shape_cache:
            return self._shape_cache[shape_name]
        else:
            raise ShapeNotExistException(f"shape \'{shape_name}\' not exist.")

    def add(self, new_shape: ShapeEntry):
        if new_shape.name not in self._shape_cache:
            self._shape_cache[new_shape.name] = new_shape
        else:
            raise ShapeExistException(f"shape \'{new_shape.name}\' already exist.")

    def remove_by_name(self, shape_name: str):
        if shape_name in self._shape_cache:
            del self._shape_cache[shape_name]
        else:
            raise ShapeNotExistException(f"shape \'{shape_name}\' not exist.")

    def remove_by_obj(self, to_rem_shape: ShapeEntry):
        self.remove_by_name(to_rem_shape.name)

    def clear(self):
        self._shape_cache.clear()


class ShapeLibraryLoader(object):

    def __init__(self, library_path: Path):
        self._path = library_path

    @classmethod
    def from_path_str(cls, library_path: str):
        path = Path(library_path)
        return cls(path)

    def _load_lib(self, lib: ShapeLibrary):
        shapelibpath = str(self._path / 'lib.rms')
        tree = etree.parse(shapelibpath)
        for child in tree.getroot().xpath('//shape'):
            lib.add(self._xml_element_to_shape_entry(child))

    def _xml_element_to_shape_entry(self, xmlelement) -> ShapeEntry:
        param = self._xml_to_param(xmlelement)
        new_shape_entry = ShapeEntry(xmlelement.get('name'), param)
        return new_shape_entry

    def _xml_to_param(self, xmlelement) -> ShapeParameter:
        newparam = ShapeParameter()
        for param in xmlelement.xpath('./param'):
            setattr(newparam, param.get('name'), self._examine_param_value(param))
        return newparam

    def _examine_param_value(self, param):
        subparam = param.xpath('./param')
        if subparam:
            newparam = ShapeParameter()
            for param in subparam:
                setattr(newparam, param.get('name'), self._examine_param_value(param))
            result = newparam
        else:
            result = param.get('value')
        return result

    def to_lib(self) -> ShapeLibrary:
        shapelib = ShapeLibrary()
        self._load_lib(shapelib)
        return shapelib
