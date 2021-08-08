"""
    Module for Vocabulary class
"""
from typing import Iterable
from collections import Counter
from pathlib import Path

# constants
UNK = "<UNK>"
BOS = "<BOS>"
EOS = "<EOS>"

class Vocabulary:
    def __init__(self, tokens: Counter[str, int], 
                 specials: list = [], min_freq: int = 1) -> None:
        """
        Builds a Vocabulary object using a Counter of token: count entries.

        Parameters
        ----------
        tokens : Counter[str, int]
            gives all tokens by frequency
        specials : list, optional
            special characters (eg <eos>) if relevant, 
            <UNK> always included
        min_freq: int, default = 1
            minimum frequency a token must have to be included

        """
        
        self.specials = specials + [UNK]
        
        self.tokens = tokens
        
        self.index_to_token = []
        
        # special tokens first; ensure that they aren't double counted
        self.index_to_token.extend(specials)
        
        for s in specials:
            del self.tokens[s]
            
        for t in self.tokens.keys():
            if self.tokens[t] >= min_freq:
                self.index_to_token.append(t)
        
        self.token_to_index = {self.index_to_token[i]: i for 
                               i in range(len(self.index_to_token))}
    
    def __len__(self) -> int:
        """
        Returns length of vocabulary

        """
        return len(self.index_to_token)
    
    def __getindex__(self, token: str) -> int:
        """
        Returns index of a token, or index of UNK

        """
        if token in self.token_to_index:
            return(self.token_to_index[token])
        else:
            return(self.token_to_index[UNK])
        
    def tokens_to_indices(self, tokens: list[str]) -> list[int]:
        """
        Given a list of tokens in the vocabulary, returns a list of 
        corresponding indices

        """
        return([self.__getindex__(t) for t in tokens])
    
    @classmethod
    def chars_from_files(cls, files: Iterable[str], 
                         enc: str = "utf8", **kwargs):
        """
        Builds a character-level vocabulary from a list of files.
        Returns a Vocabulary object

        """
        
        tokens = Counter()
        
        for f in files:
            if Path(f).is_file():
                with open(f, "r", encoding=enc) as file:
                    for line in file.readlines():
                        chars = list(line.strip("\n"))
                        tokens.update(chars)
                        
        return(cls(tokens, **kwargs))