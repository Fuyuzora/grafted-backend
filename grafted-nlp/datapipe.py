from torch.utils.data import DataLoader, Dataset, random_split
import pandas as pd
from transformers import AutoTokenizer

class _CDataset(Dataset):
    def __init__(self, file_path, data_col, label_col):
        self.df = pd.read_csv(file_path)
        self.data_col = data_col
        self.label_col = label_col
    
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, index):
        super().__getitem__(index)
        return self.df.iloc[index, self.df.columns.get_loc(self.data_col)], self.df.iloc[index, self.df.columns.get_loc(self.label_col)]



class DataPipe():
    def __init__(self, file_path, data_col, label_col, tokenizer_type, batch_size=64, shuffle=True):
        self.file_path = file_path
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_type)
        datasets = _CDataset(file_path, data_col, label_col).map(tokenizer, batched=True)
        self.train_set, self.test_set, self.val_set = random_split(datasets, [6, 2, 2])
        self.train_loader = DataLoader(self.train_set, batch_size=batch_size, shuffle=shuffle)
        self.test_loader = DataLoader(self.test_set, batch_size=batch_size, shuffle=shuffle)
        self.val_loader = DataLoader(self.val_set, batch_size=batch_size, shuffle=shuffle)
        return self.train_loader, self.test_loader, self.val_loader