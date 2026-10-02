# Darevskia_v2 - post-run synthesis & QC report

_Generated: 2026-10-02 06:45 UTC by synthesis_checks.py on the KIT server._

Project: `/data/V/toki/Darevskia_v2`  -  pipeline complete: 21/21 pairs OK (see summary_pairs.tsv).

## 1. Registry headline (all 7 genomes; registry/darevskia8.*)

- Multi-species loci in registry: **149,298**
- Variable loci (>=1 P and >=1 A; source of NEXUS matrix): **44,611**
- Loci with any X (ambiguous call): 4,608
- Loci with any U (no data): 101,903
- Flagged loci: **4,608** (expected 4608)

Top patterns (species order: dva, dvl, nai, mix, arm, unp, unm):

| pattern | dva | dvl | nai | mix | arm | unp | unm | loci |
|---|---|---|---|---|---|---|---|---|
| PPPPPPP | P | P | P | P | P | P | P | 20620 |
| PPPPUPP | P | P | P | P | U | P | P | 8211 |
| PPUPPPP | P | P | U | P | P | P | P | 7323 |
| PPPUPUP | P | P | P | U | P | U | P | 6240 |
| PPPPPUP | P | P | P | P | P | U | P | 4804 |
| UUPUUPU | U | U | P | U | U | P | U | 4675 |
| PPPAPAP | P | P | P | A | P | A | P | 3851 |
| PPPUPPP | P | P | P | U | P | P | P | 3823 |

## 2. Per-species state summary

| species | loci | P | A | U | X | %P of data | %P of all |
|---|---|---|---|---|---|---|---|
| dva | 149298 | 91864 | 20115 | 35968 | 1351 | 82.0% | 61.5% |
| dvl | 149298 | 102120 | 21840 | 23156 | 2182 | 82.4% | 68.4% |
| nai | 149298 | 91397 | 18686 | 38697 | 518 | 83.0% | 61.2% |
| mix | 149298 | 83844 | 22492 | 42421 | 541 | 78.8% | 56.2% |
| arm | 149298 | 92885 | 17576 | 38277 | 560 | 84.1% | 62.2% |
| unp | 149298 | 85417 | 22106 | 41335 | 440 | 79.4% | 57.2% |
| unm | 149298 | 97490 | 21790 | 29630 | 388 | 81.7% | 65.3% |

## 3. Coverage distribution

| k | loci (k species with P or A) | k | loci (k species with P) |
|---|---|---|---|
| 0 | 15 | 0 | 36 |
| 1 | 24 | 1 | 11519 |
| 2 | 16261 | 2 | 25859 |
| 3 | 12021 | 3 | 17239 |
| 4 | 12699 | 4 | 15750 |
| 5 | 24022 | 5 | 26927 |
| 6 | 39685 | 6 | 31348 |
| 7 | 44571 | 7 | 20620 |

## 4. Flag breakdown

| flag | count |
|---|---|
| inconsistent:dvl | 1455 |
| multicopy:dva | 1254 |
| multicopy:dvl | 727 |
| multicopy:mix | 485 |
| multicopy:arm | 479 |
| multicopy:nai | 459 |
| multicopy:unp | 369 |
| multicopy:unm | 304 |
| inconsistent:dva | 97 |
| inconsistent:unm | 84 |
| inconsistent:arm | 81 |
| inconsistent:unp | 71 |
| inconsistent:nai | 59 |
| inconsistent:mix | 56 |

By species:

- inconsistent: dvl=1455, dva=97, unm=84, arm=81, unp=71, nai=59, mix=56
- multicopy: dva=1254, dvl=727, mix=485, arm=479, nai=459, unp=369, unm=304

## 5. Per-pair QC

| pair | orth rows | MP | PM | SINE | rejected aln | rejected frac | dup names |
|---|---|---|---|---|---|---|---|
| arm-dvl | 84079 | 5784 | 1173 | 77122 | 10016 | 10.6% | 0 |
| arm-unm | 62988 | 6188 | 2728 | 54072 | 9230 | 12.8% | 0 |
| arm-unp | 56641 | 11848 | 9469 | 35324 | 18435 | 24.6% | 0 |
| dva-arm | 58997 | 927 | 4177 | 53893 | 5018 | 7.8% | 0 |
| dva-dvl | 86736 | 2203 | 455 | 84078 | 8027 | 8.5% | 0 |
| dva-mix | 61261 | 10935 | 9325 | 41001 | 17782 | 22.5% | 0 |
| dva-nai | 54795 | 7889 | 4279 | 42627 | 11740 | 17.6% | 0 |
| dva-unm | 63802 | 2700 | 2704 | 58398 | 8247 | 11.4% | 0 |
| dva-unp | 58566 | 8999 | 10679 | 38888 | 18530 | 24.0% | 0 |
| mix-arm | 58667 | 7953 | 11003 | 39711 | 17116 | 22.6% | 0 |
| mix-dvl | 83414 | 11776 | 12663 | 58975 | 24188 | 22.5% | 0 |
| mix-unm | 68462 | 10871 | 10598 | 46993 | 18965 | 21.7% | 0 |
| mix-unp | 65071 | 7740 | 7835 | 49496 | 17343 | 21.0% | 0 |
| nai-arm | 53799 | 7349 | 7438 | 39012 | 12206 | 18.5% | 0 |
| nai-dvl | 78965 | 9023 | 6038 | 63904 | 17171 | 17.9% | 0 |
| nai-mix | 59160 | 11177 | 8797 | 39186 | 16963 | 22.3% | 0 |
| nai-unm | 64229 | 6288 | 2886 | 55055 | 8852 | 12.1% | 0 |
| nai-unp | 61196 | 7528 | 4495 | 49173 | 11463 | 15.8% | 0 |
| unm-dvl | 90679 | 3948 | 3735 | 82996 | 14184 | 13.5% | 0 |
| unp-dvl | 80442 | 11531 | 12304 | 56607 | 25234 | 23.9% | 0 |
| unp-unm | 66158 | 10276 | 10606 | 45276 | 19960 | 23.2% | 0 |

## 6. Consistency checks

- Total orth-table rows: **1,418,107** vs 1,418,107 expected from build8.log -> OK
- Bundle counts vs summary_pairs.tsv (MP/PM/SINE per pair): 0 mismatches
- Duplicate alignment names in orth tables: 0
- Global status totals: {'MP': 162933, 'SINE': 1111787, 'PM': 143387}

## 7. Observations for attention (factual)

- Highest rejected-alignment fractions: arm-unp 24.6%; dva-unp 24.0%; unp-dvl 23.9%
- dvl assembly: 102120, 21840, 23156 (X/calls) - expect elevated ambiguity (fragmented legacy assembly; 31,777 contigs)
- unp-unm (paternal/maternal haplotypes) MP/PM: 10276 / 10606 - near-balanced, as expected

## 8. Files

per_species_stats.tsv, pairwise_shared_P.tsv, flag_breakdown.tsv, flag_by_species.tsv,
flagged_loci.tsv, coverage_distribution.tsv, per_pair_qc.tsv, SYNTHESIS_REPORT.md

