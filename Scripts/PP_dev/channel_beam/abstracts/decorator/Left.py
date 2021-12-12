from typing import Any, List

from NemAll_Python_Geometry import Polyhedron3D

from .Decorator import Decorator


class Left(Decorator):
    def __init__(
        self,
        element,
        symmetric_element_data: Any = None,
        symmetric: bool = False,
        data_not_to_copy: List[str] = [],  # noqa: B006
    ):
        # super().__init__(element)
        if symmetric:
            for data_member_key in symmetric_element_data:
                if data_member_key not in data_not_to_copy:
                    element.data[data_member_key] = symmetric_element_data[
                        data_member_key
                    ]

        Decorator.__init__(self, element)

    def create(self) -> List[Polyhedron3D]:
        return self._element.create()

    def __str__(self):
        return "Left " + str(self._element)
