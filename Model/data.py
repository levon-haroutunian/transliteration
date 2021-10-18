# -*- coding: utf-8 -*-
"""
    Module for dataset class (TranslitDataset)
"""

from typing import Any, Callable, Iterable
import numpy as np
from vocab import Vocabulary

# type aliases
Datum = dict[str, Any]

# constants
ORIG = "original"
TRANSLIT = "transliteration"

class Dataset:
    def __init__(self, data: list[Datum], source_vocab: Vocabulary,
                 target_vocab: Vocabulary) -> None:
        self.data = data
           
    def data_to_tensors(self, index: int) -> dict[str, np.ndarray]:
        raise NotImplementedError

    def batch_tensors(self, start: int, end: int) -> dict[str, np.ndarray]:
        raise NotImplementedError

    def __getitem__(self, idx: int) -> Datum:
        return self.data[idx]

    def __len__(self) -> int:
        return len(self.data)
    
class TranslitDataset(Dataset):
    def __init__(self, source_data: list[str], source_vocab: Vocabulary,
                 translit_data: list[str] = None, translit_key: str = None, 
                 target_vocab: Vocabulary = None) -> None:
        
        if (not translit_data and not translit_key) or \
        (translit_data and translit_key):
            raise Exception("ERROR: Must include either transliterated \
                            data OR a transliteration key.")
        
        if translit_key:
            # TODO: make translit vocab
            # TODO: make translit object
            pass
        
        if not translit_data:
            # TODO: use translit object to translit each sentence
            translit_data = None
            
            
        # create list[Datum] using source and translit data
        data = []
        
        for i in range(len(source_data)):
            data.append({ORIG: source_data[i], 
                            TRANSLIT: translit_data[i]})

        
        super(TranslitDataset, self).__init__(data, source_vocab,
                                              target_vocab)
      
        
    def translit_line(self):
         pass
        
    # TODO
    @classmethod
    def from_files(cls, source_dir: str, target_dir: str, 
                   delim: Iterable = None, vocab: Vocabulary = None):
        data = None
        return cls(data, vocab)