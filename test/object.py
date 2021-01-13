import unittest

from rapidmaps.map.shape import *
from rapidmaps.map.object import *
from rapidmaps.map.shape_lib import *

import wx


class MyTestCase(unittest.TestCase):

    def test_map_object_to_xml(self):
        app = wx.App(redirect=False)

        shape_lib = ShapeLibraryLoader(Path('./../shapes')).to_lib()
        map_object = MapObject(Map('TestMap', Path('./MyTestMap.zip')))
        shape_list = map_object.shape_obj
        map_object.background.path = Path('./examplemaps/Schlacht-in-den-Wolken_Handouts-Gareth_fc38.jpg')
        shape = shape_lib.get('Woman')
        new_obj = shape.shape_factory.create(shape.param)
        new_obj.param = shape.param
        shape_list.append(new_obj)
        shape = shape_lib.get('Woman')
        new_obj = shape.shape_factory.create(shape.param)
        new_obj.param = shape.param
        shape_list.append(new_obj)
        shape = shape_lib.get('Monk')
        new_obj = shape.shape_factory.create(shape.param)
        new_obj.param = shape.param
        shape_list.append(new_obj)
        """shape = shape_lib.get('Rectangle')
        new_obj = shape.shape_factory.create(shape.param)
        shape_list.append(new_obj)
        shape = shape_lib.get('Triangle')
        new_obj = shape.shape_factory.create(shape.param)
        shape_list.append(new_obj)"""
        mo_writer = MapObjectWriter(map_object)
        mo_writer.write()

    def test_map_object_to_zip(self):
        app = wx.App(redirect=False)
        _map = Map(name='TestMap', archive=Path('./MyTestMap.zip'))
        map_obj = MapToObjectTransformator(_map, shape_lib_path=Path('./../shapes')).transform()


if __name__ == '__main__':
    unittest.main()
