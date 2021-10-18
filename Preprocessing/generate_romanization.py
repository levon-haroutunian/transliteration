"""
    Script for generating artificially romanized data using 
    handwritten romanization template.
    
"""

import re, random, argparse, glob
import numpy as np
from pathlib import Path

# constants
NULL = "<null>"
END = "<END>"

# type aliases
trans_prob = tuple[list[str], list[float]]

# regex utilities
re_char_file = re.compile(r"(.*) --- (.*);\s*(.*)?")
re_comment_line = re.compile(r"^#")

class Romanizer:
    
    def __init__(self, char_probs: dict[str, trans_prob],
                 encoding: str = 'utf8'):
        """
        Object for generating artificially Romanized text using 
        handwritten transliteration rules and probabilities

        Parameters
        ----------
        char_probs : dict[str, trans_prob]
            keys are characters in original orthography
            (lowercase only, including punctuation if relevant)
            values are [Romanization candidates], [probabilities],
            where probabilities are cumulative
        encoding : str, optional
            default is 'utf8'.

        """
        self.char_probs = char_probs
        self.encoding = encoding
        
        # add uppercase letters to char_probs
        lowercase_chars = list(char_probs.keys())
        for char in lowercase_chars:
            if char.isalpha():
                self.char_probs[char.capitalize()] = tuple(
                    [[item.capitalize() if item != NULL else NULL 
                      for item in self.char_probs[char][0]], 
                      self.char_probs[char][1]])
                # for long characters, need to add both sentence-capitalized
                # and full-capitalized versions
                if len(char) > 1:
                    self.char_probs[char.upper()] = tuple(
                        [[item.upper() if item != NULL else NULL
                          for item in self.char_probs[char][0]], 
                         self.char_probs[char][1]])
        
        # find long chars, construct trie
        long_chars_list = []
        
        for char in self.char_probs.keys():
            if len(char) > 1:
                long_chars_list.append(char)
                
        self.long_chars = {}
        for lc in long_chars_list:
            curr = self.long_chars
            for i in range(len(lc)):
                if lc[i] not in curr:
                    curr[lc[i]] = {}
                    
                curr = curr[lc[i]]
                
                if i == len(lc) - 1:
                    curr[END] = lc
                
        
    def get_trans_char(self, char: str) -> str:
        if char == NULL:
            return('')
        
        elif char in self.char_probs:
            return(random.choices(self.char_probs[char][0], 
                                  cum_weights=self.char_probs[char][1])[0])
        else:
            return(char)
    
    def segment_str(self, string: str) -> list:
        """
        Converts string to a list, treating all the items in long_chars
        as single characters.

        """
        segments = []
        
        i = 0
        while i < len(string):
            if string[i] not in self.long_chars:
                segments.append(string[i])
                i += 1
             
            # accounts for multi-char "characters"
            else:
                candidates = []
                curr = self.long_chars[string[i]]
                j = i + 1
                while j < len(string) and string[j] in curr:
                    curr = curr[string[j]]
                    j += 1
                    if END in curr:
                        candidates.append(curr[END])
                        
                if len(candidates) == 0:
                    segments.append(string[i])
                    i += 1
                    
                else:
                    segments.append(candidates.pop())
                    i += len(segments[-1])
                    
                    
        return(segments)
                        
                
    
    def get_trans_str(self, string: str) -> str:
        result = ""
        
        sequence = self.segment_str(string)
        
        for char in sequence:
            result += self.get_trans_char(char)
            
        return(result)
    
    def romanize_file(self, in_file: str, out_file: str) -> None:
        orig_lines = open(in_file, encoding=self.encoding).readlines()
        
        with open(out_file, mode="w+", encoding=self.encoding) as file:
            for line in orig_lines:
                file.write(self.get_trans_str(line))
    
    # TODO: add any_possible option
    @classmethod
    def from_file(cls, rom_file: str, prop_typical: float = 0.9,
                  encoding: str = 'utf8',
                  # any_possible: bool = False
                  ):
        """
        Creates a Romanizer object from a .txt file containing
        a Romanization key

        Parameters
        ----------
        rom_file : str, file name for romanization key -- 
                see hye_translit_key for formatting
        prop_typical: float, amount of probability weight assigned to more
                probable transliterations; default 0.9

        """
        lines = open(rom_file, encoding=encoding).readlines()
        char_probs = {}
        
        for l in lines:
            if re_comment_line.search(l) == None:
                # strip whitespace
                l = l.strip()
                
                match = re_char_file.search(l)
                
                if match:
                    orig, most_prob_str, less_prob_str = match.groups()
                    
                    # make char list starting with most common
                    chars = [item.strip() for item in 
                            most_prob_str.split(sep=",")]
                    
                    # make prob list (cumulative weight distribution)
                    # if no less prob options, assign all weight to most prob
                    if less_prob_str == '':
                        probs = list(np.linspace(
                            0, 1, num=len(chars)+1)[1:])
                        
                    else:
                        probs = list(np.linspace(
                            0,prop_typical, num=len(chars)+1)[1:])
                        
                        # add less common chars
                        less_common = [item.strip() for item in
                                      less_prob_str.split(sep=",")]
                        chars.extend(less_common)
                        
                        probs.extend(np.linspace(
                            prop_typical, 1,num=len(less_common)+1)[1:])
                        
                    # add character and candidate transliterations to table    
                    char_probs[orig] = tuple([chars, probs])
                    
        return(Romanizer(char_probs, encoding=encoding))
                        
                    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", 
                        help="name of .txt file containing Romanization key",
                        type=str)
    parser.add_argument("--in_dir", help="name of input directory",
                        type=str)
    parser.add_argument("--out_dir", help="name of output directory",
                        default='romanized', type = str)
    parser.add_argument("--prop_typical", type=float, default=0.9, help=
                        "amount of probability assigned to most common\
                            Romanization options for each char")
    parser.add_argument("--encoding", type=str, default='utf8',
                        help="document encoding")
    
    args = parser.parse_args()
    
    # writing over existing files is not allowed        
    if Path(args.out_dir).is_dir():
        raise Exception(
            f"Choose a different directory name or delete existing \
                directory {args.out_dir}.")
        
    # build Romanization object
    romanizer = Romanizer.from_file(args.key, args.prop_typical, 
                                    encoding = args.encoding)
    
    # iterate through files and create parallel substructure
    re_in_dir = re.compile(r'{}(.*)'.format(args.in_dir))
    for file in glob.iglob(args.in_dir + "/**", recursive=True):
        new_file = args.out_dir + '/' + re_in_dir.search(file).group(1)
        orig_path = Path(file)
        new_path = Path(new_file)
        
        # create corresponding subdirectories
        if orig_path.is_dir():
            new_path.mkdir()
            
        else:
            # romanize file
            romanizer.romanize_file(file, new_file)
    
    