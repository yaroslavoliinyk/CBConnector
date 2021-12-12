from typing import List

from NemAll_Python_Geometry import (
    CalcMass,
    CreatePolyhedron,
    Move,
    Point3D,
    Polygon3D,
    Polyhedron3D,
    Vector3D,
    Mirror,
    Plane3D
)

from ..abstracts.Element import Element


class Stiffener(Element):
    def __init__(self, data):
        super().__init__(data)

    def create(self) -> List[Polyhedron3D]:
        start_polygon = Polygon3D()
        start_polygon += Point3D(0, 0, self.data["slope_data"]["inner_height"])
        start_polygon += Point3D(
            0, 0, self.data["height"] - self.data["slope_data"]["inner_height"]
        )
        start_polygon += Point3D(
            self.data["slope_data"]["inner_width"], 0, self.data["height"]
        )
        start_polygon += Point3D(
            self.data["width"] - self.data["slope_data"]["top_outer_width"],
            0,
            self.data["height"],
        )
        start_polygon += Point3D(
            self.data["width"],
            0,
            self.data["height"] - self.data["slope_data"]["top_outer_height"],
        )
        start_polygon += Point3D(
            self.data["width"], 0, self.data["slope_data"]["bot_outer_height"]
        )
        start_polygon += Point3D(
            self.data["width"] - self.data["slope_data"]["bot_outer_width"], 0, 0
        )
        start_polygon += Point3D(self.data["slope_data"]["inner_width"], 0, 0)
        start_polygon += Point3D(0, 0, self.data["slope_data"]["inner_height"])

        end_polygon = Move(start_polygon, Vector3D(0, self.data["thickness"], 0))

        err, main_stiffener_geometry = CreatePolyhedron(start_polygon, end_polygon)

        if self.data["outer"]:
            _, outer_stiffener_geometry = CreatePolyhedron(start_polygon, end_polygon)
            mirrored_plane = Plane3D(Point3D(-(self.data["pillar_web_thickness"])/2., 0, 0),
            Vector3D(-1, 0, 0))
            outer_stiffener_geometry = Mirror(
                outer_stiffener_geometry,
                ### In Left is -self.data... ; In Right is self.data
                mirrored_plane,
            )
            return [main_stiffener_geometry, outer_stiffener_geometry]
        return [main_stiffener_geometry]

    def show(self) -> bool:
        return True

    def calculate_weight(self):
        weight = 0.0

        geo_list = self.create()

        for geo in geo_list:
            err, volume, _, _ = CalcMass(geo)
            volume = volume / 1000000000

            weight += self.data["density"] * volume

        return weight

    def __str__(self):
        return "Stiffener"
