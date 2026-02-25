from __future__ import annotations

import sys
import types
from pathlib import Path

import pytest


def _install_spym_stub() -> None:
    if "spym" in sys.modules:
        return
    try:
        __import__("spym")
    except Exception:
        spym_stub = types.ModuleType("spym")

        def _missing_load(_path: str):
            raise RuntimeError("spym.load stub was used without monkeypatching in test.")

        spym_stub.load = _missing_load
        sys.modules["spym"] = spym_stub


def _install_pyqt_stub() -> None:
    if "PyQt6" in sys.modules:
        return
    try:
        __import__("PyQt6")
    except Exception:
        pyqt6_mod = types.ModuleType("PyQt6")
        qtwidgets_mod = types.ModuleType("PyQt6.QtWidgets")
        qtcore_mod = types.ModuleType("PyQt6.QtCore")

        class QMessageBoxStub:
            @staticmethod
            def warning(*_args, **_kwargs):
                return None

        class QtStub:
            class CheckState:
                Checked = 2
                Unchecked = 0

        qtwidgets_mod.QMessageBox = QMessageBoxStub
        qtcore_mod.Qt = QtStub

        pyqt6_mod.QtWidgets = qtwidgets_mod
        pyqt6_mod.QtCore = qtcore_mod

        sys.modules["PyQt6"] = pyqt6_mod
        sys.modules["PyQt6.QtWidgets"] = qtwidgets_mod
        sys.modules["PyQt6.QtCore"] = qtcore_mod


_install_spym_stub()
_install_pyqt_stub()


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    return Path(__file__).resolve().parent / "fixtures"
