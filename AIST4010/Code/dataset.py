import torch
from torch.utils.data import Dataset
import numpy as np
import nibabel as nib
import pandas as pd
import os

class IADataset(Dataset):
    def __init__(self, metadata_csv, root_dir, transform=None):
        """
        Args:
            metadata_csv (str): Path to CSV with columns ['filename', 'label_global', 'label_l_ica', ...]
            root_dir (str): Directory with .nii.gz ROI crops
        """
        self.df = pd.read_csv(metadata_csv)
        self.root_dir = root_dir
        self.transform = transform
        
        # Columns 1 to 14 contain the labels
        self.label_cols = self.df.columns[1:] 

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        filename = row['filename']
        filepath = os.path.join(self.root_dir, filename)

        # Load NIfTI
        nii = nib.load(filepath)
        img = nii.get_fdata().astype(np.float32)

        # Normalization (Z-score)
        if np.std(img) > 0:
            img = (img - np.mean(img)) / np.std(img)
        
        # Add channel dimension: (D, H, W) -> (1, D, H, W)
        img_tensor = torch.from_numpy(img).unsqueeze(0)

        # Get labels
        labels = row[self.label_cols].values.astype(np.float32)
        labels_tensor = torch.from_numpy(labels)

        return img_tensor, labels_tensor