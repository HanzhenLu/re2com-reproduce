import sys
import os
import re
import tokenize
from tqdm import tqdm

args = sys.argv[1:]

# split compound words
def split_word(word):
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
            
            else:
                word += char
        
        if word != '':
            words.append(word)
            
    return [word.lower() for word in words]

if __name__ == '__main__':
    phase = {'train':'train', 'dev':'val', 'test':'test'}
    for p in phase.keys():
        input_file = os.path.join(args[0], '{}_originalcode'.format(p))
        output_dir = os.path.join(args[1], '{}'.format(phase[p]))
        token_file = os.path.join(output_dir, 'code.original_subtoken')
        with open(input_file, 'r') as f, open(token_file, 'w') as f2:
            for line in tqdm(f):
                code = re.sub('DCNL\s+', '\n', line)
                code = re.sub('DCSP\s+', '\t', code)
                # tokenize
                with open('temp', 'w') as w:
                    w.write(code)
                sub_tokens = []
                with tokenize.open('temp') as w:
                    tokens = tokenize.generate_tokens(w.readline)
                    for token in tokens:
                        split = split_word(token.string)
                        for i in split:
                            sub_tokens.append(i.lower())
                f2.write(' '.join(' '.join(sub_tokens).split())+'\n')
    os.remove('temp')