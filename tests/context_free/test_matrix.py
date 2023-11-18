import os

from project.context_free.matrix import matrix_algo
from tests.context_free.test_cfpq import (
    graph,
    empty_cfg,
    cfg,
    full_cfg,
    expected,
    expected_all,
)

current_dir_path = os.path.dirname(os.path.realpath(__file__))


def test_empty_result(graph, empty_cfg):
    assert matrix_algo(graph, empty_cfg) == set()


def test_complex(graph, cfg, expected):
    assert matrix_algo(graph, cfg) == expected


def test_full_result(graph, full_cfg, expected_all):
    assert matrix_algo(graph, full_cfg) == expected_all
