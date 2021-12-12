import abc

from .Element import Element


class Removable(Element, abc.ABC):
    def __init__(self, data):
        super().__init__(data)
