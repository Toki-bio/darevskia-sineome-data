#!/usr/bin/env python3
"""Stratified random sample of annotated copies: the same number from each assembly (seeded, exact counts).

usage: sample_copies.py --total 30000 --seed 11 --bed dva=dva.bed.gz ... -o sample.tsv
writes species, chrom, start (0-based), end, strand, name; name = <species>_<chrom>:<start>-<end>(<strand>)
(bedtools getfasta style coordinates; '_' separates the species: '|' in names makes EMBOSS cons hang)
"""
import argparse, gzip, random

ap = argparse.ArgumentParser()
ap.add_argument('--total', type=int, required=True); ap.add_argument('--seed', type=int, default=11)
ap.add_argument('--bed', nargs='+', required=True, metavar='SP=BED'); ap.add_argument('-o', '--output', required=True)
a = ap.parse_args()
beds = [b.split('=', 1) for b in a.bed]
k = len(beds); base, extra = divmod(a.total, k)
rng = random.Random(a.seed)
with open(a.output, 'w') as out:
    for i, (sp, path) in enumerate(beds):
        op = gzip.open if path.endswith('.gz') else open
        rows = [l.rstrip('\n').split('\t') for l in op(path, 'rt') if l.strip()]
        n = base + (1 if i < extra else 0)
        for f in sorted(rng.sample(rows, n), key=lambda f: (f[0], int(f[1]))):
            strand = f[5] if len(f) > 5 else '+'
            out.write(f'{sp}\t{f[0]}\t{f[1]}\t{f[2]}\t{strand}\t{sp}_{f[0]}:{f[1]}-{f[2]}({strand})\n')
        print(f'{sp}: {n} of {len(rows)} copies')
