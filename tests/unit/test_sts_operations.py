from __future__ import annotations

import numpy as np

from gui.channel_viewers.sts_viewer_folder.sts_processing import STSOperations


def test_create_normalized_entry_iu_zero_safe() -> None:
    curve = {
        "x": np.array([-0.2, -0.1, 0.0, 0.1], dtype=float),
        "y": np.array([2.0, 2.0, 2.0, 2.0], dtype=float),
        "label": "C1",
    }
    current = np.array([1.0, 0.0, 2.0, 0.0], dtype=float)
    bias = np.array([-0.2, -0.1, 0.0, 0.1], dtype=float)

    entry = STSOperations.create_normalized_entry(curve, current, bias, mode="IU")

    assert entry is not None
    assert entry["origin"] == "normalize_IU"
    assert np.isfinite(entry["y"]).all()


def test_create_normalized_entry_imax_zero_returns_none() -> None:
    curve = {
        "x": np.array([0.0, 1.0], dtype=float),
        "y": np.array([1.0, 2.0], dtype=float),
        "label": "C2",
    }
    current = np.array([0.0, 0.0], dtype=float)
    bias = np.array([0.0, 1.0], dtype=float)

    assert STSOperations.create_normalized_entry(curve, current, bias, mode="Imax") is None


def test_lockin_derivative_amp_non_positive_falls_back_to_gradient() -> None:
    x = np.array([0.0, 1.0, 2.0, 3.0], dtype=float)
    y = np.array([0.0, 1.0, 4.0, 9.0], dtype=float)

    expected = np.gradient(y, x)
    actual = STSOperations.lockin_derivative(x, y, amp=0.0)

    assert np.allclose(actual, expected)


def test_curve_arithmetic_interpolates_when_x_axes_differ() -> None:
    all_curves = [
        {
            "x": np.array([0.0, 1.0, 2.0, 3.0], dtype=float),
            "y": np.array([0.0, 1.0, 2.0, 3.0], dtype=float),
            "label": "A",
        },
        {
            "x": np.array([0.5, 1.0, 1.5, 2.5], dtype=float),
            "y": np.array([1.0, 1.5, 2.0, 3.0], dtype=float),
            "label": "B",
        },
    ]

    entry = STSOperations.curve_arithmetic(all_curves, 0, 1, "subtract")

    assert entry["label"] == "(A-B)"
    assert entry["x"].shape == (4,)
    assert np.isfinite(entry["y"]).all()


def test_curve_arithmetic_divide_by_zero_produces_nan() -> None:
    all_curves = [
        {
            "x": np.array([0.0, 1.0], dtype=float),
            "y": np.array([2.0, 2.0], dtype=float),
            "label": "A",
        },
        {
            "x": np.array([0.0, 1.0], dtype=float),
            "y": np.array([0.0, 2.0], dtype=float),
            "label": "B",
        },
    ]

    entry = STSOperations.curve_arithmetic(all_curves, 0, 1, "divide")

    assert entry["label"] == "(A/B)"
    assert np.isnan(entry["y"][0])
    assert entry["y"][1] == 1.0


def test_get_bias_axis_returns_expected_shape_and_step() -> None:
    channel_data = {
        "attrs": {"RHK_Bias": -0.2, "RHK_Xscale": 0.1},
        "data": np.zeros((4, 2), dtype=float),
    }

    bias = STSOperations.get_bias_axis(channel_data)

    assert bias.shape == (4,)
    assert np.allclose(bias, np.array([-0.2, -0.1, 0.0, 0.1]))
