"""Rectangle relationship analyzer."""

from .enums import AdjacencyType, ContainmentType, IntersectionType
from .models import AdjacencyResult, IntersectionResult, LineSegment, Point, Rectangle


class RectangleAnalyzer:
    """Provides geometric relationship analysis between two axis-aligned rectangles."""

    @staticmethod
    def intersect(a: Rectangle, b: Rectangle) -> IntersectionResult:
        """Determine how two rectangles intersect.

        Computes the 1-D overlap range in x and y using max(x1s)/min(x2s) and
        classifies the result based on the overlap dimensions.

        Args:
            a: The first rectangle.
            b: The second rectangle.

        Returns:
            An IntersectionResult with NONE (no contact), POINT (corner touch),
            LINE (shared edge segment), or AREA (overlapping region).
        """
        ox1 = max(a.x1, b.x1)
        ox2 = min(a.x2, b.x2)
        oy1 = max(a.y1, b.y1)
        oy2 = min(a.y2, b.y2)

        if ox1 > ox2 or oy1 > oy2:
            return IntersectionResult(IntersectionType.NONE, None)

        if ox1 == ox2 and oy1 == oy2:
            return IntersectionResult(IntersectionType.POINT, Point(ox1, oy1))

        if ox1 == ox2:
            # Zero-width overlap → vertical line segment
            return IntersectionResult(
                IntersectionType.LINE,
                LineSegment(Point(ox1, oy1), Point(ox1, oy2)),
            )

        if oy1 == oy2:
            # Zero-height overlap → horizontal line segment
            return IntersectionResult(
                IntersectionType.LINE,
                LineSegment(Point(ox1, oy1), Point(ox2, oy1)),
            )

        return IntersectionResult(
            IntersectionType.AREA,
            Rectangle(ox1, oy1, ox2, oy2),
        )

    @staticmethod
    def containment(a: Rectangle, b: Rectangle) -> ContainmentType:
        """Determine strict containment between two rectangles.

        A rectangle is strictly contained only when all four of its edges lie
        entirely inside the other rectangle's interior — touching the boundary
        does not qualify.

        Args:
            a: The first rectangle.
            b: The second rectangle.

        Returns:
            ContainmentType.A_IN_B, B_IN_A, or NONE.
        """
        if b.x1 < a.x1 and a.x2 < b.x2 and b.y1 < a.y1 and a.y2 < b.y2:
            return ContainmentType.A_IN_B
        if a.x1 < b.x1 and b.x2 < a.x2 and a.y1 < b.y1 and b.y2 < a.y2:
            return ContainmentType.B_IN_A
        return ContainmentType.NONE

    @staticmethod
    def adjacency(a: Rectangle, b: Rectangle) -> AdjacencyResult:
        """Determine adjacency between two rectangles.

        Two rectangles are adjacent when they share a side segment of positive
        length. The type is determined by comparing the shared overlap against
        each rectangle's full side: PROPER when both sides are identical,
        SUB_LINE when one side fits entirely within the other, PARTIAL when
        there is a strict subset overlap. Corner touches and area overlaps
        return NONE.

        Args:
            a: The first rectangle.
            b: The second rectangle.

        Returns:
            An AdjacencyResult with the adjacency type and the shared
            LineSegment geometry, or NONE with geometry=None when not adjacent.
        """

        def _classify(shared: float, vertical: bool, span_a: tuple, span_b: tuple) -> AdjacencyResult | None:
            """Classify 1-D span overlap and build the shared segment, or return None."""
            lo = max(span_a[0], span_b[0])
            hi = min(span_a[1], span_b[1])
            if hi <= lo:
                return None  # No overlap or only a point
            a_full = (lo == span_a[0] and hi == span_a[1])
            b_full = (lo == span_b[0] and hi == span_b[1])
            if a_full and b_full:
                adj_type = AdjacencyType.PROPER
            elif a_full or b_full:
                adj_type = AdjacencyType.SUB_LINE
            else:
                adj_type = AdjacencyType.PARTIAL
            segment = (
                LineSegment(Point(shared, lo), Point(shared, hi))
                if vertical
                else LineSegment(Point(lo, shared), Point(hi, shared))
            )
            return AdjacencyResult(adj_type, segment)

        # Check vertical shared edges (a's right meets b's left, or vice versa)
        if a.x2 == b.x1:
            result = _classify(a.x2, True, (a.y1, a.y2), (b.y1, b.y2))
            if result is not None:
                return result
        if a.x1 == b.x2:
            result = _classify(a.x1, True, (a.y1, a.y2), (b.y1, b.y2))
            if result is not None:
                return result

        # Check horizontal shared edges (a's top meets b's bottom, or vice versa)
        if a.y2 == b.y1:
            result = _classify(a.y2, False, (a.x1, a.x2), (b.x1, b.x2))
            if result is not None:
                return result
        if a.y1 == b.y2:
            result = _classify(a.y1, False, (a.x1, a.x2), (b.x1, b.x2))
            if result is not None:
                return result

        return AdjacencyResult(AdjacencyType.NONE, None)
