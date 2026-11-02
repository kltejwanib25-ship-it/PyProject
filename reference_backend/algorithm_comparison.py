"""Compare partitions; expensive algorithms can be explicitly skipped."""
import pandas as pd
from reference_backend.community_detection import ALGORITHMS, detect

def compare(graph):
    rows=[];results={}
    for name in ALGORITHMS:
        try:
            r=detect(graph,name);results[name]=r
            rows.append({'algorithm':name,'communities':len(r['communities']),'modularity':r['modularity'],
                         'seconds':r['seconds'],'sizes':','.join(str(len(p)) for p in r['communities']),'status':'OK'})
        except ValueError as exc:
            rows.append({'algorithm':name,'status':str(exc)})
    return pd.DataFrame(rows),results
