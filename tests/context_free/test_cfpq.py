import os
from itertools import product

import pytest
from networkx import MultiDiGraph
from pyformlang.cfg import Variable, CFG

from project.context_free.cfg_utils import read_cfg
from project.context_free.cfpq import cfpq
from project.context_free.hellings import hellings_algo
from project.context_free.matrix import matrix_algo

current_dir_path = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture()
def graph():
    graph = MultiDiGraph()
    graph.add_nodes_from([0, 1, 2, 3])
    graph.add_edges_from(
        [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "a"}),
            (2, 0, {"label": "a"}),
            (2, 3, {"label": "b"}),
            (3, 2, {"label": "b"}),
        ]
    )

    return graph


@pytest.fixture()
def empty_cfg():
    return CFG()


@pytest.fixture()
def cfg():
    path = os.path.join(current_dir_path, "../resources/cfpq_cfg.txt")
    return read_cfg(path)


@pytest.fixture()
def full_cfg():
    path = os.path.join(current_dir_path, "../resources/cfpq_full_cfg.txt")
    return read_cfg(path)


@pytest.fixture()
def expected_pair():
    return {(1, 2), (1, 3)}


@pytest.fixture()
def expected():
    return {
        (Variable("A"), 0, 1),
        (Variable("A"), 1, 2),
        (Variable("A"), 2, 0),
        (Variable("B"), 2, 3),
        (Variable("B"), 3, 2),
        (Variable("S"), 0, 2),
        (Variable("S"), 0, 3),
        (Variable("S"), 1, 2),
        (Variable("S"), 1, 3),
        (Variable("S"), 2, 2),
        (Variable("S"), 2, 3),
        (Variable("S1"), 0, 2),
        (Variable("S1"), 0, 3),
        (Variable("S1"), 1, 3),
        (Variable("S1"), 1, 2),
        (Variable("S1"), 2, 2),
        (Variable("S1"), 2, 3),
    }


@pytest.fixture()
def expected_all(graph, full_cfg):
    return {
        (var, node1, node2)
        for var in full_cfg.variables
        for node1, node2 in product(graph.nodes, graph.nodes)
    }


@pytest.fixture()
def start_nodes():
    return {1}


@pytest.fixture()
def final_nodes():
    return {0, 1, 2, 3}


def test_hellings(graph, cfg, start_nodes, final_nodes, expected_pair):
    assert (
        cfpq(
            graph,
            cfg,
            start_nodes=start_nodes,
            final_nodes=final_nodes,
            cfpq_algo=hellings_algo,
        )
        == expected_pair
    )


def test_matrix(graph, cfg, start_nodes, final_nodes, expected_pair):
    assert (
        cfpq(
            graph,
            cfg,
            start_nodes=start_nodes,
            final_nodes=final_nodes,
            cfpq_algo=matrix_algo,
        )
        == expected_pair
    )
