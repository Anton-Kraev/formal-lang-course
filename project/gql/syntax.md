
## Abstract syntax

```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    String of string
  | Int of int
  | Bool of bool

var =
    Id of name
  | Pair of var * var
  | Triple of var * var * var

expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of Set<val> * expr // задать множество стартовых состояний
  | Set_final of Set<val> * expr // задать множество финальных состояний
  | Add_start of Set<val> * expr // добавить состояния в множество стартовых
  | Add_final of Set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)
  | Smb of expr                  // единичный переход

lambda = Fun of var * expr
```
## Concrete syntax
```
prog = (stmt "\n")*

stmt = "set " var " = " expr
     | "print" expr

var = name
    | "(" var "," var ")"
    | "(" var "," var "," var ")"

val = string
    | integer
    | boolean

expr = var
     | val
     | expr " with starts := " set<val>
     | expr " with finals := " set<val>
     | expr " with starts += " set<val>
     | expr " with finals += " set<val>
     | "starts of (" expr ")"
     | "finals of (" expr ")"
     | "reachable of (" expr ")"
     | "vertices of (" expr ")"
     | "edges of (" expr ")"
     | "labels of (" expr ")"
     | "map (" lambda ") over (" expr ")"
     | "filter (" lambda ") from (" expr ")"
     | "load " path
     | expr " && " expr
     | expr " .. " expr
     | expr " || " expr
     | "(" expr ")*"
     | "#(" expr ")"

lambda = "fun " var " -> " expr

path = string
name = letter (letter | digit | "_")*
set<val> = "{" val ("," val)* "}"

string = '"' character* '"'
integer = digit+
boolean = "true" | "false"

digit = "0".."9"
letter = "a".."z" | "A".."Z"
character = any character except double quote or backslash
```
## Examples

```
set g = load "wine"
set reachable_g = reachable of (g with starts := {1,2,3})
print reachable_g
```

```
set g = load "wine"
set r = ("a" .. "b" || "c")* with starts := {0} with finals := {0}
set labels = map (fun (_,l,_) -> l) (r && g)
print labels
```

```
set g1 = load "wine" with starts := {1,2}
set g2 = g1 with starts += {3,4,5}
set q1 = ("type" || "l1" || "l2")*
set q2 = "sub_class_of" || q2 || q3
set res1 = g1 && q1
set res2 = g2 && q2
print res1
print res2
set s1 = starts of g1
set s2 = starts of g2
set vertices1 = filter (fun v -> v in s1) from (map (fun ((u_g,u_q1),l,(v_g,v_q1)) -> u_g) over (edges of res1))
set vertices2 = filter (fun v -> v in s2) from (map (fun ((u_g,u_q2),l,(v_g,v_q2)) -> u_g) over (edges of res2))
set vertices = vertices1 && vertices2
print vertices
```
