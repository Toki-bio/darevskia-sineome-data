# Darevskia SINE_orth_loc v2 — notes (2026-10-02)

## What is here
- `old/` — the earlier AutoClaw run: SINE_orth_loc **main branch** zip, 7 Darevskia genomes, 21 pairs, KIT `/data/V/toki/Darevskia_v2`. orth tables, copy BEDs (dar_squam1), summary_pairs.tsv, registry (7 and 6 species builds), synthesis QC.
- `dva-mix/` — the **new branch** `claude/wonderful-tesla-x39s12`, commit 11771e3, run on dva vs mix. KIT `/data/V/toki/sol_v2_runs/dva-mix`. Large text files gzipped (`.gz`); alignment bundles are `alignments/aln_dva-mix_*.aln.gz`. `pipeline.log.gz` is the full log (71 MB raw).
- Not included: genomes, SAM/intermediates. Old-run alignment bundles and stat_* files exist only on KIT.

## (a) Consensus-name check
The old run did NOT use a mismatched name.
- Consensus used: `/data/V/toki/Darevskia_v2/dar_squam1.q` (copy of `/data/W/toki/Roma/darsquam1.q`, CRLF stripped), header `>dar_squam1`, 357 bp.
- BEDs: `<sp>-dar_squam1.bed` (SINE name `dar_squam1`, from `conf.sh` `SINE_NAME`).
- All four old bundles for dva-mix (MP, PM, SINE, rejected) contain the `>dar_squam1` row in every alignment sampled (4/4 files; first alignments inspected).
- The old `stat_multi_dva-mix` is 0 bytes: no multi-copy results at all. Cloud-side cause (species identified by first 3 characters of sequence names, which fails for GenBank names) — all 21 old pairs have no multi-copy results.
- New run: `~/sol_v2_runs/inputs/dar_squam1.fa` (header `>dar_squam1`), beds symlinked to the old `dva-dar_squam1.bed` / `mix-dar_squam1.bed`.

## (b) Tool check (KIT)
esl-alipid, sam2bed, mafft, seqkit, bedtools, samtools, bwa, tmux, git: all in `/usr/local/bin` or `/usr/bin`. GNU Awk 4.1.3. Python 3.12.13 (`/usr/local/bin/python3.12`; default python3 is 3.5). 48 cores; `/data/V` 2.2 TB free. Run used `PYTHON=/usr/local/bin/python3.12`, `-t 24`, scratch `~/sol_v2_runs/scratch` on `/data/V`.

## Run report: dva vs mix, new branch
Command: `SINE_orth_loc_flexible.sh -g1 dva.fna -g2 mix.fna -s dar_squam1.fa -b1 dva-dar_squam1.bed -b2 mix-dar_squam1.bed -n1 dva -n2 mix -o ~/sol_v2_runs/dva-mix -t 24 --scratch ~/sol_v2_runs/scratch --force`. Exit 0.

**Runtime:** 12,624 s (3 h 30 min), 15:20:21 -> 18:50:45 MSK. Old run of the same pair: 6,475 s.
`pipeline.log` has no timestamps, so stages are bracketed by result-file modification times only:
- start -> `stat_doubles` written (indexing, clustering, double-cluster alignment): 15:20 -> 16:57:57, about 97 min.
- 16:57:57 -> `rescue_dva-mix.tsv` written 18:32:56, about 95 min. Includes the multi/rescue stage (20,718 unresolved clusters, 58,169 copies; bwa mem both directions) and the alignment of rescued pairs; the log does not separate these.
- 18:32:56 -> end 18:50:45: bundling, statistics, orth table, about 18 min.
The rescue step therefore accounts for roughly 95 min of the extra ~100 min vs the old run (inferred from the brackets, not measured per step).

**MP / PM / SINE**

| | MP | PM | SINE | orth rows |
|---|---|---|---|---|
| old (main) | 10,935 | 9,325 | 41,001 | 61,261 |
| new (11771e3) | 10,938 | 16,197 | 63,673 | 90,808 |
| difference | +3 | +6,872 | +22,672 | +29,547 |

**Cluster fates** (`cut -f2,4 clusters_dva-mix.tsv`, fate prefix before `:`): 61,261 double resolved; 17,782 double rejected; 20,530 multi multi_unresolved; 188 poly poly_unanalysed (99,761 clusters).
Note: 20,530 multi clusters are labelled `multi_unresolved` in the fate column (stage-2 view); the rescue stage then processed 20,718 unresolved clusters (this count also includes poly). See rescue outcomes below for what happened to them.

**Rescue outcomes** (`cut -f3 rescue_dva-mix.tsv | cut -d: -f1`, per copy, 58,169 copies): resolved 36,989; no_concordant_pair 11,832; ambiguous 9,108; no_hit 240. 32,944 new locus pairs. After alignment QC: rescued:SINE 26,540, rescued:PM 6,873, rescued:MP 4, rescued:qc_failed 3,572. 29,547 rescued pairs entered the orth table as `M<n>R` clusters (MP 3, PM 6,872, SINE 22,672).
The difference 32,944 - 29,547 = 3,397 vs qc_failed 3,572 is not reconciled here.

## Regression check
New `orth_dva-mix.tsv` minus rows whose cluster starts with `M` (61,261 rows) vs old `orth_dva-mix.tsv` (61,261 rows): **0 rows differ** (comm both directions, full-row comparison, same alignment names). The consensus naming was identical and the new branch reproduces the old double-cluster results exactly.

## Open points
- PM jumped 9,325 -> 16,197 while MP stayed 10,935 -> 10,938: the rescued multi-copy loci are almost all SINE or PM (6,872 PM vs 3 MP). I have not investigated this asymmetry.
- Rejected doubles: 17,782 of 79,043 (22.5%) in both runs (identical regression result).
- The 3,397 vs 3,572 discrepancy above.
