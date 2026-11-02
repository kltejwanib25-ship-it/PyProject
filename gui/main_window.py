"""UI coordinator; all loading, analysis, comparison, and exports run off-thread."""
import traceback
from pathlib import Path
import pandas as pd
import networkx as nx
from PySide6.QtCore import QThread,Signal,QTimer
from PySide6.QtWidgets import QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,QListWidget,QStackedWidget,QPushButton,QLabel,QProgressBar,QFileDialog,QMessageBox
from gui.backend import load_csv,clean_data,sample_data,build_graph,detect,analyze,compare,export_reports,safe_csv,MODE_LABEL
from gui.dashboard import Dashboard
from gui.network_explorer import Explorer
from gui.community_page import Communities
from gui.analytics_page import Analytics
from gui.comparison_page import Comparison
from gui.dataset_page import Datasets
from gui.widgets import Page
class Worker(QThread):
    done=Signal(object);failed=Signal(str)
    def __init__(self,fn):super().__init__();self.fn=fn
    def run(self):
        try:self.done.emit(self.fn())
        except Exception:self.failed.emit(traceback.format_exc())
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__();self.setWindowTitle('CommunityScope • Social Network Intelligence');self.resize(1280,850);self.setMinimumSize(950,650)
        self.worker=None;self.graph=None;self.dataset_name='No dataset';self.dark=True;self.comparison=pd.DataFrame(columns=['algorithm','communities','modularity','seconds','sizes','status'])
        root=QWidget();self.setCentralWidget(root);layout=QHBoxLayout(root);side=QVBoxLayout()
        brand=QLabel('◉ CommunityScope');brand.setObjectName('brand');side.addWidget(brand)
        mode_label=QLabel(MODE_LABEL);mode_label.setWordWrap(True);side.addWidget(mode_label)
        self.dataset_label=QLabel('Loading dataset…');self.dataset_label.setWordWrap(True);self.dataset_label.setMaximumWidth(200);side.addWidget(self.dataset_label)
        self.nav=QListWidget();self.nav.addItems(['Overview','Network explorer','Communities','Influential users','Comparison','Datasets','Reports']);self.nav.setFixedWidth(200);side.addWidget(self.nav)
        theme=QPushButton('Switch light / dark');theme.clicked.connect(self.toggle_theme);side.addWidget(theme);layout.addLayout(side)
        self.stack=QStackedWidget();layout.addWidget(self.stack,1)
        self.dashboard=Dashboard();self.explorer=Explorer();self.communities=Communities(self.run_detection);self.analytics=Analytics();self.compare_page=Comparison(self.run_comparison)
        self.datasets=Datasets(self.import_csv,self.generate,self.export_clean)
        self.reports=Page('Export your findings','Save membership, centrality, statistics, comparison CSVs and a PDF with charts into a chosen folder. Existing report filenames in that folder will be replaced after confirmation.')
        button=QPushButton('Export analysis report bundle');button.clicked.connect(self.export);self.reports.layout.addWidget(button);self.reports.layout.addStretch()
        for p in [self.dashboard,self.explorer,self.communities,self.analytics,self.compare_page,self.datasets,self.reports]:self.stack.addWidget(p)
        self.nav.currentRowChanged.connect(self.stack.setCurrentIndex);self.nav.setCurrentRow(0)
        self.progress=QProgressBar();self.progress.setMaximumWidth(180);self.progress.hide();self.statusBar().addPermanentWidget(self.progress)
        self.toggle_theme(initial=True);QTimer.singleShot(0,self.generate)
    def toggle_theme(self,initial=False):
        if not initial:self.dark=not self.dark
        bg,card,fg,border=('#111827','#1e293b','#e5edf9','#334155') if self.dark else ('#f1f5fa','#ffffff','#172033','#d6deeb')
        self.setStyleSheet(f"QWidget {{background:{bg};color:{fg};font-family:'Segoe UI';font-size:13px;}} QFrame#card,QTableWidget,QLineEdit,QComboBox {{background:{card};border:1px solid {border};border-radius:8px;padding:8px;}} QLabel {{background:transparent;}} QToolBar {{background:#e2e8f0;}} QLabel#heading {{font-size:28px;font-weight:700;}} QLabel#metric {{font-size:32px;font-weight:700;color:#9182ff;}} QLabel#brand {{font-size:18px;font-weight:700;padding:12px;}} QPushButton {{background:#6957d9;color:white;border:0;border-radius:7px;padding:11px;}} QPushButton:disabled {{background:#64748b;}} QListWidget {{border:0;}} QListWidget::item {{padding:14px;border-radius:6px;}} QListWidget::item:selected {{background:#6957d9;color:white;}} QHeaderView::section {{background:{card};padding:8px;border:0;}} QTableWidget {{alternate-background-color:{bg};}}")
    def task(self,label,fn,callback):
        if self.worker and self.worker.isRunning():return
        self.stack.setEnabled(False);self.progress.setRange(0,0);self.progress.show();self.statusBar().showMessage(label)
        self.worker=Worker(fn);self.worker.done.connect(callback);self.worker.failed.connect(self.error);self.worker.finished.connect(self.finished);self.worker.start()
    def finished(self):self.stack.setEnabled(True);self.progress.hide()
    def error(self,message):
        self.statusBar().showMessage('Operation failed; previous dataset retained.');box=QMessageBox(self);box.setWindowTitle('CommunityScope error');box.setText(message.strip().splitlines()[-1]);box.setDetailedText(message);box.exec()
    def prepare(self,df,note,directed):
        g=build_graph(df,directed);r=detect(g);stats,metrics=analyze(g,r)
        positions=nx.spring_layout(g,seed=42,iterations=35,weight='weight') if len(g)<=500 else nx.circular_layout(g)
        return df,note,g,r,stats,metrics,positions
    def generate(self):
        directed=self.datasets.directed.isChecked();weighted=self.datasets.weighted.isChecked()
        self.task('Generating and analyzing sample…',lambda:self.prepare(*clean_data(sample_data(),directed,weighted),directed),lambda payload:self.loaded(payload,'Synthetic college • 120 users'))
    def import_csv(self):
        path,_=QFileDialog.getOpenFileName(self,'Import edge list','','CSV files (*.csv)')
        if path:
            d=self.datasets.directed.isChecked();w=self.datasets.weighted.isChecked()
            self.task('Validating and analyzing CSV…',lambda:self.prepare(*load_csv(path,d,w),d),lambda payload:self.loaded(payload,Path(path).name))
    def loaded(self,payload,name='Dataset'):
        self.dataset_name=name;self.dataset_label.setText(name)
        self.df,note,self.graph,self.result,self.stats,self.metrics,self.positions=payload
        self.comparison=pd.DataFrame(columns=['algorithm','communities','modularity','seconds','sizes','status'])
        self.compare_page.table.load(self.comparison);self.compare_page.chart.figure.clear();self.compare_page.chart.draw_idle()
        self.datasets.table.load(self.df.head(200));self.datasets.note.setText(note+' Preview: first 200 rows. Options apply to next import.')
        self.refresh();self.statusBar().showMessage(f'Ready • {len(self.graph)} users • {self.dataset_name}')
    def refresh(self):
        self.dashboard.update_data(self.stats,self.result);self.communities.update_data(self.result);self.analytics.table.load(self.metrics)
        self.explorer.update_data(self.graph,self.result,self.metrics,self.positions)
    def run_detection(self,name):
        if self.graph is None:return
        def run():
            r=detect(self.graph,name);return r,*analyze(self.graph,r)
        def done(payload):self.result,self.stats,self.metrics=payload;self.refresh();self.statusBar().showMessage('Community analysis complete')
        self.task('Detecting communities…',run,done)
    def run_comparison(self):
        if self.graph is None:return
        def done(payload):self.comparison,results=payload;self.compare_page.update_data(self.comparison,results);self.statusBar().showMessage('Comparison complete; skipped algorithms show a reason')
        self.task('Comparing algorithms…',lambda:compare(self.graph),done)
    def export_clean(self):
        if self.graph is None:return
        path,_=QFileDialog.getSaveFileName(self,'Save cleaned CSV','cleaned_network.csv','CSV (*.csv)')
        if path:self.task('Saving CSV…',lambda:safe_csv(self.df,path),lambda _:self.statusBar().showMessage('Cleaned CSV saved; spreadsheet formula prefixes escaped'))
    def export(self):
        if self.graph is None:return
        folder=QFileDialog.getExistingDirectory(self,'Choose report folder')
        if not folder:return
        names=['summary.pdf','community_membership.csv','user_centrality.csv','network_statistics.csv','algorithm_comparison.csv']
        if any((Path(folder)/n).exists() for n in names):
            if QMessageBox.question(self,'Replace reports?','Replace existing report files in this folder?')!=QMessageBox.Yes:return
        self.task('Exporting report bundle…',lambda:export_reports(folder,self.graph,self.result,self.stats,self.metrics,self.comparison),lambda p:self.statusBar().showMessage(f'Reports saved: {p}'))
    def closeEvent(self,event):
        if self.worker and self.worker.isRunning():
            QMessageBox.information(self,'Work in progress','Please wait for the current operation to finish before closing.');event.ignore()
        else:event.accept()
