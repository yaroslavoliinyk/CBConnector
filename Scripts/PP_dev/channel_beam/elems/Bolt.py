import math

import NemAll_Python_Geometry as AllplanGeo

from ..abstracts.Removable import Removable


class BoltBatch(Removable):
    def __init__(self, data):
        super().__init__(data)
        self._count_of_segments = 20
        self._length = 500
        # print("\nCreate Bolt Batch")

    def create(self):
        bolt_batch = []

        if self.data["bolts_number_x"] > 1:
            step_x = (self.data["placement_width"] - 2 * self.data["edge_distance"]) / (
                self.data["bolts_number_x"] - 1
            )

            x_range = list(
                self.__float_range(
                    self.data["edge_distance"]
                    + self.data["shift_x"] / 2 * self.data["side_sign"],
                    self.data["placement_width"]
                    - self.data["edge_distance"]
                    + self.data["shift_x"] / 2 * self.data["side_sign"],
                    step_x,
                )
            )
        else:
            x_range = [(self.data["placement_width"] + self.data["shift_x"]) / 2]

        if self.data["bolts_number_z"] > 1:
            step_z = (
                self.data["placement_height"] - 2 * self.data["edge_distance"]
            ) / (self.data["bolts_number_z"] - 1)

            z_range = list(
                self.__float_range(
                    self.data["edge_distance"],
                    self.data["placement_height"] - self.data["edge_distance"],
                    step_z,
                )
            )
        else:
            z_range = [self.data["placement_height"] / 2]

        for i in z_range:
            for j in x_range:
                bolt = self.__create_bolt_geometry(AllplanGeo.Point3D(j, 0, i))
                bolt_batch.append(bolt)

        return bolt_batch

    def show(self) -> bool:
        return self.data["is_shown"]

    def calculate_weight(self):
        return 0

    def __str__(self):
        return "Bolts Batch"

    def __create_bolt_geometry(self, location):
        cylinder = AllplanGeo.Cylinder3D(
            self.data["diameter"] / 2.0,
            self.data["diameter"] / 2.0,
            AllplanGeo.Point3D(0, 0, self._length),
        )
        cylinder = AllplanGeo.Move(
            cylinder, AllplanGeo.Vector3D(0, 0, -self._length / 2.0)
        )
        cylinder = AllplanGeo.Rotate(
            cylinder,
            AllplanGeo.Axis3D(
                AllplanGeo.Point3D(0, 0, 0), AllplanGeo.Vector3D(1, 0, 0)
            ),
            AllplanGeo.Angle(math.pi / 2),
        )
        geometry = AllplanGeo.Move(cylinder, AllplanGeo.Vector3D(location))
        err, geometry = AllplanGeo.CreatePolyhedron(geometry, self._count_of_segments)
        return geometry

    def __float_range(self, start, stop, step):
        # generator for float range
        if stop <= start:
            return

        while start <= stop + 0.001:
            yield float(start)
            start += abs(step)
