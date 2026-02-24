"""Command-line interface for rectangle relationship analysis."""

import argparse
import sys

from .analyzer import RectangleAnalyzer
from .enums import AdjacencyType, ContainmentType
from .models import AdjacencyResult, IntersectionResult, LineSegment, Point, Rectangle


def _build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser for the CLI.

    Returns:
        A configured ArgumentParser with intersect, containment, adjacency,
        and all subcommands.
    """
    parser = argparse.ArgumentParser(
        prog="python -m rectangles",
        description="Analyze geometric relationships between two axis-aligned rectangles.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Each rectangle is defined by its bottom-left (x1 y1) and top-right (x2 y2) corners.
Coordinates may be integers or decimals. Constraint: x1 < x2 and y1 < y2.

Examples:
  python -m rectangles intersect   0 0 4 4   2 2 6 6
  python -m rectangles containment 0 0 10 10  2 2 8 8
  python -m rectangles adjacency   0 0 4 4   4 0 8 4
  python -m rectangles all         0 0 4 4   4 2 8 6
        """,
    )

    subparsers = parser.add_subparsers(dest="command", metavar="<operation>")
    subparsers.required = True

    _operations = {
        "intersect":   "Determine if and how two rectangles intersect",
        "containment": "Determine if one rectangle is contained within the other",
        "adjacency":   "Determine if and how two rectangles are adjacent",
        "all":         "Run all three analyses",
    }

    for cmd, help_text in _operations.items():
        sub = subparsers.add_parser(cmd, help=help_text)
        sub.add_argument("ax1", type=float, metavar="Ax1")
        sub.add_argument("ay1", type=float, metavar="Ay1")
        sub.add_argument("ax2", type=float, metavar="Ax2")
        sub.add_argument("ay2", type=float, metavar="Ay2")
        sub.add_argument("bx1", type=float, metavar="Bx1")
        sub.add_argument("by1", type=float, metavar="By1")
        sub.add_argument("bx2", type=float, metavar="Bx2")
        sub.add_argument("by2", type=float, metavar="By2")

    return parser


def _fmt_geometry(geometry: Point | LineSegment | Rectangle | None) -> str:
    """Return a compact human-readable string for any intersection/adjacency geometry.

    Args:
        geometry: A Point, LineSegment, Rectangle, or None.

    Returns:
        A formatted string describing the geometry, or ``"none"`` if None.
    """
    if geometry is None:
        return "none"
    if isinstance(geometry, Point):
        return f"Point({geometry.x}, {geometry.y})"
    if isinstance(geometry, LineSegment):
        s, e = geometry.start, geometry.end
        return f"LineSegment({s.x}, {s.y}) → ({e.x}, {e.y})"
    if isinstance(geometry, Rectangle):
        return f"Rectangle({geometry.x1}, {geometry.y1}) → ({geometry.x2}, {geometry.y2})"
    return str(geometry)  # pragma: no cover


def _print_intersection(result: IntersectionResult) -> None:
    """Print the intersection result to stdout.

    Args:
        result: The IntersectionResult to display.
    """
    print(f"  Intersection : {result.type.value}")
    if result.geometry is not None:
        print(f"  Geometry     : {_fmt_geometry(result.geometry)}")


def _print_containment(result: ContainmentType) -> None:
    """Print the containment result to stdout.

    Args:
        result: The ContainmentType to display.
    """
    labels = {
        ContainmentType.A_IN_B: "A is strictly inside B",
        ContainmentType.B_IN_A: "B is strictly inside A",
        ContainmentType.NONE:   "neither contains the other",
    }
    print(f"  Containment  : {labels[result]}")


def _print_adjacency(result: AdjacencyResult) -> None:
    """Print the adjacency result to stdout.

    Args:
        result: The AdjacencyResult to display.
    """
    labels = {
        AdjacencyType.PROPER:   "proper",
        AdjacencyType.SUB_LINE: "sub-line",
        AdjacencyType.PARTIAL:  "partial",
        AdjacencyType.NONE:     "none",
    }
    print(f"  Adjacency    : {labels[result.type]}")
    if result.geometry is not None:
        print(f"  Shared edge  : {_fmt_geometry(result.geometry)}")


def run(argv: list[str] | None = None) -> int:
    """Parse arguments, run the requested analysis, and return an exit code.

    Accepts an optional argv list for testability; defaults to sys.argv[1:].

    Args:
        argv: Argument list to parse. Defaults to sys.argv when None.

    Returns:
        0 on success, 1 on invalid rectangle input.
    """
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        a = Rectangle(args.ax1, args.ay1, args.ax2, args.ay2)
        b = Rectangle(args.bx1, args.by1, args.bx2, args.by2)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"\n  A = ({a.x1}, {a.y1}) → ({a.x2}, {a.y2})")
    print(f"  B = ({b.x1}, {b.y1}) → ({b.x2}, {b.y2})\n")

    cmd = args.command
    if cmd in ("intersect", "all"):
        _print_intersection(RectangleAnalyzer.intersect(a, b))
    if cmd in ("containment", "all"):
        _print_containment(RectangleAnalyzer.containment(a, b))
    if cmd in ("adjacency", "all"):
        _print_adjacency(RectangleAnalyzer.adjacency(a, b))

    print()
    return 0


def main() -> None:  # pragma: no cover
    """Entry point for the CLI."""
    sys.exit(run())
