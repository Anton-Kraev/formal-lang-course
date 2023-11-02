import os
from pyformlang.cfg import CFG, Terminal, Production
from project.context_free import cfg_utils

current_dir_path = os.path.dirname(os.path.realpath(__file__))


def test_read_empty_cfg():
    path = os.path.join(current_dir_path, "../resources/empty.txt")
    empty = cfg_utils.read_cfg(path)

    assert empty.is_empty()


def test_read_cfg():
    path = os.path.join(current_dir_path, "../resources/cfg_for_read.txt")
    cfg = cfg_utils.read_cfg(path, "A")

    assert cfg.start_symbol == "A"
    assert cfg.productions == {
        Production(head, body)
        for head, body in [
            ("A", [Terminal("a"), "A"]),
            ("A", [Terminal("b")]),
            ("A", ["B", "C", "D"]),
            ("A", []),
            ("B", ["E"]),
            ("E", ["F"]),
            ("C", ["F", Terminal("c")]),
            ("D", ["A"]),
            ("D", []),
            ("F", [Terminal("t")]),
            ("N", "A"),
        ]
    }


def test_already_in_cnf():
    path = os.path.join(current_dir_path, "../resources/cfg_cnf.txt")
    cnf = cfg_utils.read_cfg(path)
    cnf_transformed = cfg_utils.cfg_to_wcnf(cnf)

    assert cnf.start_symbol == cnf_transformed.start_symbol
    assert cnf.productions == cnf_transformed.productions


def test_already_in_wcnf():
    path = os.path.join(current_dir_path, "../resources/cfg_wcnf.txt")
    wcnf = cfg_utils.read_cfg(path)
    wcnf_transformed = cfg_utils.cfg_to_wcnf(wcnf)

    assert wcnf.start_symbol == wcnf_transformed.start_symbol
    assert wcnf.productions == wcnf_transformed.productions


def test_cfg_to_wcnf():
    cfg = CFG.from_text("S -> a S b S | $")
    wcnf = cfg_utils.cfg_to_wcnf(cfg)

    assert wcnf.start_symbol == "S"
    assert wcnf.productions == {
        Production(head, body)
        for head, body in [
            ("S", []),
            ("S", ["a#CNF#", "C#CNF#1"]),
            ("C#CNF#1", ["S", "C#CNF#2"]),
            ("C#CNF#2", ["b#CNF#", "S"]),
            ("a#CNF#", [Terminal("a")]),
            ("b#CNF#", [Terminal("b")]),
        ]
    }
