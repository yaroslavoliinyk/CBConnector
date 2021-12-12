from typing import List

from NemAll_Python_Geometry import Polyhedron3D

from ..abstracts.Element import Element


class Pillar(Element):
    def __init__(self, data):
        super().__init__(data)

    def create(self) -> List[Polyhedron3D]:
        return []

    def show(self) -> bool:
        return False

    def calculate_weight(self):
        return 0

    def __str__(self):
        return "Pillar"
