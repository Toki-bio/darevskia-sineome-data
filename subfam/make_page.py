#!/usr/bin/env python3
"""HTML page of a SubFam run on a multi-genome sample, for manual peeling (style of the Tal SINE reports).

usage: make_page.py --chunks chunks.tsv --copies chunks.copies.tsv --species dva,dvl,... --names names.tsv
                    --raw-base URL --outdir DIR [--title T] [--meta meta.tsv]
  --raw-base: raw.githubusercontent.com URL of DIR (alignment links open in the MSA Viewer)
  names.tsv:  code<TAB>species name<TAB>assembly
  meta.tsv:   key<TAB>value lines shown in the overview
expects in DIR: subfam_input.aln.fa (reference + chunk consensi, aligned), chunks/<chunk>.aln.fa (members of each chunk),
sample FASTA (linked as given in meta 'sample_file')
"""
import argparse, csv, html, os, statistics, urllib.parse

# categorical slots 1-7 (fixed order = species order), light / dark
LIGHT = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#4a3aa7']
DARK = ['#3987e5', '#d95926', '#199e70', '#c98500', '#d55181', '#008300', '#9085e9']


def viewer(raw_base, path, title):
    url = raw_base.rstrip('/') + '/' + path
    return ('https://toki-bio.github.io/MSA-viewer/?url=' + urllib.parse.quote(url, safe='') +
            '&title=' + urllib.parse.quote(title))


def hist_svg(values, lo, hi, nbins, label, unit):
    w, h, pad = 260, 90, 18
    if not values:
        return '<p class="small">no data</p>'
    step = (hi - lo) / nbins
    counts = [0] * nbins
    for v in values:
        i = min(nbins - 1, max(0, int((v - lo) / step)))
        counts[i] += 1
    top = max(counts)
    bw = (w - 2) / nbins
    bars = []
    for i, c in enumerate(counts):
        bh = (h - pad) * c / top if top else 0
        x = 1 + i * bw
        a, b = lo + i * step, lo + (i + 1) * step
        bars.append(f'<rect class="bar" x="{x + 1:.1f}" y="{h - pad - bh:.1f}" width="{max(bw - 2, 1):.1f}" '
                    f'height="{bh:.1f}" rx="1"><title>{label}: {a:.0f}–{b:.0f}{unit}: {c} copies</title></rect>')
    axis = (f'<line class="axis" x1="0" y1="{h - pad}" x2="{w}" y2="{h - pad}"/>'
            f'<text class="tick" x="0" y="{h - 4}">{lo:.0f}{unit}</text>'
            f'<text class="tick" x="{w}" y="{h - 4}" text-anchor="end">{hi:.0f}{unit}</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{html.escape(label)}">{"".join(bars)}{axis}</svg>'


def stack_svg(counts, species, n):
    """composition of one chunk: one horizontal stacked bar, species in fixed order, 2px gaps"""
    w, h = 160, 14
    x, parts = 0.0, []
    for k, sp in enumerate(species):
        c = counts[sp]
        if not c:
            continue
        sw = w * c / n
        parts.append(f'<rect class="s{k}" x="{x:.1f}" y="0" width="{max(sw - 2, 0.5):.1f}" height="{h}" rx="2">'
                     f'<title>{sp}: {c} of {n}</title></rect>')
        x += sw
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="species composition">{"".join(parts)}</svg>'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chunks', required=True); ap.add_argument('--copies', required=True)
    ap.add_argument('--species', required=True); ap.add_argument('--names', required=True)
    ap.add_argument('--raw-base', required=True); ap.add_argument('--outdir', required=True)
    ap.add_argument('--title', default='SubFam run'); ap.add_argument('--meta')
    ap.add_argument('--ref-name', default='dar_squam1')
    a = ap.parse_args()
    species = a.species.split(',')
    names = {r[0]: r[1:] for r in csv.reader(open(a.names), delimiter='\t')}
    meta = [r for r in csv.reader(open(a.meta), delimiter='\t')] if a.meta else []
    md = dict(meta)
    chunks = list(csv.DictReader(open(a.chunks), delimiter='\t'))
    chunks.sort(key=lambda r: int(r['msf_order'] or 10 ** 6))
    copies = list(csv.DictReader(open(a.copies), delimiter='\t'))
    ident = {sp: [] for sp in species}
    for c in copies:
        ident.setdefault(c['copy'].split('_')[0], []).append(float(c['identity']))
    ref_col = f'median_copy_identity:{a.ref_name}'

    css = """
:root { --fg:#222; --bg:#fafafa; --card:#fff; --accent:#2a78d6; --muted:#666; --border:#e2e2e2; --head:#2c3e50;
        --thbg:#f0f3f7; --zebra:#fafbfd; --bar:#2a78d6; --axis:#b8b8b8; %s }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
        --fg:#e8e8e3; --bg:#141413; --card:#1a1a19; --accent:#3987e5; --muted:#a8a79e; --border:#33332f; --head:#e8e8e3;
        --thbg:#24241f; --zebra:#1f1f1d; --bar:#3987e5; --axis:#55554f; %s } }
:root[data-theme="dark"] { --fg:#e8e8e3; --bg:#141413; --card:#1a1a19; --accent:#3987e5; --muted:#a8a79e; --border:#33332f;
        --head:#e8e8e3; --thbg:#24241f; --zebra:#1f1f1d; --bar:#3987e5; --axis:#55554f; %s }
* { box-sizing: border-box; }
body { font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: var(--bg); color: var(--fg); margin: 0; }
header { background: linear-gradient(135deg, #2c3e50, #2a78d6); color: #fff; padding: 24px 32px; }
header h1 { margin: 0 0 6px 0; font-size: 1.5rem; } header .sub { opacity: .85; font-size: .95rem; }
nav { padding: 8px 32px; font-size: .9rem; } nav a { margin-right: 14px; color: var(--accent); }
main { max-width: 1280px; margin: 0 auto; padding: 16px; }
section.card { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 18px 22px; margin: 18px 0; }
section.card h2 { margin-top: 0; font-size: 1.15rem; color: var(--head); border-bottom: 1px solid var(--border); padding-bottom: 8px; }
p.intro, .small { color: var(--muted); font-size: .9rem; }
.kv { display: grid; grid-template-columns: max-content 1fr; gap: 4px 16px; font-size: .92rem; }
.kv .k { color: var(--muted); } .kv .v { font-family: ui-monospace, Menlo, monospace; word-break: break-all; }
.tblwrap { overflow-x: auto; }
.tbl { border-collapse: collapse; width: 100%%; font-size: .86rem; margin: 8px 0; }
.tbl th, .tbl td { border: 1px solid var(--border); padding: 4px 7px; text-align: left; white-space: nowrap; }
.tbl th { background: var(--thbg); position: sticky; top: 0; }
.tbl tbody tr:nth-child(even) { background: var(--zebra); }
.tbl td.num { text-align: right; font-variant-numeric: tabular-nums; }
.metrics { display: flex; flex-wrap: wrap; gap: 14px; margin: 8px 0 16px 0; }
.metric { background: var(--thbg); border-left: 4px solid var(--accent); padding: 10px 14px; border-radius: 4px; min-width: 150px; }
.metric .num { font-size: 1.35rem; font-weight: 600; } .metric .lbl { font-size: .78rem; color: var(--muted); text-transform: uppercase; }
.aln-link { display: inline-block; background: #2a78d6; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: .83rem; text-decoration: none; margin: 1px 0; }
.aln-link.green { background: #1f7a3a; } .aln-link.orange { background: #b4521f; }
.grid { display: grid; gap: 14px; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }
.grid h3 { margin: 4px 0; font-size: .95rem; }
svg .bar { fill: var(--bar); } svg .axis { stroke: var(--axis); stroke-width: 1; } svg .tick { fill: var(--muted); font-size: 10px; }
.legend { display: flex; flex-wrap: wrap; gap: 12px; font-size: .85rem; margin: 6px 0; }
.legend span::before { content: ""; display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 5px; background: var(--c); }
a { color: var(--accent); }
code { background: var(--thbg); padding: 1px 5px; border-radius: 3px; }
""" % tuple(' '.join(f'--s{k}:{c};' for k, c in enumerate(pal)) for pal in (LIGHT, DARK, DARK))
    css += ''.join(f'svg .s{k} {{ fill: var(--s{k}); }}\n' for k in range(len(species)))

    n_copies = len(copies)
    out = [f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
           f'<title>{html.escape(a.title)}</title><style>{css}</style></head><body>',
           f'<header><h1>{html.escape(a.title)}</h1><div class="sub">{html.escape(md.get("subtitle", ""))}</div></header>',
           '<nav><a href="#alignments">Alignments</a><a href="#overview">Overview</a><a href="#chunks">Chunks</a>'
           '<a href="#species">Species</a><a href="#peel">Peeling</a></nav><main>']
    # alignments
    out.append('<section class="card" id="alignments"><h2>Alignments &mdash; open in MSA Viewer</h2>'
               f'<p class="intro">The SubFam input alignment holds the {html.escape(a.ref_name)} consensus and one consensus '
               'per chunk of 50 MAFFT-sorted copies, in SubFam\'s final order. Peeling works on this alignment; each chunk\'s '
               'own copies are linked in the table below.</p>'
               f'<a class="aln-link green" target="_blank" href="{viewer(a.raw_base, "subfam_input.aln.fa", a.title + " SubFam input")}">'
               f'SubFam input alignment ({len(chunks)} chunk consensi + {html.escape(a.ref_name)})</a> '
               f'<a class="aln-link" href="{a.raw_base.rstrip("/")}/{html.escape(md.get("sample_file", ""))}">sample FASTA ({n_copies:,} copies)</a> '
               f'<a class="aln-link orange" href="{a.raw_base.rstrip("/")}/chunks.tsv">chunk table (TSV)</a> '
               f'<a class="aln-link orange" href="{a.raw_base.rstrip("/")}/chunks.copies.tsv">copy → chunk (TSV)</a></section>')
    # overview
    out.append('<section class="card" id="overview"><h2>Overview</h2><div class="metrics">'
               f'<div class="metric"><div class="num">{n_copies:,}</div><div class="lbl">copies in the sample</div></div>'
               f'<div class="metric"><div class="num">{len(chunks)}</div><div class="lbl">chunks of 50</div></div>'
               f'<div class="metric"><div class="num">{len(species)}</div><div class="lbl">assemblies</div></div>'
               f'<div class="metric"><div class="num">{statistics.median([float(c["identity"]) for c in copies]):.1f}%</div>'
               f'<div class="lbl">median identity to {html.escape(a.ref_name)}</div></div></div>'
               '<div class="kv">' + ''.join(f'<div class="k">{html.escape(k)}</div><div class="v">{html.escape(v)}</div>'
                                         for k, v in meta if k not in ('subtitle', 'sample_file')) + '</div>')
    out.append('<table class="tbl"><thead><tr><th>code</th><th>species</th><th>assembly</th><th>copies in sample</th>'
               '<th>median identity</th></tr></thead><tbody>')
    for k, sp in enumerate(species):
        v = ident.get(sp, [])
        nm = names.get(sp, ['', ''])
        out.append(f'<tr><td><code>{sp}</code></td><td><em>{html.escape(nm[0])}</em></td><td>{html.escape(nm[1] if len(nm) > 1 else "")}</td>'
                   f'<td class="num">{len(v):,}</td><td class="num">{statistics.median(v) if v else 0:.1f}%</td></tr>')
    out.append('</tbody></table></section>')
    # chunks
    legend = ''.join(f'<span style="--c:var(--s{k})">{sp}</span>' for k, sp in enumerate(species))
    out.append('<section class="card" id="chunks"><h2>Chunks in alignment order</h2>'
               '<p class="intro">One row per chunk, in the order of the SubFam input alignment (SubFam drops a last batch of fewer than 50 copies). Composition: the 50 copies '
               'of the chunk by assembly (hover for counts); a chunk dominated by one or two assemblies points to a '
               f'lineage-specific subfamily. Identity is to {html.escape(a.ref_name)}, gaps excluded.</p>'
               f'<div class="legend">{legend}</div><div class="tblwrap"><table class="tbl"><thead><tr><th>#</th><th>chunk</th>'
               '<th>composition</th>' + ''.join(f'<th>{sp}</th>' for sp in species) +
               '<th>median copy identity</th><th>consensus length</th><th>consensus identity</th></tr></thead><tbody>')
    for r in chunks:
        n = int(r['n'])
        counts = {sp: int(r.get(sp, 0) or 0) for sp in species}
        ch = r['chunk']
        link = viewer(a.raw_base, f'chunks/{ch}.aln.fa', f'{a.title} {ch}')
        out.append(f'<tr><td class="num">{r["msf_order"]}</td><td><a target="_blank" href="{link}">{html.escape(ch)}</a></td>'
                   f'<td>{stack_svg(counts, species, n)}</td>' + ''.join(f'<td class="num">{counts[sp]}</td>' for sp in species) +
                   f'<td class="num">{r.get(ref_col, "")}</td><td class="num">{r["cons_length"]}</td>'
                   f'<td class="num">{r["cons_identity"]}</td></tr>')
    out.append('</tbody></table></div></section>')
    # species
    out.append('<section class="card" id="species"><h2>Copies per assembly</h2>'
               f'<p class="intro">Identity of each sampled copy to {html.escape(a.ref_name)} (gaps excluded). '
               'Hover a bar for the count.</p><div class="grid">')
    for sp in species:
        out.append(f'<div><h3>{sp} &mdash; <em>{html.escape(names.get(sp, [""])[0])}</em></h3>'
                   f'{hist_svg(ident.get(sp, []), 60, 100, 40, sp, "%")}</div>')
    out.append('</div></section>')
    out.append('<section class="card" id="peel"><h2>Peeling</h2><p class="intro">Define subfamilies as groups of chunks in '
               'the SubFam input alignment and write them as <code>chunk&lt;TAB&gt;group</code> (one line per chunk, '
               'chunks left out are unassigned). From that file the next step builds one alignment and consensus per group '
               '(as <code>t1_Nseqs.al</code> on the Tal pages), assigns all copies of the seven assemblies, and adds '
               'subfamily composition, divergence and the per-group alignments to this page.</p></section>')
    out.append('</main></body></html>')
    open(os.path.join(a.outdir, 'index.html'), 'w').write('\n'.join(out))


if __name__ == '__main__':
    main()
