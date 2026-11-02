# What you do now — Karan

## 1. Run and understand
Run setup_windows.bat, then run_demo.bat. Check each of the seven screens. You can work immediately even before your friends deliver core/.

## 2. Put your part on your branch
If the team repository already exists, clone it, create your branch, and copy this package's main.py, gui/, visualization/, assets/, tests/test_gui.py and scripts into that checkout. Do not replace friends' core/ folder or overwrite their requirements/docs without reviewing differences. Put the separately labelled reference_backend/ in the repository too if the team wants independent UI development.

From the team checkout:
```powershell
git switch main
git pull origin main
git switch -c feature/ui
```
After copying and reviewing:
```powershell
git status
git add main.py gui visualization assets tests/test_gui.py
git add reference_backend requirements.txt pytest.ini .gitignore
git add setup_windows.bat run_demo.bat run_team.bat build_windows.bat build_windows.py docs README.md
git commit -m "Add AI-assisted desktop UI baseline and backend integration contract"
git push -u origin feature/ui
```
Stage only files that you intend to change; review README/requirements differences before replacing shared files. Create a pull request and ask a friend to review. If there is no shared repository yet, initialize an empty scaffold on main first, push it to your own GitHub repository, invite friends, then create feature/ui and add this part. Do not embed passwords or tokens in commands.

## 3. Send each friend their contract
Share docs/FRIEND_HANDOFF.md. Friend 1 implements data/graph functions; Friend 2 detection; Friend 3 analytics/comparison/reports. You own the screens and gui/backend.py. This contract includes helper functions as well as primary APIs, so there are no hidden imports to discover later.

## 4. Explain the files in this order
1. main.py: creates QApplication and MainWindow.
2. gui/backend.py: selects reference or team function providers.
3. gui/main_window.py: coordinates current graph/result/data and background tasks.
4. gui/dataset_page.py: controls, not CSV algorithms.
5. visualization/graph_canvas.py: draws and selects nodes.
6. Remaining page files: display metrics and results without calculating them.
7. tests/test_gui.py: confirms UI flows with temporary test data.

## 5. Integrate one working team snapshot
After friends' reviewed branches merge:
```powershell
git fetch origin
git merge origin/main
.venv\Scripts\python.exe main.py --team
```
If the backend interface is incomplete, fix the contract with the owning friend. Do not copy their algorithms into GUI files to bypass an integration error. Once all functions exist, exercise import → detect → select → compare → export. Reference-mode tests do not substitute for this team-mode run.

## 6. Your presentation
Explain: "My responsibility is the native desktop interface and integration. I connected the data and algorithm modules through a defined backend interface, built the graph explorer and tables, and used workers so calculations do not run directly on the UI event loop. The reference backend allowed independent UI testing before team integration."
Describe only work and tests you actually performed. Your next individual change could be better keyboard navigation or user help text; submit it as a separate, tested PR.
