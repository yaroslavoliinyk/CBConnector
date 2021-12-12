import math

from NemAll_Python_Geometry import (
    Angle,
    Axis2D,
    IntersectionCalculus,
    Line3D,
    Mirror,
    Point2D,
    Point3D,
    Polygon3D,
    Vector2D,
    Vector3D,
)

from .Beam import Beam


class CBeam(Beam):
    def __init__(self, data):
        super().__init__(data)
        self._data["width"] = self._data["d"]
        self._d = self._data["d"]
        self._bf = self._data["bf"]
        self._tf = self._data["tf"]
        self._tw = self._data["tw"]
        self._xb = self._data["xb"]
        self._k = self._data["k"]

    def create_shape(self) -> Polygon3D:

        # Given default ratio
        tan_a = 1 / 6.0
        # Given default angle
        beta = math.radians(130.26883890)
        polygon = Polygon3D()
        if self._data["rounded"]:
            (
                D,
                dline1,
                dline2,
                dradius,
                E,
                eline1,
                eline2,
                eradius,
            ) = self.__findaddpoints(
                self._d, self._bf, self._tf, self._tw, self._xb, self._k, tan_a, beta
            )
            polygon += Point3D(-self._xb, 0, 0)
            polygon += Point3D(-self._xb, self._d / 2, 0)
            polygon += Point3D(self._bf - self._xb, self._d / 2, 0)

            rounded_part = self._round_lines_by_radius(eline2, eline1, eradius)
            for pnt in rounded_part.Points:
                polygon += pnt

            rounded_part = self._round_lines_by_radius(dline2, dline1, dradius)
            for pnt in rounded_part.Points:
                polygon += pnt

            polygon += Point3D(self._tw - self._xb, 0, 0)
            polygon += Point3D(-self._xb, 0, 0)
            polygon2 = Mirror(
                polygon,
                Axis2D(Point2D(0, 0), Vector2D(1, 0)),
            )
            polygon2.Reverse()

            polygon2.Remove(0)
            polygon2.Remove(0)
            polygon2.RemoveLastPoint()
            polygon.RemoveLastPoint()
            polygon.RemoveLastPoint()
            polygon.Remove(0)

            polygon += polygon2
        else:
            polygon += Point3D(-self._xb, -self._d / 2, 0)
            polygon += Point3D(-self._xb, self._d / 2, 0)
            polygon += Point3D(self._bf - self._xb, self._d / 2, 0)
            polygon += Point3D(self._bf - self._xb, self._d / 2 - self._tf, 0)
            polygon += Point3D(self._tw - self._xb, self._d / 2 - self._tf, 0)
            polygon += Point3D(self._tw - self._xb, -self._d / 2 + self._tf, 0)
            polygon += Point3D(self._bf - self._xb, -self._d / 2 + self._tf, 0)
            polygon += Point3D(self._bf - self._xb, -self._d / 2, 0)
            polygon += Point3D(-self._xb, -self._d / 2, 0)

        # if self._is_frame:

        return polygon

    def show(self):
        return self._data["beam_type"] == 1

    def __str__(self):
        return "Channel Beam"

    def __findaddpoints(self, d, bf, tf, tw, xb, k, tan_a, beta):
        # Point A(x1, y1)
        x1 = tw - xb
        y1 = d / 2.0 - k
        # Point B(x2, y2)
        x2 = tw + (bf - tw) / 2 - xb
        y2 = d / 2.0 - tf
        # Point C(x3, y3)
        x3 = bf - xb
        y3 = d / 2.0
        # Find point G(xg, yg)
        xg = x3
        lg = math.fabs(x3 - x2)
        hg = lg * tan_a
        yg = y2 + hg
        # Find H(xh, yh)
        xh = x1
        lh = math.fabs(x1 - x2)
        hh = lh * tan_a
        yh = y2 - hh
        # yh          = y2 - hg
        # Find D(xd, yd)
        aaxis = Axis2D(
            Point2D(x1, y1),
            Vector2D(Angle(math.pi - beta), 1.0),
        )
        alpha = math.atan(tan_a)
        baxis = Axis2D(Point2D(x2, y2), Vector2D(Angle(alpha), 1.0))
        flag, D = IntersectionCalculus(aaxis, baxis)
        if flag:
            xd = D.X
            yd = D.Y
        else:
            raise Exception
        # Find E(xe, ye)
        сaxis = Axis2D(
            Point2D(),
            Point2D(x3, y3),
            Vector2D(Angle(math.pi - beta), 1.0),
        )
        flag, E = IntersectionCalculus(сaxis, baxis)
        if flag:
            xe = E.X
            ye = E.Y
        else:
            raise Exception
        # Find dline1
        dline1 = Line3D(Point3D(x1, y1, 0.0), Point3D(xh, yh, 0.0))
        # find dradius
        gamma = beta - math.pi / 2.0
        omega = math.pi - 2 * gamma

        line = Vector2D(Point2D(x1, y1), Point2D(xd, yd)).GetLength()
        dradius = line * math.sin(gamma) / math.sin(omega)
        # find dline2
        s = Vector2D(Point2D(x1, y1), Point2D(xh, yh)).GetLength()
        tan_tau = dradius / s
        tau = math.atan(tan_tau)
        phi = 2.0 * tau - math.pi / 2.0
        dline2 = Line3D(
            Point3D(xh, yh, 0.0),
            Vector3D(Vector2D(Angle(phi + alpha), s)),
        )
        # find eline1
        eline1 = Line3D(Point3D(xg, yg, 0.0), Point3D(xe, ye, 0.0))
        # find eraduis
        line = Vector2D(Point2D(xe, ye), Point2D(x3, y3)).GetLength()
        gamma = alpha + beta - math.pi / 2.0
        omega = 2 * math.pi - 2 * (alpha + beta)
        eradius = line * math.sin(gamma) / math.sin(omega)
        # find eline2
        s = Vector2D(Point2D(xg, yg), Point2D(xe, ye)).GetLength()
        tan_tau = eradius / s
        tau = math.atan(tan_tau)
        mu = math.pi - 2 * tau
        ro = mu + alpha
        eline2 = Line3D(
            Point3D(xg, yg, 0),
            Vector3D(Vector2D(Angle(ro), s)),
        )

        return D, dline1, dline2, dradius, E, eline1, eline2, eradius
