from pathlib import Path

from PyInstaller.utils.hooks import (
    collect_data_files,
    collect_dynamic_libs,
    collect_submodules,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_SCRIPT = PROJECT_ROOT / "main.py"


packages = (
    "PyQt6",
    "matplotlib",
    "numpy",
    "scipy",
    "spym",
    "lmfit",
    "xarray",
    "hvplot",
)

datas = []
binaries = []
hiddenimports = [
    "PyQt6.sip",
    "matplotlib.backends.backend_qtagg",
    "matplotlib.backends.backend_qt5agg",
]

for pkg in packages:
    hiddenimports += collect_submodules(pkg)
    datas += collect_data_files(pkg)
    binaries += collect_dynamic_libs(pkg)


a = Analysis(
    [str(MAIN_SCRIPT)],
    pathex=[str(PROJECT_ROOT)],
    binaries=binaries,
    datas=datas,
    hiddenimports=sorted(set(hiddenimports)),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="GUI-STM-STS",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="GUI-STM-STS",
)
