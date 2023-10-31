from tree_sitter import Language, Parser, Node
import sys
import os
import json
import tqdm
import re

args = sys.argv[1:]

# The first parameter is the location where .so file will be stored
# sencond paramenter is a list of locations where the github repository of
# the language you want to parse exists
Language.build_library(
    'tree/build/my-languages.so',
    [
        'tree/vendor/tree-sitter-python-master'
    ]
)

# load parser from .so file
python_language = Language('tree/build/my-languages.so', 'python')
python_parser = Parser()
python_parser.set_language(python_language)

# traverse AST
# copy from https://github.com/xing-hu/EMSE-DeepCom
def SBT_(cur_root_id, node_list):
    cur_root = node_list[cur_root_id]
    tmp_list = []
    tmp_list.append("(")

    str = cur_root['type']
    tmp_list.append(str)

    if 'children' in cur_root:
        chs = cur_root['children']
        for ch in chs:
            tmp_list.extend(SBT_(ch, node_list))
    tmp_list.append(")")
    tmp_list.append(str)
    return tmp_list

def get_sbt_structure(ast_list:list):
    ast_sbt = SBT_(0, ast_list)
    return ' '.join(ast_sbt) + '\n'

# use BFS to convert ASTs into lists which satisfy the interface of DeepCom
class Queue:
    def __init__(self):
        self.queue = []
        self.index = 0
    
    def enqueue(self, node):
        self.queue.append(node)
    
    def dequeue(self):
        temp = self.queue[self.index]
        self.index += 1
        return temp
    
    def is_empty(self):
        if self.index == len(self.queue):
            return True
        else:
            return False

# split compound words
def split_word(word:str):
    words = []
    
    if len(word) <= 1:
        return word

    word_parts = re.split('[^0-9a-zA-Z]', word)
    for part in word_parts:
        part_len = len(part)
        if part_len == 1:
            words.append(part)
            continue
        word = ''
        for index, char in enumerate(part):
            # condition : level|A
            if index == part_len - 1 and char.isupper() and part[index-1].islower():
                if word != '':
                    words.append(word)
                words.append(char)
                word = ''
                
            elif(index != 0 and index != part_len - 1 and char.isupper()):
                # condition 1 : FIRST|Name
                # condition 2 : first|Name
                condition1 = part[index-1].isalpha() and part[index+1].islower()
                condition2 = part[index-1].islower() and part[index+1].isalpha()
                if condition1 or condition2:
                    if word != '':
                        words.append(word)
                    word = ''
            
            else:
                word += char
        
        if word != '':
            words.append(word)
            
    return [word.lower() for word in words]
  
def BFS(root:Node):
    ast = []
    number = 0
    q = Queue()
    if len(root.named_children) == 1:
        q.enqueue(root.named_children[0])
    else:
        q.enqueue(root)
    while not q.is_empty():
        node = q.dequeue()
        ast.append({
            "type":node.type,
            "value":' '.join(split_word(str(node.text))),
            "children":[i for i in range(number+1, number+1+len(node.named_children))]
        }) 
        number += len(node.named_children)
        for i in node.named_children:
            q.enqueue(i)
    return ast
                        

phase = {'train':'train', 'dev':'val', 'test':'test'}
for p in phase.keys():
    input_file = os.path.join(args[0], '{}_originalcode'.format(p))
    output_dir = os.path.join(args[1], '{}'.format(phase[p]))
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if p == 'train':
        output_file = os.path.join(output_dir, 'train.token.ast')
    else:
        output_file = os.path.join(output_dir, 'test.token.ast')
    with open(input_file, 'r') as f, open(output_file, 'w') as f1:
        for i, line in tqdm.tqdm(enumerate(f)):
            code = line.replace('DCNL', '\n').replace('DCSP', '\t').strip()
            tree = python_parser.parse(bytes(code, 'utf8'))
            root_node = tree.root_node
            ast_list = BFS(root_node)
            SBT = get_sbt_structure(ast_list)
            f1.write(SBT)
            