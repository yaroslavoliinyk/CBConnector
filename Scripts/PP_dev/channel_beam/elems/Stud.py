import math

from NemAll_Python_Geometry import (
    Angle,
    CalcMass,
    CreatePolyhedron,
    Cylinder3D,
    Line3D,
    MakeUnion,
    Matrix3D,
    Move,
    Point3D,
    Transform,
    Vector3D,
)

from ..abstracts.Element import Element


class StudsBatch(Element):
    # Filled with left bolt batch settings if they are symmetric
    # data_left = {}

    def __init__(self, data):
        super().__init__(data)
        self._count_of_segments = 20
        self.beam = data["beam"]
        self.beam_vector = self.beam.get_vector()
        # self._is_shown = is_shown
        # print("Create Stud Batch")

    def show(self) -> bool:
        return self.data["show"]

    def calculate_weight(self):
        weight = 0.0

        stud_geo = self.__create_stud_geometry(Vector3D(0, 0, 0))

        err, volume, _, _ = CalcMass(stud_geo)
        volume = volume / 1000000000

        weight = self.data["density"] * volume * self.data["studs_number"]

        return weight

    def __str__(self):
        return "Studs Batch"

    def __create_stud_geometry(self, location: Vector3D):
        body_cylinder = Cylinder3D(
            self.data["body_diameter"] / 2.0,
            self.data["body_diameter"] / 2.0,
            Point3D(0, 0, self.data["length"]),
        )
        head_cylinder = Cylinder3D(
            self.data["head_diameter"] / 2.0,
            self.data["head_diameter"] / 2.0,
            Point3D(0, 0, self.data["head_height"]),
        )
        head_cylinder = Move(
            head_cylinder,
            Vector3D(0, 0, self.data["length"] - self.data["head_height"]),
        )
        err, body_cylinder_geometry = CreatePolyhedron(
            body_cylinder, self._count_of_segments
        )
        err, head_cylinder_geometry = CreatePolyhedron(
            head_cylinder, self._count_of_segments
        )
        err, geometry = MakeUnion(body_cylinder_geometry, head_cylinder_geometry)
        # self.geometry = Rotate(
        #     self.geometry,
        #     Axis3D(Point3D(0, 0, 0), Vector3D(0, 1, 0)),
        #     self.rotation,
        # )

        geometry = Move(geometry, location)
        return geometry

    def __float_range(self, start, stop, step):
        # generator for float range
        if stop <= start:
            return

        while start <= stop:
            yield float(start)
            start += step

    def create(self):
        studs_batch = []
        beam_vec = self.beam_vector
        beam_length = beam_vec.GetLength()
        beam_width = self.beam.get_width()
        beam_angle = math.degrees(math.atan(self.beam_vector.Z / self.beam_vector.X))
        # This offset need because when we tilt our beam and truncate it,
        # we need to count the truncated part, too.
        add_offset = beam_width * math.tan(math.radians(beam_angle))
        # beam_length = beam_length - add_offset

        step = (beam_length - self.data["start_offset"] - self.data["end_offset"]) / (
            self.data["studs_number"] - 1
        )

        """
        add_offset = beam_width * math.tan(math.radians(beam_angle))
        if(self.beam_vector.Z > 0):
            self.data["start_offset"] += add_offset
        else:
            self.data["end_offset"] += add_offset
        beam_length += add_offset
        """
        x_range = self.__float_range(
            self.data["start_offset"], beam_length - self.data["end_offset"], step
        )

        first = True
        steps = 0
        for j in x_range:
            if first:
                first = False
                j += add_offset / 2
            if steps == self.data["studs_number"] - 1:
                j -= add_offset / 2
            bolt = self.__create_stud_geometry(Vector3D(j, 0, 0))
            bolt = self.__transform_element(
                bolt,
                Line3D(0, 0, 0, 0, 1, 0),
                self.__get_degree_angle(-beam_angle),
                Vector3D(0, 0, 0),
            )
            studs_batch.append(bolt)
            steps += 1

        return studs_batch

    def __get_degree_angle(self, deg):
        # set degrees as unit (radians are default)
        rot_angle = Angle()
        rot_angle.SetDeg(deg)
        return rot_angle

    def __transform_element(self, polyhedron, rot_vector, rot_angle, move_coords):
        rotated_element = self.__rotate_element(polyhedron, rot_vector, rot_angle)
        moved_element = Move(rotated_element, move_coords)
        return moved_element

    def __rotate_element(self, polyhedron, rot_vector, rot_angle):
        transform_profile = Matrix3D()
        transform_profile.Rotation(rot_vector, rot_angle)
        return Transform(polyhedron, transform_profile)
