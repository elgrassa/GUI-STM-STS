# Runbook

## 1) Local Startup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Developer tools (optional but recommended):

```bash
pip install ruff pytest pytest-cov pip-audit
```

## 2) Quality and Security Checks

```bash
make fmt
make lint
make test
make security
```

## 3) Common Failures

### Missing dependency

- Symptom: `ModuleNotFoundError` (for example `PyQt6`, `spym`, `lmfit`).
- Action: activate `.venv`, reinstall `requirements.txt`.

### Tests fail with unknown `--cov`

- Symptom: pytest rejects `--cov=...` args.
- Action: install plugin: `pip install pytest-cov`.

### File load fails

- Symptom: GUI shows file load/parsing error.
- Typical causes:
  - unsupported extension (only `.csv`, `.sm4`)
  - malformed CSV structure
  - invalid SM4 structure/dependency incompatibility
- Action: validate with `tests/fixtures/` patterns and retry.

### No Gaussian fit output

- Symptom: fit panel does not proceed.
- Typical cause: no peaks detected or invalid selected curve.
- Action: verify curve selection and data quality; inspect peak detection step first.

## 4) Diagnostics

- Capture environment details:

```bash
python --version
pip freeze
```

- Run focused tests:

```bash
python -m pytest -q -o addopts=''
```

- For parser issues, isolate input path with parser tests in `tests/unit/test_data_parser_csv.py`.

## 5) Logging Guidance

Current modules use `logging.getLogger(__name__)` but global config is not centralized.

Recommended minimal setup in `main.py` for debugging sessions:

- configure `logging.basicConfig(level=logging.INFO)` once
- switch to `DEBUG` temporarily during parser or fit investigations
- keep GUI error dialogs concise and rely on logs for stack traces
