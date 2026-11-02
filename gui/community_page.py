import pandas as pd
from PySide6.QtWidgets import QComboBox,QPushButton,QHBoxLayout,QLabel
from gui.backend import ALGORITHMS
from gui.widgets import Page,Table
class Communities(Page):
    def __init__(self,run):
        super().__init__('Find your communities','Choose a partition algorithm. Girvan–Newman explores up to four hierarchy splits and is limited to 150 users / 600 edges.')
        row=QHBoxLayout();self.algorithm=QComboBox();self.algorithm.addItems(ALGORITHMS);self.run=QPushButton('Detect communities');self.run.clicked.connect(lambda:run(self.algorithm.currentText()))
        row.addWidget(self.algorithm);row.addWidget(self.run);self.layout.addLayout(row);self.summary=QLabel();self.layout.addWidget(self.summary)
        self.table=Table();self.layout.addWidget(self.table)
    def update_data(self,result):
        self.summary.setText(f"{result['algorithm']} | Modularity {result['modularity']:.4f} | {result['seconds']:.3f} seconds")
        self.table.load(pd.DataFrame([{'community':i,'size':len(p),'members':', '.join(p)} for i,p in enumerate(result['communities'],1)],columns=['community','size','members']))
