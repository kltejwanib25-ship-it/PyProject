"""Export a self-contained snapshot; PDF charts use native Matplotlib."""
from pathlib import Path
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_pdf import PdfPages

def safe_csv(frame, path):
    """Escape text formula prefixes for spreadsheet applications."""
    copy=frame.copy()
    for col in copy.select_dtypes(include=['object','string']).columns:
        copy[col]=copy[col].map(lambda x: "'"+x if isinstance(x,str) and x.startswith(('=','+','-','@','\t','\r')) else x)
    copy.to_csv(path,index=False)

def export_reports(folder, graph, result, stats, centrality, comparison):
    target=Path(folder);target.mkdir(parents=True,exist_ok=True)
    safe_csv(centrality[['user','community']],target/'community_membership.csv')
    safe_csv(centrality,target/'user_centrality.csv')
    safe_csv(pd.DataFrame(stats.items(),columns=['metric','value']),target/'network_statistics.csv')
    safe_csv(comparison,target/'algorithm_comparison.csv')
    with PdfPages(target/'summary.pdf') as pdf:
        fig=Figure(figsize=(8.27,11.69));ax=fig.subplots();ax.axis('off')
        lines=['COMMUNITYSCOPE','Network analysis report','',f"Algorithm: {result['algorithm']}"]
        lines += [f'{k}: {v:.5g}' if isinstance(v,float) else f'{k}: {v}' for k,v in stats.items()]
        lines += ['', 'Directed networks: communities use summed undirected projection.',
                  'Weights represent connection strength; path distance = 1 / weight.',
                  'Betweenness uses 150 sampled sources above 300 users.',
                  'Synthetic data demonstrates structure, not real influence or causation.']
        ax.text(.02,.97,'\n'.join(lines),va='top',fontsize=11,linespacing=1.8);pdf.savefig(fig)
        fig=Figure(figsize=(8.27,11.69));axs=fig.subplots(2,1)
        axs[0].bar(range(1,len(result['communities'])+1),[len(p) for p in result['communities']],color='#6c63ff')
        axs[0].set(title='Community sizes',xlabel='Community',ylabel='Users')
        top=centrality.sort_values('pagerank',ascending=False).head(10)
        axs[1].barh(top.user.astype(str),top.pagerank,color='#16a6a1');axs[1].set(title='Top PageRank users')
        fig.tight_layout();pdf.savefig(fig)
        if not comparison.empty:
            fig=Figure(figsize=(8.27,6));ax=fig.subplots();ok=comparison[comparison.status=='OK']
            ax.bar(ok.algorithm,ok.modularity,color='#6c63ff');ax.set(title='Algorithm modularity comparison',ylabel='Modularity')
            ax.tick_params(axis='x',rotation=20);fig.tight_layout();pdf.savefig(fig)
    return target
