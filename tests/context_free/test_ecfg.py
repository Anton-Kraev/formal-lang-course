import os
from pyformlang.cfg import CFG, Terminal, Variable
from pyformlang.regular_expression import Regex
from project.context_free.ecfg import ECFG
from project.context_free.cfg_utils import read_cfg
from project.regular.finite_automata_construct import regex_to_min_dfa

current_dir_path = os.path.dirname(os.path.realpath(__file__))


def test_empty_cfg():
    cfg = CFG()
    ecfg = ECFG.from_cfg(cfg)

    assert ecfg.start_symbol == "S"
    assert not any([ecfg.variables, ecfg.terminals, ecfg.productions])


def test_cfg_in_wcnf():
    path = os.path.join(current_dir_path, "../resources/cfg_wcnf.txt")
    cfg = read_cfg(path)
    ecfg = ECFG.from_cfg(cfg)

    assert ecfg.start_symbol == "S"
    assert ecfg.variables == {"S", "A", "B", "C"}
    assert ecfg.terminals == {Terminal("a"), Terminal("b")}
    for actual, expected in zip(
        [
            (head, body.to_epsilon_nfa())
            for head, body in sorted(ecfg.productions.items(), key=lambda x: x[0].value)
        ],
        [
            (Variable(head), Regex(body).to_epsilon_nfa())
            for head, body in [
                ("A", "a"),
                ("B", "b"),
                ("C", "(S B)|$"),
                ("S", "(A C)|(A B)"),
            ]
        ],
    ):
        assert actual[0] == expected[0]
        assert actual[1].is_equivalent_to(expected[1])
