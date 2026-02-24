# Rectangle Analyzer

![CI](https://github.com/<your-username>/EY_Interview/actions/workflows/ci.yml/badge.svg)

A Python library that analyzes geometric relationships between axis-aligned rectangles in 2D space. Covers three operations: **intersection**, **containment**, and **adjacency**.

---

## Requirements

- Python 3.10+
- pytest
- pytest-cov

Install dependencies:

```bash
pip install pytest pytest-cov
```

---

## Project Structure

```
rectangles/
  __init__.py          # Public exports
  models.py            # Point, LineSegment, Rectangle, IntersectionResult
  enums.py             # IntersectionType, ContainmentType, AdjacencyType
  analyzer.py          # RectangleAnalyzer — the three algorithms
tests/
  test_intersection.py
  test_containment.py
  test_adjacency.py
main.py                # Demo script
setup.cfg              # pytest + coverage configuration
```

---

## Usage

Each rectangle is defined by its **bottom-left** `(x1, y1)` and **top-right** `(x2, y2)` corners, where `x1 < x2` and `y1 < y2`.

```python
from rectangles import Rectangle, RectangleAnalyzer

a = Rectangle(0, 0, 4, 4)
b = Rectangle(2, 2, 6, 6)
```

### Intersection

Determines whether two rectangles intersect and classifies the result.

```python
from rectangles import RectangleAnalyzer, IntersectionType

result = RectangleAnalyzer.intersect(a, b)
print(result.type)      # IntersectionType.AREA
print(result.geometry)  # Rectangle(x1=2, y1=2, x2=4, y2=4)
```

| Type | Description | Geometry returned |
|------|-------------|-------------------|
| `NONE` | No contact | `None` |
| `POINT` | Corners touch | `Point` |
| `LINE` | Shared edge segment | `LineSegment` |
| `AREA` | Overlapping region | `Rectangle` |

### Containment

Determines whether one rectangle is **strictly** inside the other. Touching edges do not count.

```python
from rectangles import ContainmentType

inner = Rectangle(2, 2, 8, 8)
outer = Rectangle(0, 0, 10, 10)

result = RectangleAnalyzer.containment(inner, outer)
print(result)  # ContainmentType.A_IN_B
```

| Result | Description |
|--------|-------------|
| `A_IN_B` | `a` is strictly inside `b` |
| `B_IN_A` | `b` is strictly inside `a` |
| `NONE` | Neither is contained |

### Adjacency

Determines whether two rectangles share a side segment of positive length.

```python
from rectangles import AdjacencyType

a = Rectangle(0, 0, 4, 4)
b = Rectangle(4, 1, 8, 3)  # b's left side sits inside a's right side

result = RectangleAnalyzer.adjacency(a, b)
print(result)  # AdjacencyType.SUB_LINE
```

| Type | Description |
|------|-------------|
| `PROPER` | Full sides are identical |
| `SUB_LINE` | One rectangle's full side lies inside the other's longer side |
| `PARTIAL` | Sides partially overlap |
| `NONE` | Not adjacent (includes gaps, corner touches, and area overlaps) |

---

## CLI

Analyze any two rectangles directly from the command line:

```bash
# Single operation
python -m rectangles intersect   0 0 4 4   2 2 6 6
python -m rectangles containment 0 0 10 10  2 2 8 8
python -m rectangles adjacency   0 0 4 4   4 0 8 4

# Run all three at once
python -m rectangles all 0 0 4 4 4 0 8 4
```

Coordinates are provided as `x1 y1 x2 y2` for rectangle A followed by `x1 y1 x2 y2` for rectangle B. Integers and decimals are both accepted.

```
  A = (0.0, 0.0) → (4.0, 4.0)
  B = (4.0, 0.0) → (8.0, 4.0)

  Intersection : line
  Geometry     : LineSegment(4.0, 0.0) → (4.0, 4.0)
  Containment  : neither contains the other
  Adjacency    : proper
  Shared edge  : LineSegment(4.0, 0.0) → (4.0, 4.0)
```

## Running the Demo

```bash
python main.py
```

---

## Running Tests

```bash
# Run all tests with coverage report
pytest

# Run a single test file
pytest tests/test_intersection.py

# Run a single test by name
pytest tests/test_adjacency.py::TestProperAdjacency::test_proper_right_side

# Generate an HTML coverage report
pytest --cov-report=html && open htmlcov/index.html
```

Coverage is enforced on every run. The build fails if total coverage drops below **95%**.

Current status: **65 tests, 100% coverage**.

---

## Algorithm Design

All three algorithms run in **O(1)** time and space.

**Intersection** — computes the 1-D overlap range in x and y independently using `max(x1s)` and `min(x2s)`. The combination of zero/positive width and height maps to the four result types.

**Containment** — four strict inequality comparisons (`<` not `<=`) per axis. Touching edges use equality so they correctly return `NONE`.

**Adjacency** — checks if any pair of edges are co-linear (e.g. `a.x2 == b.x1`), then classifies the 1-D span overlap on the shared axis:
- overlap equals both spans → `PROPER`
- overlap equals exactly one span → `SUB_LINE`
- overlap is a strict subset of both → `PARTIAL`
- overlap is a point or empty → `NONE`
