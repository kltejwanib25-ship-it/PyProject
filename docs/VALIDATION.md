# Validation of Karan UI package

Executed on Linux with Python 3.12 and QT_QPA_PLATFORM=offscreen.
Result: **5 passed, 14 dependency deprecation warnings in 11.29 seconds**.
Pinned requirements installed successfully. compileall succeeded.

Tests cover startup with 120 synthetic users; user selection; community filtering and node sizing; algorithm change; comparison; theme toggle; CSV import and active filename; invalid CSV error while preserving the previous graph; worker UI re-enabling; report export; empty dataset import; explicit failure on missing team backend; and selection of a temporary compatible team fixture in a subprocess.

The team-mode fixture used reference implementations under the core namespace to check the integration route. This does not verify future teammates' code. The sidebar modes and actual current dataset were visually inspected on the dashboard and network explorer.

Not tested: Windows 10/11 native launch, Windows file dialogs and DPI scaling, PyInstaller Windows executables, or integration with friends' not-yet-delivered modules. No prebuilt executable included. Use run_team.bat and repeat the full workflow after integrating their modules.

Run from this package folder: python -m pytest -q. UI tests default to offscreen. Reference-mode tests use supplied reference_backend code, not teammates' future core implementations.
