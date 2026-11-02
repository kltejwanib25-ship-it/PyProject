# Karan's part — CommunityScope desktop UI and integration

This is the UI member's runnable contribution, derived from the AI-assisted CommunityScope reference project. It is not a claim that Karan has already written or independently tested this code. Read it, adapt it and record your actual work.

## Start on Windows
1. Extract this folder and install Python 3.11 (64-bit).
2. Double-click **setup_windows.bat** once; internet is needed to install packages.
3. Double-click **run_demo.bat**. The desktop opens with 120 fictional users.
4. Open this folder in VS Code and select `.venv/Scripts/python.exe` as interpreter.

Terminal equivalent:
```powershell
py -3.11 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py --demo
```

## What is YOUR part?
- `main.py`: desktop entry point and setup-error handling.
- `gui/`: all seven screens, navigation, themes, tables, file dialogs and threaded integration.
- `visualization/`: interactive Qt/Matplotlib network canvas and comparison charts.
- `tests/test_gui.py`: UI integration checks.
- Windows setup, run and build scripts, assets and integration documentation.

## What belongs to your friends?
Their final code lives in **core/**, which is intentionally absent from this package. `reference_backend/` is supplied reference support so you can run and test your UI today. Its algorithms compute real results; they are not fake UI values. It is not part of your individual algorithm contribution. The sidebar clearly labels reference mode.

Once friends deliver core/ (see docs/FRIEND_HANDOFF.md), run **run_team.bat**. Missing functions produce a setup error; team mode never silently switches to reference calculations. `main.py` without flags chooses core when available, otherwise reference. Use --demo or --team for an unambiguous run.

## Try your part
Overview → inspect counts. Network explorer → select Student_001, use filter and node sizing, zoom/pan. Communities → change algorithm. Influential users → sort columns. Comparison → run all. Datasets → import CSV (options apply to next import). Reports → select folder to export. Comparison must run first for comparison report content. Dark/light toggle is at the bottom of the sidebar.

CSV needs source,target and optional positive weight. Self-rows declare users without loops; duplicate strengths sum. Directed community detection uses a summed undirected projection. Limit 2,000 nodes/20,000 connections; Girvan–Newman 150 nodes/600 edges and four splits; betweenness sampled above 300 nodes. Plots draw at most 4,000 edges. No force cancellation; wait before closing a running task. See the reference backend for exact computation contracts.

## Tests
```powershell
.venv\Scripts\python.exe -m pytest -q
```
Tests are UI/integration tests using the reference backend, not proof that teammates' future modules work. See docs/VALIDATION.md.

## Build
Run `build_windows.bat` for a reference demo executable. Once core is delivered, run `build_windows.bat --team` for the team executable. Run builds on Windows. Distribute the whole dist output folder, not just the exe. No prebuilt exe is included.

Read **docs/KARAN_START_HERE.md** next for your exact Git and development workflow.
