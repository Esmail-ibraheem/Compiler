class Node:
    def __init__(self, op, arg1=None, arg2=None, result=None):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

def to_tac(ast):
    def visit(node):
        if node is None:
            return None
        elif node.op == "BeginFunc":
            return _BeginFunc(node.result)
        elif node.op == "EndFunc":
            return _EndFunc()
        elif node.op == "Assign":
            return _Assign(node.result, visit(node.arg1), visit(node.arg2))
        elif node.op == "PushParam":
            return _PushParam(node.result, visit(node.arg1))
        elif node.op == "LCall":
            return _LCall(node.result, visit(node.arg1), visit(node.arg2))
        elif node.op == "PopParams":
            return _PopParams(node.result)
        elif node.op == "Ident":
            return _Ident(node.result)
        elif node.op == "Int":
            return _Int(node.result)
        else:
            raise ValueError(f"Unknown operator: {node.op}")

    return "".join(map(lambda x: str(x) + "\n", astwalk(visit(ast))))


def astwalk(node):
    if node is None:
        return []
    elif isinstance(node, list):
        return sum((astwalk(n) for n in node), [])
    else:
        return [node]   

class _BeginFunc:
    def __init__(self, result):
        self.op = "BeginFunc"
        self.result = result

    def __str__(self):
        return f"BeginFunc\nIdent({self.result})"

class _EndFunc:
    def __init__(self):
        self.op = "EndFunc"

    def __str__(self):
        return f"EndFunc"

class _Assign:
    def __init__(self, result, arg1, arg2):
        self.op = "Assign"
        self.result = result
        self.arg1 = arg1
        self.arg2 = arg2

    def __str__(self):
        return f"Assign\nIdent({self.result})\n{self.arg1}\n{self.arg2}"

class _PushParam:
    def __init__(self, result, arg1):
        self.op = "PushParam"
        self.result = result
        self.arg1 = arg1

    def __str__(self):
        return f"PushParam\nIdent({self.result})\n{self.arg1}"

class _LCall:
    def __init__(self, result, arg1, arg2):
        self.op = "LCall"
        self.result = result
        self.arg1 = arg1
        self.arg2 = arg2

    def __str__(self):
        return f"LCall\nIdent({self.result})\n{self.arg1}\n{self.arg2}"

class _PopParams:
    def __init__(self, result):
        self.op = "PopParams"
        self.result = result

    def __str__(self):
        return f"PopParams\nIdent({self.result})"

class _Ident:
    def __init__(self, result):
        self.op = "Ident"
        self.result = result

    def __str__(self):
        return f"Ident({self.result})"
        
class _Int:
    def __init__(self, result):
        self.op = "Int"
        self.result = result

    def __str__(self):
        return f"Int({self.result})"


ast = Node(
    "BeginFunc",
    Node("Ident", "to"),
    [
        Node("Assign", "to", Node("Int", 137)),
        Node(
            "BeginFunc",
            Node("Ident", "X"),
            [
                Node("Assign", Node("Field", Node("This", 0), 0), Node("Ident", "a")),
                Node("Assign", Node("Field", Node("This", 0), 8), Node("Ident", "X")),
                Node("EndFunc"),
            ],
        ),
        Node("EndFunc"),
        Node("Ident", "to"),
    ],
)

print(to_tac(ast))
