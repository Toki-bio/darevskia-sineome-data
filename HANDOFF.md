# Darevskia pan-SINEome: handoff (state on 2026-10-08)

For any Claude session (cloud, Desktop, VS Code) that picks up this project. Everything below is on GitHub; nothing
lives only in a cloud container. Read this file, then `plans/dar8-followups.md` (branch `actions/pairs21`).

## Repositories

| repo | what | where to look |
|---|---|---|
| [Toki-bio/SINE_orth_loc](https://github.com/Toki-bio/SINE_orth_loc) | the pipeline (orthologous SINE loci between two assemblies; pan-SINEome registry; nested/close/satellite handling; read genotyping) | development branch **`claude/wonderful-tesla-x39s12`** (head `bdc2134`), not `main` |
| [Toki-bio/darevskia-sineome-data](https://github.com/Toki-bio/darevskia-sineome-data) (public, GitHub Pages from `main`) | all data, results, plans, cloud workflows | branches below |
| [Toki-bio/knowlege](https://github.com/Toki-bio/knowlege) | notes: `projects/te-anchor-graph-pansineome.md`, `methods/erast-for-orthologous-loci.md`, `methods/tint-nested-transpositions.md` | `main` |
| [Toki-bio/SubFam](https://github.com/Toki-bio/SubFam), [SINEderella](https://github.com/Toki-bio/SINEderella) | subfamily tools (SubFam.sh used unchanged) | |
| [Toki-bio/CLsat_workflow](https://github.com/Toki-bio/CLsat_workflow), [CLsat-viewer](https://github.com/Toki-bio/CLsat-viewer) | satellite DNA in the same assemblies; methods borrowed for SINE dimers/satellites | |
| Toki-bio/sineclose (private) | closing N-runs / contig ends with Illumina pairs; planned for M sites of dvl | |

## Branches of darevskia-sineome-data

| branch | content |
|---|---|
| `main` | `old/` (v2.0 orth tables, copy BEDs `old/beds/<sp>-dar_squam1.bed.gz`, old registry), `pan/dar7.*` (pan-SINEome dar7), `dva-mix-v2/` (KIT run with rescue), `subfam/` (SubFam pages, see below), `index.html` (Pages landing), this file |
| `actions/pairs21` | **current results**: `pairs/<pair>/` for all 21 pairs (orth, clusters, rescue, nested, superseded, stat files, logs), `pairs/REPORT.md`, `pairs/nest/` (sine_nest scans per genome), **`pan/dar8.*`** (pan-SINEome dar8; evidence split in `dar8.evidence.part00/01.tsv.gz`), **`plans/`** (all plans) |
| `subfam` | workflow `subfam.yml` that produced the SubFam runs (copied to `main`) |
| `bpp` | `bpp/bpp_loci.py`, workflow `bpp.yml`, `bpp/test500/` (500-locus BPP test + `NOTES.md`) |
| `actions/nest`, `actions/genotype` | earlier runs: sine_nest on dva/mix; read genotypes of D. valentini individuals (v245 etc.) |

## Genomes (codes used everywhere)

| code | accession | assembly | note |
|---|---|---|---|
| dva | GCA_034642135.1 | Dar_val_2.0 | D. valentini |
| dvl | GCA_024498535.1 | Dval_245 | D. valentini, legacy, 31,777 sequences; individual v245 (10x reads SRR16117178) |
| nai | GCA_034642065.1 | Dar_nair_1.0 | D. nairensis |
| mix | GCA_034641385.1 | Dar_mix_1.0 | D. mixta |
| arm | GCA_034641395.1 | Dar_arm_1.0 | D. armeniaca (parthenogen, mixta × valentini) |
| unp | GCA_032766555.1 | D.uni.pHiFi.1.0 | D. unisexualis "paternal" haplotype |
| unm | GCA_032766585.1 | D.uni.mHiFi.1.0 | D. unisexualis "maternal" haplotype |

FASTA headers are cut to the first word (GenBank accession). SINE: dar_squam1 (357 bp; extracted from
`dva-mix-v2/alignments/aln_dva-mix_SINE.aln.gz`, row `>dar_squam1`).

## What was done (Oct 2026)

1. **SINE_orth_loc v2.2** (branch `claude/wonderful-tesla-x39s12`): flank-indel masking, contig-end → state M,
   alignment-derived insertion anchors, `sine_nest.py` (nested/split/dimer/satellite/close copies, TSD check, TinT
   chronology, compound-locus orthology, supersede), `STAGE=prep|align|finish` + `SHARD=k/N` to split a pair across
   machines (identical output), `sine_registry.py --previous` reads gzipped builds. Docs: README, `docs/pan-sineome.md`,
   `docs/toga2-lessons.md`.
2. **All 21 pairs rerun** on GitHub Actions (run 37462585105; 168 alignment shards); registry **dar8** built with
   `--previous pan/dar7` (workflow `registry21.yml`, run 37559512997). dar8: 169,327 groups, 50,810 variable;
   P 714k, A 169k, U 236k, X 65k, M 1.5k. dva-mix agrees with the KIT run (65,570/14,548/12,973 vs 64,235/14,514/12,941).
3. **Open issue found in dar8**: X rose 5.9k → 65k, almost all "multicopy" groups with two copies on two contigs in
   nai/arm/dva — assemblies 0.25–0.55 Gb larger than unp/unm/mix: retained haplotigs (plan item 1/2).
4. **SubFam on 30,000 copies** (equal number from each of the 7 assemblies, seed 11; 600 chunks of 50):
   page https://toki-bio.github.io/darevskia-sineome-data/subfam/dar_squam1_30000/ (files in `main:subfam/`).
   Rough structure: main 351–357 bp type (~98 % to dar_squam1), 363–370 bp variants, 382–386 bp old type (~93 %);
   all shared by the 7 assemblies. **Waiting for Sergei's manual peeling** (chunk → group TSV).
5. **Plans written** (branch `actions/pairs21`, `plans/`): `dar8-followups.md` (items 1–7 with gates and a status
   table), `cactus-monsoon-prompt.md` (Minigraph-Cactus on Monsoon in gates), `dimers-satellites.md` (design after
   CLsat; 0 of 714,365 SINE copies lie inside a CLsat array).
6. **BPP** (item 7): toy recovered τ/θ except the youngest split; 500-locus real test (branch `bpp`) runs in ~13 min
   but shows the parthenogen assemblies are haplotype mosaics (unm alternates nai-/val-like loci within chromosomes;
   unp nai- and mix-like; arm val-like) → parthenogens cannot be simple BPP tips. See `bpp/test500/NOTES.md`.

## What is paused and why

| work | waits for |
|---|---|
| all remaining SINE work (haplotig rule, satellites, dimers, genes × SINE age, subfamily assignment of all copies) | Sergei's peeling of the SubFam chunks; reassignment may follow |
| BPP full run, parthenogen phasing, sineclose on M sites | raw reads (expected within days) |
| Cactus | Sergei starting `plans/cactus-monsoon-prompt.md` in Claude Code on Monsoon |
| Podarcis gene projection (miniprot; toy P. muralis → P. raffonei) | could start now (genome-level); awaiting go-ahead |

## Rules for any session

- Heavy compute: GitHub Actions on this public repo (4 vCPU, 16 GB, 6 h per job) or Monsoon (`/scratch/sk4386`,
  Slurm partition `core`, chains with `--dependency=afterok`). KIT (`toki@85.89.102.78`, port 22, ed25519 key only) is
  reachable only from the local Claude Desktop: one long-lived connection, no per-command connections, never write
  into `/data/V/toki/Darevskia_v2`, never store passwords, never copy private keys into a cloud environment.
- Every heavy step goes toy (known truth) → partial data → full, with a pass check between.
- Workflows on `actions/pairs21`: `pairs21.yml` is dispatch-only (an edit must not rerun all pairs); `registry21.yml`
  rebuilds dar8 from that run's artifacts (artifacts expire; the tables themselves are committed).
- GitHub limits: files ≤ 100 MB (split large tables); pattern artifact downloads list at most 200 artifacts per run.
- EMBOSS `cons` hangs on sequence names containing `|`; SubFam inputs use `<sp>_<locus>`.

## Next steps when unblocked

1. Peeling TSV arrives → build per-group alignments/consensi (`t<k>_<n>seqs.al` as on the Tal pages), assign all copies
   of the 7 assemblies (SINEderella step 2), finish the subfamily page.
2. Reads arrive → per-locus/per-block parent assignment of unp/unm/arm along chromosomes; then BPP (bisexual species
   first, parthenogens via MSC-I), sineclose on dvl M sites.
3. Then plan items in order: minimap2 synteny + haplotig rule (dar8.1) → satellites → M recovery → dimers → genes × SINE
   age → Cactus comparison.
