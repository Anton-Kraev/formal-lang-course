from __future__ import annotations

from typing import Dict
from pyformlang.finite_automaton import Symbol, EpsilonNFA
from ecfg import ECFG


class RSM:
    def __init__(self, start_symbol: Symbol, boxes: Dict[Symbol, EpsilonNFA]):
        self.start_symbol = start_symbol
        self.boxes = boxes

    @staticmethod
    def from_ecfg(ecfg: ECFG) -> RSM:
        start_symbol = Symbol(ecfg.start_symbol.value)
        boxes = {
            symbol: regex.to_epsilon_nfa() for symbol, regex in ecfg.productions.items()
        }

        return RSM(start_symbol, boxes)

    def minimize(self) -> RSM:
        self.boxes = {symbol: enfa.minimize() for symbol, enfa in self.boxes.items()}

        return self
