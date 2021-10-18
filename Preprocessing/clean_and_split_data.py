"""
    Script for combining data files and splitting them into train/dev/split.
    Assumes similar structure in source and target files.
    Removes all lines that contain characters that appear fewer than 
    specified number of times 
    
    Split is 80% train, 10% dev, 10% test
"""

import glob, re

from sys import argv
from pathlib import Path
from random import shuffle

from vocab import Vocabulary

# regex patterns
re_whitespace = re.compile('\s+')

if __name__ == "__main__":
    source, target, out, min_freq = argv[1:]
    min_freq = int(min_freq)
    # args[0] is source directory
    # args[2] is target directory
    # args[3] is out directory
    # args[4] is min_freq for char vocab
    
    # remove any slashes from  dir names
    target = re.sub('//', '', target)
    target = re.sub('\/', '', target)
    source = re.sub('//', '', source)
    source = re.sub('\/', '', source)
    
    source_files = glob.glob(source + "/**", recursive=True)
    
    # weed out subdir folders
    source_files = [f for f in source_files if Path(f).is_file()]
    
    target_files = [re.sub(source,target,f) for f in source_files]
    
    data = []
    
    vocabulary = Vocabulary.chars_from_files(source_files, min_freq=min_freq)
    char_set = vocabulary.token_to_index.keys()
    
    # combine + clean data, maintaining connection between src and tgt
    for i in range(len(source_files)):
        src_lines = open(source_files[i], encoding='utf8').readlines()
        tgt_lines = open(target_files[i], encoding='utf8').readlines()
        
        clean_src_lines = []
        clean_tgt_lines = []
        
        for i in range(len(src_lines)):
            line = src_lines[i].strip('\n')
            
            # discard empty strings
            if re_whitespace.fullmatch(line) == None:
                
                # make sure line has no OOV chars
                line_chars = ''.join(line.split())
                line_chars = set(line_chars)
                if len(line_chars.difference(char_set)) == 0:
                    clean_src_lines.append(line)
                    clean_tgt_lines.append(tgt_lines[i].strip('\n'))
            
        
        data.extend(zip(clean_src_lines,clean_tgt_lines))
        
        
    # shuffle data and split
    shuffle(data)
    first_break = round(len(data)* .8)
    second_break = round(len(data)*.9)
    
    train = data[:first_break]
    dev = data[first_break:second_break]
    test = data[second_break:]
    
    # write train files
    source_train = open(out+"/src_train", mode='w+', encoding='utf8')
    source_train.write('\n'.join([line[0] for line in train]))
    source_train.close()
    target_train = open(out+"/tgt_train", mode='w+', encoding='utf8')
    target_train.write('\n'.join([line[1] for line in train]))
    target_train.close()
    
   # write dev files
    source_dev = open(out+"/src_dev",mode='w+', encoding='utf8')
    source_dev.write('\n'.join([line[0] for line in dev]))
    source_dev.close()
    target_dev = open(out+"/tgt_dev",mode='w+', encoding='utf8')
    target_dev.write('\n'.join([line[1] for line in dev]))
    target_dev.close()
    
    # write test files
    source_test = open(out+"/src_test",mode='w+', encoding='utf8')
    source_test.write('\n'.join([line[0] for line in test]))
    source_test.close()
    target_test = open(out+"/tgt_test",mode='w+', encoding='utf8')
    target_test.write('\n'.join([line[1] for line in test]))
    target_test.close()