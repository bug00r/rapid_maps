from pathlib import Path
from lxml import etree


class ShapeLibrary(object):

    def __init__(self, path: str, tree):
        self._path = path
        self._tree = tree
        for child in self._tree.getroot():
            print(f"{child.tag} -> name: {child.get('name')}")
        self._shape_cache = {}


class ShapeLibraryLoader(object):

    def __init__(self, library_path: Path):
        self._path = library_path

    @classmethod
    def from_path_str(cls, library_path: str):
        path = Path(library_path)
        return cls(path)

    def to_lib(self) -> ShapeLibrary:
        shapelibpath = str(self._path / 'lib.rms')
        shapelib = ShapeLibrary(shapelibpath, etree.parse(shapelibpath))
        return shapelib
