"""Shared native table and page components."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QTableWidget,QTableWidgetItem,QHeaderView
class NumberItem(QTableWidgetItem):
    def __lt__(self,other):
        try: return float(self.text())<float(other.text())
        except ValueError: return self.text()<other.text()
class Table(QTableWidget):
    def __init__(self):
        super().__init__();self.setAlternatingRowColors(True);self.setEditTriggers(QTableWidget.NoEditTriggers)
    def load(self,frame):
        self.setSortingEnabled(False);self.clear();self.setRowCount(len(frame));self.setColumnCount(len(frame.columns))
        self.setHorizontalHeaderLabels([str(c).replace('_',' ').title() for c in frame.columns])
        for r,row in enumerate(frame.itertuples(index=False,name=None)):
            for c,v in enumerate(row): self.setItem(r,c,NumberItem(f'{v:.6g}' if isinstance(v,float) else str(v)))
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontalHeader().setStretchLastSection(True);self.setSortingEnabled(True)
class Page(QWidget):
    def __init__(self,title,subtitle):
        super().__init__();self.layout=QVBoxLayout(self);self.layout.setContentsMargins(26,22,26,22);self.layout.setSpacing(14)
        h=QLabel(title);h.setObjectName('heading');self.layout.addWidget(h)
        label=QLabel(subtitle);label.setWordWrap(True);self.layout.addWidget(label)
