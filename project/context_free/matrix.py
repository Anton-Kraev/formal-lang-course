from typing import Set, Tuple

from networkx import MultiDiGraph
from pyformlang.cfg import CFG
from scipy.sparse import csr_matrix

from project.context_free.cfg_utils import cfg_to_wcnf


def matrix_algo(graph: MultiDiGraph, cfg: CFG) -> Set[Tuple[str, int, int]]:
    wcnf = cfg_to_wcnf(cfg)
    eps_prods = {prod.head for prod in wcnf.productions if len(prod.body) == 0}
    term_prods = [
        (prod.head, prod.body) for prod in wcnf.productions if len(prod.body) == 1
    ]
    var_prods = [
        (prod.head, prod.body) for prod in wcnf.productions if len(prod.body) == 2
    ]

    nodes_num = graph.number_of_nodes()
    matrices = {
        var: csr_matrix((nodes_num, nodes_num), dtype=bool) for var in wcnf.variables
    }

    for start, final, label in graph.edges(data="label"):
        for var, term in term_prods:
            if term[0].value == label:
                matrices[var][start, final] = True
    for var in eps_prods:
        matrices[var].setdiag(True)

    changed = True
    while changed:
        changed = False
        for head, body in var_prods:
            prev = matrices[head]
            curr = prev + matrices[body[0]] @ matrices[body[1]]
            matrices[head] = curr
            changed = changed or curr.nnz != prev.nnz

    return {
        (var, start, final)
        for var, matrix in matrices.items()
        for start, final in zip(*matrix.nonzero())
    }
