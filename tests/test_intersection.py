"""Tests for rectangle intersection detection and classification."""

import pytest

from rectangles import (
    IntersectionType,
    LineSegment,
    Point,
    Rectangle,
    RectangleAnalyzer,
)

# ---------------------------------------------------------------------------
# No intersection
# ---------------------------------------------------------------------------

class TestNoIntersection:
    @pytest.mark.parametrize("a,b", [
        pytest.param(Rectangle(0, 0, 4, 4), Rectangle(6, 0, 10, 4), id="separate_horizontal"),
        pytest.param(Rectangle(0, 0, 4, 4), Rectangle(0, 6, 4, 10), id="separate_vertical"),
        pytest.param(Rectangle(0, 0, 3, 3), Rectangle(5, 5, 9,  9), id="separate_diagonal"),
        pytest.param(Rectangle(0, 0, 2, 2), Rectangle(3, 3, 5,  5), id="gap_between"),
    ])
    def test_no_intersection(self, a, b):
        result = RectangleAnalyzer.intersect(a, b)
        assert result.type == IntersectionType.NONE
        assert result.geometry is None


# ---------------------------------------------------------------------------
# Point intersection (corners touch)
# ---------------------------------------------------------------------------

class TestPointIntersection:
    @pytest.mark.parametrize("a,b,expected", [
        pytest.param(Rectangle(0, 0, 4, 4), Rectangle(4, 4, 8, 8), Point(4, 4), id="top_right_meets_bottom_left"),
        pytest.param(Rectangle(4, 0, 8, 4), Rectangle(0, 4, 4, 8), Point(4, 4), id="top_left_meets_bottom_right"),
        pytest.param(Rectangle(0, 4, 4, 8), Rectangle(4, 0, 8, 4), Point(4, 4), id="bottom_right_meets_top_left"),
        pytest.param(Rectangle(4, 4, 8, 8), Rectangle(0, 0, 4, 4), Point(4, 4), id="bottom_left_meets_top_right"),
    ])
    def test_point_intersection(self, a, b, expected):
        result = RectangleAnalyzer.intersect(a, b)
        assert result.type == IntersectionType.POINT
        assert result.geometry == expected


# ---------------------------------------------------------------------------
# Line intersection (shared edge segment)
# ---------------------------------------------------------------------------

class TestLineIntersection:
    @pytest.mark.parametrize("a,b,expected_endpoints", [
        pytest.param(
            Rectangle(0, 0, 4, 4), Rectangle(4, 0, 8, 4),
            {Point(4, 0), Point(4, 4)},
            id="full_vertical_edge",
        ),
        pytest.param(
            Rectangle(0, 0, 4, 4), Rectangle(0, 4, 4, 8),
            {Point(0, 4), Point(4, 4)},
            id="full_horizontal_edge",
        ),
        pytest.param(
            Rectangle(0, 0, 4, 4), Rectangle(4, 2, 8, 6),
            {Point(4, 2), Point(4, 4)},
            id="partial_vertical_edge",
        ),
        pytest.param(
            Rectangle(0, 0, 4, 4), Rectangle(2, 4, 6, 8),
            {Point(2, 4), Point(4, 4)},
            id="partial_horizontal_edge",
        ),
        pytest.param(
            Rectangle(0, 0, 4, 4), Rectangle(4, 1, 8, 3),
            {Point(4, 1), Point(4, 3)},
            id="sub_line_vertical",
        ),
    ])
    def test_line_intersection(self, a, b, expected_endpoints):
        result = RectangleAnalyzer.intersect(a, b)
        assert result.type == IntersectionType.LINE
        assert isinstance(result.geometry, LineSegment)
        assert {result.geometry.start, result.geometry.end} == expected_endpoints


# ---------------------------------------------------------------------------
# Area intersection (overlapping region with positive area)
# ---------------------------------------------------------------------------

class TestAreaIntersection:
    @pytest.mark.parametrize("a,b,expected_region", [
        pytest.param(Rectangle(0, 0, 4, 4), Rectangle(2, 2,  6,  6), Rectangle(2, 2, 4, 4), id="diagonal_overlap"),
        pytest.param(Rectangle(0, 0, 6, 6), Rectangle(2, 1,  8,  5), Rectangle(2, 1, 6, 5), id="asymmetric_overlap"),
        pytest.param(
            Rectangle(2, 2, 6, 6), Rectangle(0, 0, 4, 4), Rectangle(2, 2, 4, 4),
            id="overlap_bottom_left_corner",
        ),
    ])
    def test_area_intersection(self, a, b, expected_region):
        result = RectangleAnalyzer.intersect(a, b)
        assert result.type == IntersectionType.AREA
        assert result.geometry == expected_region

    def test_one_inside_other(self, large_rect, inner_rect):
        result = RectangleAnalyzer.intersect(large_rect, inner_rect)
        assert result.type == IntersectionType.AREA
        assert result.geometry == inner_rect

    def test_identical_rectangles(self, unit_rect):
        result = RectangleAnalyzer.intersect(unit_rect, unit_rect)
        assert result.type == IntersectionType.AREA
        assert result.geometry == unit_rect

    def test_symmetry(self, unit_rect):
        b = Rectangle(2, 2, 6, 6)
        assert RectangleAnalyzer.intersect(unit_rect, b) == RectangleAnalyzer.intersect(b, unit_rect)


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------

class TestInputValidation:
    @pytest.mark.parametrize("x1,y1,x2,y2", [
        pytest.param(4, 0, 2, 4, id="x1_greater_than_x2"),
        pytest.param(0, 4, 4, 2, id="y1_greater_than_y2"),
        pytest.param(0, 0, 0, 4, id="x1_equals_x2"),
    ])
    def test_invalid_rectangle(self, x1, y1, x2, y2):
        with pytest.raises(ValueError):
            Rectangle(x1, y1, x2, y2)
