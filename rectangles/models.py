"""Immutable geometry primitives and result types."""

from __future__ import annotations

from dataclasses import dataclass

from .enums import AdjacencyType, IntersectionType


@dataclass(frozen=True)
class Point:
    """An immutable 2D point."""
    x: float
    y: float


@dataclass(frozen=True)
class LineSegment:
    """An immutable 2D line segment."""
    start: Point
    end: Point


@dataclass(frozen=True)
class Rectangle:
    """An immutable axis-aligned rectangle defined by bottom-left and top-right corners.

    Constraints: x1 < x2 and y1 < y2.
    """
    x1: float
    y1: float
    x2: float
    y2: float

    def __post_init__(self) -> None:
        """Validate that the rectangle coordinates form a proper bounding box.

        Raises:
            ValueError: If x1 >= x2 or y1 >= y2.
        """
        if self.x1 >= self.x2:
            raise ValueError(f"x1 ({self.x1}) must be less than x2 ({self.x2})")
        if self.y1 >= self.y2:
            raise ValueError(f"y1 ({self.y1}) must be less than y2 ({self.y2})")


@dataclass(frozen=True)
class IntersectionResult:
    """Result of an intersection check, carrying the type and optional geometry."""
    type: IntersectionType
    geometry: Point | LineSegment | Rectangle | None


@dataclass(frozen=True)
class AdjacencyResult:
    """Result of an adjacency check, carrying the type and the shared segment."""
    type: AdjacencyType
    geometry: LineSegment | None
