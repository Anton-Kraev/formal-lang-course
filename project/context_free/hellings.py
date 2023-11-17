from typing import Set, Tuple

from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Terminal, Variable

from project.context_free.cfg_utils import cfg_to_wcnf


def hellings_algo(graph: MultiDiGraph, cfg: CFG) -> Set[Tuple[str, int, int]]:
    wcnf = cfg_to_wcnf(cfg)
    eps_prods = {prod.head for prod in wcnf.productions if len(prod.body) == 0}
    term_prods = [
        (prod.head, prod.body) for prod in wcnf.productions if len(prod.body) == 1
    ]
    var_prods = [
        (prod.head, prod.body) for prod in wcnf.productions if len(prod.body) == 2
    ]

    reachable = {
        (variable, node, node) for node in graph.nodes for variable in eps_prods
    } | {
        (head, start, final)
        for start, final, label in graph.edges(data="label")
        for head, body in term_prods
        if body[0] == Terminal(label)
    }
    queue = reachable.copy()

    while queue:
        new = set()
        var1, v1, u1 = queue.pop()

        for var2, v2, u2 in reachable:
            if u2 == v1:
                new |= {
                    (head, v2, u1)
                    for head, body in var_prods
                    if body == [var2, var1] and (head, v2, u1) not in reachable
                }

            if v2 == u1:
                new |= {
                    (head, v1, u2)
                    for head, body in var_prods
                    if body == [var1, var2] and (head, v1, u2) not in reachable
                }

        reachable |= new
        queue |= new

    return reachable
