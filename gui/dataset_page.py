from PySide6.QtWidgets import QPushButton,QHBoxLayout,QCheckBox,QLabel
from gui.widgets import Page,Table
class Datasets(Page):
    def __init__(self,importer,generator,exporter):
        super().__init__('Dataset studio','CSV columns: source, target, optional weight. Positive finite strengths only. Duplicate strengths are summed. A self-row declares a user without adding a self-loop. Limits: 10 MB, 2,000 users, 20,000 edges.')
        row=QHBoxLayout();self.directed=QCheckBox('Directed connections');self.weighted=QCheckBox('Use weights');self.weighted.setChecked(True)
        row.addWidget(self.directed);row.addWidget(self.weighted);self.layout.addLayout(row)
        row=QHBoxLayout()
        for title,fn in [('Import CSV',importer),('Generate sample',generator),('Export cleaned CSV',exporter)]:
            button=QPushButton(title);button.clicked.connect(fn);row.addWidget(button)
        self.layout.addLayout(row);self.note=QLabel('Options apply on next import or generation. Preview shows the first 200 rows.');self.note.setWordWrap(True);self.layout.addWidget(self.note)
        self.table=Table();self.layout.addWidget(self.table)
