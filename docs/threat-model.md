# Threat Model

## Scope

Desktop-only app with local file ingestion. Focus is on:

- untrusted input files (`.csv`, `.sm4`)
- availability risk (large files / expensive operations)
- dependency and repo hygiene risk
- export safety on local filesystem

## Assets

- Integrity of parsed measurement data and derived curves.
- Availability of the desktop app during analysis.
- Local files produced by export (CSV/PNG).
- Repository integrity (dependencies, secrets).

## Trust Boundaries and Entry Points

- File boundary: user-selected file -> `gui/data_parser.py::load_file`.
- Parser boundary:
  - CSV path: `load_csv_file`
  - SM4 path: `load_sm4_file` -> `load_sm4` (`spym.load`)
- Export boundary:
  - STS export in `sts_viewer.py`
  - TOPO export in `topo_viewer.py`

## Top Risks and Controls

1. Malformed input causes parser failures.
- Impact: run interruption, potential loss of in-session work.
- Current controls: typed parser errors (`ParseError` for SM4 path), extension routing, defensive conversions.

2. Very large files cause memory/CPU pressure (DoS-like local freeze).
- Impact: unresponsive GUI or process termination.
- Current controls: SM4 point guard (`MAX_SM4_CHANNEL_POINTS`).

3. File overwrite during export.
- Impact: accidental local data loss.
- Current controls: explicit overwrite path handling and error dialogs.

4. Dependency vulnerabilities.
- Impact: inherited supply-chain risk.
- Current controls: `pip-audit` local and CI workflow.

5. Secret leakage in repository.
- Impact: credential exposure.
- Current controls: `gitleaks` local/CI scan + SARIF upload.

## Mitigation Checklist

- [ ] Add CSV size/row limits before full in-memory read.
- [ ] Add consistent user-facing parse messages for all parser exceptions.
- [ ] Consider safer export pattern (write temp file then atomic replace).
- [ ] Keep Dependabot/CodeQL/security workflows enabled and green.
- [ ] Add real `.sm4` integration tests once sample-data policy allows.

## Residual Risk

Highest remaining risk is local availability degradation from oversized or adversarial input files. This is acceptable for desktop scientific tooling, but should be continuously reduced via parser limits and tests.
