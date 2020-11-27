import unittest
from rapidmaps.map.state import MapStateType, MapStateEntity, MapState, MapStateTranslator


class MyTestCase(unittest.TestCase):

    def test_map_sate_type(self):
        self.assertEqual(MapStateType.contains(MapStateType.UNKNOWN), True)
        self.assertEqual(MapStateType.contains('WRONG'), False)
        self.assertEqual(MapStateType.get_default(MapStateType.SELECTED_POS),
                         MapStateType.SELECTED_POS)
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
        state2 = MapStateEntity(MapStateType.SELECTED_POS, (100, 100), (0, 0))
        self.assertEqual(state2.type, MapStateType.SELECTED_POS)
        self.assertEqual(state2.is_type(MapStateType.SELECTED_POS), True)

        self.assertNotEqual(state2.type, MapStateType.UNKNOWN)
        self.assertEqual(state2.is_type(MapStateType.UNKNOWN), False)
        self.assertEqual(state2.is_type(None), False)

    def test_map_state(self):
        ms = MapState()
        self.assertEqual(ms.get('Wrong'), None)
        self.assertEqual(ms.get(0), None)

        ms.set(MapStateType.SELECTED_POS, (1, 1))
        me = ms.get(MapStateType.SELECTED_POS)
        self.assertEqual(me.type, MapStateType.SELECTED_POS)
        self.assertEqual(me.is_type(MapStateType.SELECTED_POS), True)
        self.assertEqual(me.value, (1, 1))
        self.assertNotEqual(me.value, (1, 2))

    def test_map_state_translator(self):
        ms = MapState()
        mst = MapStateTranslator(ms)
        self.assertRaises(ValueError, MapStateTranslator, None)
        self.assertRaises(ValueError, MapStateTranslator, "Wrong")


if __name__ == '__main__':
    unittest.main()
