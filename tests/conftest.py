"""Shared pytest fixtures for rectangle tests."""

import pytest

from rectangles import Rectangle


@pytest.fixture
def unit_rect():
    """A 4x4 rectangle anchored at the origin — the most common test shape."""
    return Rectangle(0, 0, 4, 4)


@pytest.fixture
def large_rect():
    """A 10x10 rectangle anchored at the origin."""
    return Rectangle(0, 0, 10, 10)


@pytest.fixture
def inner_rect():
    """An 8x8 rectangle with a 2-unit margin — strictly inside large_rect."""
    return Rectangle(2, 2, 8, 8)
