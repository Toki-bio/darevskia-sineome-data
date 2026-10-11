#!/usr/bin/env python3
"""Within-genome status of copies (fs9) against dar8's multicopy groups of one genome.

usage: compare_dar8.py --groups dar8.groups.tsv.gz --sp nai --bed copies.named.bed --status DIR/copy_status.tsv
                       --pairs DIR/flank_groups.tsv --dup DUP/dupregion.copies -o OUT.tsv
For every dar8 group whose cell for SP lists >= 2 copies (flag multicopy:SP), each copy is matched to an annotated copy
(overlap) and the group is classified:
  twin_pair     two of its copies are fs9 twins of each other (tier 1 or 2; array pairs reported as array_pair)
  twin_other    a copy is a twin, but not of another copy in the group
  dup_region    no twin, but a copy's flank maps elsewhere in the genome (fs9_dupregion)
  untestable    no twin/dup-region and a copy is masked/untestable
  unexplained   all copies unique and no duplicated flank
Prints a summary for all multicopy groups, and separately for those with copies on two different contigs.
"""
import argparse, bisect, collections, csv, gzip, re

CELL = re.compile(r'^(.+):(\d+)-(\d+)\(([+-])\)$')
ap = argparse.ArgumentParser()
for k in ('groups', 'sp', 'bed', 'status', 'pairs', 'dup'): ap.add_argument('--' + k, required=True)
ap.add_argument('-o', '--output', required=True)
a = ap.parse_args()
idx = collections.defaultdict(list)
for l in open(a.bed):
    f = l.rstrip('\n').split('\t'); idx[f[0]].append((int(f[1]), int(f[2]), f[3]))
for v in idx.values(): v.sort()
starts = {k: [x[0] for x in v] for k, v in idx.items()}
def copy_at(ch, s, e):
    v = idx.get(ch, []); i = bisect.bisect_left(starts.get(ch, []), s - 1000); best = None; bo = 0
    while i < len(v) and v[i][0] < e + 50:
        o = min(e, v[i][1]) - max(s, v[i][0])
        if o > bo: bo, best = o, v[i][2]
        i += 1
    return best
st = {r[0]: r[1] for r in csv.reader(open(a.status), delimiter='\t')}
pair = {}
with open(a.pairs) as fh:
    next(fh)
    for l in fh:
        f = l.rstrip('\n').split('\t'); pair[frozenset((f[0], f[1]))] = f[6]
dup = {l.strip() for l in open(a.dup) if l.strip()}
fh = gzip.open(a.groups, 'rt'); h = fh.readline().rstrip('\n').split('\t')
summ = collections.Counter(); summ2 = collections.Counter()
with open(a.output, 'w') as out:
    out.write('group\tclass\tcontigs\tcopies\tstatuses\n')
    for line in fh:
        r = dict(zip(h, line.rstrip('\n').split('\t')))
        if f'multicopy:{a.sp}' not in r['flags']: continue
        cells = [CELL.match(c) for c in r[a.sp].split(',') if CELL.match(c)]
        if len(cells) < 2: continue
        cps = [copy_at(m.group(1), int(m.group(2)), int(m.group(3))) for m in cells]
        cps = [c for c in cps if c]
        nctg = len({m.group(1) for m in cells})
        sts = [st.get(c, 'none') for c in cps]
        cls = 'unexplained'
        pk = [pair.get(frozenset((x, y))) for i, x in enumerate(cps) for y in cps[i + 1:] if x != y]
        if 'twin' in pk: cls = 'twin_pair'
        elif 'array' in pk: cls = 'array_pair'
        elif any(s.startswith('twin') for s in sts): cls = 'twin_other'
        elif any(c in dup for c in cps): cls = 'dup_region'
        elif any(s in ('masked', 'untestable') for s in sts): cls = 'untestable'
        elif len(cps) < 2: cls = 'copy_not_annotated'
        summ[cls] += 1
        if nctg > 1: summ2[cls] += 1
        out.write(f"{r['group']}\t{cls}\t{nctg}\t{','.join(cps)}\t{','.join(sts)}\n")
for name, s in (('all multicopy groups', summ), ('copies on >= 2 contigs', summ2)):
    t = sum(s.values()); print(f'{name}: {t}')
    for k, v in s.most_common(): print(f'  {k}\t{v}\t{100 * v / t:.1f}%')
