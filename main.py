"""Demo script — showcases intersection, containment, and adjacency analysis."""

from rectangles import Rectangle, RectangleAnalyzer
from rectangles.enums import AdjacencyType, ContainmentType


def section(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def show_intersection(label: str, a: Rectangle, b: Rectangle) -> None:
    result = RectangleAnalyzer.intersect(a, b)
    print(f"\n{label}")
    print(f"  A = {a}")
    print(f"  B = {b}")
    print(f"  Type     : {result.type.value}")
    print(f"  Geometry : {result.geometry}")


def show_containment(label: str, a: Rectangle, b: Rectangle) -> None:
    result = RectangleAnalyzer.containment(a, b)
    descriptions = {
        ContainmentType.A_IN_B: "A is strictly inside B",
        ContainmentType.B_IN_A: "B is strictly inside A",
        ContainmentType.NONE:   "Neither contains the other",
    }
    print(f"\n{label}")
    print(f"  A = {a}")
    print(f"  B = {b}")
    print(f"  Result : {descriptions[result]}")


def show_adjacency(label: str, a: Rectangle, b: Rectangle) -> None:
    result = RectangleAnalyzer.adjacency(a, b)
    descriptions = {
        AdjacencyType.PROPER:   "Proper  — full sides match",
        AdjacencyType.SUB_LINE: "Sub-line — one full side lies inside the other",
        AdjacencyType.PARTIAL:  "Partial — sides partially overlap",
        AdjacencyType.NONE:     "Not adjacent",
    }
    print(f"\n{label}")
    print(f"  A        : {a}")
    print(f"  B        : {b}")
    print(f"  Type     : {descriptions[result.type]}")
    print(f"  Geometry : {result.geometry}")


def main() -> None:
    # ------------------------------------------------------------------ #
    # Intersection                                                         #
    # ------------------------------------------------------------------ #
    section("INTERSECTION")

    show_intersection(
        "No intersection (separate rectangles)",
        Rectangle(0, 0, 4, 4),
        Rectangle(6, 0, 10, 4),
    )
    show_intersection(
        "Point intersection (corners touch)",
        Rectangle(0, 0, 4, 4),
        Rectangle(4, 4, 8, 8),
    )
    show_intersection(
        "Line intersection (shared full edge)",
        Rectangle(0, 0, 4, 4),
        Rectangle(4, 0, 8, 4),
    )
    show_intersection(
        "Line intersection (partial shared edge)",
        Rectangle(0, 0, 4, 4),
        Rectangle(4, 2, 8, 6),
    )
    show_intersection(
        "Area intersection (overlapping region)",
        Rectangle(0, 0, 6, 6),
        Rectangle(3, 3, 9, 9),
    )
    show_intersection(
        "Area intersection (one inside the other)",
        Rectangle(0, 0, 10, 10),
        Rectangle(2, 2, 8, 8),
    )

    # ------------------------------------------------------------------ #
    # Containment                                                          #
    # ------------------------------------------------------------------ #
    section("CONTAINMENT")

    show_containment(
        "A strictly inside B",
        Rectangle(2, 2, 8, 8),
        Rectangle(0, 0, 10, 10),
    )
    show_containment(
        "B strictly inside A",
        Rectangle(0, 0, 10, 10),
        Rectangle(3, 3, 7, 7),
    )
    show_containment(
        "Neither (overlapping)",
        Rectangle(0, 0, 5, 5),
        Rectangle(3, 3, 8, 8),
    )
    show_containment(
        "Neither (touching edge — not containment)",
        Rectangle(0, 1, 4, 3),
        Rectangle(0, 0, 5, 4),
    )

    # ------------------------------------------------------------------ #
    # Adjacency                                                            #
    # ------------------------------------------------------------------ #
    section("ADJACENCY")

    show_adjacency(
        "Proper — full sides identical",
        Rectangle(0, 0, 4, 4),
        Rectangle(4, 0, 8, 4),
    )
    show_adjacency(
        "Sub-line — A's full side inside B's longer side",
        Rectangle(0, 1, 4, 3),
        Rectangle(4, 0, 8, 4),
    )
    show_adjacency(
        "Sub-line — B's full side inside A's longer side",
        Rectangle(0, 0, 4, 4),
        Rectangle(4, 1, 8, 3),
    )
    show_adjacency(
        "Partial — sides partially overlap",
        Rectangle(0, 0, 4, 4),
        Rectangle(4, 2, 8, 6),
    )
    show_adjacency(
        "Not adjacent — gap between rectangles",
        Rectangle(0, 0, 4, 4),
        Rectangle(5, 0, 9, 4),
    )
    show_adjacency(
        "Not adjacent — corner touch only",
        Rectangle(0, 0, 4, 4),
        Rectangle(4, 4, 8, 8),
    )
    show_adjacency(
        "Not adjacent — area overlap",
        Rectangle(0, 0, 5, 5),
        Rectangle(3, 3, 8, 8),
    )

    print()


if __name__ == "__main__":
    main()
