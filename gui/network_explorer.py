from PySide6.QtWidgets import QHBoxLayout,QLineEdit,QComboBox,QLabel
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from visualization.graph_canvas import GraphCanvas
from gui.widgets import Page
class Explorer(Page):
    def __init__(self):
        super().__init__('Network explorer','Click a node to inspect it. Use the toolbar to zoom, pan, reset, or save an image. Maximum 4,000 drawn edges.')
        row=QHBoxLayout();self.search=QLineEdit();self.search.setPlaceholderText('Exact user name, then Enter');self.filter=QComboBox()
        self.size=QComboBox();self.size.addItems(['degree','pagerank','betweenness','closeness'])
        row.addWidget(self.search);row.addWidget(self.filter);row.addWidget(self.size);self.layout.addLayout(row)
        self.canvas=GraphCanvas();self.layout.addWidget(NavigationToolbar2QT(self.canvas,self));self.layout.addWidget(self.canvas)
        self.details=QLabel('Select a user to see their community and connections.');self.details.setWordWrap(True);self.layout.addWidget(self.details)
        self.data=None;self.selected=None
        self.canvas.selected.connect(self.select);self.search.returnPressed.connect(lambda:self.select(self.search.text().strip()))
        self.filter.currentIndexChanged.connect(self.redraw);self.size.currentIndexChanged.connect(self.redraw)
    def update_data(self,g,result,metrics,positions):
        self.data=(g,result,metrics,positions);self.selected=None;self.filter.blockSignals(True);self.filter.clear();self.filter.addItem('All communities',None)
        for i,p in enumerate(result['communities'],1):self.filter.addItem(f'Community {i} ({len(p)})',i)
        self.filter.blockSignals(False);self.redraw()
    def redraw(self):
        if self.data:
            g,r,m,pos=self.data;scores=dict(zip(m.user,m[self.size.currentText()]))
            self.canvas.render(g,pos,r['mapping'],scores,self.filter.currentData(),self.selected)
    def select(self,name):
        if not self.data:return
        g,r,m,pos=self.data
        if name not in g:self.details.setText('No user with that exact name.');return
        self.selected=name;row=m[m.user==name].iloc[0]
        self.details.setText(f"{name} | Community {r['mapping'][name]} | Connections: {g.degree(name)} | PageRank: {row.pagerank:.5f} | Betweenness: {row.betweenness:.5f}")
        self.redraw()
