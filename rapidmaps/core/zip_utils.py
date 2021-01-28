import zipfile
from lxml import etree


class MapFileException(Exception):
    pass


class MapFileNotExistException(Exception):
    pass


def extract_map_name(zip_path: str) -> str:
    with zipfile.ZipFile(zip_path) as mapzip:

        zipfilenames = mapzip.namelist()

        if 'index.map' in zipfilenames:
            with mapzip.open('index.map') as myfile:
                root = etree.XML(myfile.read())
                map_name = root.attrib.get('name')
                if not map_name:
                    raise MapFileException("Missing Name in Map File oO.")
        else:
            raise MapFileException("Invalid or Corrupt Mapfile :(.")

    return map_name