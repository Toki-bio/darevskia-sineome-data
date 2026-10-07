#!/usr/bin/env python3
"""Per-chunk table of a SubFam run.

SubFam (github.com/Toki-bio/SubFam) sorts the input copies with MAFFT, cuts them into batches (<prefix>_NNN.bnk),
builds one consensus per batch (<prefix>_NNN.bnk.cons) and aligns the consensi (<prefix>.msf). This script reports per
batch: the number of copies of each species (the part of the copy name before the first '_'; '|' in names makes EMBOSS cons hang), the identity of every copy and of
the batch consensus to each reference consensus (EMBOSS needle, gaps excluded from the denominator), and the position
of the batch in the final alignment.

usage: chunk_table.py --dir RUN_DIR --prefix PREFIX --ref REF.fa [--label-field 2] -o chunks.tsv
  --label-field K: also count the K-th '_' field of copy names (e.g. the true subfamily in a simulation)
writes chunks.tsv and copies.tsv (copy, chunk, best reference, identity)
"""
import argparse, collections, glob, os, re, subprocess, tempfile

def fasta(path):
    name, seq = None, []
    for line in open(path):
        line = line.rstrip()
        if line.startswith('>'):
            if name is not None: yield name, ''.join(seq)
            name, seq = line[1:].split()[0], []
        elif name is not None: seq.append(line)
    if name is not None: yield name, ''.join(seq)

def needle_identity(ref_seq, query_fa, tmp):
    """identity (%) of every query to ref: identical columns / aligned columns without gaps in either sequence"""
    rf = os.path.join(tmp, 'ref.fa'); open(rf, 'w').write('>ref\n' + ref_seq + '\n')
    out = os.path.join(tmp, 'needle.txt')
    subprocess.run(['needle', '-asequence', rf, '-bsequence', query_fa, '-gapopen', '10', '-gapextend', '0.5',
                    '-aformat3', 'fasta', '-outfile', out, '-auto'], check=True)
    res, recs = {}, list(fasta(out))
    for i in range(0, len(recs), 2):
        a, b = recs[i][1].upper(), recs[i + 1][1].upper()
        cols = [(x, y) for x, y in zip(a, b) if x != '-' and y != '-']
        res[recs[i + 1][0]] = 100.0 * sum(x == y for x, y in cols) / len(cols) if cols else 0.0
    return res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', required=True); ap.add_argument('--prefix', required=True)
    ap.add_argument('--ref', required=True); ap.add_argument('--label-field', type=int, default=0)
    ap.add_argument('-o', '--output', required=True)
    a = ap.parse_args()
    refs = list(fasta(a.ref))
    bnks = sorted(glob.glob(os.path.join(a.dir, f'{a.prefix}_*.bnk')))
    order = {}
    msf = os.path.join(a.dir, f'{a.prefix}.msf')
    if os.path.exists(msf):
        for line in open(msf):
            m = re.match(r'\s*Name:\s+(\S+)', line)
            if m: order.setdefault(m.group(1), len(order) + 1)
    with tempfile.TemporaryDirectory() as tmp:
        allc = os.path.join(tmp, 'copies.fa'); member = {}; alias = {}
        with open(allc, 'w') as fh:     # needle rewrites names with ':' or '(': write index names, map back
            for b in bnks:
                chunk = os.path.basename(b)
                for n, s in fasta(b):
                    member[n] = chunk; alias[f'c{len(alias)}'] = n; fh.write(f'>c{len(alias) - 1}\n{s.replace("-", "")}\n')
        cons = os.path.join(tmp, 'cons.fa')
        with open(cons, 'w') as fh:
            for b in bnks:
                for n, s in fasta(b + '.cons'):
                    fh.write(f'>{os.path.basename(b)}\n{s.replace("-", "")}\n')
        ident_copy = {r: {alias[k]: v for k, v in needle_identity(s, allc, tmp).items()} for r, s in refs}
        ident_cons = {r: needle_identity(s, cons, tmp) for r, s in refs}
    species = sorted({n.split('_')[0] for n in member})
    labels = sorted({n.split('_')[a.label_field - 1] for n in member}) if a.label_field else []
    rnames = [r for r, _ in refs]
    with open(os.path.splitext(a.output)[0] + '.copies.tsv', 'w') as out:
        out.write('copy\tchunk\tbest_ref\tidentity\n')
        for n, c in member.items():
            r = max(rnames, key=lambda r: ident_copy[r].get(n, 0))
            out.write(f'{n}\t{c}\t{r}\t{ident_copy[r].get(n, 0):.1f}\n')
    with open(a.output, 'w') as out:
        out.write('\t'.join(['chunk', 'msf_order', 'n'] + species + [f'label:{l}' for l in labels] +
                            ['cons_length', 'cons_best_ref', 'cons_identity'] + [f'median_copy_identity:{r}' for r in rnames]) + '\n')
        for b in bnks:
            chunk = os.path.basename(b)
            mem = [n for n, c in member.items() if c == chunk]
            sp = collections.Counter(n.split('_')[0] for n in mem)
            lab = collections.Counter(n.split('_')[a.label_field - 1] for n in mem) if a.label_field else {}
            cseq = ''.join(s for _, s in fasta(b + '.cons')).replace('-', '')
            best = max(rnames, key=lambda r: ident_cons[r].get(chunk, 0))
            med = []
            for r in rnames:
                v = sorted(ident_copy[r].get(n, 0) for n in mem)
                med.append(f'{v[len(v) // 2]:.1f}' if v else '')
            out.write('\t'.join([chunk, str(order.get(chunk, '')), str(len(mem))] + [str(sp[s]) for s in species] +
                                [str(lab[l]) for l in labels] + [str(len(cseq)), best, f'{ident_cons[best].get(chunk, 0):.1f}'] + med) + '\n')

if __name__ == '__main__':
    main()
