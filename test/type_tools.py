import unittest
from rapidmaps.core.type_tools import same_type


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(same_type(None, None), False)
        self.assertEqual(same_type('', None), False)
        self.assertEqual(same_type(None, ''), False)
        self.assertEqual(same_type('', 0), False)
        self.assertEqual(same_type('', 0.1), False)
        self.assertEqual(same_type(0, ''), False)
        self.assertEqual(same_type(0.1, ''), False)
        self.assertEqual(same_type('', ''), True)


if __name__ == '__main__':
    unittest.main()
