#!/usr/bin/env python3
"""Multilocus input for BPP from the pan-SINEome: the flanks of orthologous SINE insertions.

  select  --groups G.tsv.gz --n N --flank F --spacing S --seed 11 -o loci.tsv
          groups present as single unflagged copies in every genome (pattern all P); one locus per group = left flank
          + right flank of the copy (F bp each, SINE removed), loci at least S bp apart along the reference genome
          (default unm) and sampled at random (seeded)
  extract --loci loci.tsv --species SP --genome SP.fa >> flanks.fa
          the two flanks of every locus in genome SP, joined, in the copy's orientation (samtools faidx)
  build   --loci loci.tsv --fasta flanks.fa --imap MAP -o PREFIX [--exclude SP ...] [--min-id 85] [--max-n 0.2]
          MAFFT per locus, filters (any pair below --min-id % identity = paralog or misassignment; > --max-n missing),
          writes PREFIX.txt (BPP sequence file), PREFIX.Imap.txt, PREFIX.loci.tsv (kept loci and why others were dropped)
"""
import argparse, bisect, collections, csv, gzip, random, re, subprocess, sys, tempfile, os

CELL = re.compile(r'^(.+):(\d+)-(\d+)\(([+-])\)$')
RC = str.maketrans('ACGTNacgtn', 'TGCANtgcan')


def select(a):
    fh = gzip.open(a.groups, 'rt')
    h = fh.readline().rstrip('\n').split('\t')
    sp = h[h.index('flags') + 1:]
    cand = []
    for line in fh:
        r = dict(zip(h, line.rstrip('\n').split('\t')))
        if set(r['pattern']) != {'P'} or r['flags'] not in ('', '.'):
            continue
        cells = {s: CELL.match(r[s]) for s in sp}
        if any(m is None for m in cells.values()):
            continue
        cand.append((r['group'], {s: m.groups() for s, m in cells.items()}))
    rng = random.Random(a.seed)
    rng.shuffle(cand)
    taken = collections.defaultdict(list)          # reference chrom -> sorted positions
    out = []
    for g, c in cand:
        ch, s, e, st = c[a.reference]
        pos = int(s); lst = taken[ch]
        i = bisect.bisect_left(lst, pos)
        if (i < len(lst) and lst[i] - pos < a.spacing) or (i > 0 and pos - lst[i - 1] < a.spacing):
            continue
        lst.insert(i, pos); out.append((g, c))
        if len(out) == a.n:
            break
    with open(a.output, 'w') as fo:
        fo.write('locus\tgroup\t' + '\t'.join(sp) + '\n')
        for k, (g, c) in enumerate(out, 1):
            fo.write(f'L{k:05d}\t{g}\t' + '\t'.join('{}:{}-{}({})'.format(*c[s]) for s in sp) + '\n')
    print(f'{len(cand)} candidate groups (all P, unflagged, single copy); {len(out)} loci >= {a.spacing} bp apart on {a.reference}',
          file=sys.stderr)


def extract(a):
    rows = list(csv.DictReader(open(a.loci), delimiter='\t'))
    regs = []
    for r in rows:
        ch, s, e, st = CELL.match(r[a.species]).groups(); s, e = int(s), int(e)
        regs.append((r['locus'], ch, max(0, s - a.flank), s, e, e + a.flank, st))
    q = []
    for _, ch, l0, l1, r0, r1, _ in regs:
        q += [f'{ch}:{l0 + 1}-{l1}', f'{ch}:{r0 + 1}-{r1}']
    res = subprocess.run(['samtools', 'faidx', a.genome, '-r', '/dev/stdin'], input='\n'.join(q) + '\n',
                         capture_output=True, text=True, check=True).stdout
    seqs = []
    for line in res.splitlines():
        if line.startswith('>'): seqs.append([])
        else: seqs[-1].append(line)
    seqs = [''.join(x).upper() for x in seqs]
    for k, (loc, ch, l0, l1, r0, r1, st) in enumerate(regs):
        left, right = seqs[2 * k], seqs[2 * k + 1]
        s = left + right if st == '+' else (left + right).translate(RC)[::-1]
        sys.stdout.write(f'>{loc}|{a.species}\n{s}\n')


def ident(x, y):
    cols = [(p, q) for p, q in zip(x, y) if p in 'ACGT' and q in 'ACGT']
    return 100.0 * sum(p == q for p, q in cols) / len(cols) if cols else 0.0


def build(a):
    imap = dict(l.split() for l in open(a.imap) if l.strip())
    seqs = collections.defaultdict(dict)
    name = None
    for line in open(a.fasta):
        line = line.strip()
        if line.startswith('>'):
            loc, sp = line[1:].split('|'); name = (loc, sp); seqs[loc][sp] = ''
        elif name: seqs[name[0]][name[1]] += line
    kept, report = [], []
    with tempfile.TemporaryDirectory() as tmp:
        for loc in sorted(seqs):
            d = seqs[loc]
            d = {sp: x for sp, x in d.items() if sp not in a.exclude}
            if set(d) != set(imap) - set(a.exclude):
                report.append((loc, 'missing species')); continue
            if max(s.count('N') / max(len(s), 1) for s in d.values()) > a.max_n:
                report.append((loc, 'too many N')); continue
            f = os.path.join(tmp, 'l.fa')
            open(f, 'w').write(''.join(f'>{sp}\n{s}\n' for sp, s in d.items()))
            out = subprocess.run(['mafft', '--quiet', '--auto', f], capture_output=True, text=True, check=True).stdout
            aln, cur = {}, None
            for line in out.splitlines():
                if line.startswith('>'): cur = line[1:].strip(); aln[cur] = ''
                else: aln[cur] += line.strip().upper()
            sps = sorted(aln)
            low = min(ident(aln[x], aln[y]) for i, x in enumerate(sps) for y in sps[i + 1:])
            if low < a.min_id:
                report.append((loc, f'min pairwise identity {low:.1f}')); continue
            kept.append((loc, aln, low))
    with open(a.output + '.txt', 'w') as fo:
        for loc, aln, _ in kept:
            L = len(next(iter(aln.values())))
            fo.write(f'{len(aln)} {L}\n\n')
            for sp in sorted(aln):
                fo.write(f'^{sp}  {aln[sp].replace("N", "-")}\n')
            fo.write('\n')
    with open(a.output + '.Imap.txt', 'w') as fo:
        for sp in sorted(imap):
            if sp in a.exclude: continue
            fo.write(f'{sp}\t{imap[sp]}\n')
    with open(a.output + '.loci.tsv', 'w') as fo:
        fo.write('locus\tstatus\n')
        for loc, aln, low in kept: fo.write(f'{loc}\tkept (min identity {low:.1f})\n')
        for loc, why in report: fo.write(f'{loc}\tdropped: {why}\n')
    print(f'{len(kept)} loci kept, {len(report)} dropped: ' +
          ', '.join(f'{k} {v}' for k, v in collections.Counter(w.split(' ')[0] if not w.startswith('min') else 'low identity'
                                                               for _, w in report).items()), file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('select'); s.add_argument('--groups', required=True); s.add_argument('--n', type=int, default=500)
    s.add_argument('--spacing', type=int, default=200000); s.add_argument('--reference', default='unm')
    s.add_argument('--seed', type=int, default=11); s.add_argument('-o', '--output', required=True)
    e = sub.add_parser('extract'); e.add_argument('--loci', required=True); e.add_argument('--species', required=True)
    e.add_argument('--genome', required=True); e.add_argument('--flank', type=int, default=250)
    b = sub.add_parser('build'); b.add_argument('--loci', required=True); b.add_argument('--fasta', required=True)
    b.add_argument('--imap', required=True); b.add_argument('-o', '--output', required=True)
    b.add_argument('--exclude', nargs='*', default=[], help='genomes left out (e.g. arm, a hybrid, for MSC without introgression)')
    b.add_argument('--min-id', type=float, default=85); b.add_argument('--max-n', type=float, default=0.2)
    a = ap.parse_args()
    {'select': select, 'extract': extract, 'build': build}[a.cmd](a)


if __name__ == '__main__':
    main()
