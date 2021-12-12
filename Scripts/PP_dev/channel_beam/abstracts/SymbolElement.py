import abc
from typing import Any, List


class SymbolElement(abc.ABC):
    def __init__(self) -> None:
        self.model_ele_list: List[Any] = []
        pass

    abc.abstractmethod

    def create_element(self) -> List[Any]:
        raise NotImplementedError(
            "Implement method create_element in %s" % self.__class__.__name__
        )
