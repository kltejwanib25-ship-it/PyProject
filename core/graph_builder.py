"""Strength weights become inverse distances for shortest-path metrics."""
import networkx as nx

def build_graph(frame, directed: bool = False) -> nx.Graph:
    graph = nx.DiGraph() if directed else nx.Graph()
    for a,b,w in frame.itertuples(index=False,name=None):
        graph.add_nodes_from([a,b])
        if a != b: graph.add_edge(a,b,weight=float(w),distance=1.0/float(w))
    return graph

def community_graph(graph: nx.Graph) -> nx.Graph:
    """Explicit undirected projection: reciprocal strengths are summed."""
    if not graph.is_directed(): return graph.copy()
    result=nx.Graph();result.add_nodes_from(graph)
    for a,b,d in graph.edges(data=True):
        w=d.get('weight',1)+result.get_edge_data(a,b,{}).get('weight',0)
        result.add_edge(a,b,weight=w,distance=1/w)
    return result
