grammar grammarGQL;

prog: (stmt NEWLINE)* EOF;

stmt
    : 'set ' var ' = ' expr
    | 'print ' expr
    ;

var
    : NAME
    | '(' var ',' var ')'
    | '(' var ',' var ',' var ')'
    ;

val
    : STRING
    | INTEGER
    | BOOLEAN
    ;

expr
    : var
    | val
    | expr ' with starts := ' set_val
    | expr ' with finals := ' set_val
    | expr ' with starts += ' set_val
    | expr ' with finals += ' set_val
    | 'starts of (' expr ')'
    | 'finals of (' expr ')'
    | 'reachable of (' expr ')'
    | 'vertices of (' expr ')'
    | 'edges of (' expr ')'
    | 'labels of (' expr ')'
    | 'map (' lambda ') over (' expr ')'
    | 'filter (' lambda ') from (' expr ')'
    | 'load ' STRING
    | expr ' && ' expr
    | expr ' .. ' expr
    | expr ' || ' expr
    | '(' expr ')*'
    | '#(' expr ')'
    ;

set_val: '{' val (',' val)* '}';
lambda: 'fun ' var ' -> ' expr;

STRING: '"' ~["*\\]+ '"';
INTEGER: [0-9]+;
BOOLEAN: 'true' | 'false';

NAME: (LETTER | '_') (LETTER | DIGIT | '_')*;
LETTER: [a-z] | [A-Z];
DIGIT: [0-9];
NEWLINE: [\r\n]+;
