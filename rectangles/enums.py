"""Enumerations for rectangle relationship types."""

from enum import Enum


class IntersectionType(Enum):
    """Classifies how two rectangles intersect."""
    NONE = "none"
    POINT = "point"
    LINE = "line"
    AREA = "area"


class ContainmentType(Enum):
    """Classifies containment relationship between two rectangles."""
    NONE = "none"
    A_IN_B = "a_in_b"
    B_IN_A = "b_in_a"


class AdjacencyType(Enum):
    """Classifies how two rectangles share a side."""
    NONE = "none"
    PROPER = "proper"
    SUB_LINE = "sub_line"
    PARTIAL = "partial"
