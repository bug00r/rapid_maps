import wx
import zipfile

from lxml import etree
from pathlib import Path

from rapidmaps.map.meta import Map
from rapidmaps.map.shape import ShapeParameter, Shape
from rapidmaps.map.shape_lib import XmlTagToParameterTransformator, ShapeFactory, ShapeEntry


class MapBackground(object):
    def __init__(self):
        self._image = None
        self._path = None
        self._bitmap = None

    @property
    def image(self) -> wx.Image:
        return self._image

    @image.setter
    def image(self, new_image: wx.Image):
        self._image = new_image

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, _path: Path):
        self._path = _path

    @property
    def bitmap(self):
        used_bitmap = self._bitmap
        if used_bitmap is None and self._image is not None:
            used_bitmap = self._image.ConvertToBitmap()
            self._bitmap = used_bitmap
        return used_bitmap


class MapObject(object):
    """This class contains all loaded meta files.
       This should be handled lazy."""
    def __init__(self, _map: Map):
        self._map = _map
        self._bg = MapBackground()
        self._shape_obj = []

    @property
    def background(self) -> MapBackground:
        return self._bg

    @property
    def shape_obj(self) -> list:
        return self._shape_obj

    @property
    def map(self) -> Map:
        return self._map


class MapToObjectTransformator(object):

    def __init__(self, _map: Map, shape_lib_path: Path):
        self._map = _map
        self._shape_factory = ShapeFactory(shape_lib_path)

    def _xml_to_shape_reinit(self, xmlelement, shape: Shape):
        if shape is not None and xmlelement is not None:
            for child in xmlelement:
                tag_name = child.tag
                if tag_name == 'pos':
                    shape.set_pos(wx.Point(int(child.get('x')), int(child.get('y'))))
                elif tag_name == 'size':
                    shape.set_size(wx.Size(int(child.get('w')), int(child.get('h'))))
                elif tag_name == 'rotation':
                    shape.set_angle(int(child.get('angle')))
                elif tag_name == 'label':
                    shape.set_name(child.get('value'))

    def transform(self) -> MapObject:
        """TODO reading zip file from Map and fill MapObject with parameter and Background,
        shapes and so on"""
        map_obj = MapObject(self._map)

        if self._map.archive_path.exists():

            with zipfile.ZipFile(str(self._map.archive_path)) as mapzip:
                with mapzip.open('index.map') as myfile:
                    root = etree.XML(myfile.read())

            for shape in root.xpath('shape'):
                shape_param = XmlTagToParameterTransformator(shape).transform()
                shape_obj = self._shape_factory.create(shape_param)
                self._xml_to_shape_reinit(shape, shape_obj)
                map_obj.shape_obj.append(shape_obj)

            bg = root.xpath('background')
            if len(bg) > 0:
                bg_path_str = bg[0].attrib.get('file')
                bg_path = Path(bg_path_str)
                bg_image = wx.Image(bg_path_str, wx.BITMAP_TYPE_ANY)
                map_obj.background.path = bg_path
                map_obj.background.image = bg_image

        return map_obj


class MapObjectWriter(object):

    file_skeleton = b'<?xml version="1.0" encoding="UTF-8"?><map></map>'
    excluded_parm = ['type', 'name']

    def __init__(self, map_object: MapObject):
        self._map_object = map_object

    def _shape_param_to_xml_entity(self, param_obj: ShapeParameter):
        param_tag = etree.Element('param')
        if isinstance(param_obj, ShapeParameter):
            for key, value in filter(lambda entry: entry[0] not in self.excluded_parm,
                                     param_obj.__dict__.items()):
                sup_param_tag = etree.Element('param', name=key)
                if isinstance(value, ShapeParameter):
                    xml_entity = self._shape_param_to_xml_entity(value)
                    sup_param_tag.append(xml_entity)
                else:
                    sup_param_tag.attrib['value'] = str(value)

                param_tag.append(sup_param_tag)
        else:
            param_tag.attrib['value'] = str(param_obj)

        return param_tag

    def write(self):
        """TODO creating zip archive and save to map path. If map path not exist
        as reason of a new map, rise an exception, catch them and edit path with dialog"""
        root = etree.XML(self.file_skeleton)
        map_tree = etree.ElementTree(root)

        root.attrib['name'] = self._map_object.map.name

        background = etree.Element('background')
        background.attrib['file'] = str(self._map_object.background.path.absolute())
        root.append(background)

        for shape in self._map_object.shape_obj:
            shape_tag = etree.Element('shape')
            shape_tag.attrib['type'] = shape.param.type
            shape_tag.attrib['name'] = shape.param.name
            shape_tag.attrib['group'] = shape.param.group

            for key, value in filter(lambda entry: entry[0] not in self.excluded_parm,
                                     shape.param.__dict__.items()):
                param_tag = self._shape_param_to_xml_entity(value)
                param_tag.attrib['name'] = key
                shape_tag.append(param_tag)

            etree.SubElement(shape_tag, 'pos', attrib={'x': str(shape.get_pos().x),
                                                       'y': str(shape.get_pos().y)})

            etree.SubElement(shape_tag, 'size', attrib={'w': str(shape.get_size().width),
                                                       'h': str(shape.get_size().height)})

            etree.SubElement(shape_tag, 'rotation', attrib={'angle': str(shape.get_angle())})

            etree.SubElement(shape_tag, 'label', attrib={'value': shape.get_name()})

            root.append(shape_tag)

        if not self._map_object.map.archive_path.parent.exists():
            self._map_object.map.archive_path.parent.mkdir()

        with zipfile.ZipFile(str(self._map_object.map.archive_path), mode='w') as mapzip:
            mapzip.writestr('index.map', etree.tostring(root, pretty_print=True))
