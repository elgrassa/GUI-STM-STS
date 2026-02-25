# Architecture (C4-lite)

## Context

`GUI-STM-STS` is a single-process desktop app for local STM/STS data analysis.

- Primary actor: researcher/operator using a local workstation.
- Input: `.csv` and `.sm4` files selected in GUI.
- Output: interactive plots, derived curves, optional CSV/PNG exports.
- External services: none (offline/local workflow).

## Container View

### 1) Desktop UI container (PyQt6)

- Entry point: `main.py`
- Window orchestration and file open flow: `gui/main_window.py`
- STS screen and interactions: `gui/channel_viewers/sts_viewer_folder/sts_viewer.py`
- Topography screen and interactions: `gui/channel_viewers/topo_viewer.py`
- UI utilities/styles: `gui/helpers/metadata_tab.py`, `gui/helpers/styles.py`

### 2) Parsing/data container

- Module: `gui/data_parser.py`
- Responsibilities:
  - route by extension (`load_file`)
  - parse CSV/SM4 (`load_csv_file`, `load_sm4_file`)
  - normalize channel/metadata shape (`MeasurementData`, channel builders)

### 3) Analysis container

- STS processing: `gui/channel_viewers/sts_viewer_folder/sts_processing.py`
- Peak fitting: `gui/channel_viewers/sts_viewer_folder/fit_gauss.py`
- Responsibilities:
  - filtering, normalization, derivative, arithmetic
  - peak detection and Gaussian fit

## Component View (key module map)

- `main.py`: starts `QApplication` and main window.
- `gui/main_window.py`: loads file via `DataManager`; opens STS or TOPO viewer.
- `gui/data_parser.py`: source-of-truth for file ingestion and metadata/channel normalization.
- `gui/channel_viewers/sts_viewer_folder/sts_viewer.py`: curve selection, operations, export.
- `gui/channel_viewers/topo_viewer.py`: 2D map rendering, smoothing/flatten, export.
- `gui/channel_viewers/sts_viewer_folder/sts_processing.py`: pure numeric transforms.
- `gui/channel_viewers/sts_viewer_folder/fit_gauss.py`: fit workflow and fit report panel.

## Data Flow

### CSV path

1. User opens `.csv` in `MainWindow`.
2. `DataManager.load_file` calls `data_parser.load_file`.
3. `load_csv_file` parses rows and metadata, builds channels.
4. `MeasurementData` is returned to GUI.
5. Viewer opens and operations run on in-memory arrays.

### SM4 path

1. User opens `.sm4` in `MainWindow`.
2. `load_file` dispatches to `load_sm4_file`.
3. `load_sm4` seam calls `spym.load`.
4. Channels are normalized via `build_channels_from_sm4`.
5. Viewer opens and processing uses the same downstream flow as CSV.

## Known Constraints

- UI and parser are in one process; malformed large files can impact responsiveness.
- `.sm4` coverage in tests is mocked until sample files can be added.
- No backend/service boundary; reliability depends on parser and local environment.
