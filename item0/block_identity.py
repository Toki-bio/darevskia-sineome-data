#!/usr/bin/env python3
"""Identity of duplicated blocks: for every contig pair that carries >= MIN twin pairs (fs9 flank_groups.tsv, class twin),
align the two contigs with minimap2 (-x asm20, one pair at a time) and report the aligned blocks.

usage: block_identity.py --genome G.fa --pairs flank_groups.tsv --min 5 --threads 4 -o PREFIX
writes PREFIX.pairs.tsv  contig_a contig_b len_a len_b twin_pairs aligned_bp(a) frac_a frac_b identity(blast-like) longest_block
       PREFIX.summary.txt   distribution of block identity weighted by aligned bp
"""
import argparse, collections, os, subprocess, tempfile, concurrent.futures as cf

ap = argparse.ArgumentParser()
ap.add_argument('--genome', required=True); ap.add_argument('--pairs', required=True)
ap.add_argument('--min', type=int, default=5); ap.add_argument('--threads', type=int, default=4)
ap.add_argument('--max-pairs', type=int, default=3000); ap.add_argument('--bed', help='copies BED (name -> contig); default: contig from chrom:start-end names'); ap.add_argument('-o', '--output', required=True)
a = ap.parse_args()
size = {l.split('\t')[0]: int(l.split('\t')[1]) for l in open(a.genome + '.fai')}
chrom_of = {l.split('\t')[3]: l.split('\t')[0] for l in open(a.bed)} if a.bed else {}
cnt = collections.Counter()
with open(a.pairs) as fh:
    next(fh)
    seen = set()
    for l in fh:
        f = l.rstrip('\n').split('\t')
        if f[6] != 'twin' or (f[0], f[1]) in seen: continue
        seen.add((f[0], f[1]))
        ca, cb = (chrom_of.get(x) or x.rsplit(':', 1)[0] for x in (f[0], f[1]))
        if ca != cb: cnt[tuple(sorted((ca, cb)))] += 1
todo = [(k, v) for k, v in cnt.most_common() if v >= a.min][:a.max_pairs]
tmp = tempfile.mkdtemp()

def run(job):
    k, ((ca, cb), n) = job
    fa, fb = os.path.join(tmp, f'{k}_a.fa'), os.path.join(tmp, f'{k}_b.fa')   # one pair per file name: a contig can be in several pairs at once
    subprocess.run(f'samtools faidx {a.genome} {ca} > {fa}; samtools faidx {a.genome} {cb} > {fb}', shell=True, check=True)
    out = subprocess.run(['minimap2', '-c', '-x', 'asm20', '-t', '1', '--secondary=no', fa, fb], capture_output=True, text=True).stdout
    os.remove(fa); os.remove(fb)
    al = mt = 0; longest = 0; ivs_a = []; ivs_b = []
    for line in out.splitlines():
        f = line.split('\t')
        if int(f[11]) < 1: continue                   # MAPQ 0: repeat-driven
        m, L = int(f[9]), int(f[10]); mt += m; al += L; longest = max(longest, L)
        ivs_b.append((int(f[2]), int(f[3]))); ivs_a.append((int(f[7]), int(f[8])))
    def cover(iv):
        iv.sort(); tot = 0; s = e = -1
        for x, y in iv:
            if x > e: tot += max(0, e - s); s, e = x, y
            else: e = max(e, y)
        return tot + max(0, e - s)
    ca_cov, cb_cov = cover(ivs_a), cover(ivs_b)
    return (ca, cb, size[ca], size[cb], n, ca_cov, ca_cov / size[ca], cb_cov / size[cb], 100.0 * mt / al if al else 0.0, longest, al)

with cf.ThreadPoolExecutor(a.threads) as ex: res = list(ex.map(run, enumerate(todo)))
with open(a.output + '.pairs.tsv', 'w') as fo:
    fo.write('contig_a\tcontig_b\tlen_a\tlen_b\ttwin_pairs\taligned_a\tfrac_a\tfrac_b\tidentity\tlongest_block\n')
    for r in res: fo.write('\t'.join([r[0], r[1], str(r[2]), str(r[3]), str(r[4]), str(r[5]), f'{r[6]:.3f}', f'{r[7]:.3f}', f'{r[8]:.2f}', str(r[9])]) + '\n')
bins = [(99.5, 101), (99, 99.5), (98, 99), (97, 98), (95, 97), (90, 95), (0, 90)]
w = collections.Counter(); tot = sum(r[10] for r in res)
for r in res:
    for lo, hi in bins:
        if lo <= r[8] < hi: w[(lo, hi)] += r[10]
with open(a.output + '.summary.txt', 'w') as fo:
    fo.write(f'contig pairs with >= {a.min} twin pairs: {len(todo)} (of {len(cnt)} cross-contig pairs); aligned {tot / 1e6:.2f} Mb\n')
    fo.write('block identity (alignment-length weighted, matches / alignment columns):\n')
    for lo, hi in bins: fo.write(f'  {lo}-{min(hi, 100)} %: {100 * w[(lo, hi)] / tot if tot else 0:.1f} % of aligned bp\n')
    fr = sorted(r[6] for r in res)
    if fr: fo.write(f'median fraction of contig a aligned to its partner: {fr[len(fr) // 2]:.2f}\n')
print(open(a.output + '.summary.txt').read())
