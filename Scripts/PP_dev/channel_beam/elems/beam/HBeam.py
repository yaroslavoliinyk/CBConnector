# from typing import List

from NemAll_Python_Geometry import Line3D, Point3D, Polygon3D

from .Beam import Beam


class HBeam(Beam):
    def __init__(self, data):
        super().__init__(data)
        self._data["width"] = self._data["d"]
        self._d = self._data["d"]
        self._bf = self._data["bf"]
        self._tf = self._data["tf"]
        self._tw = self._data["tw"]
        self._k1 = self._data["k1"]

    def create_shape(self) -> Polygon3D:
        interior_rounding_radius = self._k1 - self._tw / 2
        exterior_rounding_radius = self._tf / 2
        polygon = Polygon3D()

        if self._data["rounded"]:
            polygon += Point3D(-self._bf / 2, self._d / 2, 0)
            polygon += Point3D(self._bf / 2, self._d / 2, 0)
            rounded_part = self._round_lines_by_radius(
                Line3D(
                    Point3D(self._bf / 2, self._d / 2, 0),
                    Point3D(self._bf / 2, self._d / 2 - self._tf, 0),
                ),
                Line3D(
                    Point3D(self._bf / 2, self._d / 2 - self._tf, 0),
                    Point3D(self._tw / 2, self._d / 2 - self._tf, 0),
                ),
                exterior_rounding_radius,
            )
            for pnt in rounded_part.Points:
                polygon += pnt
            rounded_part = self._round_lines_by_radius(
                Line3D(
                    Point3D(self._bf / 2, self._d / 2 - self._tf, 0),
                    Point3D(self._tw / 2, self._d / 2 - self._tf, 0),
                ),
                Line3D(
                    Point3D(self._tw / 2, self._d / 2 - self._tf, 0),
                    Point3D(self._tw / 2, -self._d / 2 + self._tf, 0),
                ),
                interior_rounding_radius,
            )
            for pnt in rounded_part.Points:
                polygon += pnt
            rounded_part = self._round_lines_by_radius(
                Line3D(
                    Point3D(self._tw / 2, self._d / 2 - self._tf, 0),
                    Point3D(self._tw / 2, -self._d / 2 + self._tf, 0),
                ),
                Line3D(
                    Point3D(self._tw / 2, -self._d / 2 + self._tf, 0),
                    Point3D(self._bf / 2, -self._d / 2 + self._tf, 0),
                ),
                interior_rounding_radius,
            )
            for pnt in rounded_part.Points:
                polygon += pnt
            rounded_part = self._round_lines_by_radius(
                Line3D(
                    Point3D(self._tw / 2, -self._d / 2 + self._tf, 0),
                    Point3D(self._bf / 2, -self._d / 2 + self._tf, 0),
                ),
                Line3D(
                    Point3D(self._bf / 2, -self._d / 2 + self._tf, 0),
                    Point3D(self._bf / 2, -self._d / 2, 0),
                ),
                exterior_rounding_radius,
            )
            for pnt in rounded_part.Points:
                polygon += pnt
            polygon += Point3D(self._bf / 2, -self._d / 2, 0)
            polygon += Point3D(-self._bf / 2, -self._d / 2, 0)
            rounded_part = self._round_lines_by_radius(
                Line3D(
                    Point3D(-self._bf / 2, -self._d / 2, 0),
                    Point3D(-self._bf / 2, -self._d / 2 + self._tf, 0),
                ),
                Line3D(
                    Point3D(-self._bf / 2, -self._d / 2 + self._tf, 0),
                    Point3D(-self._tw / 2, -self._d / 2 + self._tf, 0),
                ),
                exterior_rounding_radius,
            )
            for pnt in rounded_part.Points:
                polygon += pnt
            rounded_part = self._round_lines_by_radius(
                Line3D(
                    Point3D(-self._bf / 2, -self._d / 2 + self._tf, 0),
                    Point3D(-self._tw / 2, -self._d / 2 + self._tf, 0),
                ),
                Line3D(
                    Point3D(-self._tw / 2, -self._d / 2 + self._tf, 0),
                    Point3D(-self._tw / 2, self._d / 2 - self._tf, 0),
                ),
                interior_rounding_radius,
            )
            for pnt in rounded_part.Points:
                polygon += pnt
            rounded_part = self._round_lines_by_radius(
                Line3D(
                    Point3D(-self._tw / 2, -self._d / 2 + self._tf, 0),
                    Point3D(-self._tw / 2, self._d / 2 - self._tf, 0),
                ),
                Line3D(
                    Point3D(-self._tw / 2, self._d / 2 - self._tf, 0),
                    Point3D(-self._bf / 2, self._d / 2 - self._tf, 0),
                ),
                interior_rounding_radius,
            )
            for pnt in rounded_part.Points:
                polygon += pnt
            rounded_part = self._round_lines_by_radius(
                Line3D(
                    Point3D(-self._tw / 2, self._d / 2 - self._tf, 0),
                    Point3D(-self._bf / 2, self._d / 2 - self._tf, 0),
                ),
                Line3D(
                    Point3D(-self._bf / 2, self._d / 2 - self._tf, 0),
                    Point3D(-self._bf / 2, self._d / 2, 0),
                ),
                exterior_rounding_radius,
            )
            for pnt in rounded_part.Points:
                polygon += pnt
            polygon += Point3D(-self._bf / 2, self._d / 2, 0)
        else:
            polygon += Point3D(-self._bf / 2, self._d / 2, 0)
            polygon += Point3D(self._bf / 2, self._d / 2, 0)
            polygon += Point3D(self._bf / 2, self._d / 2 - self._tf, 0)
            polygon += Point3D(self._tw / 2, self._d / 2 - self._tf, 0)
            polygon += Point3D(self._tw / 2, -self._d / 2 + self._tf, 0)
            polygon += Point3D(self._bf / 2, -self._d / 2 + self._tf, 0)
            polygon += Point3D(self._bf / 2, -self._d / 2, 0)
            polygon += Point3D(-self._bf / 2, -self._d / 2, 0)
            polygon += Point3D(-self._bf / 2, -self._d / 2 + self._tf, 0)
            polygon += Point3D(-self._tw / 2, -self._d / 2 + self._tf, 0)
            polygon += Point3D(-self._tw / 2, self._d / 2 - self._tf, 0)
            polygon += Point3D(-self._bf / 2, self._d / 2 - self._tf, 0)
            polygon += Point3D(-self._bf / 2, self._d / 2, 0)

        return polygon

    def show(self):
        return self._data["beam_type"] == 2

    def __str__(self):
        return "H-Beam"
