import sys
from typing import List

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Utility as AllplanUtil
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
from NemAll_Python_Geometry import (
    Angle,
    Line3D,
    MakeSubtraction,
    Matrix3D,
    Move,
    Point2D,
    Point3D,
    Polyhedron3D,
    Transform,
    Vector2D,
    Vector3D,
    eGeometryErrorCode,
)
from PythonPart import PythonPart, View2D3D

from .abstracts.decorator.Left import Left
from .abstracts.decorator.Right import Right
from .abstracts.Element import Element
from .abstracts.SymbolElement import SymbolElement
from .elems.beam.CBeam import CBeam
from .elems.beam.HBeam import HBeam
from .elems.beam.Setup import Setup
from .elems.Bolt import BoltBatch
from .elems.Connector import Connector
from .elems.DimensionBatch import DimensionBatch
from .elems.Pillar import Pillar
from .elems.Stiffener import Stiffener
from .elems.Stud import StudsBatch
from .elems.symbols.SpecialDimensionSymbol import SpecialDimensionSymbol
from .elems.symbols.WeldSymbol import WeldSymbol
from .elems.views.FrontView import FrontView

setup: Setup = None


def check_allplan_version(build_ele, version):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Delete unused arguments
    del build_ele
    del version

    # Support all versions
    return True


def modify_element_property(build_ele, name, value):
    """
    Modify property of element

    Args:
        build_ele:  the building element.
        name:       the name of the property.
        value:      new value for property.

    Returns:
        True/False if palette refresh is necessary
    """
    if name == "BoltEdgeOffsetBeamLeft":
        if value >= build_ele.BeamStartLength.value / 2:
            build_ele.BoltEdgeOffsetBeamLeft.value = build_ele.BeamStartLength.value / 4
            msg = AllplanUtil.ShowMessageBox(
                "Edge distance to bolt centers can`t exceed beam entry length!",
                AllplanUtil.MB_OK,
            )
            print(msg)

    if name == "BoltEdgeOffsetBeamRight":
        if value >= build_ele.BeamEndLength.value / 2:
            build_ele.BoltEdgeOffsetBeamRight.value = build_ele.BeamEndLength.value / 4
            msg = AllplanUtil.ShowMessageBox(
                "Edge distance to bolt centers can`t exceed beam entry length!",
                AllplanUtil.MB_OK,
            )
            print(msg)

    return True


def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """
    print(sys.version)

    # SET SHIFT VECTOR
    # RightSided.set_shift_vector(
    #    build_ele.XHandleOffset.value, build_ele.ZHandleOffset.value
    # )
    # RightSided.set_symmetric(build_ele.LeftBeamSameAsRightCheckbox.value)
    Setup.upload_data()
    setup = Setup(build_ele.BeamTypeRadioGroup.value, build_ele)
    if build_ele.BeamTypeRadioGroup.value == 1:
        build_ele.SectionName.value = build_ele.CBeamSettingsName.value
        beam_unit = build_ele.CBeamSettingsUnit.value
    elif build_ele.BeamTypeRadioGroup.value == 2:
        build_ele.SectionName.value = build_ele.HBeamSettingsName.value
        beam_unit = build_ele.HBeamSettingsUnit.value
    else:
        raise Exception("Beam Type radio group doesn't exist!!")
    beam_settings = build_ele.SectionName.value

    # ----------------------------------------  MODEL ----------------------------------------------
    model = ChannelBeam(
        {
            "spacing": build_ele.XHandleOffset.value,
            "offset": build_ele.ZHandleOffset.value,
            "pp_name": "ChannelBeam",
            "params_list": build_ele.get_params_list(),
            "hash": build_ele.get_hash(),
            "python_file": build_ele.pyp_file_name,
            "angle": build_ele.ZRotationAngle.value,
            "is_pp": build_ele.CreateAsPythonPartCheckbox.value,
            "handles_params": {
                "left_beam_height": build_ele.LeftBeamHeight.value,
                "flange_thickness": build_ele.LeftBeamFlangeThickness.value,
                "web_thickness": build_ele.LeftBeamWebThickness.value,
                "left_stiffener_width": build_ele.LeftStiffenerPlateWidth.value,
            },
            "weight_measurement": build_ele.WeightAttributeCombobox.value,
            "ref_pnt_offset_vec": Vector3D(0, 0, -build_ele.LeftBeamHeight.value),
        },
        doc,
    )
    Right.set_offset(model.data["spacing"], model.data["offset"])

    # -------------------------------------  PILLAR LEFT ---------------------------------------------
    pillar_left = Left(
        Pillar(
            {
                "height": build_ele.LeftBeamHeight.value,
                "flange_thickness": build_ele.LeftBeamFlangeThickness.value,
                "web_thickness": build_ele.LeftBeamWebThickness.value,
                "offset_flange": build_ele.LeftBeamZOffset.value,
                "offset_web": build_ele.LeftBeamXOffset.value,
                "stiffener_width": build_ele.LeftStiffenerPlateWidth.value,
                "density": 7900,
            }
        )
    )

    pillar_right = Right(
        Pillar(
            {
                "height": build_ele.RightBeamHeight.value,
                "flange_thickness": build_ele.RightBeamFlangeThickness.value,
                "web_thickness": build_ele.RightBeamWebThickness.value,
                "offset_flange": build_ele.RightBeamZOffset.value,
                "offset_web": build_ele.RightBeamXOffset.value,
                "stiffener_width": build_ele.RightStiffenerPlateWidth.value,
                "density": 7900,
            }
        ),
        symmetric_element_data=pillar_left.data,
        symmetric=build_ele.LeftBeamSameAsRightCheckbox.value,
    )

    stiffener_left = Left(
        Stiffener(
            {
                "height": pillar_left.data["height"]
                - pillar_left.data["flange_thickness"] * 2,
                "width": build_ele.LeftStiffenerPlateWidth.value,
                "thickness": build_ele.LeftStiffenerPlateThickness.value,
                "slope_data": {
                    "inner_width": build_ele.LeftStiffenerPlateInnerSlopeWidth.value,
                    "inner_height": build_ele.LeftStiffenerPlateInnerSlopeHeight.value,
                    "top_outer_width": build_ele.LeftStiffenerPlateTopOuterSlopeWidth.value,
                    "top_outer_height": build_ele.LeftStiffenerPlateTopOuterSlopeHeight.value,
                    "bot_outer_width": build_ele.LeftStiffenerPlateBottomOuterSlopeWidth.value,
                    "bot_outer_height": build_ele.LeftStiffenerPlateBottomOuterSlopeHeight.value,
                },
                "pillar_web_thickness": pillar_left.data["web_thickness"],
                "outer": build_ele.LeftOuterStiffenerCheckbox.value,
                "density": 7900,
            }
        )
    )

    stiffener_right = Right(
        Stiffener(
            {
                "height": pillar_right.data["height"]
                - pillar_right.data["flange_thickness"] * 2,
                "width": build_ele.RightStiffenerPlateWidth.value,
                "thickness": build_ele.RightStiffenerPlateThickness.value,
                "slope_data": {
                    "inner_width": build_ele.RightStiffenerPlateInnerSlopeWidth.value,
                    "inner_height": build_ele.RightStiffenerPlateInnerSlopeHeight.value,
                    "top_outer_width": build_ele.RightStiffenerPlateTopOuterSlopeWidth.value,
                    "top_outer_height": build_ele.RightStiffenerPlateTopOuterSlopeHeight.value,
                    "bot_outer_width": build_ele.RightStiffenerPlateBottomOuterSlopeWidth.value,
                    "bot_outer_height": build_ele.RightStiffenerPlateBottomOuterSlopeHeight.value,
                },
                "pillar_web_thickness": pillar_right.data["web_thickness"],
                "outer": build_ele.RightOuterStiffenerCheckbox.value,
                "density": 7900,
            }
        ),
        symmetric_element_data=stiffener_left.data,
        symmetric=build_ele.RightStiffenerSameAsLeft.value,
        data_not_to_copy=["height", "pillar_web_thickness"],
    )

    connector_left = Left(
        Connector(
            {
                "height": build_ele.ConnectorPlateHeightLeft.value,
                "width": build_ele.ConnectorPlateWidthLeft.value,
                "thickness": build_ele.ConnectorPlateThicknessLeft.value,
                "show": build_ele.LeftConnectorPlateCheckbox.value,
                "density": 7900,
            }
        )
    )

    connector_right = Right(
        Connector(
            {
                "height": build_ele.ConnectorPlateHeightRight.value,
                "width": build_ele.ConnectorPlateWidthRight.value,
                "thickness": build_ele.ConnectorPlateThicknessRight.value,
                "show": build_ele.RightConnectorPlateCheckbox.value,
                "density": 7900,
            }
        ),
        symmetric_element_data=connector_left.data,
        symmetric=build_ele.LeftConnectorPlateSameAsRightCheckbox.value,
    )

    # ----------------------------------------  CONNECTOR BOLT BATCH LEFT -----------------------
    connector_bolt_batch_left = Left(
        BoltBatch(
            {
                "diameter": build_ele.BoltDiameterConnectorLeft.value,
                "bolts_number_x": build_ele.BoltNumberXConnectorLeft.value,
                "bolts_number_z": build_ele.BoltNumberYConnectorLeft.value,
                "edge_distance": build_ele.BoltEdgeOffsetConnectorLeft.value,
                "placement_width": stiffener_left.data["width"]
                - pillar_left.data["offset_web"],
                "placement_height": connector_left.data["height"],
                "is_shown": connector_left.data["show"],
                "density": 7900,
                "shift_x": 0,
                "side_sign": 0,
            }
        )
    )
    connector_bolt_batch_right = Right(
        BoltBatch(
            {
                "diameter": build_ele.BoltDiameterConnectorRight.value,
                "bolts_number_x": build_ele.BoltNumberXConnectorRight.value,
                "bolts_number_z": build_ele.BoltNumberYConnectorRight.value,
                "edge_distance": build_ele.BoltEdgeOffsetConnectorRight.value,
                "placement_width": stiffener_right.data["width"]
                - pillar_right.data["offset_web"],
                "placement_height": connector_right.data["height"],
                "is_shown": connector_right.data["show"],
                "density": 7900,
                "shift_x": 0,
                "side_sign": 0,
            }
        ),
        symmetric_element_data=connector_bolt_batch_left.data,
        symmetric=build_ele.LeftConnectorPlateSameAsRightCheckbox.value,
        data_not_to_copy=["placement_width", "placement_height", "is_shown"],
    )

    beam_type = build_ele.BeamTypeRadioGroup.value
    if beam_type == 1:
        full_beam_data = {
            "start_length": build_ele.BeamStartLength.value,
            "start_height": build_ele.BeamStartHeight.value
            if connector_left.show()
            else pillar_left.data["offset_flange"],
            "end_length": build_ele.BeamEndLength.value,
            "end_height": build_ele.BeamEndHeight.value
            if connector_right.show()
            else pillar_right.data["offset_flange"],
            "multiplier": 25.4,
            "rounded": build_ele.IsRoundedChannelBeam.value,
            "beam_type": build_ele.BeamTypeRadioGroup.value,
            "beam_unit": beam_unit,
        }
        full_beam_data.update(setup.cbeam_data(beam_settings, beam_unit))
        beam = CBeam(full_beam_data)
    elif beam_type == 2:
        full_beam_data = {
            "start_length": build_ele.BeamStartLength.value,
            "start_height": build_ele.BeamStartHeight.value
            if connector_left.show()
            else pillar_left.data["offset_flange"],
            "end_length": build_ele.BeamEndLength.value,
            "end_height": build_ele.BeamEndHeight.value
            if connector_right.show()
            else pillar_right.data["offset_flange"],
            "multiplier": 25.4,
            "rounded": build_ele.IsRoundedChannelBeam.value,
            "beam_type": build_ele.BeamTypeRadioGroup.value,
            "beam_unit": beam_unit,
        }
        full_beam_data.update(setup.hbeam_data(beam_settings, beam_unit))
        beam = HBeam(full_beam_data)
    else:
        raise Exception("No such Beam type.")

    # ------ Building everything ------
    model.add_child_element(
        pillar_left,
        child_local_point=Point3D(0, 0, 0),
        child_shift_vector=model.data["ref_pnt_offset_vec"],
    )
    model.add_child_element(
        pillar_right,
        child_local_point=Point3D(0, 0, 0),
        child_shift_vector=model.data["ref_pnt_offset_vec"],
    )

    pillar_left.add_child_element(
        stiffener_left,
        child_local_point=Point3D(0, 0, 0),
        child_shift_vector=Vector3D(
            pillar_left.data["web_thickness"] / 2,
            0,
            pillar_left.data["flange_thickness"],
        ),
    )

    pillar_right.add_child_element(
        stiffener_right,
        child_local_point=Point3D(0, 0, 0),
        child_shift_vector=Vector3D(
            pillar_right.data["web_thickness"] / 2,
            0,
            pillar_right.data["flange_thickness"],
        ),
    )

    stiffener_left.add_child_element(
        connector_left,
        child_local_point=Point3D(0, 0, 0),
        child_shift_vector=Vector3D(
            pillar_left.data["offset_web"],
            stiffener_left.data["thickness"],
            pillar_left.data["offset_flange"],
        ),
    )

    stiffener_right.add_child_element(
        connector_right,
        child_local_point=Point3D(0, 0, 0),
        child_shift_vector=Vector3D(
            pillar_right.data["offset_web"],
            stiffener_right.data["thickness"],
            pillar_right.data["offset_flange"],
        ),
    )

    connector_left.add_child_element(
        connector_bolt_batch_left,
        child_local_point=Point3D(0, 0, 0),
        child_shift_vector=Vector3D(0, 0, 0),
    )

    connector_right.add_child_element(
        connector_bolt_batch_right,
        child_local_point=Point3D(0, 0, 0),
        child_shift_vector=Vector3D(0, 0, 0),
    )

    beam.set_start_point(stiffener_left, connector_left)
    beam.set_end_point(stiffener_right, connector_right)

    # TODO child_local_point now consider only left connector
    # change to consider both connectors
    shift_on_y = beam.data["tw"] / 2.0 if isinstance(beam, HBeam) else beam.data["xb"]

    stiffener_left.add_child_element(
        beam,
        # child_local_point=Point3D(0, shift_on_y, -connector_left.data["height"] / 2),
        child_local_point=Point3D(0, shift_on_y, 0),
        child_shift_vector=beam.get_shift_vector(stiffener_left.reference_point),
    )

    # ----------------------------------------  BEAM BOLT BATCH LEFT -----------------------
    beam_bolt_batch_left = Left(
        BoltBatch(
            {
                "diameter": build_ele.BoltDiameterBeamLeft.value,
                "bolts_number_x": build_ele.BoltNumberXBeamLeft.value,
                "bolts_number_z": build_ele.BoltNumberYBeamLeft.value,
                "edge_distance": build_ele.BoltEdgeOffsetBeamLeft.value,
                "placement_width": beam.data["start_length"],
                "placement_height": min(connector_left.data["height"], beam.get_width())
                if connector_left.show()
                else beam.get_width(),
                "is_shown": True
                if build_ele.ConnectionTypeRadioGroup.value == 1
                else False,
                "shift_x": beam.get_tilt_beam_shift_x(),
                "side_sign": 1,
            }
        )
    )

    # ----------------------------------------  BEAM BOLT BATCH RIGHT ----------------------
    beam_bolt_batch_right = Left(
        BoltBatch(
            {
                "diameter": build_ele.BoltDiameterBeamRight.value,
                "bolts_number_x": build_ele.BoltNumberXBeamRight.value,
                "bolts_number_z": build_ele.BoltNumberYBeamRight.value,
                "edge_distance": build_ele.BoltEdgeOffsetBeamRight.value,
                "placement_width": beam.data["end_length"],
                "placement_height": min(
                    connector_right.data["height"], beam.get_width()
                )
                if connector_right.show()
                else beam.get_width(),
                "is_shown": True
                if build_ele.ConnectionTypeRadioGroup.value == 1
                else False,
                "shift_x": beam.get_tilt_beam_shift_x(),
                "side_sign": -1,
            }
        ),
        symmetric_element_data=beam_bolt_batch_left.data,
        symmetric=build_ele.BeamRightBoltsSameAsLeft.value,
        data_not_to_copy=[
            "placement_width",
            "placement_height",
            "is_shown",
            "side_sign",
        ],
    )

    # ----------------------------------------  STUDS BATCH ----------------------
    studs_batch = StudsBatch(
        {
            "length": build_ele.StudLength.value,
            "body_diameter": build_ele.StudBodyDiameter.value,
            "head_diameter": build_ele.StudHeadDiameter.value,
            "head_height": build_ele.StudHeadHeight.value,
            "studs_number": build_ele.StudNumber.value,
            "start_offset": build_ele.StudStartDistance.value,
            "end_offset": build_ele.StudEndDistance.value,
            "beam": beam,
            "show": build_ele.StudShowCheckbox.value,
            "density": 7900,
        }
    )

    beam.add_child_element(
        studs_batch,
        child_local_point=Point3D(0, 0, 0),
        child_shift_vector=Vector3D(0, 0, beam.get_width() / 2),
    )

    beam.add_child_element(
        beam_bolt_batch_left,
        child_local_point=Point3D(0, 0, 0),
        child_shift_vector=Vector3D(
            0, 0, -beam_bolt_batch_left.data["placement_height"] / 2
        ),
    )

    beam.add_child_element(
        beam_bolt_batch_right,
        child_local_point=Point3D(0, 0, 0),
        child_shift_vector=Vector3D(
            beam.get_vector().X - beam_bolt_batch_right.data["placement_width"],
            0,
            beam.get_vector().Z - beam_bolt_batch_right.data["placement_height"] / 2,
        ),
    )

    # ------ Views creation -------
    front_view = FrontView(
        {
            "z_rotation": model.data["angle"],
            "show": build_ele.CreateViewsCheckbox.value,
        }
    )
    front_view.reference_point = Point3D(0, 500, 0)
    geometries = [
        list_ele[1]
        for list_ele in model.build()
        if str(list_ele[0]).find("Bolts Batch") == -1
    ]
    front_view.set_min_max_box(geometries)

    front_view.reference_point = Move(
        front_view.reference_point,
        Vector3D(0, max([pnt.Y for pnt in front_view.get_clipping_path().Points]), 0),
    )

    dimension_batch_front_view = DimensionBatch(
        AllplanBasisElements.DimensionProperties(
            doc, AllplanBasisElements.Dimensioning.eDimensionLine
        )
    )

    # Left Beam Depth dim
    dimension_batch_front_view.push_back(
        [pillar_left.reference_point,
        pillar_left.reference_point + Vector3D(0, 0, pillar_left.data["height"])],
        Vector2D(-400, 0),
        Vector2D(0, 1),
        " " + build_ele.LeftBeamDepthTailingText.value,
    )

    # Right Beam Depth dim
    if pillar_left.data["height"] != pillar_right.data["height"]:
        dimension_batch_front_view.push_back(
            [pillar_right.reference_point,
            pillar_right.reference_point + Vector3D(0, 0, pillar_right.data["height"])],
            Vector2D(400, 0),
            Vector2D(0, 1),
            " " + build_ele.RightBeamDepthTailingText.value,
        )

    # Beam Spacing dim
    dim_offset = -200 if model.data["offset"] >= 0 else model.data["offset"] - 200
    dimension_batch_front_view.push_back(
        [pillar_left.reference_point,
        pillar_right.reference_point],
        Vector2D(0, dim_offset),
        Vector2D(1, 0),
        " " + build_ele.GirderSpacingTailingText.value,
    )

    # Left Beam bolt batch dimensions
    if (
        beam_bolt_batch_left.data["placement_width"]
        - 2 * beam_bolt_batch_left.data["edge_distance"]
        > 0
        and beam_bolt_batch_left.data["placement_height"]
        - 2 * beam_bolt_batch_left.data["edge_distance"] > 0
    ) and beam_bolt_batch_left.data["is_shown"]:
        if beam_bolt_batch_left.data["bolts_number_x"] > 1:
            beam_bolt_batch_left_step = (
                beam_bolt_batch_left.data["placement_width"]
                - 2 * beam_bolt_batch_left.data["edge_distance"]
            ) / (beam_bolt_batch_left.data["bolts_number_x"] - 1)
            dimension_batch_front_view.push_back(
                [
                    beam_bolt_batch_left.reference_point
                    + Vector3D(
                        beam_bolt_batch_left.data["edge_distance"]
                        + beam_bolt_batch_left.data["shift_x"]
                        / 2
                        * beam_bolt_batch_left.data["side_sign"],
                        0,
                        0,
                    ),
                    beam_bolt_batch_left.reference_point
                    + Vector3D(
                        beam_bolt_batch_left.data["edge_distance"]
                        + beam_bolt_batch_left.data["shift_x"]
                        / 2
                        * beam_bolt_batch_left.data["side_sign"]
                        + beam_bolt_batch_left_step,
                        0,
                        0,
                    ),
                ],
                Vector2D(0, 200),
                Vector2D(1, 0),
                " " + build_ele.LeftBoltPitchTailingText.value,
            )

        dimension_batch_front_view.push_back(
            [
                beam_bolt_batch_left.reference_point
                + Vector3D(
                    beam_bolt_batch_left.data["shift_x"]
                    / 2
                    * beam_bolt_batch_left.data["side_sign"],
                    0,
                    0,
                ),
                beam_bolt_batch_left.reference_point
                + Vector3D(
                    beam_bolt_batch_left.data["shift_x"]
                    / 2
                    * beam_bolt_batch_left.data["side_sign"],
                    0,
                    beam_bolt_batch_left.data["edge_distance"],
                ),
            ],
            Vector2D(200, 0),
            Vector2D(0, 1),
            " " + build_ele.LeftBoltEdgeDistanceTailingText.value,
        )

    # Right Beam bolt batch dimensions
    if (
        beam_bolt_batch_right.data["placement_width"]
        - 2 * beam_bolt_batch_right.data["edge_distance"]
        > 0
        and beam_bolt_batch_right.data["placement_height"]
        - 2 * beam_bolt_batch_right.data["edge_distance"] > 0
    ) and beam_bolt_batch_right.data["is_shown"]:
        if beam_bolt_batch_right.data["bolts_number_x"] > 1:
            beam_bolt_batch_right_step = (
                beam_bolt_batch_right.data["placement_width"]
                - 2 * beam_bolt_batch_right.data["edge_distance"]
            ) / (beam_bolt_batch_right.data["bolts_number_x"] - 1)
            dimension_batch_front_view.push_back(
                [
                    beam_bolt_batch_right.reference_point
                    + Vector3D(
                        beam_bolt_batch_right.data["edge_distance"]
                        + beam_bolt_batch_right.data["shift_x"]
                        / 2
                        * beam_bolt_batch_right.data["side_sign"],
                        0,
                        0,
                    ),
                    beam_bolt_batch_right.reference_point
                    + Vector3D(
                        beam_bolt_batch_right.data["edge_distance"]
                        + beam_bolt_batch_right.data["shift_x"]
                        / 2
                        * beam_bolt_batch_right.data["side_sign"]
                        + beam_bolt_batch_right_step,
                        0,
                        0,
                    ),
                ],
                Vector2D(0, 200),
                Vector2D(1, 0),
                " " + build_ele.RightBoltPitchTailingText.value,
            )

        dimension_batch_front_view.push_back(
            [
                beam_bolt_batch_right.reference_point
                + Vector3D(
                    beam_bolt_batch_right.data["shift_x"]
                    / 2
                    * beam_bolt_batch_right.data["side_sign"],
                    0,
                    0,
                ),
                beam_bolt_batch_right.reference_point
                + Vector3D(
                    beam_bolt_batch_right.data["shift_x"]
                    / 2
                    * beam_bolt_batch_right.data["side_sign"],
                    0,
                    beam_bolt_batch_right.data["edge_distance"],
                ),
            ],
            Vector2D(-200, 0),
            Vector2D(0, 1),
            " " + build_ele.RightBoltEdgeDistanceTailingText.value,
        )

    front_view.set_dimensions(dimension_batch_front_view)

    weld_symbols_list: List[WeldSymbol] = []

    general_weld_props = {
        "weld_type": build_ele.WeldTypeAll.value,
        "location": build_ele.LocationAll.value,
        "groove_type": build_ele.GrooveTypeAll.value,
        "weld_around": build_ele.WeldAroundAll.value,
        "field_weld": build_ele.FieldWeldAll.value,
        "show_size": build_ele.ShowSizeAll.value,
        "weld_size": build_ele.WeldSizeAll.value,
        "weld_size0": build_ele.WeldSizeOAll.value,
        "groove_size": build_ele.GrooveSizeAAll.value,
        "groove_size0": build_ele.GrooveSizeOAll.value,
        "show_length": build_ele.ShowLengthAll.value,
        "weld_length": build_ele.WeldLengthAll.value,
        "weld_length0": build_ele.WeldLengthOAll.value,
        "show_pitch": build_ele.ShowPitchAll.value,
        "weld_pitch": build_ele.WeldPitchAll.value,
        "weld_pitch0": build_ele.WeldPitchOAll.value,
        "tail_note": build_ele.TailNoteAll.value,
    }

    beam_start_pnt = beam.get_start_point()
    beam_end_pnt = beam.get_end_point()

    main_beam_start_weld_symbol = WeldSymbol(
        {
            "weld_type": build_ele.WeldTypeChannelBeamStart.value,
            "location": build_ele.LocationChannelBeamStart.value,
            "groove_type": build_ele.GrooveTypeChannelBeamStart.value,
            "weld_around": build_ele.WeldAroundChannelBeamStart.value,
            "field_weld": build_ele.FieldWeldChannelBeamStart.value,
            "show_size": build_ele.ShowSizeChannelBeamStart.value,
            "weld_size": build_ele.WeldSizeChannelBeamStart.value,
            "weld_size0": build_ele.WeldSizeOChannelBeamStart.value,
            "groove_size": build_ele.GrooveSizeAChannelBeamStart.value,
            "groove_size0": build_ele.GrooveSizeOChannelBeamStart.value,
            "show_length": build_ele.ShowLengthChannelBeamStart.value,
            "weld_length": build_ele.WeldLengthChannelBeamStart.value,
            "weld_length0": build_ele.WeldLengthOChannelBeamStart.value,
            "show_pitch": build_ele.ShowPitchChannelBeamStart.value,
            "weld_pitch": build_ele.WeldPitchChannelBeamStart.value,
            "weld_pitch0": build_ele.WeldPitchOChannelBeamStart.value,
            "tail_note": build_ele.TailNoteChannelBeamStart.value,
        }
        if not build_ele.SameWeldSymbolSettingsForAllCheckbox.value
        else general_weld_props,
        doc,
        [Point2D(beam_start_pnt.X, beam_start_pnt.Z)],
        Vector2D(100, -300),
    )
    if not beam_bolt_batch_left.data["is_shown"]:
        weld_symbols_list.append(main_beam_start_weld_symbol)

    main_beam_end_weld_symbol = WeldSymbol(
        {
            "weld_type": build_ele.WeldTypeChannelBeamEnd.value,
            "location": build_ele.LocationChannelBeamEnd.value,
            "groove_type": build_ele.GrooveTypeChannelBeamEnd.value,
            "weld_around": build_ele.WeldAroundChannelBeamEnd.value,
            "field_weld": build_ele.FieldWeldChannelBeamEnd.value,
            "show_size": build_ele.ShowSizeChannelBeamEnd.value,
            "weld_size": build_ele.WeldSizeChannelBeamEnd.value,
            "weld_size0": build_ele.WeldSizeOChannelBeamEnd.value,
            "groove_size": build_ele.GrooveSizeAChannelBeamEnd.value,
            "groove_size0": build_ele.GrooveSizeOChannelBeamEnd.value,
            "show_length": build_ele.ShowLengthChannelBeamEnd.value,
            "weld_length": build_ele.WeldLengthChannelBeamEnd.value,
            "weld_length0": build_ele.WeldLengthOChannelBeamEnd.value,
            "show_pitch": build_ele.ShowPitchChannelBeamEnd.value,
            "weld_pitch": build_ele.WeldPitchChannelBeamEnd.value,
            "weld_pitch0": build_ele.WeldPitchOChannelBeamEnd.value,
            "tail_note": build_ele.TailNoteChannelBeamEnd.value,
        }
        if not build_ele.SameWeldSymbolSettingsForAllCheckbox.value
        else general_weld_props,
        doc,
        [Point2D(beam_end_pnt.X, beam_end_pnt.Z)],
        Vector2D(-100, -300),
    )
    if not beam_bolt_batch_right.data["is_shown"]:
        weld_symbols_list.append(main_beam_end_weld_symbol)

    front_view.add_weld_symbols(weld_symbols_list)

    special_dim_symbols: List[SpecialDimensionSymbol] = []

    left_stiffener_plate_ref_pnt = stiffener_left.reference_point
    left_stiffener_plate_width_thickness_symbol = SpecialDimensionSymbol(
        doc,
        Point2D(
            left_stiffener_plate_ref_pnt.X + stiffener_left.data["width"] / 3,
            left_stiffener_plate_ref_pnt.Z + stiffener_left.data["height"] / 4,
        ),
        Vector2D(-stiffener_left.data["width"] * 4 / 3, -100)
        if stiffener_left.data["outer"]
        else Vector2D(-stiffener_left.data["width"] / 3, -100),
        (
            str(round(stiffener_left.data["width"] / 25.4, 3))
            + '" X '
            + str(round(stiffener_left.data["thickness"] / 25.4, 3))
            + '" ' + build_ele.LeftStiffenerPlateTailingText.value
        )
        if build_ele.ShowDimensionInInchesCheckbox.value
        else (
            str(round(stiffener_left.data["width"], 3))
            + " X "
            + str(round(stiffener_left.data["thickness"], 3))  + " "  + build_ele.LeftStiffenerPlateTailingText.value
        ),
    )
    special_dim_symbols.append(left_stiffener_plate_width_thickness_symbol)

    if (
        stiffener_left.data["width"] != stiffener_right.data["width"]
        or stiffener_left.data["thickness"] != stiffener_right.data["thickness"]
    ):
        right_stiffener_plate_ref_pnt = stiffener_right.reference_point
        right_stiffener_plate_width_thickness_symbol = SpecialDimensionSymbol(
            doc,
            Point2D(
                right_stiffener_plate_ref_pnt.X - stiffener_right.data["width"] / 3,
                right_stiffener_plate_ref_pnt.Z + stiffener_right.data["height"] / 4,
            ),
            Vector2D(stiffener_right.data["width"] * 4 / 3, -100)
            if stiffener_right.data["outer"]
            else Vector2D(stiffener_right.data["width"] / 3, -100),
            (
                str(round(stiffener_right.data["width"] / 25.4, 3))
                + '" X '
                + str(round(stiffener_right.data["thickness"] / 25.4, 3))
                + '" ' + build_ele.RightStiffenerPlateTailingText.value
            )
            if build_ele.ShowDimensionInInchesCheckbox.value
            else (
                str(round(stiffener_right.data["width"], 3))
                + " X "
                + str(round(stiffener_right.data["thickness"], 3))  + " " +  build_ele.RightStiffenerPlateTailingText.value
            ),
        )
        special_dim_symbols.append(right_stiffener_plate_width_thickness_symbol)

    # Beam Name Special Text
    move_vec = Vector3D(beam.get_start_point(), beam.get_end_point())
    move_vec.Normalize(move_vec.GetLength() / 4.)

    beam_text_pnt = beam.get_start_point() + move_vec

    beam_name_text_symbol = SpecialDimensionSymbol(
        doc,
        Point2D(beam_text_pnt.X, beam_text_pnt.Z),
        Vector2D(0, -beam.get_width() / 2. - 200),
        build_ele.SectionName.value,
    )
    special_dim_symbols.append(beam_name_text_symbol)

    # Left Beam Special Text
    if build_ele.ShowLeftBeamTextCheckbox.value:
        left_pillar_ref_pnt = pillar_left.reference_point
        left_beam_text_symbol = SpecialDimensionSymbol(
            doc,
            Point2D(left_pillar_ref_pnt.X, left_pillar_ref_pnt.Z + pillar_left.data["height"]),
            Vector2D(0, 200),
            build_ele.LeftBeamSpecialText.value,
        )
        special_dim_symbols.append(left_beam_text_symbol)

    # Right Beam Special Text
    if build_ele.ShowRightBeamTextCheckbox.value:
        right_pillar_ref_pnt = pillar_right.reference_point
        right_beam_text_symbol = SpecialDimensionSymbol(
            doc,
            Point2D(right_pillar_ref_pnt.X, right_pillar_ref_pnt.Z + pillar_right.data["height"]),
            Vector2D(0, 200),
            build_ele.RightBeamSpecialText.value,
        )
        special_dim_symbols.append(right_beam_text_symbol)

    front_view.add_special_dimension_symbols(special_dim_symbols)

    front_view_ele, symbol_ele_list = front_view.create()

    model.add_view_symbol_elements(symbol_ele_list)

    # ------ Building everything ------
    model_ele_list = []
    model_ele_list.extend(model.get_model_ele_list(model.build()))
    model_ele_list.append(front_view_ele)

    handles_list = []
    handles_list.extend(model.create_handles_list())

    ChannelBeam.model_ele_list = model_ele_list
    ChannelBeam.handles_list = handles_list

    return model_ele_list, handles_list


def on_control_event(build_ele, event_id):
    """
    On control event

    Args:
        build_ele:  the building element.
        event_id:   event id of control.

    Returns:
        True/False if palette refresh is necessary
    """
    print("Buttons.py (on_control_event called, eventId: ", event_id, ")")
    Setup.upload_data()
    setup = Setup(build_ele.BeamTypeRadioGroup.value, build_ele)
    if event_id == 1000:
        setup.launch()

    if build_ele.BeamTypeRadioGroup.value == 1:
        build_ele.SectionName.value = build_ele.CBeamSettingsName.value
    elif build_ele.BeamTypeRadioGroup.value == 2:
        build_ele.SectionName.value = build_ele.HBeamSettingsName.value
    else:
        raise Exception("Beam Type radio group doesn't exist!!")

    # create_element(build_ele, "")

    return True


def move_handle(build_ele, handle_prop, input_pnt, doc):
    """
    Modify the element geometry by handles

    Args:
        build_ele:  the building element.
        handle_prop handle properties
        input_pnt:  input point
        doc:        input document
    """

    build_ele.change_property(handle_prop, input_pnt)
    return create_element(build_ele, doc)


class ChannelBeam(Element):
    def __init__(self, data, doc):
        self.doc = doc
        super().__init__(data)
        self.view_symbol_elements: List[SymbolElement] = []
        self.handles_list = []
        self.model_ele_list = []

    def get_model_ele_list(self, model_obj_list):
        polyhedron_list = self.__rotate(self.__subtract_removable(model_obj_list))
        model_3d_list = []
        for geometry in polyhedron_list:
            model_3d_list.append(
                AllplanBasisElements.ModelElement3D(self.com_prop, geometry)
            )

        if len(self.view_symbol_elements) > 0:
            model_3d_list.extend(self.view_symbol_elements)

        self.model_ele_list = model_3d_list

        return self.__create_PP(model_3d_list)

    def add_view_symbol_elements(self, view_symbol_elements):
        self.view_symbol_elements = view_symbol_elements

    def __subtract_removable(self, model_obj_list) -> List[Polyhedron3D]:
        creatable: List[Polyhedron3D] = list()
        removable: List[Polyhedron3D] = list()

        for element_type, polyhedron in model_obj_list:
            # if isinstance(element_type, BoltBatch):
            if str(element_type).find("Bolts Batch") != -1:
                removable.append(polyhedron)
            else:
                creatable.append(polyhedron)

        for i in range(len(creatable)):
            for removable_polyhedron in removable:
                err, polyhedron = MakeSubtraction(creatable[i], removable_polyhedron)
                if err == eGeometryErrorCode.eOK:
                    creatable[i] = polyhedron

        return creatable

    def __rotate(self, model_ele_list):
        rot_mat = Matrix3D()
        rot_mat.Rotation(
            Line3D(Point3D(), Point3D(0, 0, 1000)),
            self.__degree(self.data["angle"]),
        )
        new_ele_list = []
        for ele in model_ele_list:
            ele = Transform(ele, rot_mat)
            new_ele_list.append(ele)

        return new_ele_list

    def __create_PP(self, model_ele_list):
        """
        PythonPart with attributes creation method

        Args:

        Returns:
            Model elements list
        """
        if self.data["is_pp"]:
            views = [View2D3D(model_ele_list)]

            attr_list = self.create_attributes()

            pythonpart = PythonPart(
                self.data["pp_name"],
                parameter_list=self.data["params_list"],
                hash_value=self.data["hash"],
                python_file=self.data["python_file"],
                views=views,
                attribute_list=attr_list,
            )

            model_ele_list = pythonpart.create()

        return model_ele_list

    def create_attributes(self):
        """
        Methods for creation of attributes(weight) for PythonPart
        """
        attr_list = []

        self.weight = self.get_weight()
        self.weight = (
            # TODO what is this number?
            self.weight * 2.2046
            if self.data["weight_measurement"] == "Lb"
            else self.weight
        )

        attr_list.append(
            AllplanBaseElements.AttributeDouble(721, self.weight)
        )  # Weight

        return attr_list

    def create_handles_list(self):
        handle_list = []
        rot_mat = Matrix3D()
        rot_mat.Rotation(
            Line3D(Point3D(), Point3D(0, 0, 1000)),
            self.__degree(self.data["angle"]),
        )

        x_handle_offset_height = (
            self.data["handles_params"]["left_beam_height"]
            + self.data["offset"]
            + self.data["handles_params"]["flange_thickness"]
        )

        dir_vec = Vector3D(Point3D(0, 0, 0), Point3D(1, 0, 0))
        dir_vec = Transform(dir_vec, rot_mat)
        handle_list.append(
            HandleProperties(
                "XHandleOffset",
                Point3D(self.data["spacing"], 0, x_handle_offset_height),
                Point3D(0, 0, x_handle_offset_height),
                [("XHandleOffset", HandleDirection.vector_dir)],
                HandleDirection.vector_dir,
                True,
                1.0,
                None,
                dir_vec,
            )
        )
        handle_list.append(
            HandleProperties(
                "LeftBeamHeight",
                Point3D(0, 0, self.data["handles_params"]["left_beam_height"]),
                Point3D(0, 0, 0),
                [("LeftBeamHeight", HandleDirection.z_dir)],
                HandleDirection.z_dir,
                True,
            )
        )
        handle_list.append(
            HandleProperties(
                "LeftBeamFlangeThickness",
                Point3D(0, 0, 0),
                Point3D(0, 0, -self.data["handles_params"]["flange_thickness"]),
                [("LeftBeamFlangeThickness", HandleDirection.z_dir)],
                HandleDirection.z_dir,
                False,
            )
        )
        # self.data["handles_params"]["left_beam_height"]
        handle_list.append(
            HandleProperties(
                "ZHandleOffset",
                Point3D(
                    self.data["spacing"],
                    0,
                    self.data["offset"],
                ),
                Point3D(
                    self.data["spacing"],
                    0,
                    0,
                ),
                [("ZHandleOffset", HandleDirection.z_dir)],
                HandleDirection.z_dir,
                False,
            )
        )

        handle_list.append(
            HandleProperties(
                "ZRotationAngle",
                Point3D(
                    self.data["handles_params"]["left_stiffener_width"]
                    + self.data["handles_params"]["web_thickness"]
                    + 50,
                    0,
                    0,
                ),
                Point3D(0, 0, 0),
                [("ZRotationAngle", HandleDirection.angle)],
                HandleDirection.angle,
            )
        )
        for handle in handle_list:
            translate_mat = Matrix3D()
            translate_mat.SetTranslation(self.data["ref_pnt_offset_vec"])
            handle.transform(translate_mat)

        if self.data["angle"]:
            for handle in handle_list:
                handle.transform(rot_mat)

        self.handles_list = handle_list

        return handle_list

    def __degree(self, angle):
        rot_angle = Angle()
        rot_angle.SetDeg(angle)

        return rot_angle

    # def create(self) -> List[Polyhedron3D]:
    def create(self):
        return []

    def show(self) -> bool:
        return False

    def calculate_weight(self):
        return 0

    def __str__(self):
        return "Channel Beam"
