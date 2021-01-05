from pathlib import Path
from lxml import etree
import wx

from rapidmaps.map.shape import Shape, ImageShape


class ShapeExistException(Exception):
    pass


class ShapeNotExistException(Exception):
    pass


class ShapeParameter(object):
    pass


class ShapeCreator(object):

    def __init__(self, param: ShapeParameter):
        self._param = param
        self._lib_path = None

    def create(self) -> Shape:
        pass

    def set_lib_path(self, lib_path: Path):
        self._lib_path = lib_path


class UnknownShapeCreator(ShapeCreator):

    def __init__(self, param: ShapeParameter):
        super().__init__(param)

    def create(self) -> Shape:
        return None


class ShapeImageCreator(ShapeCreator):

    def __init__(self, param: ShapeParameter):
        super().__init__(param)

    def create(self) -> Shape:
        shape_obj = ImageShape()
        shape_obj.set_name(self._param.name)
        img_path = self._lib_path.joinpath(*self._param.file.split('/'))
        shape_obj.set_image(wx.Image(str(img_path), wx.BITMAP_TYPE_ANY))
        return shape_obj


class ShapeFactory(object):

    creator_pool = {
        'image': ShapeImageCreator,
        'unknown': UnknownShapeCreator
    }

    def __init__(self, library_path: Path):
        self._lib_path = library_path

    def create(self, param: ShapeParameter) -> Shape:
        creator_clazz = self.creator_pool.get(param.type, UnknownShapeCreator)
        creator_obj = creator_clazz(param)
        creator_obj.set_lib_path(self._lib_path)
        return creator_obj.create()


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


class ShapeEntryMetaWrapper(object):

    def __init__(self, entry: ShapeEntry):
        self._entry = entry

    @property
    def name(self):
        return self._entry.param.name

    @property
    def group(self):
        return self._entry.param.group

    @property
    def shape(self):
        return self._entry.shape


class ShapeLibrary(object):

    def __init__(self):
        self._shape_cache = {}
        self._shape_meta = None

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

    def get_shapes(self):
        if not self._shape_meta:
            self._shape_meta = [ShapeEntryMetaWrapper(shape) for shape in self._shape_cache.values()]
        return self._shape_meta


class ShapeLibraryLoader(object):

    def __init__(self, library_path: Path):
        self._path = library_path
        self._shape_factory = ShapeFactory(library_path)

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
        self._create_shape(new_shape_entry)
        return new_shape_entry

    def _xml_to_param(self, xmlelement) -> ShapeParameter:
        newparam = ShapeParameter()
        setattr(newparam, 'name', xmlelement.get('name', default='UNKNOWN'))
        setattr(newparam, 'type', xmlelement.get('type', default='UNKNOWN'))
        setattr(newparam, 'group', xmlelement.getparent().get('name', default='UNKNOWN'))
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

    def _create_shape(self, entry: ShapeEntry):
        if not entry.shape:
            entry.shape = self._shape_factory.create(entry.param)

    def to_lib(self) -> ShapeLibrary:
        shapelib = ShapeLibrary()
        self._load_lib(shapelib)
        return shapelib
