from typing import Set, Tuple, Callable

from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable

from project.context_free.hellings import hellings_algo


def cfpq(
    graph: MultiDiGraph,
    cfg: CFG,
    start_symbol: Variable = Variable("S"),
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
    cfpq_algo: Callable[[MultiDiGraph, CFG], Set[Tuple[str, int, int]]] = hellings_algo,
) -> Set[Tuple[int, int]]:
    start_nodes = start_nodes if start_nodes is not None else graph.nodes
    final_nodes = final_nodes if final_nodes is not None else graph.nodes
    all_triplets = cfpq_algo(graph, cfg)

    return {
        (start, final)
        for symbol, start, final in all_triplets
        if Variable(symbol) == start_symbol
        and start in start_nodes
        and final in final_nodes
    }
