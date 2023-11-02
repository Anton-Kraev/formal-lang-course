import os
from pyformlang.cfg import CFG, Terminal, Variable
from pyformlang.regular_expression import Regex
from project.context_free.ecfg import ECFG
from project.context_free.rsm import RSM
from project.context_free.cfg_utils import read_cfg

current_dir_path = os.path.dirname(os.path.realpath(__file__))


def test_empty_cfg():
    cfg = CFG()
    ecfg = ECFG.from_cfg(cfg)
    rsm = RSM.from_ecfg(ecfg)

    assert rsm.start_symbol == "S"
    assert rsm.boxes == {}


def test_cfg_to_rsm():
    path = os.path.join(current_dir_path, "../resources/cfg_cnf.txt")
    cfg = read_cfg(path)
    ecfg = ECFG.from_cfg(cfg)
    rsm = RSM.from_ecfg(ecfg)

    assert rsm.start_symbol == "S"
    for actual, expected in zip(
        [
            (symbol, box)
            for symbol, box in sorted(rsm.boxes.items(), key=lambda x: x[0].value)
        ],
        [
            (Variable(head), Regex(body).to_epsilon_nfa())
            for head, body in [
                ("A", "a"),
                ("B", "b"),
                ("S", "(A B)|c|$"),
            ]
        ],
    ):
        assert actual[0] == expected[0]
        assert actual[1].is_equivalent_to(expected[1])
