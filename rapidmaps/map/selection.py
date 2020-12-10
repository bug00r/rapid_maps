from rapidmaps.map.shape import Shape
from wx import Point as wxPoint


class Selections(object):
    def __init__(self):
        self._shapes = dict()

    def add(self, shape: Shape):
        id_shape = id(shape)
        if id_shape not in self._shapes:
            shape.set_selected(True)
            self._shapes[id_shape] = shape

    def remove(self, shape: Shape):
        id_shape = id(shape)
        if id_shape in self._shapes:
            shape.set_selected(False)
            del self._shapes[id_shape]

    def contains(self, shape):
        return id(shape) in self._shapes

    def clear(self):
        for ids, shape in self._shapes.items():
            shape.set_selected(False)
        self._shapes.clear()

    def action(self, action: callable, parameter):
        for ids, shape in self._shapes.items():
            action(shape, *parameter)

    def action_on(self, action: str, parameter: list):
        for ids, shape in self._shapes.items():
            if hasattr(shape.__class__, action) and callable(getattr(shape.__class__, action)):
                getattr(shape.__class__, action)(shape, *parameter)

    def intersect_any(self, point: wxPoint) -> bool:
        for ids, shape in self._shapes.items():
            if shape.intersect_by(point):
                return True
        return False

    def is_empty(self):
        return len(self._shapes) == 0

