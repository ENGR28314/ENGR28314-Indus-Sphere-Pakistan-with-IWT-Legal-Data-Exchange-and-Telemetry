import networkx as nx
import pandas as pd

def build_water_network(edges):
    g = nx.DiGraph()
    for edge in edges:
        g.add_edge(edge["from"], edge["to"], capacity=float(edge.get("capacity", 0)))
    return g

def max_flow(edges, source, sink):
    g = build_water_network(edges)
    value, flow = nx.maximum_flow(g, source, sink, capacity="capacity")
    rows = []
    for u, targets in flow.items():
        for v, amount in targets.items():
            rows.append({"from":u,"to":v,"flow":amount})
    return value, pd.DataFrame(rows)
