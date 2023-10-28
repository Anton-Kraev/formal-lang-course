from __future__ import annotations

from typing import Dict, Set
from pyformlang.cfg import CFG, Variable, Terminal
from pyformlang.regular_expression import Regex


class ECFG:
    def __init__(
        self,
        start_symbol: Variable,
        variables: Set[Variable],
        terminals: Set[Terminal],
        productions: Dict[Variable, Regex],
    ):
        self.start_symbol = start_symbol
        self.variables = variables
        self.terminals = terminals
        self.productions = productions

    @staticmethod
    def from_cfg(cfg: CFG) -> ECFG:
        start_symbol = cfg.start_symbol or Variable("S")
        variables = set(cfg.variables or [])
        terminals = set(cfg.terminals or [])

        productions: Dict[Variable, Regex] = {}
        if cfg.productions:
            for head, body in cfg.productions:
                prev_body = productions.get(head)
                curr_body = Regex(" ".join([el.value for el in body]))
                productions[head] = (
                    prev_body.union(curr_body) if prev_body else curr_body
                )

        return ECFG(start_symbol, variables, terminals, productions)
