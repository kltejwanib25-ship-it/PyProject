from gui.widgets import Page,Table
class Analytics(Page):
    def __init__(self):
        super().__init__('Influential users','Click a column heading to rank users. Degree: direct connections. Betweenness: bridges. Closeness: reachability (incoming for directed graphs). PageRank: importance passed through connections. Clustering: connected neighbors. Weights are strength; distances are inverse strength. Betweenness samples 150 sources above 300 users.')
        self.table=Table();self.layout.addWidget(self.table)
