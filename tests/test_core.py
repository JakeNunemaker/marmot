"""Tests for the `marmot._core` module."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2019, Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


import numpy as np
import pytest

from marmot import ge, gt, le, lt, true, false


def test_gt(state):

    with pytest.raises(TypeError):
        _ = gt(False)

    with pytest.raises(TypeError):
        _ = gt("2")

    constraint = gt(70)
    expected = np.concatenate([np.array([False] * 5), np.array([True] * 5)])

    assert all(constraint(state["temp"]) == expected)


def test_ge(state):

    with pytest.raises(TypeError):
        _ = ge(False)

    with pytest.raises(TypeError):
        _ = ge("2")

    constraint = ge(70)
    expected = np.concatenate([np.array([False] * 4), np.array([True] * 6)])

    assert all(constraint(state["temp"]) == expected)


def test_lt(state):

    with pytest.raises(TypeError):
        _ = lt(False)

    with pytest.raises(TypeError):
        _ = lt("2")

    constraint = lt(70)
    expected = np.concatenate([np.array([True] * 4), np.array([False] * 6)])

    assert all(constraint(state["temp"]) == expected)


def test_le(state):

    with pytest.raises(TypeError):
        _ = le(False)

    with pytest.raises(TypeError):
        _ = le("2")

    constraint = le(70)
    expected = np.concatenate([np.array([True] * 5), np.array([False] * 5)])

    assert all(constraint(state["temp"]) == expected)


def test_true(state):

    constraint = true()
    expected = np.concatenate([np.array([False] * 6), np.array([True] * 4)])

    output = constraint(state["workday"])
    assert all(output == expected)


def test_false(state):

    constraint = false()
    expected = np.concatenate([np.array([True] * 6), np.array([False] * 4)])

    output = constraint(state["workday"])
    assert all(output == expected)
