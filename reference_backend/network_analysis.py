"""Network metrics with disclosed approximation for larger graphs."""
import networkx as nx
import pandas as pd
from reference_backend.graph_builder import community_graph

def analyze(graph: nx.Graph, result: dict):
    n=len(graph); und=community_graph(graph)
    if n:
        degree=nx.degree_centrality(graph) if n>1 else {x:0.0 for x in graph}
        between=nx.betweenness_centrality(graph,k=min(n,150) if n>300 else None,weight='distance',seed=42)
        close=nx.closeness_centrality(graph,distance='distance')
        page=nx.pagerank(graph,weight='weight',max_iter=500)
        cluster=nx.clustering(und,weight='weight')
    else: degree=between=close=page=cluster={}
    rows=[{'user':x,'community':result['mapping'][x],'degree':degree[x],'betweenness':between[x],
           'closeness':close[x],'pagerank':page[x],'clustering':cluster[x]} for x in graph]
    table=pd.DataFrame(rows,columns=['user','community','degree','betweenness','closeness','pagerank','clustering'])
    stats={'Users':n,'Connections':graph.number_of_edges(),'Communities':len(result['communities']),
           'Density':nx.density(graph),'Average clustering':sum(cluster.values())/n if n else 0,
           'Modularity':result['modularity'],'Connected components':nx.number_connected_components(und),
           'Directed':graph.is_directed(),'Betweenness sampled':n>300}
    return stats,table
