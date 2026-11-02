from PySide6.QtWidgets import QPushButton
from gui.widgets import Page,Table
from visualization.charts import ComparisonChart
class Comparison(Page):
    def __init__(self,run):
        super().__init__('Compare approaches','Timing measures detection only. Modularity favors within-group links; the highest score does not prove a socially correct partition.')
        self.run=QPushButton('Compare all algorithms');self.run.clicked.connect(run);self.layout.addWidget(self.run)
        self.table=Table();self.layout.addWidget(self.table);self.chart=ComparisonChart();self.layout.addWidget(self.chart)
    def update_data(self,frame,results):self.table.load(frame);self.chart.update_data(frame,results)
