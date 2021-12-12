from typing import List

from NemAll_Python_Geometry import (
    CalcMass,
    CreatePolyhedron,
    Move,
    Point3D,
    Polygon3D,
    Polyhedron3D,
    Vector3D,
)

from ..abstracts.Element import Element


class Connector(Element):
    def __init__(self, data):
        super().__init__(data)

    def create(self) -> List[Polyhedron3D]:
        start_polygon = Polygon3D()
        start_polygon += Point3D(0, 0, 0)
        start_polygon += Point3D(0, 0, self.data["height"])
        start_polygon += Point3D(self.data["width"], 0, self.data["height"])
        start_polygon += Point3D(self.data["width"], 0, 0)
        start_polygon += Point3D(0, 0, 0)

        end_polygon = Move(start_polygon, Vector3D(0, self.data["thickness"], 0))

        err, geometry = CreatePolyhedron(start_polygon, end_polygon)
        return [geometry]

    def show(self) -> bool:
        return self.data["show"]

    def calculate_weight(self):
        weight = 0.0

        geo_list = self.create()

        for geo in geo_list:
            err, volume, _, _ = CalcMass(geo)
            volume = volume / 1000000000

            weight += self.data["density"] * volume

        return weight

    def __str__(self):
        return "Connector"
