from __future__ import annotations

import numpy as np

from gui import data_parser as dp


def test_to_float_safe_parses_trimmed_numeric_string() -> None:
    assert dp.to_float_safe(" 1,234.5 ; ") == 1234.5


def test_to_float_safe_returns_default_for_invalid_value() -> None:
    assert dp.to_float_safe("not-a-number", default=-1.0) == -1.0


def test_is_metric_channel_returns_true_for_metric_units() -> None:
    channel = {"attrs": {"RHK_Xunits": "m", "RHK_Yunits": "nm", "RHK_Zunits": "angstrom"}}
    assert dp.is_metric_channel(channel) is True


def test_is_metric_channel_returns_false_for_non_metric_units() -> None:
    channel = {"attrs": {"RHK_Xunits": "V", "RHK_Yunits": "A", "RHK_Zunits": "A"}}
    assert dp.is_metric_channel(channel) is False


def test_infer_channel_type_returns_sts_for_non_metric_units() -> None:
    attrs = {"RHK_Xunits": "V", "RHK_Yunits": "A", "RHK_Zunits": "A"}
    assert dp.infer_channel_type(attrs) == "sts"


def test_extract_surface_size_returns_unknown_when_attrs_missing() -> None:
    assert dp.extract_surface_size({}) == "Unknown"


def test_extract_surface_size_computes_for_metric_topography() -> None:
    attrs = {
        "RHK_Xunits": "m",
        "RHK_Yunits": "m",
        "RHK_Xscale": "1e-9",
        "RHK_Yscale": "2e-9",
        "RHK_Xsize": "100",
        "RHK_Ysize": "50",
    }

    assert dp.extract_surface_size(attrs) == "[1.0e-07, 1.0e-07] m"


def test_extract_bias_range_formats_expected_range() -> None:
    attrs = {"RHK_Bias": "-0.2", "RHK_Xscale": "0.1", "RHK_Xsize": "4", "RHK_Xunit": "V"}
    assert dp.extract_bias_range(attrs) == "[-0.2000, 0.2000] V"


def test_build_common_metadata_for_csv_topo_contains_expected_fields() -> None:
    attrs = {
        "RHK_Xscale": "1e-9",
        "RHK_Yscale": "2e-9",
        "RHK_Xsize": "100",
        "RHK_Ysize": "50",
        "RHK_Xunits": "m",
        "RHK_Yunits": "m",
        "RHK_Bias": "0.0",
        "RHK_Date": "2025-01-01",
    }
    metadata = dp.build_common_metadata("/tmp/sample.csv", attrs, "topo", file_type="csv")
    assert metadata["Original"] == "sample.csv"
    assert metadata["CSV filename"] == "sample.csv"
    assert metadata["Date"] == "2025-01-01"
    assert metadata["Surface size (STM)"] != "Unknown"


def test_build_channel_from_csv_sets_defaults_and_returns_2d_array() -> None:
    x = np.array([-0.2, -0.1, 0.0], dtype=float)
    y = np.array([1.0, 2.0, 3.0], dtype=float)  # 1D on purpose
    metadata = {"CSV filename": "sample.csv"}
    channel = dp.build_channel_from_csv(x, y, metadata, ["Current"])["csv_data"]

    assert channel["type"] == "sts"
    assert channel["data"].shape == (3, 1)
    assert channel["attrs"]["File"] == "sample.csv"
    assert channel["attrs"]["CSV_Ylabels"] == ["Current"]
    assert channel["attrs"]["RHK_Xunits"] == "V"
