import unittest

from rapidmaps.map.meta import *


class MyTestCase(unittest.TestCase):

    def test_map_meta_history_read(self):
        mh_loader = MapHistoryLoader(Path())
        map_history = mh_loader.load()
        maps = map_history.get_maps()
        self.assertEqual(len(maps), 3)
        self.assertEqual(maps[0].name, "Map Gareth")
        self.assertEqual(maps[1].name, "Map Werheim")
        self.assertEqual(maps[2].name, "Map Andergast")
        self.assertEqual(str(map_history.get(maps[0].name).archive_path),
                         "/home/bug0r/map_gareth.zip")
        self.assertEqual(str(map_history.get(maps[1].name).archive_path),
                         "/home/bug0r/map_werheim.zip")
        self.assertEqual(str(map_history.get(maps[2].name).archive_path),
                         "/home/bug0r/map_andergast.zip")

    def test_map_meta_history_write(self):
        mh_loader = MapHistoryLoader(Path())
        map_history = mh_loader.load()
        map_history.add(Map("AddedMap1", Path("/home/bug0r/AddedMap1.zip")))
        map_history.add(Map("AddedMap2", Path("/home/bug0r/AddedMap2.zip")))
        map_history.add(Map("AddedMap3", Path("/home/bug0r/AddedMap3.zip")))
        writer = MapHistoryWriter(Path('./test_write_history'))
        writer.write(map_history)

        mh_loader = MapHistoryLoader(Path('./test_write_history'))
        map_history = mh_loader.load()
        maps = map_history.get_maps()
        self.assertEqual(len(maps), 6)
        self.assertEqual(maps[0].name, "Map Gareth")
        self.assertEqual(maps[1].name, "Map Werheim")
        self.assertEqual(maps[2].name, "Map Andergast")
        self.assertEqual(maps[3].name, "AddedMap1")
        self.assertEqual(maps[4].name, "AddedMap2")
        self.assertEqual(maps[5].name, "AddedMap3")
        self.assertEqual(str(map_history.get(maps[0].name).archive_path),
                         "/home/bug0r/map_gareth.zip")
        self.assertEqual(str(map_history.get(maps[1].name).archive_path),
                         "/home/bug0r/map_werheim.zip")
        self.assertEqual(str(map_history.get(maps[2].name).archive_path),
                         "/home/bug0r/map_andergast.zip")
        self.assertEqual(str(map_history.get(maps[3].name).archive_path),
                         "/home/bug0r/AddedMap1.zip")
        self.assertEqual(str(map_history.get(maps[4].name).archive_path),
                         "/home/bug0r/AddedMap2.zip")
        self.assertEqual(str(map_history.get(maps[5].name).archive_path),
                         "/home/bug0r/AddedMap3.zip")

    def test_map_meta_history_load_error(self):
        mh_loader = MapHistoryLoader(Path('./error_history'))
        self.assertRaises(InvalidMapDataException, mh_loader.load)

        mh_loader = MapHistoryLoader(Path('./error_history_2'))
        self.assertRaises(InvalidMapDataException, mh_loader.load)

    def test_map_meta_history_edit_error(self):
        mh_loader = MapHistoryLoader(Path('./test_write_history'))
        mh = mh_loader.load()
        self.assertRaises(MapNotExistException, mh.get, 'error')
        self.assertRaises(MapExistException, mh.add, Map("AddedMap1", Path("/home/bug0r/AddedMap1.zip")))

    def test_invalid_map_creation(self):
        self.assertRaises(MissingMapNameException, Map, None, Path("/home/bug0r/AddedMap1.zip"))
        self.assertRaises(MissingMapNameException, Map, "", Path("/home/bug0r/AddedMap1.zip"))
