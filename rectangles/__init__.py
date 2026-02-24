"""Rectangle analysis package."""

from .analyzer import RectangleAnalyzer
from .enums import AdjacencyType, ContainmentType, IntersectionType
from .models import AdjacencyResult, IntersectionResult, LineSegment, Point, Rectangle

__all__ = [
    "Rectangle",
    "Point",
    "LineSegment",
    "IntersectionResult",
    "AdjacencyResult",
    "IntersectionType",
    "ContainmentType",
    "AdjacencyType",
    "RectangleAnalyzer",
]
