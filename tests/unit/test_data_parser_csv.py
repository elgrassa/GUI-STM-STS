from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from gui import data_parser as dp


def _fixture(fixtures_dir: Path, name: str) -> str:
    return str(fixtures_dir / name)


class FakeDataArray:
    def __init__(self, data: np.ndarray, attrs: dict):
        self.data = data
        self.attrs = attrs


class FakeSm4Data:
    def __init__(self, data_vars: dict[str, FakeDataArray]):
        self.data_vars = data_vars

    def __getitem__(self, key: str) -> FakeDataArray:
        return self.data_vars[key]


def test_load_csv_file_happy_path_sts(fixtures_dir: Path) -> None:
    measurement = dp.load_csv_file(_fixture(fixtures_dir, "sts_valid.csv"))

    channels = measurement.channels
    assert list(channels.keys()) == ["csv_data"]
    channel = channels["csv_data"]

    assert channel["type"] == "sts"
    assert channel["data"].shape == (4, 2)
    assert channel["data"].dtype == float
    assert measurement.metadata["CSV filename"] == "sts_valid.csv"
    assert "Bias range (STS)" in measurement.metadata


def test_load_csv_file_zero_numeric_values_are_handled(fixtures_dir: Path) -> None:
    measurement = dp.load_csv_file(_fixture(fixtures_dir, "sts_valid.csv"))
    channel = measurement.channels["csv_data"]
    assert channel["data"][2, 0] == 0.0


def test_load_csv_file_happy_path_topo(fixtures_dir: Path) -> None:
    measurement = dp.load_csv_file(_fixture(fixtures_dir, "topo_valid.csv"))
    channel = measurement.channels["csv_topo"]

    assert channel["type"] == "topo"
    assert channel["data"].shape == (4, 2)
    assert channel["attrs"]["RHK_Xsize"] == 2
    assert channel["attrs"]["RHK_Ysize"] == 4
    assert measurement.metadata["Surface size (STM)"] != "Unknown"


def test_load_csv_file_missing_columns_raises_value_error(fixtures_dir: Path) -> None:
    with pytest.raises(ValueError, match="CSV header must contain Index"):
        dp.load_csv_file(_fixture(fixtures_dir, "csv_missing_columns.csv"))


def test_load_csv_file_invalid_short_raises_value_error(fixtures_dir: Path) -> None:
    with pytest.raises(ValueError, match="CSV file too short or invalid format"):
        dp.load_csv_file(_fixture(fixtures_dir, "sts_invalid_short.csv"))


def test_load_csv_file_invalid_topo_raises_value_error(fixtures_dir: Path) -> None:
    with pytest.raises(ValueError, match="Invalid TOPO CSV format"):
        dp.load_csv_file(_fixture(fixtures_dir, "topo_invalid.csv"))


def test_load_csv_file_non_numeric_values_do_not_crash(fixtures_dir: Path) -> None:
    measurement = dp.load_csv_file(_fixture(fixtures_dir, "csv_non_numeric.csv"))
    channel = measurement.channels["csv_data"]
    # All Y columns are non-numeric and are dropped by the parser.
    assert channel["data"].shape == (3, 0)
    assert channel["data"].dtype == float


def test_load_csv_file_huge_values_parses_without_exception(fixtures_dir: Path) -> None:
    measurement = dp.load_csv_file(_fixture(fixtures_dir, "csv_huge_values.csv"))
    channel = measurement.channels["csv_data"]
    assert channel["data"].shape == (3, 2)
    assert np.isinf(channel["data"]).any()


def test_load_file_rejects_non_string_path() -> None:
    with pytest.raises(TypeError, match="path must be a string"):
        dp.load_file(123)  # type: ignore[arg-type]


def test_load_file_raises_for_missing_file() -> None:
    with pytest.raises(FileNotFoundError):
        dp.load_file("this_file_should_not_exist_12345.csv")


def test_load_file_rejects_unsupported_extension(tmp_path: Path) -> None:
    txt_file = tmp_path / "sample.txt"
    txt_file.write_text("hello", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported file type"):
        dp.load_file(str(txt_file))


def test_data_manager_load_file_delegates_to_module_loader(monkeypatch: pytest.MonkeyPatch) -> None:
    fake = dp.MeasurementData("fake.csv", {"k": "v"}, {"a": {"title": "A"}})

    def fake_loader(path: str) -> dp.MeasurementData:
        assert path == "fake.csv"
        return fake

    monkeypatch.setattr(dp, "load_file", fake_loader)

    manager = dp.DataManager()
    out = manager.load_file("fake.csv")

    assert out is fake
    assert manager.current_data is fake
    assert manager.filepath == "fake.csv"


def test_sm4_happy_path_mocked(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_data = FakeSm4Data(
        {
            "sts": FakeDataArray(
                data=np.array([1.0, 2.0, 3.0, 4.0]),
                attrs={
                    "long_name": "dI/dU",
                    "RHK_Xunits": "V",
                    "RHK_Yunits": "A",
                    "RHK_Zunits": "A",
                    "RHK_Bias": -0.2,
                    "RHK_Xscale": 0.1,
                    "RHK_Xsize": 4,
                    "RHK_Date": "2025-01-01",
                },
            ),
            "topo": FakeDataArray(
                data=np.array([[1.0, 2.0], [3.0, 4.0]]),
                attrs={
                    "long_name": "Topography",
                    "RHK_Xunits": "m",
                    "RHK_Yunits": "m",
                    "RHK_Zunits": "m",
                    "RHK_Xscale": 1e-9,
                    "RHK_Yscale": 1e-9,
                    "RHK_Xsize": 2,
                    "RHK_Ysize": 2,
                },
            ),
        }
    )

    monkeypatch.setattr(dp, "load_sm4", lambda _path: fake_data)
    measurement = dp.load_sm4_file("synthetic.sm4")

    assert measurement.path == "synthetic.sm4"
    assert set(measurement.channels.keys()) == {"sts", "topo"}
    assert measurement.channels["sts"]["type"] == "sts"
    assert "topo" in measurement.channels
    assert measurement.channels["topo"]["type"] == "topo"
    assert measurement.channels["sts"]["data"].shape == (4, 1)
    assert measurement.channels["topo"]["data"].shape == (2, 2)
    assert measurement.metadata["Surface size (STM)"] != "Unknown"


def test_sm4_missing_keys_mocked(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(dp, "load_sm4", lambda _path: object())
    with pytest.raises(dp.ParseError, match="missing data_vars"):
        dp.load_sm4_file("invalid.sm4")

    class MissingAttrsDataArray:
        def __init__(self):
            self.data = np.array([1.0, 2.0])

    broken = FakeSm4Data({"broken": MissingAttrsDataArray()})  # type: ignore[arg-type]
    monkeypatch.setattr(dp, "load_sm4", lambda _path: broken)
    with pytest.raises(dp.ParseError, match="missing attrs"):
        dp.load_sm4_file("invalid.sm4")


def test_parse_sm4_large_input_guard(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(dp, "MAX_SM4_CHANNEL_POINTS", 10)

    fake_data = FakeSm4Data(
        {
            "sts": FakeDataArray(
                data=np.arange(12, dtype=float),
                attrs={
                    "long_name": "dI/dU",
                    "RHK_Xunits": "V",
                    "RHK_Yunits": "A",
                    "RHK_Zunits": "A",
                },
            )
        }
    )

    monkeypatch.setattr(dp, "load_sm4", lambda _path: fake_data)
    with pytest.raises(dp.ParseError, match="exceeds size limit"):
        dp.load_sm4_file("large.sm4")
