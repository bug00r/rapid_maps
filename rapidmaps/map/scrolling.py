class ScrollbarParameter(object):
    def __init__(self):
        self._pos = 0
        self._thumbsize = 0
        self._maxpos = 0
        self._page_size = 0

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos

    @property
    def thumb_size(self):
        return self._thumbsize

    @thumb_size.setter
    def thumb_size(self, thumbsize):
        self._thumbsize = thumbsize

    @property
    def max_pos(self):
        return self._maxpos

    @max_pos.setter
    def max_pos(self, maxpos):
        self._maxpos = maxpos

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        self._page_size = page_size


class ScrollbarDimensions(object):
    def __init__(self, horizontal=None, vertical=None):
        self._vertical = vertical if vertical else ScrollbarParameter()
        self._horizontal = horizontal if horizontal else ScrollbarParameter()

    @property
    def vertical(self):
        return self._vertical

    @property
    def horizontal(self):
        return self._horizontal

    @vertical.setter
    def vertical(self, vertical=None):
        self._vertical = vertical if vertical else ScrollbarParameter()

    @horizontal.setter
    def horizontal(self, horizontal=None):
        self._horizontal = horizontal if horizontal else ScrollbarParameter()
