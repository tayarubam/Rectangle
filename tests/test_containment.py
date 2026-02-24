"""Tests for rectangle containment detection."""

import pytest

from rectangles import ContainmentType, Rectangle, RectangleAnalyzer

# ---------------------------------------------------------------------------
# A strictly inside B
# ---------------------------------------------------------------------------

class TestAInsideB:
    @pytest.mark.parametrize("a,b", [
        pytest.param(Rectangle(2, 2, 8, 8), Rectangle(0,  0, 10, 10), id="centered"),
        pytest.param(Rectangle(1, 1, 3, 3), Rectangle(0,  0, 10, 10), id="small_inside_large"),
        pytest.param(Rectangle(1, 1, 9, 9), Rectangle(0,  0, 10, 10), id="near_edge_not_touching"),
    ])
    def test_a_inside_b(self, a, b):
        assert RectangleAnalyzer.containment(a, b) == ContainmentType.A_IN_B


# ---------------------------------------------------------------------------
# B strictly inside A
# ---------------------------------------------------------------------------

class TestBInsideA:
    @pytest.mark.parametrize("a,b", [
        pytest.param(Rectangle(0,  0, 10, 10), Rectangle(2, 2, 8, 8), id="large_contains_centered"),
        pytest.param(Rectangle(0,  0, 20, 20), Rectangle(5, 5, 6, 6), id="large_contains_tiny"),
    ])
    def test_b_inside_a(self, a, b):
        assert RectangleAnalyzer.containment(a, b) == ContainmentType.B_IN_A

    def test_symmetry(self, large_rect, inner_rect):
        """Swapping A and B flips the containment direction."""
        assert RectangleAnalyzer.containment(large_rect, inner_rect) == ContainmentType.B_IN_A
        assert RectangleAnalyzer.containment(inner_rect, large_rect) == ContainmentType.A_IN_B


# ---------------------------------------------------------------------------
# Neither contained — overlapping, separate, or adjacent
# ---------------------------------------------------------------------------

class TestNeitherContained:
    @pytest.mark.parametrize("a,b", [
        pytest.param(Rectangle(0, 0, 5, 5), Rectangle(3, 3, 8, 8), id="overlapping"),
        pytest.param(Rectangle(0, 0, 4, 4), Rectangle(6, 6, 10, 10), id="completely_separate"),
        pytest.param(Rectangle(0, 0, 4, 4), Rectangle(5, 0,  9,  4), id="side_by_side_with_gap"),
        pytest.param(Rectangle(0, 0, 4, 4), Rectangle(4, 0,  8,  4), id="adjacent_right"),
        pytest.param(Rectangle(0, 0, 4, 4), Rectangle(0, 4,  4,  8), id="adjacent_top"),
    ])
    def test_not_contained(self, a, b):
        assert RectangleAnalyzer.containment(a, b) == ContainmentType.NONE


# ---------------------------------------------------------------------------
# Touching edges do NOT count as containment
# ---------------------------------------------------------------------------

class TestTouchingEdgesNotContainment:
    @pytest.mark.parametrize("a,b", [
        pytest.param(Rectangle(0, 1, 4, 3), Rectangle(0, 0, 5, 4), id="shared_left_edge"),
        pytest.param(Rectangle(1, 1, 5, 3), Rectangle(0, 0, 5, 4), id="shared_right_edge"),
        pytest.param(Rectangle(1, 0, 3, 4), Rectangle(0, 0, 5, 5), id="shared_bottom_edge"),
        pytest.param(Rectangle(1, 1, 3, 5), Rectangle(0, 0, 5, 5), id="shared_top_edge"),
        pytest.param(Rectangle(0, 0, 5, 5), Rectangle(0, 0, 5, 5), id="identical_rectangles"),
        pytest.param(Rectangle(0, 0, 3, 3), Rectangle(0, 0, 5, 5), id="shared_corner"),
    ])
    def test_touching_is_not_containment(self, a, b):
        assert RectangleAnalyzer.containment(a, b) == ContainmentType.NONE
