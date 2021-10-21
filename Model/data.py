"""
    Module for dataset objects RomanizationDataset and
    RomanizationDataLoader, which inherit from corresponding
    torch classes
"""

import torch

from torch.utils.data import DataLoader, Dataset
from torch import Tensor
from typing import Any, Callable, Iterable

from vocab import Vocabulary

# type aliases
Datum = list[list, list]

# constants
PAD = "<PAD>"

class RomanizationDataset(Dataset):
    def __init__(self, data: list[Datum], source_vocab: Vocabulary,
                 target_vocab: Vocabulary) -> None:
        super().__init__()
        self.data = data
        self.src_vocab = source_vocab
        self.tgt_vocab = target_vocab
        
    def __getitem__(self, index) -> Datum:
        return(self.data[index])
    
    def __len__(self) -> int:
        return(len(self.data))
        
    @classmethod
    def from_files(cls, src_files: list[str], tgt_files: list[str], 
                   min_freq: int = 1, encoding: str = 'utf8'):
        # make source and target vocab objects
        src_vocab = Vocabulary.from_files(src_files, specials = [PAD],
                                          min_freq = min_freq)
        tgt_vocab = Vocabulary.from_files(tgt_files, specials = [PAD],
                                          min_freq = min_freq)
        
        # convert files to list of indices
        data: list[Datum] = []
        for i in range(len(src_files)):
            src_lines = open(src_files[i], encoding=encoding).readlines()
            tgt_lines = open(tgt_files[i], encoding=encoding).readlines()
            
            for j in range(len(src_lines)):
                # make lists of chars
                src = list(''.join(src_lines[j].split()))
                tgt = list(''.join(tgt_lines[j].split()))
                
                data.append([src_vocab.tokens_to_indices(src), 
                             tgt_vocab.tokens_to_indices(tgt)])
                
        return RomanizationDataset(data, src_vocab, tgt_vocab)  
    
class RomanizationDataLoader(DataLoader):
    def __init__(self, data: RomanizationDataset, batch_size: int = 256, **kwargs):
        self.dataset = data
        super().__init__(self.dataset, batch_size = batch_size,
                         shuffle=True, collate_fn = self.pad_batches,
                         **kwargs)
    
    @classmethod
    def pad_batches(cls, samples):
        # pad index must be 0
        x = [s[0] for s in samples]
        y = [s[1] for s in samples]
        
        max_x_len = max([len(s) for s in x])
        max_y_len = max([len(s) for s in y])
    
        for s in x:
            while len(s) < max_x_len:
                s.append(0)
                
        for s in y:
            while len(s) < max_y_len:
                s.append(0)
                
        return Tensor(x), Tensor(y)
    
    @classmethod
    def from_files(cls, src_files: list[str], tgt_files: list[str],
                    min_freq: int = 1, **kwargs):       
         dataset = RomanizationDataset.from_files(src_files, tgt_files,
                                                  min_freq=min_freq)
         return RomanizationDataLoader(data=dataset, **kwargs)
        
    