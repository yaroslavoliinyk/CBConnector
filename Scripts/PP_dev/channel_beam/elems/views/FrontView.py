from typing import Any, List, Tuple

import NemAll_Python_Geometry as AllplanGeo
from StdReinfShapeBuilder.RotationAngles import RotationAngles

from ...abstracts.ViewElement import SectionDirections, ViewElement, ViewMatTypes
from ..DimensionBatch import DimensionBatch
from ..symbols.SpecialDimensionSymbol import SpecialDimensionSymbol
from ..symbols.WeldSymbol import WeldSymbol


class FrontView(ViewElement):
    def __init__(self, data):
        super().__init__(data)
        self.z_rotation: AllplanGeo.Angle = AllplanGeo.Angle(0)
        self.z_rotation.SetDeg(data["z_rotation"])
        self.min_max_box: AllplanGeo.MinMax3D = None
        self.symbols_shift_vector: AllplanGeo.Vector2D() = None

    def set_min_max_box(self, geometries) -> None:
        max_x = max([pnt.X for pnt in geometries[0].GetVertices()])
        max_y = max([pnt.Y for pnt in geometries[0].GetVertices()])
        max_z = max([pnt.Z for pnt in geometries[0].GetVertices()])
        min_x = min([pnt.X for pnt in geometries[0].GetVertices()])
        min_y = min([pnt.Y for pnt in geometries[0].GetVertices()])
        min_z = min([pnt.Z for pnt in geometries[0].GetVertices()])

        for geometry in geometries:
            if len(geometry.GetVertices()) > 0:
                new_max_x = max([pnt.X for pnt in geometry.GetVertices()])
                max_x = new_max_x if new_max_x > max_x else max_x

                new_max_y = max([pnt.Y for pnt in geometry.GetVertices()])
                max_y = new_max_y if new_max_y > max_y else max_y

                new_max_z = max([pnt.Z for pnt in geometry.GetVertices()])
                max_z = new_max_z if new_max_z > max_z else max_z

                new_min_x = min([pnt.X for pnt in geometry.GetVertices()])
                min_x = new_min_x if new_min_x < min_x else min_x

                new_min_y = min([pnt.Y for pnt in geometry.GetVertices()])
                min_y = new_min_y if new_min_y < min_y else min_y

                new_min_z = min([pnt.Z for pnt in geometry.GetVertices()])
                min_z = new_min_z if new_min_z < min_z else min_z

        self.min_max_box = AllplanGeo.MinMax3D(
            AllplanGeo.Point3D(min_x, min_y, min_z),
            AllplanGeo.Point3D(max_x, max_y, max_z),
        )

    def add_weld_symbols(self, weld_symbols: List[WeldSymbol]) -> None:
        """
        Method adds objects of WeldSymbol class for main beam in channel beam
        """
        shift_vector = self.get_shift_vector_for_symbols()
        for weld_symbol in weld_symbols:
            weld_symbol.start_points = [
                start_pnt + shift_vector for start_pnt in weld_symbol.start_points
            ]
            weld_symbol.end_point = weld_symbol.end_point + shift_vector
            self._symbol_elements.append(weld_symbol)

    def add_special_dimension_symbols(
        self, special_dim_symbols: List[SpecialDimensionSymbol]
    ) -> None:
        """
        Method adds objects of WeldSymbol class for main beam in channel beam
        """
        shift_vector = self.get_shift_vector_for_symbols()
        for special_dim_symbol in special_dim_symbols:
            special_dim_symbol.start_point = (
                special_dim_symbol.start_point + shift_vector
            )
            special_dim_symbol.end_point = special_dim_symbol.end_point + shift_vector
            self._symbol_elements.append(special_dim_symbol)

    def get_shift_vector_for_symbols(self) -> AllplanGeo.Vector2D:
        if self.symbols_shift_vector:
            return self.symbols_shift_vector
        else:
            self.symbols_shift_vector = AllplanGeo.Vector2D(
                self.reference_point.X - self.min_max_box.Min.X,
                self.reference_point.Y - self.min_max_box.Min.Z,
            )
            return self.symbols_shift_vector

    def set_dimensions(self, dimensions: DimensionBatch):
        dimensions.rotate_on_z(self.z_rotation)
        super().set_dimensions(dimensions)

    # Redefining ViewElement abstract methods
    def get_view_matrix(self) -> AllplanGeo.Matrix3D:
        return RotationAngles(
            0, 0, -self.z_rotation.GetDeg()
        ).get_rotation_matrix() * AllplanGeo.Matrix3D(ViewMatTypes["front"])

    def get_min_max_lev(self) -> Tuple[Any, Any]:
        return self.min_max_box.Min.Z, self.min_max_box.Max.Z

    def get_section_body(self) -> AllplanGeo.Polyhedron3D:
        section_body = None
        try:
            section_body = AllplanGeo.Polyhedron3D.CreateCuboid(
                self.min_max_box.Min, self.min_max_box.Max
            )
            section_body = AllplanGeo.Rotate(
                section_body,
                AllplanGeo.Axis3D(
                    AllplanGeo.Point3D(0, 0, 0), AllplanGeo.Vector3D(0, 0, 1)
                ),
                self.z_rotation,
            )
        except Exception:
            raise Exception("Cannot create section body for view element")
        return section_body

    def get_clipping_path(self) -> AllplanGeo.Polyline2D:
        clipping_path = AllplanGeo.Polyline2D()
        try:
            clipping_path += AllplanGeo.Point2D(
                self.min_max_box.Min.X, self.min_max_box.Min.Y
            )
            clipping_path += AllplanGeo.Point2D(
                self.min_max_box.Min.X, self.min_max_box.Max.Y
            )
            clipping_path += AllplanGeo.Point2D(
                self.min_max_box.Max.X, self.min_max_box.Max.Y
            )
            clipping_path += AllplanGeo.Point2D(
                self.min_max_box.Max.X, self.min_max_box.Min.Y
            )
            clipping_path += AllplanGeo.Point2D(
                self.min_max_box.Min.X, self.min_max_box.Min.Y
            )
            clipping_path = AllplanGeo.Rotate(clipping_path, self.z_rotation)
        except Exception:
            raise Exception("Cannot create clipping path")
        return clipping_path

    def get_direction_vector(self):
        return AllplanGeo.Rotate(
            SectionDirections["front"],
            AllplanGeo.Axis3D(
                AllplanGeo.Point3D(0, 0, 0), AllplanGeo.Vector3D(0, 0, 1)
            ),
            self.z_rotation,
        )  # <-- View direction

    def show(self) -> bool:
        return self.data["show"]

    def __str__(self):
        return "FrontView"
