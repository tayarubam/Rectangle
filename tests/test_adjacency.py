"""Tests for rectangle adjacency detection and classification.

Adjacency definitions:
  PROPER   — the entire side of A equals the entire side of B
  SUB_LINE — one rectangle's full side lies completely inside the other's longer side
  PARTIAL  — only part of one side overlaps with part of another side
  NONE     — no shared side segment (includes gaps, corner touches, and area overlaps)
"""

import pytest

from rectangles import AdjacencyType, Rectangle, RectangleAnalyzer
from rectangles.models import LineSegment, Point

# ---------------------------------------------------------------------------
# Proper adjacency (entire matching sides)
# ---------------------------------------------------------------------------

class TestProperAdjacency:
    @pytest.mark.parametrize("a,b,expected_segment", [
        pytest.param(
            Rectangle(0, 0, 4, 4), Rectangle(4, 0, 8, 4),
            LineSegment(Point(4, 0), Point(4, 4)),
            id="right_side",
        ),
        pytest.param(
            Rectangle(4, 0, 8, 4), Rectangle(0, 0, 4, 4),
            LineSegment(Point(4, 0), Point(4, 4)),
            id="left_side",
        ),
        pytest.param(
            Rectangle(0, 0, 4, 4), Rectangle(0, 4, 4, 8),
            LineSegment(Point(0, 4), Point(4, 4)),
            id="top_side",
        ),
        pytest.param(
            Rectangle(0, 4, 4, 8), Rectangle(0, 0, 4, 4),
            LineSegment(Point(0, 4), Point(4, 4)),
            id="bottom_side",
        ),
    ])
    def test_proper_adjacency(self, a, b, expected_segment):
        result = RectangleAnalyzer.adjacency(a, b)
        assert result.type == AdjacencyType.PROPER
        assert result.geometry == expected_segment


# ---------------------------------------------------------------------------
# Sub-line adjacency (one full side contained inside a longer side)
# ---------------------------------------------------------------------------

class TestSubLineAdjacency:
    @pytest.mark.parametrize("a,b,expected_segment", [
        pytest.param(
            Rectangle(0, 0, 4, 4), Rectangle(4, -2, 8, 6),
            LineSegment(Point(4, 0), Point(4, 4)),
            id="a_right_inside_b_left",
        ),
        pytest.param(
            Rectangle(0, 0, 4, 4), Rectangle(4,  1, 8, 3),
            LineSegment(Point(4, 1), Point(4, 3)),
            id="b_left_inside_a_right",
        ),
        pytest.param(
            Rectangle(1, 0, 3, 4), Rectangle(0,  4, 4, 8),
            LineSegment(Point(1, 4), Point(3, 4)),
            id="a_top_inside_b_bottom",
        ),
        pytest.param(
            Rectangle(0, 0, 4, 4), Rectangle(1,  4, 3, 8),
            LineSegment(Point(1, 4), Point(3, 4)),
            id="b_bottom_inside_a_top",
        ),
    ])
    def test_sub_line_adjacency(self, a, b, expected_segment):
        result = RectangleAnalyzer.adjacency(a, b)
        assert result.type == AdjacencyType.SUB_LINE
        assert result.geometry == expected_segment


# ---------------------------------------------------------------------------
# Partial adjacency (partial side overlap)
# ---------------------------------------------------------------------------

class TestPartialAdjacency:
    @pytest.mark.parametrize("a,b,expected_segment", [
        pytest.param(
            Rectangle(0, 0, 4, 4), Rectangle(4, 2, 8, 6),
            LineSegment(Point(4, 2), Point(4, 4)),
            id="right_partial_upper",
        ),
        pytest.param(
            Rectangle(4, 2, 8, 6), Rectangle(0, 0, 4, 4),
            LineSegment(Point(4, 2), Point(4, 4)),
            id="left_partial_lower",
        ),
        pytest.param(
            Rectangle(0, 0, 4, 4), Rectangle(2, 4, 6, 8),
            LineSegment(Point(2, 4), Point(4, 4)),
            id="top_partial_right",
        ),
        pytest.param(
            Rectangle(2, 4, 6, 8), Rectangle(0, 0, 4, 4),
            LineSegment(Point(2, 4), Point(4, 4)),
            id="bottom_partial_left",
        ),
        pytest.param(
            Rectangle(0, 2, 4, 6), Rectangle(4, 0, 8, 4),
            LineSegment(Point(4, 2), Point(4, 4)),
            id="right_partial_lower",
        ),
    ])
    def test_partial_adjacency(self, a, b, expected_segment):
        result = RectangleAnalyzer.adjacency(a, b)
        assert result.type == AdjacencyType.PARTIAL
        assert result.geometry == expected_segment


# ---------------------------------------------------------------------------
# Symmetry — all adjacency types must be order-independent
# ---------------------------------------------------------------------------

class TestAdjacencySymmetry:
    @pytest.mark.parametrize("a,b", [
        pytest.param(Rectangle(0, 0, 4, 4), Rectangle(4, 0, 8, 4), id="proper"),
        pytest.param(Rectangle(0, 0, 4, 4), Rectangle(4, 1, 8, 3), id="sub_line"),
        pytest.param(Rectangle(0, 0, 4, 4), Rectangle(4, 2, 8, 6), id="partial"),
    ])
    def test_adjacency_symmetric(self, a, b):
        assert RectangleAnalyzer.adjacency(a, b) == RectangleAnalyzer.adjacency(b, a)


# ---------------------------------------------------------------------------
# Not adjacent
# ---------------------------------------------------------------------------

class TestNotAdjacent:
    @pytest.mark.parametrize("a,b", [
        pytest.param(Rectangle(0, 0, 4, 4), Rectangle(5,  0,  9,  4), id="gap_horizontal"),
        pytest.param(Rectangle(0, 0, 4, 4), Rectangle(0,  5,  4,  9), id="gap_vertical"),
        pytest.param(Rectangle(0, 0, 4, 4), Rectangle(4,  4,  8,  8), id="corner_touch_top_right"),
        pytest.param(Rectangle(4, 4, 8, 8), Rectangle(0,  0,  4,  4), id="corner_touch_bottom_left"),
        pytest.param(Rectangle(0, 0, 5, 5), Rectangle(3,  3,  8,  8), id="area_overlap"),
        pytest.param(Rectangle(0, 0, 10, 10), Rectangle(2, 2,  8,  8), id="one_inside_other"),
        pytest.param(Rectangle(0, 0, 3,  3), Rectangle(5,  5,  9,  9), id="separate_diagonal"),
        pytest.param(Rectangle(0, 0, 4,  2), Rectangle(4,  3,  8,  6), id="aligned_no_y_overlap"),
        pytest.param(Rectangle(0, 0, 2,  4), Rectangle(3,  4,  6,  8), id="aligned_no_x_overlap"),
    ])
    def test_not_adjacent(self, a, b):
        result = RectangleAnalyzer.adjacency(a, b)
        assert result.type == AdjacencyType.NONE
        assert result.geometry is None
