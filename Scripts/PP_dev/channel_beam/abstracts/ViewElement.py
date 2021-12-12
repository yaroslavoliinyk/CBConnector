import abc
from typing import Any, List, Tuple

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Utility as AllplanUtility
from NemAll_Python_Geometry import Point3D, Polyhedron3D

from ..elems.DimensionBatch import DimensionBatch
from .SymbolElement import SymbolElement

ViewMatTypes = {
    "top": AllplanGeo.eProjectionMatrixType.TOP_2D,
    "front": AllplanGeo.eProjectionMatrixType.FRONT_2D,
    "back": AllplanGeo.eProjectionMatrixType.REAR_2D,
    "left": AllplanGeo.eProjectionMatrixType.LEFT_2D,
    "right": AllplanGeo.eProjectionMatrixType.RIGHT_2D,
    "bottom": AllplanGeo.eProjectionMatrixType.BOTTOM_2D,
}

SectionDirections = {
    "top": AllplanGeo.Vector3D(0, 0, -1),
    "front": AllplanGeo.Vector3D(0, 1, 0),
    "back": AllplanGeo.Vector3D(0, -1, 0),
    "left": AllplanGeo.Vector3D(1, 0, 0),
    "right": AllplanGeo.Vector3D(-1, 0, 0),
    "bottom": AllplanGeo.Vector3D(0, 0, 1),
}


class ViewElement(abc.ABC):
    def __init__(self, data):
        self._section_general_properties: AllplanBasisElements.SectionGeneralProperties = (
            self.__get_general_sect_props()
        )
        self._data = data
        self._dimension_elements: List[
            AllplanBasisElements.DimensionLineElement
        ] = list()
        self._text_elements: List[AllplanBasisElements.TextElement] = list()
        self._symbol_elements: List[SymbolElement] = list()
        self._reference_point: Point3D = Point3D(0, 0, 0)

    # --------------- Getters and Setters ----------------------

    @property
    def section_general_properties(
        self,
    ) -> AllplanBasisElements.SectionGeneralProperties:
        """Get section common properties"""
        return self._section_general_properties

    @section_general_properties.setter
    def section_general_properties(
        self, value: AllplanBasisElements.SectionGeneralProperties
    ):
        """Set section common properties"""
        self._section_general_properties = value

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

    # --------------- End of Getters and Setters ----------------------
    def create(self):
        """
        To create view element we need to get all properties of view element,
        Set placement point, Set dimension elements, Get other symbols

        :return: NemAll_Python_BasisElements.ViewSectionElement
        """
        view_ele = None
        elements_list: List[Any] = []
        if self.show():
            view_ele = AllplanBasisElements.ViewSectionElement()

            self.section_general_properties.PlacementPoint = AllplanGeo.Point2D(
                self.reference_point
            )

            view_ele.GeneralSectionProperties = self.section_general_properties
            view_ele.ViewMatrix = self.get_view_matrix()
            view_ele.TextElements = self._text_elements
            view_ele.DimensionElements = self._dimension_elements
            view_ele.SectionDefinitionData = self.__get_section_def_data()

            if len(self._symbol_elements) != 0:
                for element in self._symbol_elements:
                    elements_list.extend(element.create_element())
        return view_ele, elements_list

    def __get_section_def_data(self) -> AllplanBasisElements.SectionDefinitionData:
        section_def_data = AllplanBasisElements.SectionDefinitionData()
        section_def_data.SectionBody = self.get_section_body()
        section_def_data.ClippingPath = self.get_clipping_path()
        section_def_data.DirectionVector = self.get_direction_vector()
        return section_def_data

    def __get_general_sect_props(self) -> AllplanBasisElements.SectionGeneralProperties:
        """
        Method initialize the section and view properties from default settings

        :return:            NemAll_Python_BasisElements.SectionGeneralProperties - general view properties
        """
        # ----------------- initialize the section and view properties
        view_props = AllplanBasisElements.SectionGeneralProperties(True)

        view_format_props = view_props.FormatProperties
        view_filter_props = view_props.FilterProperties
        view_label_props = view_props.LabelingProperties

        # ----------------- section format properties
        view_format_props.IsEliminationOn = True
        view_format_props.EliminationAngle = 22

        # ----------------- labeling properties
        view_label_props.HeadingOn = False

        # ----------------- section drawing files properties
        view_draw_files_props = AllplanBasisElements.SectionDrawingFilesProperties()

        drawing_file_number = AllplanUtility.VecIntList()
        drawing_file_number.append(
            AllplanBaseElements.DrawingFileService.GetActiveFileNumber()
        )

        view_draw_files_props.DrawingNumbers = drawing_file_number

        # ----------------- section filter properties
        view_filter_props.DrawingFilesProperties = view_draw_files_props

        # ----------------- general section properties
        view_props = AllplanBasisElements.SectionGeneralProperties(True)

        view_props.Status = AllplanBasisElements.SectionGeneralProperties.State.Hidden
        view_props.ShowSectionBody = True
        view_props.FormatProperties = view_format_props
        view_props.FilterProperties = view_filter_props
        view_props.LabelingProperties = view_label_props
        view_props.PlacementPointType = (
            AllplanBasisElements.SectionGeneralProperties.PlacementPointPosition.TopLeft
        )

        return view_props

    def set_dimensions(self, dimensions: DimensionBatch):
        if dimensions:
            for dim_ele in dimensions:
                self._dimension_elements.append(dim_ele)

    @abc.abstractmethod
    def get_min_max_lev(self) -> Tuple[Any, Any]:
        raise NotImplementedError(
            "Implement method __get_min_max_lev in %s" % self.__class__.__name__
        )

    @abc.abstractmethod
    def get_view_matrix(self) -> AllplanGeo.Matrix3D:
        raise NotImplementedError(
            "Implement method __get_view_matrix in %s" % self.__class__.__name__
        )

    @abc.abstractmethod
    def get_section_body(self) -> Polyhedron3D:
        raise NotImplementedError(
            "Implement method __get_section_body in %s" % self.__class__.__name__
        )

    @abc.abstractmethod
    def get_clipping_path(self) -> AllplanGeo.Polyline2D:
        raise NotImplementedError(
            "Implement method __get_clipping_path in %s" % self.__class__.__name__
        )

    @abc.abstractmethod
    def get_direction_vector(self) -> AllplanGeo.Vector3D:
        raise NotImplementedError(
            "Implement method __get_direction_vector in %s" % self.__class__.__name__
        )

    @abc.abstractmethod
    def show(self) -> bool:
        raise NotImplementedError(
            "Implement method show in %s" % self.__class__.__name__
        )

    @abc.abstractclassmethod
    def __str__(self):
        raise NotImplementedError(
            "Implement method __str__ in %s" % self.__class__.__name__
        )
