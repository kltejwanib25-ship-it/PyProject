"""Deterministic community partitions using NetworkX implementations."""
from time import perf_counter
import networkx as nx
from reference_backend.graph_builder import community_graph
ALGORITHMS = ['Louvain','Girvan–Newman','Greedy Modularity','Label Propagation']

def detect(graph: nx.Graph, algorithm: str = 'Louvain') -> dict:
    start=perf_counter();g=community_graph(graph)
    if algorithm not in ALGORITHMS: raise ValueError('Unknown algorithm')
    if algorithm=='Girvan–Newman' and (len(g)>150 or g.number_of_edges()>600):
        raise ValueError('Girvan–Newman limited to 150 users / 600 edges; choose another algorithm.')
    if not g.number_of_edges(): parts=[{n} for n in g]
    elif algorithm=='Louvain': parts=nx.community.louvain_communities(g,weight='weight',seed=42)
    elif algorithm=='Greedy Modularity': parts=nx.community.greedy_modularity_communities(g,weight='weight')
    elif algorithm=='Label Propagation': parts=list(nx.community.asyn_lpa_communities(g,weight='weight',seed=42))
    else:
        # Bound the hierarchy to four splits; retain best modularity, including initial components.
        parts=list(nx.connected_components(g));best=nx.community.modularity(g,parts,weight='weight')
        def bridge(h):
            scores=nx.edge_betweenness_centrality(h,weight='distance')
            return max(scores,key=scores.get)
        from itertools import islice
        for candidate in islice(nx.community.girvan_newman(g,most_valuable_edge=bridge),4):
            score=nx.community.modularity(g,candidate,weight='weight')
            if score>best: parts=list(candidate);best=score
    parts=sorted([sorted(p) for p in parts],key=lambda p:(-len(p),p))
    return {'algorithm':algorithm,'communities':parts,'mapping':{n:i+1 for i,p in enumerate(parts) for n in p},
            'modularity':nx.community.modularity(g,parts,weight='weight') if g.number_of_edges() else 0.0,
            'seconds':perf_counter()-start}
