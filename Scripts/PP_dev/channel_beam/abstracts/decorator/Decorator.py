from typing import Any

from NemAll_Python_Geometry import Point3D, Vector3D

from ..Element import Element


class Decorator(Element):
    def __init__(self, element: Element):
        super().__init__(element.data)
        self._element = element

    # --------------- End of Getters and Setters ----------------------

    def build(self):
        return Element.build(self)

    def calculate_weight(self):
        return self._element.calculate_weight()

    def add_child_element(
        self,
        child_element: Any,
        child_local_point: Point3D,
        child_shift_vector: Vector3D,
    ) -> None:
        Element.add_child_element(
            self, child_element, child_local_point, child_shift_vector
        )

    def show(self) -> bool:
        return self._element.show()
