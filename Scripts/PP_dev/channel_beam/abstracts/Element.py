import abc
from typing import Any, List, Set, Tuple

import NemAll_Python_BaseElements as AllplanBaseElements
from NemAll_Python_Geometry import Move, Point3D, Polyhedron3D, Vector3D


class Element(abc.ABC):

    elements_displayable = {"creatable": [], "removable": []}

    def __init__(self, data):
        self._com_prop: Any = AllplanBaseElements.CommonProperties()
        self._com_prop.GetGlobalProperties()
        self._data = data
        self._weight = 0
        self._child_elements: Set[Element] = set()
        self._reference_point: Point3D = Point3D(0, 0, 0)
        self._shift_vectors: List[Vector3D] = list()
        self._reference_point_not_updated_error: Any = Exception(
            " class reference point has not been updated!\n " + "Continue after update!"
        )

    # --------------- Getters and Setters ----------------------
    @property
    def com_prop(self) -> Any:
        """Get standart common properties"""
        return self._com_prop

    @com_prop.setter
    def com_prop(self, value):
        """Set standart common properties"""
        self._com_prop = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def reference_point(self) -> Point3D:
        return self._reference_point

    @reference_point.setter
    def reference_point(self, value: Point3D):
        self._reference_point = value

    # @property
    # def shift_vector(self) -> Vector3D:
    #    return self._shift_vector

    # --------------- End of Getters and Setters ----------------------
    def build(self):
        elements_list: List[Tuple[Any, Polyhedron3D]] = list()
        if self.show():
            for element in self.create():
                element = Move(element, Vector3D(self.reference_point))
                elements_list.append((self, element))

        if not self.empty_child_elements():
            for element in self.get_child_elements():
                elements_list.extend(element.build())
        return elements_list

    def get_weight(self):
        """
        Get weight of an element and all child elements
        """
        if self.show():
            self._weight += self.calculate_weight()

        if not self.empty_child_elements():
            for element in self.get_child_elements():
                self._weight += element.get_weight()

        return self._weight

    def get_child_elements(self):
        return self._child_elements

    def empty_child_elements(self) -> bool:
        return len(self._child_elements) == 0

    def move_reference_point(self, shift_vectors):
        for shift_vector in shift_vectors:
            self._reference_point = Move(self.reference_point, shift_vector)

    def add_child_element(
        self,
        child_element: Any,
        child_local_point: Point3D,
        child_shift_vector: Vector3D,
    ) -> None:
        child_shift_vector = child_element.define_child_vector(
            child_shift_vector, child_local_point
        )
        child_element._shift_vectors.extend(self._shift_vectors)
        child_element._shift_vectors.append(child_shift_vector)

        child_element.move_reference_point(child_element._shift_vectors)

        self._child_elements.add(child_element)

    def remove_child_element(self, child_element: Any):
        if child_element in self._child_elements:
            child_element.shift_vector = None
            self._child_elements.remove(child_element)
            return True
        raise Exception("Nothing to remove!")

    def define_child_vector(self, child_shift_vector, child_local_point):
        return child_shift_vector + Vector3D(child_local_point).Reverse()

    @abc.abstractmethod
    def create(self) -> List[Polyhedron3D]:
        pass

    @abc.abstractmethod
    def show(self) -> bool:
        pass

    @abc.abstractmethod
    def calculate_weight(self):
        """
        Method that calculates this object weight.
        If object has no weight than this method should return 0.
        """
        pass

    @abc.abstractclassmethod
    def __str__(self):
        pass
