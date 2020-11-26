import unittest
from rapidmaps.map.state import MapStateType, MapStateEntity


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
        raise NotImplementedError("missing tests")


if __name__ == '__main__':
    unittest.main()
