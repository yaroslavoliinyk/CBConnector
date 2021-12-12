# Initial development – Allbau Software GmbH, http://www.allplan-tools.de
import math
from typing import List

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeo

from ...abstracts.SymbolElement import SymbolElement


class WeldSymbol(SymbolElement):
    def __init__(
        self,
        data,
        document,
        start_pnts: List[AllplanGeo.Point2D],
        end_pnt_move_vector: AllplanGeo.Vector2D,
    ):
        super().__init__()
        self.document = document

        self.start_points = start_pnts
        self.end_point = start_pnts[0] + end_pnt_move_vector

        self.weld_type = data["weld_type"]
        self.location = data["location"]
        self.groove_type = data["groove_type"]

        self.weld_around = data["weld_around"]
        self.field_weld = data["field_weld"]

        self.ref_length = 10
        self.text_scale = 1

        self.show_size = data["show_size"]
        self.weld_size = data["weld_size"]
        self.weld_size0 = data["weld_size0"]
        self.groove_size = data["groove_size"]
        self.groove_size0 = data["groove_size0"]

        self.show_length = data["show_length"]
        self.weld_length = data["weld_length"]
        self.weld_length0 = data["weld_length0"]

        self.show_pitch = data["show_pitch"]
        self.weld_pitch = data["weld_pitch"]
        self.weld_pitch0 = data["weld_pitch0"]

        self.tail_note = data["tail_note"]

        self.com_prop = AllplanBaseElements.CommonProperties()

    def create_element(self):  # noqa C901
        """
        Draw the preview
        """

        scaling_factor = self.document.GetScalingFactor()
        length = self.ref_length
        refLength = length * scaling_factor

        # Arrow Line
        for pt in self.start_points:
            pt1 = AllplanGeo.Point2D(pt)
            pt2 = AllplanGeo.Point2D(self.end_point)

            line1 = AllplanGeo.Line2D(pt1, pt2)
            self.model_ele_list.append(
                AllplanBasisElements.ModelElement2D(self.com_prop, line1)
            )

            dir = 1
            if self.start_points[0].X > self.end_point.X:
                dir = -1

            # Arrow Head
            a = 15 * (math.pi / 180)
            d = refLength * 0.1
            dx = pt2.X - pt1.X
            dy = pt2.Y - pt1.Y
            angle = math.atan2(dx, dy)
            angle1 = angle + a
            angle2 = angle - a
            ah1 = AllplanGeo.Point2D(
                pt1.X + math.sin(angle1) * d, pt1.Y + math.cos(angle1) * d
            )
            ah2 = AllplanGeo.Point2D(
                pt1.X + math.sin(angle2) * d, pt1.Y + math.cos(angle2) * d
            )
            arrow = AllplanGeo.Polygon2D()
            arrow += pt1
            arrow += ah1
            arrow += ah2
            arrow += pt1
            props = AllplanBasisElements.FillingProperties()
            props.FirstColor = AllplanBasisElements.ARGB(0, 0, 0, 0)
            self.model_ele_list.append(
                AllplanBasisElements.FillingElement(self.com_prop, props, arrow)
            )
            self.model_ele_list.append(
                AllplanBasisElements.ModelElement2D(self.com_prop, arrow)
            )

        # Reference Line
        pt3 = AllplanGeo.Point2D(pt2.X + refLength * dir, pt2.Y)
        line2 = AllplanGeo.Line2D(pt2, pt3)
        self.model_ele_list.append(
            AllplanBasisElements.ModelElement2D(self.com_prop, line2)
        )

        # Weld Symbol
        w = refLength * 0.175
        h = w

        midX = pt2.X + (pt3.X - pt2.X) * 0.5
        midPoint = AllplanGeo.Point2D(midX - w * 0.25, pt2.Y)

        if self.weld_type == "Fillet":
            if self.location != "NA":
                p1 = AllplanGeo.Point2D(midPoint.X - w * 0.5, midPoint.Y)
                p2 = AllplanGeo.Point2D(midPoint.X + w * 0.5, midPoint.Y)
                if self.location == "Other":
                    p3 = AllplanGeo.Point2D(p1.X, midPoint.Y + h)
                else:
                    p3 = AllplanGeo.Point2D(p1.X, midPoint.Y - h)

                line3 = AllplanGeo.Line2D(p2, p3)
                self.model_ele_list.append(
                    AllplanBasisElements.ModelElement2D(self.com_prop, line3)
                )
                line4 = AllplanGeo.Line2D(p1, p3)
                self.model_ele_list.append(
                    AllplanBasisElements.ModelElement2D(self.com_prop, line4)
                )

                if self.location == "Both":
                    p3 = AllplanGeo.Point2D(p1.X, midPoint.Y + h)
                    line5 = AllplanGeo.Line2D(p2, p3)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line5)
                    )
                    line6 = AllplanGeo.Line2D(p1, p3)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line6)
                    )

        r = w * 0.5
        if self.weld_type == "Spot":
            if self.location == "Arrow":
                p3 = AllplanGeo.Point2D(midPoint.X, midPoint.Y - r)
            if self.location == "Other":
                p3 = AllplanGeo.Point2D(midPoint.X, midPoint.Y + r)
            if self.location == "NA":
                p3 = AllplanGeo.Point2D(midPoint.X, midPoint.Y)

            if self.location != "Both":
                circle = AllplanGeo.Arc2D(p3, r, r, math.pi / 2, 0, math.pi * 2, True)
                self.model_ele_list.append(
                    AllplanBasisElements.ModelElement2D(self.com_prop, circle)
                )

        if self.weld_type == "Back":
            if self.location == "Arrow":
                circle = AllplanGeo.Arc2D(midPoint, r, r, math.pi, 0, math.pi, True)
                self.model_ele_list.append(
                    AllplanBasisElements.ModelElement2D(self.com_prop, circle)
                )
            if self.location == "Other":
                circle = AllplanGeo.Arc2D(midPoint, r, r, 0, 0, math.pi, True)
                self.model_ele_list.append(
                    AllplanBasisElements.ModelElement2D(self.com_prop, circle)
                )

        if self.weld_type == "Groove":
            if self.groove_type == "Square":
                p1 = AllplanGeo.Point2D(midPoint.X - w * 0.25, midPoint.Y)
                p2 = AllplanGeo.Point2D(midPoint.X + w * 0.25, midPoint.Y)
                p3 = AllplanGeo.Point2D(p1.X, midPoint.Y - h)
                p4 = AllplanGeo.Point2D(p2.X, midPoint.Y - h)
                p5 = AllplanGeo.Point2D(p1.X, midPoint.Y + h)
                p6 = AllplanGeo.Point2D(p2.X, midPoint.Y + h)
                if (
                    self.location == "Arrow"
                    or self.location == "Both"
                    or self.location == "NA"
                ):
                    line1 = AllplanGeo.Line2D(p1, p3)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line1)
                    )
                    line2 = AllplanGeo.Line2D(p2, p4)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line2)
                    )
                if (
                    self.location == "Other"
                    or self.location == "Both"
                    or self.location == "NA"
                ):
                    line3 = AllplanGeo.Line2D(p1, p5)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line3)
                    )
                    line4 = AllplanGeo.Line2D(p2, p6)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line4)
                    )

            if self.groove_type == "V":
                w1 = w * 0.75
                p1 = AllplanGeo.Point2D(midPoint.X - w1, midPoint.Y - w1)
                p2 = AllplanGeo.Point2D(midPoint.X + w1, midPoint.Y - w1)
                p3 = AllplanGeo.Point2D(p1.X, midPoint.Y + w1)
                p4 = AllplanGeo.Point2D(p2.X, midPoint.Y + w1)
                if self.location == "Arrow" or self.location == "Both":
                    line1 = AllplanGeo.Line2D(midPoint, p1)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line1)
                    )
                    line2 = AllplanGeo.Line2D(midPoint, p2)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line2)
                    )
                if self.location == "Other" or self.location == "Both":
                    line3 = AllplanGeo.Line2D(midPoint, p3)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line3)
                    )
                    line4 = AllplanGeo.Line2D(midPoint, p4)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line4)
                    )

            if self.groove_type == "Bevel":
                p1 = AllplanGeo.Point2D(midPoint.X - w * 0.5, midPoint.Y)
                p2 = AllplanGeo.Point2D(p1.X, midPoint.Y + w)
                p3 = AllplanGeo.Point2D(p1.X + w, midPoint.Y + w)
                p4 = AllplanGeo.Point2D(p1.X, midPoint.Y - w)
                p5 = AllplanGeo.Point2D(p1.X + w, midPoint.Y - w)
                if self.location == "Other" or self.location == "Both":
                    line1 = AllplanGeo.Line2D(p1, p2)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line1)
                    )
                    line2 = AllplanGeo.Line2D(p1, p3)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line2)
                    )
                if self.location == "Arrow" or self.location == "Both":
                    line3 = AllplanGeo.Line2D(p1, p4)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line3)
                    )
                    line4 = AllplanGeo.Line2D(p1, p5)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line4)
                    )

            if self.groove_type == "U":
                r = w * 0.6
                p1 = AllplanGeo.Point2D(midPoint.X, midPoint.Y + h * 0.4)
                p2 = AllplanGeo.Point2D(midPoint.X, midPoint.Y - h * 0.4)
                p3 = AllplanGeo.Point2D(midPoint.X, p1.Y + r)
                p4 = AllplanGeo.Point2D(midPoint.X, p2.Y - r)
                if self.location == "Other" or self.location == "Both":
                    line1 = AllplanGeo.Line2D(midPoint, p1)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line1)
                    )
                    arc = AllplanGeo.Arc2D(p3, r, r, math.pi, 0, math.pi, True)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, arc)
                    )
                if self.location == "Arrow" or self.location == "Both":
                    line1 = AllplanGeo.Line2D(midPoint, p2)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line1)
                    )
                    arc = AllplanGeo.Arc2D(p4, r, r, 0, 0, math.pi, True)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, arc)
                    )

            if self.groove_type == "J":
                r = w * 0.6
                pm = AllplanGeo.Point2D(midPoint.X - r * 0.5, midPoint.Y)
                p1 = AllplanGeo.Point2D(midPoint.X - r * 0.5, midPoint.Y + h)
                p2 = AllplanGeo.Point2D(midPoint.X - r * 0.5, midPoint.Y - h)
                if self.location == "Other" or self.location == "Both":
                    line1 = AllplanGeo.Line2D(pm, p1)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line1)
                    )
                    arc = AllplanGeo.Arc2D(
                        p1, r, r, math.pi * 1.5, 0, math.pi / 2, True
                    )
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, arc)
                    )
                if self.location == "Arrow" or self.location == "Both":
                    line1 = AllplanGeo.Line2D(pm, p2)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line1)
                    )
                    arc = AllplanGeo.Arc2D(p2, r, r, 0, 0, math.pi / 2, True)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, arc)
                    )

            if self.groove_type == "FlareV":
                r = w * 0.65
                w1 = r * 0.35
                p1 = AllplanGeo.Point2D(midPoint.X - w1 * 0.5 - r, midPoint.Y)
                p2 = AllplanGeo.Point2D(midPoint.X + w1 * 0.5 + r, midPoint.Y)
                if self.location == "Arrow" or self.location == "Both":
                    arc = AllplanGeo.Arc2D(
                        p1, r, r, math.pi * 1.5, 0, math.pi / 2, True
                    )
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, arc)
                    )
                    arc = AllplanGeo.Arc2D(p2, r, r, math.pi, 0, math.pi / 2, True)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, arc)
                    )
                if self.location == "Other" or self.location == "Both":
                    arc = AllplanGeo.Arc2D(p1, r, r, 0, 0, math.pi / 2, True)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, arc)
                    )
                    arc = AllplanGeo.Arc2D(p2, r, r, math.pi / 2, 0, math.pi / 2, True)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, arc)
                    )

            if self.groove_type == "FlareBevel":
                r = w * 0.65
                w1 = r * 0.35
                w2 = (r + w1) / 2
                p1 = AllplanGeo.Point2D(midPoint.X - w2 * 0.5, midPoint.Y)
                p2 = AllplanGeo.Point2D(p1.X + w2 * 2, midPoint.Y)
                p3 = AllplanGeo.Point2D(p1.X, midPoint.Y + r)
                p4 = AllplanGeo.Point2D(p1.X, midPoint.Y - r)
                if self.location == "Arrow" or self.location == "Both":
                    line1 = AllplanGeo.Line2D(p1, p4)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line1)
                    )
                    arc = AllplanGeo.Arc2D(p2, r, r, math.pi, 0, math.pi / 2, True)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, arc)
                    )
                if self.location == "Other" or self.location == "Both":
                    line1 = AllplanGeo.Line2D(p1, p3)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, line1)
                    )
                    arc = AllplanGeo.Arc2D(p2, r, r, math.pi / 2, 0, math.pi / 2, True)
                    self.model_ele_list.append(
                        AllplanBasisElements.ModelElement2D(self.com_prop, arc)
                    )

        # Weld All-Around
        if self.weld_around:
            warCircle = AllplanGeo.Arc2D(
                pt2, r * 0.65, r * 0.65, math.pi / 2, 0, math.pi * 2, True
            )
            self.model_ele_list.append(
                AllplanBasisElements.ModelElement2D(self.com_prop, warCircle)
            )

        # Field Weld
        if self.field_weld:
            p4 = AllplanGeo.Point2D(pt2.X, pt2.Y + h)
            fw_line1 = AllplanGeo.Line2D(pt2, p4)
            self.model_ele_list.append(
                AllplanBasisElements.ModelElement2D(self.com_prop, fw_line1)
            )
            p5 = AllplanGeo.Point2D(p4.X + w * 0.5 * dir, p4.Y - h * 0.2)
            p6 = AllplanGeo.Point2D(p4.X, p4.Y - h * 0.4)
            polygon = AllplanGeo.Polygon2D()
            polygon += p4
            polygon += p5
            polygon += p6
            polygon += p4
            props = AllplanBasisElements.FillingProperties()
            props.FirstColor = AllplanBasisElements.ARGB(0, 0, 0, 0)
            self.model_ele_list.append(
                AllplanBasisElements.FillingElement(self.com_prop, props, polygon)
            )
            self.model_ele_list.append(
                AllplanBasisElements.ModelElement2D(self.com_prop, polygon)
            )

        # Tail information if NOTE added
        text_prop = AllplanBasisElements.TextProperties()
        th = length * 0.1 * self.text_scale
        tw = th * 0.75
        if self.tail_note != "":
            text_prop.Height = th
            text_prop.Width = tw
            if dir > 0:
                text_prop.Alignment = AllplanBasisElements.TextAlignment.eLeftMiddle
            else:
                text_prop.Alignment = AllplanBasisElements.TextAlignment.eRightMiddle
            text_prop.Type = AllplanBasisElements.TextType.eNormalText
            tnp = AllplanGeo.Point2D(pt3.X + w * 0.5 * dir, pt3.Y)
            self.model_ele_list.append(
                AllplanBasisElements.TextElement(
                    self.com_prop, text_prop, self.tail_note, tnp
                )
            )
            # Add extra lines on end of ref line
            tnp1 = AllplanGeo.Point2D(pt3.X + w * 0.5 * dir, pt3.Y + w * 0.5)
            tnp2 = AllplanGeo.Point2D(pt3.X + w * 0.5 * dir, pt3.Y - w * 0.5)
            tn_line1 = AllplanGeo.Line2D(pt3, tnp1)
            self.model_ele_list.append(
                AllplanBasisElements.ModelElement2D(self.com_prop, tn_line1)
            )
            tn_line2 = AllplanGeo.Line2D(pt3, tnp2)
            self.model_ele_list.append(
                AllplanBasisElements.ModelElement2D(self.com_prop, tn_line2)
            )

        # Left Hand Note
        txt = ""
        if self.show_size:
            if self.location == "Arrow" or self.location == "Both":
                txt = self.weld_size
                if self.weld_type == "Groove" and self.groove_size != "":
                    txt = txt + "(" + self.groove_size + ")"
                text_prop.Height = th
                text_prop.Width = tw
                text_prop.Alignment = AllplanBasisElements.TextAlignment.eMiddleTop
                text_prop.Type = AllplanBasisElements.TextType.eNormalText
                sp1 = AllplanGeo.Point2D(midPoint.X - refLength * 0.25, pt3.Y - h * 0.2)
                self.model_ele_list.append(
                    AllplanBasisElements.TextElement(self.com_prop, text_prop, txt, sp1)
                )
            if self.location == "Other" or self.location == "Both":
                txt = self.weld_size0
                if self.weld_type == "Groove" and self.groove_size0 != "":
                    txt = txt + "(" + self.groove_size0 + ")"
                text_prop.Height = th
                text_prop.Width = tw
                text_prop.Alignment = AllplanBasisElements.TextAlignment.eMiddleBottom
                text_prop.Type = AllplanBasisElements.TextType.eNormalText
                sp2 = AllplanGeo.Point2D(midPoint.X - refLength * 0.25, pt3.Y + h * 0.2)
                self.model_ele_list.append(
                    AllplanBasisElements.TextElement(self.com_prop, text_prop, txt, sp2)
                )

        # Right Hand Note
        txt = ""
        if self.show_length:
            if self.location == "Arrow" or self.location == "Both":
                txt = self.weld_length
                if self.show_pitch:
                    txt = txt + "-" + self.weld_pitch
                text_prop.Height = th
                text_prop.Width = tw
                text_prop.Alignment = AllplanBasisElements.TextAlignment.eMiddleTop
                text_prop.Type = AllplanBasisElements.TextType.eNormalText
                lp1 = AllplanGeo.Point2D(midPoint.X + refLength * 0.3, pt3.Y - h * 0.2)
                self.model_ele_list.append(
                    AllplanBasisElements.TextElement(self.com_prop, text_prop, txt, lp1)
                )
            if self.location == "Other" or self.location == "Both":
                txt = self.weld_length0
                if self.show_pitch:
                    txt = txt + "-" + self.weld_pitch0
                text_prop.Height = th
                text_prop.Width = tw
                text_prop.Alignment = AllplanBasisElements.TextAlignment.eMiddleBottom
                text_prop.Type = AllplanBasisElements.TextType.eNormalText
                lp2 = AllplanGeo.Point2D(midPoint.X + refLength * 0.3, pt3.Y + h * 0.2)
                self.model_ele_list.append(
                    AllplanBasisElements.TextElement(self.com_prop, text_prop, txt, lp2)
                )

        return self.model_ele_list
