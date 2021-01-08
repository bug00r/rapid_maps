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
        shape_list.append(shape_lib.get('Woman'))
        shape_list.append(shape_lib.get('Warrior'))
        shape_list.append(shape_lib.get('Monk'))
        shape_list.append(shape_lib.get('Rectangle'))
        shape_list.append(shape_lib.get('Triangle'))
        mo_writer = MapObjectWriter(map_object)
        mo_writer.write()


    def test_map_object_to_zip(self):
        map_obj = MapToObjectTransformator(Map('TestMap', Path('./MyTestMap.zip'))).transform()


    """
    def test_map_sate_type(self):
        self.assertEqual(MapStateType.contains(MapStateType.UNKNOWN), True)
        self.assertEqual(MapStateType.contains('WRONG'), False)
        self.assertEqual(MapStateType.get_default(MapStateType.MOUSE_LEFT_POS),
                         MapStateType.MOUSE_LEFT_POS)
        self.assertEqual(MapStateType.get_default('WRONG'),
                         MapStateType.UNKNOWN)

    def test_maps_state_entity(self):
        state = MapStateEntity(MapStateType.UNKNOWN, 2)
        self.assertNotEqual(state, None)
        self.assertEqual(state.value, 2)
        self.assertEqual(state.last_value, None)
        state.value = 4
        self.assertEqual(state.value, 4)
        self.assertEqual(state.last_value, 2)
        state2 = MapStateEntity(MapStateType.MOUSE_LEFT_POS, (100, 100), (0, 0))
        self.assertEqual(state2.type, MapStateType.MOUSE_LEFT_POS)
        self.assertEqual(state2.is_type(MapStateType.MOUSE_LEFT_POS), True)

        self.assertNotEqual(state2.type, MapStateType.UNKNOWN)
        self.assertEqual(state2.is_type(MapStateType.UNKNOWN), False)
        self.assertEqual(state2.is_type(None), False)

    def test_map_state(self):
        ms = MapState()
        self.assertEqual(ms.get('Wrong'), None)
        self.assertEqual(ms.get(0), None)

        ms.set(MapStateType.MOUSE_LEFT_POS, (1, 1))
        me = ms.get(MapStateType.MOUSE_LEFT_POS)
        self.assertEqual(me.type, MapStateType.MOUSE_LEFT_POS)
        self.assertEqual(me.is_type(MapStateType.MOUSE_LEFT_POS), True)
        self.assertEqual(me.value, (1, 1))
        self.assertNotEqual(me.value, (1, 2))

    def test_map_state_translator(self):
        ms = MapState()
        sel = Selections()
        mst = MapStateTranslator(ms, sel)
        self.assertRaises(ValueError, MapStateTranslator, None, None)
        self.assertRaises(ValueError, MapStateTranslator, "Wrong", "bla")

    def test_mst_selection_was_moved(self):
        ms = MapState()
        sel = Selections()
        mst = MapStateTranslator(ms, sel)
        sel.add(Point())
        ms.set(MapStateType.MOUSE_POS, wx.Point(0, 0))
        ms.set(MapStateType.MOUSE_POS, wx.Point(1, 1))
        ms.set(MapStateType.MOUSE_LEFT, True)
        ms.set(MapStateType.MOUSE_LEFT, False)
        self.assertEqual(mst.selection_was_moved, True)
        sel.clear()
        self.assertEqual(mst.selection_was_moved, False)
    """

if __name__ == '__main__':
    unittest.main()
