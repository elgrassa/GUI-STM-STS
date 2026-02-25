# Design and Implementation of a Graphical User Interface in Python for the Analysis and Visualization of STM/STS Spectroscopic Data

A Python-based GUI tool for the analysis, processing, and visualization of scanning tunneling spectroscopy (STS) data, with a particular focus on high-bias spectroscopy.


## Background

This project focuses on the analysis of data obtained from scanning tunneling microscopy (STM) and scanning tunneling spectroscopy (STS), with particular emphasis on high-bias spectroscopy. The main objective was to design and implement a Python-based graphical user interface that supports efficient and interactive analysis of spectroscopic data.


## Features

The developed GUI tool provides a comprehensive set of tools for the analysis of STM/STS spectroscopic data, including:

- Loading and parsing measurement files in `.sm4` and `.csv` formats using a modular data parser.
- Interactive visualization of spectroscopic curves and topographic channels.
- A collection of signal processing tools, including:
  - normalization,
  - filtering,
  - subtraction,
  - division,
  - averaging,
  - numerical differentiation.
- Automatic detection of local maxima in spectroscopic curves.
- Gaussian curve fitting for each detected peak, enabling the extraction of characteristic parameters such as peak position, amplitude, and standard deviation.
- Automatic estimation of the work function of the investigated material based on fitted peak parameters.
- Display and searchable view of metadata associated with each measurement channel.
- Basic data validation and safety mechanisms to prevent invalid operations (e.g. division by zero).

The software was tested and validated using real experimental data, confirming its correctness and practical usefulness in quantitative STM/STS data analysis.


## Requirements

- Python 3.11 or newer
- Required Python packages are listed in `requirements.txt`


## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/SofiaDmytrenko/GUI-STM-STS.git
```
``` bash
cd GUI-STM-STS
```

Create a virtual environment:
``` bash
python -m venv .venv
```
Activate the virtual environment:

On Linux / macOS:
``` bash
source .venv/bin/activate
```

On Windows:
``` bash
.venv\Scripts\activate
```


Install the required dependencies:
``` bash
pip install -r requirements.txt
```

Install developer tooling (lint, formatting, tests, coverage):
``` bash
pip install ruff pytest pytest-cov pip-audit
```

Install `gitleaks` from the official project releases:
[gitleaks installation guide](https://github.com/gitleaks/gitleaks#installation)

Install packaging tooling:
```bash
pip install pyinstaller
```


## Usage

After installing the requirements and activating the virtual environment, run the GUI tool using:
```bash
python main.py
```

> [!NOTE]
> The program is intended to be run from a Python IDE (e.g., PyCharm, VS Code) or from the terminal. Make sure the virtual environment is active before running the script.

## Development

Setup:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install ruff pytest pytest-cov
```

Dependency lock (preferred for reproducible installs):
```bash
pip install pip-tools
pip-compile --output-file requirements.lock requirements.txt
pip install -r requirements.lock
```

`requirements.txt` remains the editable input list. CI installs from `requirements.lock`.

Quality commands:
```bash
make fmt
make lint
make test
```

### Documentation

Quick technical overview and operations guide:
- [Architecture (C4-lite)](docs/architecture.md)
- [Threat model](docs/threat-model.md)
- [Runbook](docs/runbook.md)
- [Testing strategy](docs/testing.md)

### Packaging (PyInstaller)

Build command (all platforms):
```bash
python packaging/build.py
```

Artifacts are generated under `dist/GUI-STM-STS/`.

- Windows (`windows-latest`): executable bundle with `GUI-STM-STS.exe`
- macOS (`macos-latest`): app bundle folder with executable in `dist/GUI-STM-STS/`
- Linux (`ubuntu-latest`): executable folder in `dist/GUI-STM-STS/`

Automated build artifacts are produced by:
- [CI workflow](.github/workflows/ci.yml)
- [Release build workflow](.github/workflows/release-build.yml)

### Loading and Visualizing Data

Click the "Open File" button and select a measurement file in .sm4 or .csv format.
Available measurement channels will be displayed.
<p align="center">
  <img src="images/main_window.png" width="60%"/>
</p>

Select a channel to view its topography or spectroscopic curves.
<table>
  <tr>
    <td align="center">
      <img src="images/topo_viewer.png"/>
      <p>Topo Viewer</p>
    </td>
    <td align="center">
      <img src="images/sts_viewer.png"/>
      <p>STS Viewer</p>
    </td>
  </tr>
</table>

Apply the built-in signal processing tools to the curves:
- normalization
- filtering
- subtracting
- dividing
- averaging
- differentiating

<table>
  <tr>
    <td align="center">
      <img src="images/fit_gauss.png"/>
      <p>FitGauss</p>
    </td>
    <td align="center">
      <img src="images/fer_peaks.png"/>
      <p>FER peak positions</p>
    </td>
  </tr>
</table>

Use the automatic peak detection and Gaussian fitting module to extract parameters such as:
- peak position
- amplitude
- standard deviation (σ)
- work function of the material

### Viewing Metadata
Metadata for each measurement channel is available within the GUI and can be searched or filtered as needed.
<p align="center">
  <img src="images/metadata_tab.png" width="60%"/>
</p>


## Project structure
<pre>
GUI-STS/
├── gui/                                  # Main GUI folder containing modules that define windows, toolbars, viewers, and layouts.
|    ├── channel_viewers/
|    |   ├── topo_viewer.py               # Module responsible for displaying STM topography images.
|    |   └── sts_viewer_folder/ 
|    |         ├── sts_viewer.py          # Main module for analyzing STS curves.
|    |         ├── sts_toolbar.py         # Provides buttons for STS signal processing functions.
|    |         ├── sts_processing.py      # Signal processing functions.
|    |         └── fit_gauss.py           # Peak detection and Gaussian fitting.
|    ├── helpers/
|    |   ├── metadata_tab.py              # Module for displaying and searching metadata associated with measurement channels.
|    |   └── styles.py                    # Defines visual styles, themes, and GUI element appearance for consistency.
|    ├── data_parser.py                   # Module for reading `.sm4` and `.csv` files
|    └── main_window.py                   # First window displayed; allows to open files, select channels and view file metadata.
├── main.py                               # Entry point to launch the GUI.
├── pyproject.toml                        # Ruff, pytest and coverage configuration.
├── Makefile                              # Helper targets: fmt, lint, test.
├── .gitleaks.toml                        # Secret-scanning configuration (extends gitleaks defaults).
├── SECURITY.md                           # Security policy and vulnerability reporting process.
├── docs/
|    ├── architecture.md                  # C4-lite architecture and CSV/SM4 data flow.
|    ├── threat-model.md                  # Threat model focused on file ingestion risks.
|    ├── runbook.md                       # Local operation and troubleshooting guide.
|    └── testing.md                       # Test scope, mocked SM4 strategy, and plan.
├── packaging/
|    ├── stm_sts.spec                     # PyInstaller spec used for standalone builds.
|    └── build.py                         # Cross-platform helper script for PyInstaller builds.
├── requirements.txt                      # Python dependencies.
├── .github                               # GitHub-specific configuration, workflows or actions.
├── .gitignore                            # Files and folders to ignore in version control
├── README.md                             # Project documentation
└── images/                               # Folder for screenshots used in the README.
    ├── main_window.png
    ├── sts_viewer.png
    ├── topo_viewer.png
    ├── fit_gauss.png
    ├── fer_peaks.png
    └── metadata_tab.png
</pre>

## Testing

The repository is configured for `pytest` + `pytest-cov` and includes Makefile commands:

```bash
make test
```

Current automated tests focus on pure logic and file parsing (no Qt event loop startup),
including synthetic CSV fixtures under `tests/fixtures/`.

SM4 parsing tests are currently mocked (injectable loader strategy) until real `.sm4`
sample files can be included by policy.
The mocked path monkeypatches `gui.data_parser.load_sm4` to keep CI deterministic and Qt-free.

At the moment, functionality is still primarily validated manually using experimental STM/STS data.

## Troubleshooting

- If Gaussian fitting cannot continue (for example, no peaks detected), STS viewer errors are shown in a message box instead of failing silently.
- Matplotlib Qt canvas imports are unified to `backend_qtagg` for PyQt6 viewers (`STSViewer`, `TopoViewer`, and fit dialogs).

## Security

This repository includes free GitHub-native security checks for a public repository.

GitHub security automation:
- Dependabot updates Python dependencies from `requirements.txt` weekly (grouped updates): [`.github/dependabot.yml`](.github/dependabot.yml)
- CodeQL static analysis for Python on `push`, `pull_request`, and weekly schedule: [`.github/workflows/codeql.yml`](.github/workflows/codeql.yml)
- Security workflow with dependency audit + secret scan: [`.github/workflows/security-scheduled.yml`](.github/workflows/security-scheduled.yml)

Notes:
- `gitleaks` results are uploaded as SARIF to GitHub Code Scanning.
- `pip-audit` currently runs as fail-on-findings (no native SARIF output in this setup).

Run dependency vulnerability scanning:
```bash
make audit-deps
```

Run secret scanning:
```bash
make scan-secrets
```

Run both checks:
```bash
make security
```

Equivalent direct commands:
```bash
pip-audit -r requirements.txt
gitleaks detect --source . --config .gitleaks.toml --redact --no-banner
```

See [SECURITY.md](SECURITY.md) for reporting guidance.


## Limitations

- Supported file formats: `.sm4` and `.csv`
- Currently, only **Gaussian fitting** is implemented; other theoretical functions (Lorentzian, exponential, etc.) are not supported. 
- When saving data in `.csv` format, **only one measurement channel can be saved at a time**.  
- **Normalization cannot be performed correctly** on `.csv` data if the corresponding I–V curve ("Current" channel) is missing, since normalization requires the current measurements for accurate processing.
