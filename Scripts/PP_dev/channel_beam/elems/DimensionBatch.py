# Initial development – Allbau Software GmbH, http://www.allplan-tools.de

import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeo


class DimensionBatch:
    """
    Data class for dimensions.
    """

    def __init__(self, dim_prop):
        self.dim_points_list = []
        self.offs_vec_list = []
        self.dir_vec_list = []
        self.tailing_text_prop = []
        self.dim_prop = dim_prop
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < len(self.dim_points_list):
            self.counter += 1

            dim_prop = AllplanBasisElements.DimensionProperties(self.dim_prop)
            dim_prop.TailingCharacters = self.tailing_text_prop[self.counter - 1]

            dim_nodes = AllplanGeo.Point3DList()
            if not isinstance(
                self.dim_points_list[self.counter - 1], AllplanGeo.Point3DList
            ):
                for point in self.dim_points_list[self.counter - 1]:
                    dim_nodes.append(point)
            else:
                dim_nodes = self.dim_points_list[self.counter - 1]

            return AllplanBasisElements.DimensionLineElement(
                dim_nodes,
                self.offs_vec_list[self.counter - 1],
                self.dir_vec_list[self.counter - 1],
                dim_prop,
            )
        else:
            raise StopIteration

    @staticmethod
    def copy(another):
        if isinstance(another, DimensionBatch):
            new_obj = DimensionBatch()
            for points, offs_vec, dir_vec in another:
                new_obj.dim_points_list.append(
                    [AllplanGeo.Point3D(pnt) for pnt in points]
                )
                new_obj.offs_vec_list.append(AllplanGeo.Vector2D(offs_vec))
                new_obj.dir_vec_list.append(AllplanGeo.Vector2D(dir_vec))

            return new_obj

    def rotate_on_z(self, z_rotation: AllplanGeo.Angle):
        for i, dim_pnts in enumerate(self.dim_points_list):
            for j, dim_pnt in enumerate(dim_pnts):
                self.dim_points_list[i][j] = AllplanGeo.Rotate(dim_pnt, z_rotation)

    def push_back(self, point_list, offs_vec, dir_vec, tailing_text = ""):
        self.dim_points_list.append(point_list)
        self.offs_vec_list.append(offs_vec)
        self.dir_vec_list.append(dir_vec)
        self.tailing_text_prop.append(tailing_text)

    def extend(self, other):
        self.dim_points_list.extend(other.dim_points_list)
        self.offs_vec_list.extend(other.offs_vec_list)
        self.dir_vec_list.extend(other.dir_vec_list)
        self.tailing_text_prop.extend(other.tailing_text)

    def is_empty(self):
        return len(self.dim_points_list) == 0

    def __repr__(self):
        """
        General object info
        """
        description = (
            "<%s>\n"
            "   dim_point_list          = %s\n"
            "   offs_vec_list           = %s\n"
            "   dir_vec_list            = %s\n"
            % (
                self.__class__.__name__,
                self.dim_points_list,
                self.offs_vec_list,
                self.dir_vec_list,
            )
        )

        return description
