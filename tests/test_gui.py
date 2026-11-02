import os,time
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

def pump(app,window):
    deadline=time.monotonic()+60
    while time.monotonic()<deadline:
        app.processEvents();time.sleep(.02)
        if window.worker and window.worker.isFinished():app.processEvents();return
    raise AssertionError('Worker timeout')
def test_desktop(tmp_path):
    app=QApplication.instance() or QApplication([]);window=MainWindow();errors=[];window.error=lambda message:errors.append(message)
    window.show();app.processEvents();pump(app,window)
    assert not errors;assert len(window.graph)==120
    window.explorer.select('Student_001');assert 'Student_001' in window.explorer.details.text()
    window.explorer.filter.setCurrentIndex(1);window.explorer.size.setCurrentIndex(1)
    window.run_detection('Label Propagation');pump(app,window);assert window.result['algorithm']=='Label Propagation'
    window.run_comparison();pump(app,window);assert len(window.comparison)==4;assert not errors
    window.toggle_theme();app.processEvents();window.grab().save(str(tmp_path/'gui.png'));window.close()

def test_import_error_and_export(tmp_path,monkeypatch):
    from PySide6.QtWidgets import QFileDialog
    app=QApplication.instance() or QApplication([]);window=MainWindow();errors=[];window.error=lambda message:errors.append(message)
    window.show();app.processEvents();pump(app,window)
    sample=tmp_path/'six_users.csv'
    sample.write_text('source,target,weight\nA,B,3\nB,C,3\nC,A,3\nD,E,3\nE,F,3\nF,D,3\nC,D,1\n')
    monkeypatch.setattr(QFileDialog,'getOpenFileName',lambda *a,**k:(str(sample),'CSV'))
    window.import_csv();pump(app,window)
    assert len(window.graph)==6 and window.graph.number_of_edges()==7
    assert window.dataset_name=='six_users.csv'
    original=window.graph
    sample.write_text('source,target,weight\nA,B,wrong\n')
    window.import_csv();pump(app,window)
    assert errors and 'ValueError' in errors[-1];assert window.graph is original
    assert window.stack.isEnabled()
    folder=tmp_path/'reports';folder.mkdir()
    monkeypatch.setattr(QFileDialog,'getExistingDirectory',lambda *a,**k:str(folder))
    window.export();pump(app,window)
    assert (folder/'summary.pdf').read_bytes().startswith(b'%PDF')
    assert (folder/'user_centrality.csv').exists()
    window.close()

def test_empty_import(tmp_path,monkeypatch):
    from PySide6.QtWidgets import QFileDialog
    app=QApplication.instance() or QApplication([]);window=MainWindow();errors=[];window.error=lambda message:errors.append(message)
    window.show();app.processEvents();pump(app,window)
    sample=tmp_path/'empty.csv';sample.write_text('source,target,weight\n')
    monkeypatch.setattr(QFileDialog,'getOpenFileName',lambda *a,**k:(str(sample),'CSV'))
    window.import_csv();pump(app,window)
    assert not errors;assert len(window.graph)==0;assert window.dashboard.cards['Users'].text()=='0'
    window.close()

def test_missing_team_backend_fails():
    import subprocess,sys
    env=dict(os.environ,COMMUNITYSCOPE_BACKEND='team')
    result=subprocess.run([sys.executable,'-c','import gui.backend'],env=env,capture_output=True,text=True)
    assert result.returncode!=0;assert 'Missing integration function' in result.stderr

def test_team_backend_switch(tmp_path):
    import subprocess,sys,shutil
    from pathlib import Path
    # Isolated compatible team fixture; does not modify the delivered project.
    root=Path(__file__).resolve().parents[1]
    shutil.copytree(root/'reference_backend',tmp_path/'core',ignore=shutil.ignore_patterns('__pycache__'))
    for p in (tmp_path/'core').glob('*.py'):p.write_text(p.read_text().replace('reference_backend.','core.'))
    env=dict(os.environ,COMMUNITYSCOPE_BACKEND='team',PYTHONPATH=str(tmp_path)+os.pathsep+str(root))
    result=subprocess.run([sys.executable,'-c',
        'from gui.backend import *; assert TEAM_MODE; d,n=clean_data(sample_data()); g=build_graph(d); r=detect(g); s,m=analyze(g,r); assert len(m)==120; print(MODE_LABEL)'],
        cwd=tmp_path,env=env,capture_output=True,text=True)
    assert result.returncode==0,result.stderr;assert 'TEAM MODULES' in result.stdout
