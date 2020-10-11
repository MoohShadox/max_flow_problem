from random import random

import pandas as pd
import numpy as np

def load_graph(file_txt):
    l = open(file_txt)
    nodes_set = set()
    sources = set()
    puits = set()
    edges = []
    for i in l:
        s1,s2,p = i.strip().split(",")
        edges.append((s1,s2,p))
        nodes_set.add(s1)
        nodes_set.add(s2)
        if(s1.startswith("s")):
            sources.add(s1)
        if(s2.startswith("p")):
            puits.add(s2)
    return list(nodes_set), list(edges), list(sources), list(puits)


