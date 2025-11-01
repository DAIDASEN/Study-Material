from dataclasses import dataclass
from typing import List, Dict, Optional

import torch
from torch.utils.data import Dataset


@dataclass
class SequenceExample:
	id: str
	seq: str
	label: Optional[int] = None


def chunk_sequence(seq: str, k: int, stride: int) -> List[str]:
	chunks = []
	if len(seq) <= k:
		return [seq]
	i = 0
	while i < len(seq):
		chunks.append(seq[i:i + k])
		if i + k >= len(seq):
			break
		i += stride
	return chunks


class FastaCSVDataset(Dataset):
	def __init__(self, rows: List[Dict], tokenizer, max_len: int = 1022, stride: int = 512, is_train: bool = True):
		self.examples = [SequenceExample(r['id'], r['seq'], r.get('label')) for r in rows]
		self.tokenizer = tokenizer
		self.max_len = max_len
		self.stride = stride
		self.is_train = is_train


	def __len__(self):
		return len(self.examples)


	def __getitem__(self, idx):
		ex = self.examples[idx]
		chunks = chunk_sequence(ex.seq, self.max_len, self.stride)
		# ESM tokenizer通常按空格分隔单氨基酸token
		spaced = [" ".join(list(c)) for c in chunks]
		toks = self.tokenizer(spaced, return_tensors='pt', padding=True, truncation=True, add_special_tokens=True)
		item = {
			'input_ids': toks['input_ids'],  # [C, L]
			'attention_mask': toks['attention_mask'],
			'n_chunks': toks['input_ids'].shape[0],
			'id': ex.id,
		}
		if ex.label is not None:
			item['labels'] = torch.tensor(ex.label, dtype=torch.long)
		return item


def collate_fn(batch):
	# batch is a list of dicts where each value is per-sample tensors
	# We keep chunks per sample; model will handle chunk aggregation.
	return batch
