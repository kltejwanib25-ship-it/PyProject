"""Native Matplotlib Qt canvas with picking and navigation toolbar support."""
from PySide6.QtCore import Signal
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import networkx as nx
class GraphCanvas(FigureCanvasQTAgg):
    selected=Signal(str)
    def __init__(self):
        super().__init__(Figure(figsize=(8,6),facecolor='#f4f6fb'));self.ax=self.figure.subplots();self.nodes=[]
        self.mpl_connect('pick_event',self.pick)
    def pick(self,event):
        if event.artist is getattr(self,'points',None) and len(event.ind): self.selected.emit(self.nodes[event.ind[0]])
    def render(self,g,positions,mapping,scores,community=None,selected=None):
        self.ax.clear();self.ax.set_axis_off()
        self.nodes=[n for n in g if community is None or mapping[n]==community]
        h=g.subgraph(self.nodes)
        # Keep rendering bounded; metrics always use the entire graph.
        edges=list(h.edges())[:4000]
        nx.draw_networkx_edges(h,positions,edgelist=edges,ax=self.ax,alpha=.18,width=.7,arrows=False)
        self.points=nx.draw_networkx_nodes(h,positions,nodelist=self.nodes,ax=self.ax,
            node_color=[mapping[n] for n in self.nodes],cmap='tab20',vmin=1,vmax=max(2,max(mapping.values(),default=1)),node_size=[55+800*scores.get(n,0) for n in self.nodes],alpha=.9)
        self.points.set_picker(5)
        if selected in h:
            neighbors=set(g.neighbors(selected))&set(h)
            nx.draw_networkx_nodes(h,positions,nodelist=[selected],node_color='#ffbf47',node_size=260,ax=self.ax)
            nx.draw_networkx_edges(h,positions,edgelist=[(selected,n) for n in neighbors],edge_color='#f59e0b',width=2,ax=self.ax,arrows=False)
            nx.draw_networkx_labels(h,positions,labels={selected:selected},font_size=9,ax=self.ax)
        self.ax.set_title(f'{len(h)} visible users • {len(edges)} displayed connections',fontsize=10)
        self.figure.tight_layout();self.draw_idle()
