from PySide6.QtWidgets import QGridLayout,QLabel,QFrame,QVBoxLayout
from gui.widgets import Page
class Dashboard(Page):
    def __init__(self):
        super().__init__('Your network, understood.','Discover groups, find bridge users, and explain how people connect.')
        self.grid=QGridLayout();self.layout.addLayout(self.grid);self.cards={}
        for i,key in enumerate(['Users','Connections','Communities','Density','Average clustering','Modularity','Connected components']):
            card=QFrame();card.setObjectName('card');box=QVBoxLayout(card);box.addWidget(QLabel(key));value=QLabel('—');value.setObjectName('metric');box.addWidget(value)
            self.grid.addWidget(card,i//3,i%3);self.cards[key]=value
        self.info=QLabel('Start with the 120-user synthetic college network, or import a CSV in Datasets.');self.info.setWordWrap(True);self.info.setMinimumHeight(70)
        self.layout.addWidget(self.info);self.layout.addStretch()
    def update_data(self,stats,result):
        for k,v in self.cards.items(): v.setText(f'{stats[k]:.4f}' if isinstance(stats[k],float) else str(stats[k]))
        self.info.setText(f"{result['algorithm']} • {result['seconds']:.3f} s • Communities describe connectivity, not personal traits.\nDirected data uses an undirected projection for communities; analytics retain direction.")
