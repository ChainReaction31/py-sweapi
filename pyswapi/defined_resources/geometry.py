from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class GeoWKT(Enum):
    POINT = "POINT"
    LINESTRING = "LINESTRING"
    POLYGON = "POLYGON"
    MULTIPOINT = "MULTIPOINT"
    MULTILINESTRING = "MULTILINESTRING"
    MULTIPOLYGON = "MULTIPOLYGON"
    GEOMETRYCOLLECTION = "GEOMETRYCOLLECTION"


class Dimensionality(Enum):
    ZERO = "EMPTY"
    TWO = ""
    THREE = "Z"
    FOUR = "ZM"


@dataclass
class Geometry:
    values = None
    dimensionality: int = ""
    wkt_type = None

    def set_point(self, coords: Point):
        self.values = coords
        self.wkt_type = GeoWKT.POINT

    def set_multipoint(self, coords: list[Point]):
        self.values = coords
        self.wkt_type = GeoWKT.MULTIPOINT

    def set_linestring(self, coords: list[Point]):
        self.values = coords
        self.wkt_type = GeoWKT.LINESTRING

    def set_multilinestring(self, coords: list[list[Point]]):
        self.values = coords
        self.wkt_type = GeoWKT.MULTILINESTRING

    def set_polygon(self, coords: list[Point]):
        self.values = coords
        self.wkt_type = GeoWKT.POLYGON

    def set_multipolygon(self, coords: list[list[Point]]):
        self.values = coords
        self.wkt_type = GeoWKT.MULTIPOLYGON

    def set_geometrycollection(self, geoms: list[Geometry]):
        self.values = geoms
        self.wkt_type = GeoWKT.GEOMETRYCOLLECTION

    def get_as_string(self):
        # TODO: change the string rep of the values field to use parens instead of brackets
        return f"{self.wkt_type}({self.values})"


@dataclass
class Point:
    values: list[float]

    def __repr__(self):
        str_rep = ""
        for val in self.values:
            str_rep += f"{val} "

        str_rep = str_rep[:-1]
        return str_rep
