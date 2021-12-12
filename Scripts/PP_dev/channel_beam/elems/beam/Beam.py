import abc
import math

import GeometryValidate as GeometryValidate
from NemAll_Python_Geometry import (
    Angle,
    CreatePolyhedron,
    ExtrudedAreaSolid3D,
    FilletCalculus3D,
    Line3D,
    MakeIntersection,
    MakeSubtraction,
    Matrix3D,
    Move,
    Path3D,
    Point3D,
    Polygon3D,
    PolygonalArea3D,
    Polygonize,
    Polyhedron3D,
    Transform,
    Vector3D,
)

from ...abstracts.Element import Element


class Beam(Element, abc.ABC):
    def __init__(self, data):
        super().__init__(data)
        self.__start_point: Point3D = None
        self.__end_point: Point3D = None
        self.__shift_vector: Vector3D = None
        self._length = None
        self._vector = None
        self._angle = None
        self._tilt_beam_shift_x = 0

    def get_width(self):
        return self.data["width"]

    def get_tilt_beam_shift_x(self):
        return self._tilt_beam_shift_x

    def get_length(self):
        if not self.__start_point and not self.__end_point:
            raise Exception("Set start and end point first")
        return self._length

    def get_vector(self):
        return self._vector

    def set_start_point(self, stiffener_left: Element, connector_left: Element):
        if connector_left.show():
            x = connector_left.reference_point.X + connector_left.data["width"]
            y = connector_left.reference_point.Y
            z = connector_left.reference_point.Z + connector_left.data["height"] / 2
        else:
            x = stiffener_left.reference_point.X + stiffener_left.data["width"]
            y = stiffener_left.reference_point.Y
            z = stiffener_left.reference_point.Z + self.data["width"] / 2

        x -= self.data["start_length"]
        z += self.data["start_height"]
        self.__start_point = Point3D(x, y, z)

    def get_start_point(self) -> Point3D:
        return self.__start_point

    def set_end_point(self, stiffener_right: Element, connector_right: Element):
        if connector_right.show():
            x = connector_right.reference_point.X - connector_right.data["width"]
            y = connector_right.reference_point.Y
            z = connector_right.reference_point.Z + connector_right.data["height"] / 2
        else:
            x = stiffener_right.reference_point.X - stiffener_right.data["width"]
            y = stiffener_right.reference_point.Y
            z = stiffener_right.reference_point.Z + self.data["width"] / 2

        x += self.data["end_length"]
        z += self.data["end_height"]
        self.__end_point = Point3D(x, y, z)

        self._vector = Vector3D(self.__start_point, self.__end_point)
        self._length = self._vector.GetLength()
        self._angle = math.degrees(math.atan(self._vector.Z / self._vector.X))
        self.data["width"] = self.data["width"] / math.cos(math.radians(self._angle))

        if self._angle != 0:
            # TODO !!!BAD WAY!!!
            # this is necessary to save correct beam entry length when beam is tilted and edges are cut
            # still has deviation because of start and end point recalculation
            # HOW TO CALCULATE self._angle WITHOUT START AND END POINT??

            # calculate cos of beam angle
            sin_a = self.__calculate_angle_info(self._angle)[0]
            d_x = abs(sin_a) * self.data["d"] / 2

            self.__start_point = self.__start_point + Point3D(-d_x, 0, 0)
            self.__end_point = self.__end_point + Point3D(d_x, 0, 0)
            self._vector = Vector3D(self.__start_point, self.__end_point)
            self._length = self._vector.GetLength()
            self._angle = math.degrees(math.atan(self._vector.Z / self._vector.X))

            sin_a, cos_a, _ = self.__calculate_angle_info(self._angle)

            self._tilt_beam_shift_x = abs(sin_a) * self.data["d"]

    def get_end_point(self) -> Point3D:
        return self.__end_point

    def get_shift_vector(self, shiftable_point: Point3D):
        """
        Shiftable point = point we will shift from
        e.g. shift the beam from left stiffener ref point
        means that left stiffener ref point is a shiftable point
        """
        return Vector3D(shiftable_point, self.__start_point)

    def create(self):
        polygon = self.create_shape()
        polyhedron = self._extrude(polygon)
        polyhedron = self.__rotate_element(
            polyhedron, Line3D(0, 0, 0, 0, 1, 0), self.__get_degree_angle(90)
        )
        polyhedron = self.__rotate_element(
            polyhedron, Line3D(0, 0, 0, 1, 0, 0), self.__get_degree_angle(-90)
        )
        polyhedron = self.__transform_element(
            polyhedron,
            Line3D(0, 0, 0, 0, 1, 0),
            self.__get_degree_angle(-self._angle),
            Vector3D(0, 0, 0),
        )

        polyhedron = self.__cut_edges(polyhedron, self.data)

        return [polyhedron]

    def __cut_edges(self, beam_geometry, beam_data):
        # cut edges of beam, so they are || axis Z

        if self._angle == 0:
            return beam_geometry

        sin_a, cos_a, _ = self.__calculate_angle_info(self._angle)

        shift_x = abs(sin_a) * beam_data["d"]
        shift_y = 2 * beam_data["bf"]
        shift_z = 2 * abs(cos_a) * beam_data["d"]

        end_beam_z = self.get_vector().Z
        end_beam_x = abs(cos_a) * self.get_length()

        intersect_polyhedron = Polyhedron3D.CreateCuboid(shift_x, shift_y, shift_z)

        intersect_geometry_left = self.__define_intersection(
            -shift_x / 2,
            -shift_y / 2,
            -shift_z / 2,
            intersect_polyhedron,
            beam_geometry,
        )

        intersect_geometry_right = self.__define_intersection(
            end_beam_x - shift_x / 2,
            -shift_y / 2,
            end_beam_z - shift_z / 2,
            intersect_polyhedron,
            beam_geometry,
        )

        err, subtract_geometry = MakeSubtraction(beam_geometry, intersect_geometry_left)
        err, subtract_geometry = MakeSubtraction(
            subtract_geometry, intersect_geometry_right
        )

        return subtract_geometry

    def __define_intersection(
        self, shift_x, shift_y, shift_z, intersect_polyhedron, main_geometry
    ):
        trans_to_ref_point = Matrix3D()
        trans_to_ref_point.Translate(Vector3D(shift_x, shift_y, shift_z))

        intersect_polyhedron = Transform(intersect_polyhedron, trans_to_ref_point)
        err, intersect_geometry = MakeIntersection(main_geometry, intersect_polyhedron)

        return intersect_geometry
        # return intersect_polyhedron

    def calculate_weight(self):
        weight = 0.0
        nominal_weight = self.data["W"]

        if self.data["beam_unit"] == "imperial":
            length = self._length / 304.8
        else:
            length = self._length / 1000

        weight = nominal_weight * length

        if self.data["beam_unit"] == "imperial":
            weight = weight / 2.2046

        return weight

    @abc.abstractclassmethod
    def create_shape(self) -> Polygon3D:
        pass

    def _extrude(self, sect_poly):
        area = PolygonalArea3D()
        # area += self.sect_poly
        area += sect_poly

        solid = ExtrudedAreaSolid3D()
        solid.SetDirection(Vector3D(0, 0, self._length))
        solid.SetExtrudedArea(area)

        err, element3d = CreatePolyhedron(solid)
        if GeometryValidate.polyhedron(err):
            return element3d
        pass

    def _round_lines_by_radius(self, line1, line2, radius, number_of_segments=22):
        _, line1, line2, fillet = FilletCalculus3D.Calculate(line1, line2, radius)
        path = Path3D()
        path += fillet
        polyline = Polygonize(path, number_of_segments)
        return polyline

    def __get_degree_angle(self, deg):
        # set degrees as unit (radians are default)
        rot_angle = Angle()
        rot_angle.SetDeg(deg)
        return rot_angle

    def __calculate_beam_angle(self):
        return math.degrees(math.acos(self.get_vector().X / self.get_length()))

    def __calculate_angle_info(self, tilt_angle):
        # calculate sin and cos
        sin_a = math.sin(math.radians(tilt_angle))
        cos_a = math.cos(math.radians(tilt_angle))
        tg_a = math.tan(math.radians(tilt_angle))

        return sin_a, cos_a, tg_a

    def __transform_element(self, polyhedron, rot_vector, rot_angle, move_coords):
        rotated_element = self.__rotate_element(polyhedron, rot_vector, rot_angle)
        moved_element = Move(rotated_element, move_coords)
        return moved_element

    def __rotate_element(self, polyhedron, rot_vector, rot_angle):
        transform_profile = Matrix3D()
        transform_profile.Rotation(rot_vector, rot_angle)
        return Transform(polyhedron, transform_profile)
