"""Tests for the CLI interface."""

import pytest

from rectangles.cli import _fmt_geometry, run

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def output(capsys) -> str:
    return capsys.readouterr().out


def stderr(capsys) -> str:
    return capsys.readouterr().err


# ---------------------------------------------------------------------------
# Intersect command
# ---------------------------------------------------------------------------

class TestIntersectCommand:
    @pytest.mark.parametrize("args,expected_type,expected_geometry", [
        pytest.param(
            ["intersect", "0", "0", "4", "4", "6", "0", "10", "4"],
            "none", None,
            id="no_intersection",
        ),
        pytest.param(
            ["intersect", "0", "0", "4", "4", "4", "4", "8", "8"],
            "point", "Point(4.0, 4.0)",
            id="point_intersection",
        ),
        pytest.param(
            ["intersect", "0", "0", "4", "4", "4", "0", "8", "4"],
            "line", "LineSegment",
            id="line_intersection",
        ),
        pytest.param(
            ["intersect", "0", "0", "4", "4", "2", "2", "6", "6"],
            "area", "Rectangle",
            id="area_intersection",
        ),
    ])
    def test_intersect(self, capsys, args, expected_type, expected_geometry):
        assert run(args) == 0
        out = output(capsys)
        assert expected_type in out
        if expected_geometry:
            assert expected_geometry in out

    def test_shows_both_rectangles(self, capsys):
        run(["intersect", "0", "0", "4", "4", "2", "2", "6", "6"])
        out = output(capsys)
        assert "0.0" in out
        assert "4.0" in out


# ---------------------------------------------------------------------------
# Containment command
# ---------------------------------------------------------------------------

class TestContainmentCommand:
    @pytest.mark.parametrize("args,expected_label", [
        pytest.param(
            ["containment", "2", "2", "8", "8", "0", "0", "10", "10"],
            "A is strictly inside B",
            id="a_in_b",
        ),
        pytest.param(
            ["containment", "0", "0", "10", "10", "2", "2", "8", "8"],
            "B is strictly inside A",
            id="b_in_a",
        ),
        pytest.param(
            ["containment", "0", "0", "5", "5", "3", "3", "8", "8"],
            "neither contains the other",
            id="neither",
        ),
    ])
    def test_containment(self, capsys, args, expected_label):
        assert run(args) == 0
        assert expected_label in output(capsys)


# ---------------------------------------------------------------------------
# Adjacency command
# ---------------------------------------------------------------------------

class TestAdjacencyCommand:
    @pytest.mark.parametrize("args,expected_type,shows_geometry", [
        pytest.param(
            ["adjacency", "0", "0", "4", "4", "4", "0", "8", "4"],
            "proper", True,
            id="proper",
        ),
        pytest.param(
            ["adjacency", "0", "0", "4", "4", "4", "1", "8", "3"],
            "sub-line", True,
            id="sub_line",
        ),
        pytest.param(
            ["adjacency", "0", "0", "4", "4", "4", "2", "8", "6"],
            "partial", True,
            id="partial",
        ),
        pytest.param(
            ["adjacency", "0", "0", "4", "4", "6", "0", "10", "4"],
            "none", False,
            id="not_adjacent",
        ),
    ])
    def test_adjacency(self, capsys, args, expected_type, shows_geometry):
        assert run(args) == 0
        out = output(capsys)
        assert expected_type in out
        if shows_geometry:
            assert "Shared edge" in out


# ---------------------------------------------------------------------------
# All command
# ---------------------------------------------------------------------------

class TestAllCommand:
    def test_all_shows_three_sections(self, capsys):
        run(["all", "0", "0", "4", "4", "4", "0", "8", "4"])
        out = output(capsys)
        assert "Intersection" in out
        assert "Containment" in out
        assert "Adjacency" in out

    def test_all_returns_zero(self):
        assert run(["all", "0", "0", "4", "4", "2", "2", "6", "6"]) == 0


# ---------------------------------------------------------------------------
# Decimal coordinates
# ---------------------------------------------------------------------------

class TestDecimalCoordinates:
    def test_float_coords(self, capsys):
        assert run(["intersect", "0.5", "0.5", "4.5", "4.5", "2.0", "2.0", "6.0", "6.0"]) == 0
        assert "area" in output(capsys)


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

class TestErrorHandling:
    @pytest.mark.parametrize("args,error_fragment", [
        pytest.param(
            ["intersect", "4", "0", "2", "4", "0", "0", "4", "4"],
            "x1",
            id="rect_a_invalid_x",
        ),
        pytest.param(
            ["intersect", "0", "0", "4", "4", "4", "4", "8", "2"],
            "y1",
            id="rect_b_invalid_y",
        ),
    ])
    def test_invalid_rectangle(self, capsys, args, error_fragment):
        assert run(args) == 1
        assert error_fragment in stderr(capsys)


# ---------------------------------------------------------------------------
# _fmt_geometry helper
# ---------------------------------------------------------------------------

class TestFmtGeometry:
    def test_none_returns_none_string(self):
        assert _fmt_geometry(None) == "none"
