# Testing Strategy

## Scope

Tests are focused on pure parsing/data logic and run without starting Qt (`QApplication`).

## Parsing map (.sm4 path)

- `gui/data_parser.py::load_file`  
  Routes by extension (`.csv` / `.sm4`)
- `gui/data_parser.py::load_sm4_file`  
  Main `.sm4` parsing entry point
- `gui/data_parser.py::load_sm4`  
  Default reader abstraction (uses `spym.load`)
- `gui/data_parser.py::build_channels_from_sm4`  
  Converts SM4 channels to normalized internal channel dict

## Mocked SM4 strategy (no real files)

- Tests monkeypatch `gui.data_parser.load_sm4` with a deterministic loader stub.
- No binary `.sm4` fixtures are stored in the repository.
- Mocked structures emulate minimal `spym` shape (`data_vars`, `data`, `attrs`).
- Invalid structure tests assert `ParseError` with clear messages.

## What is currently covered

- CSV fixtures:
  - happy path
  - missing columns
  - non-numeric values
  - empty file
- SM4 mocked cases:
  - happy path
  - invalid structure
  - large-input guard

## Planned

Add real `.sm4` integration tests once permission to include sample files is granted.
