# Initial development – Allbau Software GmbH, http://www.allplan-tools.de
import math

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeo

from ...abstracts.SymbolElement import SymbolElement


class SpecialDimensionSymbol(SymbolElement):
    def __init__(self, document, start_pnt, end_pnt_shift_vector, text):
        super().__init__()
        self.document = document

        self.start_point = start_pnt
        self.end_point = start_pnt + end_pnt_shift_vector

        self.txt = text

        self.ref_length = 10
        self.text_scale = 1

        self.com_prop = AllplanBaseElements.CommonProperties()

    def create_element(self):
        """
        Create elements
        """
        scaling_factor = self.document.GetScalingFactor()
        length = self.ref_length
        refLength = length * scaling_factor

        # Arrow Line
        pt1 = AllplanGeo.Point2D(self.start_point)
        pt2 = AllplanGeo.Point2D(self.end_point)

        line1 = AllplanGeo.Line2D(pt1, pt2)
        self.model_ele_list.append(
            AllplanBasisElements.ModelElement2D(self.com_prop, line1)
        )

        dir = 1
        if self.start_point.X > self.end_point.X:
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
        text_prop = AllplanBasisElements.TextProperties()
        th = length * 0.1 * self.text_scale
        tw = th * 0.75

        # Left Hand Note
        txt = self.txt
        text_prop.Height = th
        text_prop.Width = tw
        text_prop.Alignment = AllplanBasisElements.TextAlignment.eMiddleBottom
        text_prop.Type = AllplanBasisElements.TextType.eNormalText
        sp2 = AllplanGeo.Point2D(midPoint.X - refLength * 0.25, pt3.Y + h * 0.2)
        self.model_ele_list.append(
            AllplanBasisElements.TextElement(self.com_prop, text_prop, txt, sp2)
        )

        return self.model_ele_list
