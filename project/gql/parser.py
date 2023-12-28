from pydot import Dot, Node, Edge
from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl

from project.gql.grammarGQLLexer import grammarGQLLexer
from project.gql.grammarGQLParser import grammarGQLParser
from project.gql.grammarGQLListener import grammarGQLListener


def get_parser(input_: InputStream) -> grammarGQLParser:
    lexer = grammarGQLLexer(input_)
    stream = CommonTokenStream(lexer)
    parser = grammarGQLParser(stream)
    return parser


def check(input_: str) -> bool:
    parser = get_parser(InputStream(input_))
    parser.prog()
    return parser.getNumberOfSyntaxErrors() == 0


def write_to_dot(input_: str, path: str):
    if not check(input_):
        raise ValueError("The input does not belong to the language.")
    parser = get_parser(InputStream(input_))
    listener = DotTreeListener()
    ParseTreeWalker().walk(listener, parser.prog())
    listener.dot.write(path)


class DotTreeListener(grammarGQLListener):
    def __init__(self):
        self.dot = Dot("tree", graph_type="digraph")
        self.num_nodes = 0
        self.nodes = {}
        self.rules = grammarGQLParser.ruleNames
        super(DotTreeListener, self).__init__()

    def enterEveryRule(self, ctx: ParserRuleContext):
        if ctx not in self.nodes:
            self.num_nodes += 1
            self.nodes[ctx] = self.num_nodes
        if ctx.parentCtx:
            self.dot.add_edge(Edge(self.nodes[ctx.parentCtx], self.nodes[ctx]))
        label = self.rules[ctx.getRuleIndex()]
        self.dot.add_node(Node(self.nodes[ctx], label=label))

    def visitTerminal(self, node: TerminalNodeImpl):
        self.num_nodes += 1
        self.dot.add_edge(Edge(self.nodes[node.parentCtx], self.num_nodes))
        self.dot.add_node(Node(self.num_nodes, label=f"{node.getText()}"))
