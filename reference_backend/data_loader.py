"""Validated edge lists; self-rows encode isolates and are not graph edges."""
from pathlib import Path
import numpy as np
import pandas as pd
MAX_NODES = 2000
MAX_EDGES = 20000

def load_csv(path: str | Path, directed: bool = False, weighted: bool = True):
    if Path(path).stat().st_size > 10_000_000:
        raise ValueError('CSV exceeds 10 MB limit.')
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    return clean_data(frame, directed, weighted)

def clean_data(frame: pd.DataFrame, directed: bool = False, weighted: bool = True):
    if not {'source','target'} <= set(frame.columns):
        raise ValueError('CSV requires source and target columns.')
    if len(frame) > 100000:
        raise ValueError('Input exceeds 100,000 rows.')
    df = frame[['source','target']].copy()
    for col in ['source','target']:
        df[col] = df[col].fillna('').astype(str).str.strip()
        if (df[col] == '').any():
            raise ValueError(f'Missing {col} value. Correct the CSV and retry.')
        if (df[col].str.len() > 120).any():
            raise ValueError('User names must be at most 120 characters.')
    df['weight'] = pd.to_numeric(frame['weight'], errors='coerce') if weighted and 'weight' in frame else 1.0
    if not np.isfinite(df['weight']).all() or (df['weight'] <= 0).any():
        raise ValueError('Weights must be finite positive numbers.')
    if not directed:
        pairs = [sorted((a,b)) for a,b in zip(df.source,df.target)]
        if pairs: df[['source','target']] = pairs
    before = len(df)
    df = df.groupby(['source','target'],as_index=False,sort=True).weight.sum()
    if not weighted: df['weight'] = 1.0
    if not np.isfinite(df.weight).all(): raise ValueError('Aggregated weights overflow.')
    nodes = set(df.source) | set(df.target)
    if len(nodes)>MAX_NODES or len(df)>MAX_EDGES:
        raise ValueError('Limit: 2,000 users and 20,000 connections.')
    note = f'{before-len(df)} duplicate rows merged; {(df.source==df.target).sum()} self-rows retained as user declarations.'
    return df, note

def sample_data(seed: int = 42, size: int = 120) -> pd.DataFrame:
    import random
    rng=random.Random(seed); rows=[]
    names=[f'Student_{i+1:03d}' for i in range(size)]
    for i,a in enumerate(names):
        rows.append((a,a,1))
        for j in range(i+1,size):
            same=i//30==j//30
            if rng.random() < (0.20 if same else 0.008):
                rows.append((a,names[j],rng.randint(3,8) if same else 1))
    for i in range(0,size-30,30): rows.append((names[i],names[i+30],2))
    return pd.DataFrame(rows,columns=['source','target','weight'])
