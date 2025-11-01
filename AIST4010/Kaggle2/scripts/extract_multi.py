#!/usr/bin/env python3
"""
Launch parallel embedding extraction jobs for multiple backbone models,
pinning each job to a specific GPU.

Usage example:
  python scripts/extract_multi.py \
    --data_dir processed \
    --tasks \
      model=hf_models/facebook__esm2_t30_150M_UR50D,out=features/esm2_t30,layers=last,-2,-3,-4,gpu=3 \
      model=Rostlab/prot_bert_bfd,out=features/protbert_bfd,layers=last,-2,-3,-4,gpu=4 \
    --max_len 1022 --stride 512
"""
import argparse
import os
import shlex
import subprocess
from pathlib import Path


def parse_task(s: str):
    # format: key=value comma-separated
    parts = s.split(',')
    d = {}
    for p in parts:
        if '=' in p:
            k, v = p.split('=', 1)
            d[k.strip()] = v.strip()
    required = ['model', 'out', 'layers', 'gpu']
    for r in required:
        if r not in d:
            raise ValueError(f"Missing '{r}' in task: {s}")
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data_dir', type=Path, default=Path('processed'))
    ap.add_argument('--tasks', nargs='+', required=True,
                    help='Tasks like model=...,out=...,layers=...,gpu=IDX')
    ap.add_argument('--max_len', type=int, default=1022)
    ap.add_argument('--stride', type=int, default=512)
    args = ap.parse_args()

    procs = []
    for t in args.tasks:
        cfg = parse_task(t)
        env = os.environ.copy()
        env['CUDA_VISIBLE_DEVICES'] = cfg['gpu']
        cmd = [
            'python', 'scripts/extract_embeddings.py',
            '--data_dir', str(args.data_dir),
            '--model_name', cfg['model'],
            '--max_len', str(args.max_len),
            '--stride', str(args.stride),
            '--out_dir', cfg['out'],
            '--layers', cfg['layers'],
        ]
        print('LAUNCH:', ' '.join(shlex.quote(c) for c in cmd), 'on GPU', cfg['gpu'])
        proc = subprocess.Popen(cmd, env=env)
        procs.append(proc)

    # wait all
    code = 0
    for p in procs:
        rc = p.wait()
        if rc != 0:
            code = rc
    raise SystemExit(code)


if __name__ == '__main__':
    main()
