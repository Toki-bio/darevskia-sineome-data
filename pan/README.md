# Darevskia pan-SINEome (dar_squam1), build dar7 — from the 21 old pairs

Orthologous groups of dar_squam1 SINE copies across 7 Darevskia genomes, built from the
21 pairwise orth tables in `../old/orth/` (SINE_orth_loc main branch, Oct 1–2 2026) and the
copy BEDs in `../old/beds/`. Format: [docs/pan-sineome.md](https://github.com/Toki-bio/SINE_orth_loc/blob/claude/wonderful-tesla-x39s12/docs/pan-sineome.md).

    sine_registry.py build old/orth/*.tsv.gz --species dva,dvl,nai,mix,arm,unp,unm \
        --copies dva=old/beds/dva-dar_squam1.bed.gz ... --copies unm=old/beds/unm-dar_squam1.bed.gz -o dar7

Code: Toki-bio/SINE_orth_loc, branch claude/wonderful-tesla-x39s12, commit 153d30b.

| File | Content |
| :- | :- |
| `dar7.groups.tsv.gz` | 149,234 groups: family, pattern, flags, copy or empty site per species |
| `dar7.copies.tsv.gz` | all 714,365 annotated copies, their group or why they have none |
| `dar7.evidence.tsv.gz` | the 1,418,107 pairwise rows behind the groups |
| `dar7.matrix.tsv`, `dar7.patterns.tsv` | group × species states; groups per pattern |
| `dar7.nex` | NEXUS 0/1 matrix of the 44,601 variable groups (P and A) |
| `dar7.aliases.tsv` | empty (first build) |
| `dar7.edges.tsv.gz` | anchor graph: groups whose sites are neighbours along a genome, spacer (bp) per genome (247,529 edges) |
| `dar7.breakpoints.tsv.gz` | adjacencies of one genome broken in another (groups with one site in both); `a_specific` = kept by no other genome |
| `dar7.dupblocks.tsv` | runs of >= 3 consecutive multicopy sites in one genome |

## Caveat: no multi-copy loci

The old runs' multi stage identified species by the first 3 characters of sequence names;
with GenBank names (JAWWNG…, JAWWNH…) every multi cluster was dropped (`stat_multi_*`
empty). Fixed in SINE_orth_loc 8ff1ecf, together with a two-flank rescue of multi-copy
clusters. Expect more groups and fewer U once the pairs are rerun.

## Copies

| species | copies | grouped | no validated pair | within 300 bp of another copy |
| :- | -: | -: | -: | -: |
| dva | 100,996 | 70.6% | 25.9% | 3.6% |
| dvl | 128,417 | 80.3% | 11.6% | 8.1% |
| nai | 116,276 | 65.2% | 30.8% | 4.1% |
| mix | 86,889 | 81.3% | 15.4% | 3.3% |
| arm | 111,467 | 66.1% | 30.4% | 3.5% |
| unp | 83,322 | 86.9% | 9.7% | 3.4% |
| unm | 86,998 | 91.7% | 4.7% | 3.7% |

## Flags

- `unannotated` (35,414 groups): SINE present by alignment (ComPair.sh) but no annotated copy at
  the site — mostly copies below the annotation thresholds (65% identity, 80% length) that a
  partner genome's flank found. In dva–mix, unannotated present sites have a median of 287
  identical nt with the consensus vs 324 for annotated ones.
- `multicopy` (3,956) and `inconsistent` (1,903): ambiguous groups (state X).

## To check: parthenogen assemblies

Share of species-specific loci per pair, (MP+PM)/(MP+PM+SINE), from `../old/summary_pairs.tsv`
(dva–dvl, two assemblies of one species: 0.031):

- D. unisexualis: unm (labelled maternal) – dva 0.085, – nai 0.143; unp (labelled paternal) –
  dva 0.336, – nai 0.196. The haplotype closest to D. valentini (expected paternal species) is
  the one labelled maternal. Check what mHiFi/pHiFi mean for GCA_032766585 / GCA_032766555
  before any parent-specific interpretation.
- D. armeniaca: arm – dva 0.087, – mix 0.323: the collapsed assembly is valentini-like.

## Anchor graph (added with SINE_orth_loc 4640840; same groups and IDs as dar7)

Adjacencies kept between genomes (groups with a single site in both): mix, unp and unm keep
97-98% of each other's; dva-mix 96%; arm and nai are the outliers (arm-nai 78%).

Species-specific breakpoints (adjacency kept by no other genome) — candidates for misjoins of
that assembly or rearrangements on its lineage:

| genome | other chromosome | moved, 1-100 kb | moved, 0.1-1 Mb | moved, > 1 Mb |
| :- | -: | -: | -: | -: |
| dva | 975 | 1,462 | 564 | 14 |
| dvl | 969 | 2,350 | 229 | 15 |
| nai | 1,744 | 7,544 | 1,042 | 22 |
| mix | 1,634 | 466 | 153 | 39 |
| arm | 1,590 | 6,461 | 2,884 | 33 |
| unp | 1,527 | 459 | 132 | 38 |
| unm | 1,059 | 193 | 70 | 18 |

`other chromosome` includes adjacencies at scaffold ends of fragmented assemblies. arm and
nai have thousands of local order changes that no other genome shares; for arm (a collapsed
assembly of a hybrid) haplotype switching during scaffolding is one candidate cause. To check
in the alignments / Hi-C maps before any biological reading.

Duplicated blocks (>= 3 consecutive multicopy sites): dva 40 blocks (131 sites), mix 23 (72),
others 1-4 — consistent with regions assembled twice in dva (see dva-mix: 6,997 mix copies with
exactly two equal placements in dva).
