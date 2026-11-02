from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
class ComparisonChart(FigureCanvasQTAgg):
    def __init__(self):super().__init__(Figure(figsize=(8,4),facecolor='#f4f6fb'))
    def update_data(self,frame,results):
        self.figure.clear();axes=self.figure.subplots(1,3);ok=frame[frame.status=='OK']
        for ax,col in zip(axes[:2],['modularity','seconds']):
            ax.bar(ok.algorithm,ok[col],color='#7866ec');ax.set_title(col.title());ax.tick_params(axis='x',labelrotation=45,labelsize=7)
        for name,r in results.items():axes[2].plot(range(1,len(r['communities'])+1),sorted([len(p) for p in r['communities']],reverse=True),marker='.',label=name)
        axes[2].set_title('Sorted community sizes');axes[2].legend(fontsize=6);self.figure.tight_layout();self.draw_idle()
