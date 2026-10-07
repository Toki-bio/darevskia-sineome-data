#!/usr/bin/env python3
"""extract.py SAMPLE.tsv SPECIES GENOME.fa >> sample.fa : sequences of one species' sampled copies (strand-aware, samtools faidx)"""
import subprocess, sys
tsv, sp, genome = sys.argv[1:4]
rows = [l.rstrip('\n').split('\t') for l in open(tsv) if l.split('\t')[0] == sp]
for strand in '+-':
    sel = [r for r in rows if r[4] == strand]
    if not sel: continue
    regs = [f'{r[1]}:{int(r[2]) + 1}-{r[3]}' for r in sel]
    out = subprocess.run(['samtools', 'faidx', genome] + (['-i'] if strand == '-' else []) + ['-r', '/dev/stdin'],
                         input='\n'.join(regs) + '\n', capture_output=True, text=True, check=True).stdout
    seqs, cur = [], None
    for line in out.splitlines():
        if line.startswith('>'): seqs.append([]); continue
        seqs[-1].append(line)
    assert len(seqs) == len(sel), (sp, strand, len(seqs), len(sel))
    for r, s in zip(sel, seqs):
        sys.stdout.write(f'>{r[5]}\n{"".join(s)}\n')
