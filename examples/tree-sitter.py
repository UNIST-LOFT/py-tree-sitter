import tree_sitter_python as tspython
from tree_sitter import Language, Parser
from sys import argv

PY_LANGUAGE = Language(tspython.language(), 'python')
parser = Parser()
parser.set_language(PY_LANGUAGE)

with open(argv[1],'r') as f:
    root = parser.parse(bytes(f.read(),'utf-8'))

root.root_node.print_tree()