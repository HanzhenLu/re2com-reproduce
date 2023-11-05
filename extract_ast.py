import sys
import os
import ast
import re
import tokenize

args = sys.argv[1:]

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

def get_sbt_structure(ast_list):
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
  
def BFS(root):
    ast_list = []
    number = 0
    q = Queue()
    q.enqueue(root)
    pat = re.compile(r'.*_ast\.(.*)\'.*')
    while not q.is_empty():
        node = q.dequeue()
        match = re.match(pat, str(type(node)).lower())
        _type = match.group(1)
        children = []
        for child in ast.iter_child_nodes(node):
            children.append(child)
        ast_list.append({
            "type":_type,
            "children":[i for i in range(number+1, number+1+len(children))]
        }) 
        number += len(children)
        for i in children:
            q.enqueue(i)
    return ast_list

if __name__ == '__main__':
    phase = {'train':'train', 'dev':'val', 'test':'test'}
    for p in phase.keys():
        input_file = os.path.join(args[0], '{}_originalcode'.format(p))
        output_dir = os.path.join(args[1], '{}'.format(phase[p]))
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        if p == 'train':
            ast_file = os.path.join(output_dir, 'train.token.ast')
        else:
            ast_file = os.path.join(output_dir, 'test.token.ast')
        with open(input_file, 'r') as f, open(ast_file, 'w') as f1:
            for line in f:
                code = re.sub('DCNL\s+', '\n', line)
                code = re.sub('DCSP\s+', '\t', code)
                
                # extract ast
                root = ast.parse(code)
                ast_list = BFS(root)
                SBT = get_sbt_structure(ast_list)
                f1.write(SBT)
                
                

