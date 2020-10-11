from pulp import *

from matrix_management import load_graph


def solve(graph):
    nodes_set, edges_set, sources, puits = load_graph(graph)
    prob = LpProblem("Max_flow",LpMaximize)
    variables = LpVariable.dicts("S",(nodes_set,nodes_set),0,None,LpVariable)
    for i in sources:
        edges_from_src = [variables[s][d] for s,d,w in edges_set if s == i]
        prob += lpSum(edges_from_src)
    for i in nodes_set:
        edges_from_node = [variables[s][d] for s,d,w in edges_set if s == i]
        edges_to_node = [variables[s][d]  for s,d,w in edges_set if d == i]
        if(len(edges_to_node) > 0 and len(edges_from_node) > 0):
            prob += (lpSum(edges_to_node) == lpSum(edges_from_node))
    for s,d,w in edges_set:
        prob += variables[s][d] <= float(w)
    prob.solve()
    affectations = {}
    for v in prob.variables():
        affectations[tuple(v.name.split("_")[1:])] = v.varValue
    return affectations
