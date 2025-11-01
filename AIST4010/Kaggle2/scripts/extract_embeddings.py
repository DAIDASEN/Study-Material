#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import torch
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel

# ensure local src
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.dataset import chunk_sequence


def mean_pool(last_hidden_state: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
    # last_hidden_state: [C, L, H], attention_mask: [C, L]
    mask = attention_mask.unsqueeze(-1)  # [C, L, 1]
    summed = (last_hidden_state * mask).sum(dim=1)
    counts = mask.sum(dim=1).clamp_min(1)
    return summed / counts


def _select_layers(hidden_states, last_hidden_state, layers_spec: str):
    # layers_spec like "last,-2,-3,-4" or "-1,-2,-3,-4"
    selected = []
    tokens = [s.strip() for s in layers_spec.split(',') if s.strip()]
    for t in tokens:
        if t == 'last' or t == '-1':
            selected.append(last_hidden_state)
        else:
            try:
                idx = int(t)
                selected.append(hidden_states[idx])
            except Exception:
                # fallback to last
                selected.append(last_hidden_state)
    return selected


def extract_split(df: pd.DataFrame, tokenizer, model, max_len: int, stride: int, device: torch.device, layers: str) -> np.ndarray:
    feats = []
    model.eval()
    with torch.no_grad():
        for _, row in tqdm(df.iterrows(), total=len(df)):
            seq = row['seq']
            chunks = chunk_sequence(seq, max_len, stride)
            spaced = [" ".join(list(c)) for c in chunks]
            toks = tokenizer(spaced, return_tensors='pt', padding=True, truncation=True, add_special_tokens=True)
            input_ids = toks['input_ids'].to(device)
            attention_mask = toks['attention_mask'].to(device)
            with torch.autocast(device_type='cuda' if torch.cuda.is_available() else 'cpu', dtype=torch.float16 if torch.cuda.is_available() else torch.bfloat16):
                out = model(input_ids=input_ids, attention_mask=attention_mask, output_hidden_states=True)
                last = out.last_hidden_state  # [C, L, H]
                hiddens = out.hidden_states  # tuple(len=L+1): [C,L,H]
                reps = []
                for hs in _select_layers(hiddens, last, layers):
                    pooled_chunks = mean_pool(hs, attention_mask)  # [C, H]
                    reps.append(pooled_chunks.mean(dim=0))  # [H]
                rep = torch.cat(reps, dim=-1)
            feats.append(rep.float().cpu().numpy())
    return np.stack(feats, axis=0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data_dir', type=Path, default=Path('processed'))
    ap.add_argument('--model_name', type=str, default='hf_models/facebook__esm2_t33_650M_UR50D')
    ap.add_argument('--max_len', type=int, default=1022)
    ap.add_argument('--stride', type=int, default=512)
    ap.add_argument('--out_dir', type=Path, default=Path('features/esm2_t33'))
    ap.add_argument('--layers', type=str, default='last,-2,-3,-4', help='Comma list of layers to pool and concat, e.g., last,-2,-3,-4')
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(args.model_name, do_lower_case=False)
    model = AutoModel.from_pretrained(args.model_name)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    for split in ['train', 'val', 'test']:
        df = pd.read_csv(args.data_dir / f'{split}.csv')
        feats = extract_split(df, tokenizer, model, args.max_len, args.stride, device, args.layers)
        np.save(args.out_dir / f'{split}_feats.npy', feats)
        (args.out_dir / f'{split}_ids.csv').write_text('\n'.join(df['id'].astype(str).tolist()))
        if 'label' in df.columns:
            np.save(args.out_dir / f'{split}_labels.npy', df['label'].values)

    print(f"Saved features to {args.out_dir}")


if __name__ == '__main__':
    main()
