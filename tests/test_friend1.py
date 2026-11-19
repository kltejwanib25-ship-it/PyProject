import pandas as pd
import networkx as nx
import pytest
from core.data_loader import clean_data,load_csv,sample_data
from core.graph_builder import build_graph,community_graph

@pytest.mark.parametrize('weight',['bad','0','-1','inf',''])
def test_bad_weights(weight):
    with pytest.raises(ValueError):clean_data(pd.DataFrame([['A','B',weight]],columns=['source','target','weight']))

def test_load_and_duplicates(tmp_path):
    p=tmp_path/'input.csv';p.write_text('source,target,weight\nA,B,2\nB,A,3\nC,C,1\n')
    df,note=load_csv(p);g=build_graph(df)
    assert g['A']['B']['weight']==5;assert g.degree('C')==0;assert '1 duplicate' in note
    df,_=load_csv(p,True);g=build_graph(df,True);assert g.number_of_edges()==2
    assert community_graph(g)['A']['B']['weight']==5
    df,_=load_csv(p,weighted=False);assert build_graph(df)['A']['B']['weight']==1

@pytest.mark.parametrize('text',['x,y\nA,B','source,target\n,B','source,target\nA,'])
def test_bad_csv(tmp_path,text):
    p=tmp_path/'bad.csv';p.write_text(text)
    with pytest.raises(ValueError):load_csv(p)

def test_node_limit():
    frame=pd.DataFrame({'source':[f'n{i}' for i in range(2001)],'target':[f'n{i}' for i in range(2001)]})
    with pytest.raises(ValueError,match='2,000'):clean_data(frame)
