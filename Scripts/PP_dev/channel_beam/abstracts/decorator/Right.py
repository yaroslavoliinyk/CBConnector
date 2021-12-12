from typing import Any, List

from NemAll_Python_Geometry import Mirror, Plane3D, Point3D, Polyhedron3D, Vector3D

from .Decorator import Decorator


class Right(Decorator):
    __horizontal: float = 0.0
    __vertical: float = 0.0
    __plane: Plane3D = None
    __full_plane: Plane3D = None

    def __init__(
        self,
        element,
        symmetric_element_data: Any = None,
        symmetric: bool = False,
        data_not_to_copy: List[str] = [],  # noqa: B006
    ):
        if symmetric:
            for data_member_key in symmetric_element_data:
                if data_member_key not in data_not_to_copy:
                    element.data[data_member_key] = symmetric_element_data[
                        data_member_key
                    ]
        super().__init__(element)
        # self.move_reference_point(Vector3D(Right.horizontal, 0, Right.vertical))
        self.move_reference_point([Vector3D(Right.__horizontal, 0, Right.__vertical)])

    @staticmethod
    def set_offset(horizontal, vertical):
        Right.__horizontal = horizontal
        Right.__vertical = vertical
        p1 = Point3D(0, 0, 0)
        p2 = Point3D(0, 1, 0)
        p3 = Point3D(0, 0, 1)
        Right.__plane = Plane3D(p1, p2, p3)

        p1 = Point3D(Right.__horizontal / 2, 0, 0)
        p2 = Point3D(Right.__horizontal / 2, 1, 0)
        p3 = Point3D(Right.__horizontal / 2, 0, 1)
        Right.__full_plane = Plane3D(p1, p2, p3)

    def create(self) -> List[Polyhedron3D]:
        # return self._element.create()
        elements = self._element.create()
        for i in range(len(elements)):
            elements[i] = Mirror(elements[i], Right.__plane)
        return elements

    """def add_child_element(
        self,
        child_element: Any,
        child_local_point: Point3D,
        child_shift_vector: Vector3D,
    ):
        child_shift_vector = child_shift_vector + Vector3D(child_local_point).Reverse()
        child_shift_vector = Mirror(child_shift_vector, Right.__full_plane)
        child_element._shift_vectors.extend(self._shift_vectors)
        child_element._shift_vectors.append(child_shift_vector)

        child_element.move_reference_point(child_element._shift_vectors)
        self._child_elements.add(child_element)"""

    def define_child_vector(self, child_shift_vector, child_local_point):
        child_shift_vector = child_shift_vector + Vector3D(child_local_point).Reverse()
        child_shift_vector = Mirror(child_shift_vector, Right.__full_plane)

        return child_shift_vector

    def __str__(self):
        return "Right " + str(self._element)
