import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Node
from sys import argv
from typing import List, Tuple, Union

PY_LANGUAGE = Language(tspython.language(),'python')
parser = Parser()
parser.set_language(PY_LANGUAGE)

with open(argv[1],'r') as f:
    root1 = parser.parse(bytes(f.read(),'utf-8'))

with open(argv[2],'r') as f:
    root2 = parser.parse(bytes(f.read(),'utf-8'))

diffs:List[Tuple[Union[Node,None],Union[Node,None]]]=[]
def compare_ast(node_1: Node,node_2: Node):
    global diffs

    if node_1.type != node_2.type:
        # Different node if type is different
        print('Different type found')
        print('Node a:')
        node_1.print_tree()
        print('Node b:')
        node_2.print_tree()
        diffs.append((node_1,node_2,))
        return
    if node_1.value != node_2.value:
        # Different node if the value is different
        print('Different value found')
        print('Node a:')
        node_1.print_tree()
        print('Node b:')
        node_2.print_tree()
        diffs.append((node_1, node_2,))
        return

    if node_1.named_child_count > node_2.named_child_count:
        # Node 1 has more children
        for i in range(node_2.named_child_count):
            compare_ast(node_1.named_child(i), node_2.named_child(i))

        print('Node a has more children')
        for i in range(node_2.named_child_count,node_1.named_child_count):
            print(f'{i}:')
            node_1.named_child(i).print_tree()
            diffs.append((node_1.named_child(i),None,))
    elif node_2.named_child_count > node_1.named_child_count:
        # Node 2 has more children
        for i in range(node_1.named_child_count):
            compare_ast(node_1.named_child(i), node_2.named_child(i))

        print('Node b has more children')
        for i in range(node_1.named_child_count,node_2.named_child_count):
            print(f'{i}:')
            node_2.named_child(i).print_tree()
            diffs.append((None,node_2.named_child(i),))
    else:
        for a,b in zip(node_1.named_children,node_2.named_children):
            compare_ast(a,b)

compare_ast(root1.root_node, root2.root_node)