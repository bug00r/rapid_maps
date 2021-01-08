import wx
from lxml import etree
import zipfile

from rapidmaps.map.meta import Map
from rapidmaps.map.shape import ShapeParameter


class MapBackground(object):
    def __init__(self):
        self._image = None

    @property
    def image(self) -> wx.Image:
        return self._image

    @image.setter
    def image(self, new_image: wx.Image):
        self._image = new_image


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

    def __init__(self, _map: Map):
        self._map = _map

    def transform(self) -> MapObject:
        """TODO reading zip file from Map and fill MapObject with parameter and Background,
        shapes and so on"""
        map_obj = MapObject(self._map)

        with zipfile.ZipFile(str(self._map.archive_path)) as mapzip:
            with mapzip.open('index.map') as myfile:
                root = etree.XML(myfile.read())

        for shape in root.xpath('shape'):
            print(etree.tostring(shape, pretty_print=True))
            for param in shape.xpath('param'):
                print("----", etree.tostring(param, pretty_print=True))

        #CONTINUE HERE!!!!

        return map_obj


class MapObjectWriter(object):

    file_skeleton = b'<?xml version="1.0" encoding="UTF-8"?><map></map>'
    excluded_parm = ['type', 'group', 'name']

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

            if shape.shape:
                etree.SubElement(shape_tag, 'pos', attrib={'x': str(shape.shape.get_pos().x),
                                                           'y': str(shape.shape.get_pos().y)})

                etree.SubElement(shape_tag, 'size', attrib={'w': str(shape.shape.get_size().width),
                                                           'h': str(shape.shape.get_size().height)})

                etree.SubElement(shape_tag, 'rotation', attrib={'angle': str(shape.shape.get_angle())})

                etree.SubElement(shape_tag, 'label', attrib={'value': shape.shape.get_name()})

            root.append(shape_tag)

        with zipfile.ZipFile(str(self._map_object.map.archive_path), mode='w') as mapzip:
            mapzip.writestr('index.map', etree.tostring(root, pretty_print=True))
