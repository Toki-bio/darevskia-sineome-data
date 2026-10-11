# Item 0, gate (a): within-genome uniqueness on toys (2026-10-11)

Tool: SINEderella `flankscan/fs9_twins.sh` (twins) and `fs9_dupregion.sh` (duplicated neighbourhood).

## A bug found and fixed in fs9_twins

The genome 20-mer repeat filter never masked a 5' flank: 5' flanks are stored reversed (outward from the junction)
and the lookup used the reversed k-mer, which is neither the k-mer nor its reverse complement. Fixed on SINEderella
branch `claude/fs9-5prime-kmer-mask` (commit 73f1b56, not merged). Also: since 2026-10-05 the default is SOFTMASK=0
while `tests/test_fs9.sh` still expects SOFTMASK=1 behaviour for the hot-spot case.

| fs9 toy (382 copies) | before fix, SOFTMASK=0 | fixed, SOFTMASK=0 | fixed, SOFTMASK=1 |
|---|---|---|---|
| shuffled control (expect 0 twins) | 6 | 0 | 0 |
| hot-spot insertions in a LINE called twin (of 40) | 40 | 27 | 0 |
| unique copies called twin (of 300) | 0 | 0 | 0 |
| planted segdups ≥ 85 % found (12) / 78 % as tier 2 (2) / 73 % (2) | 12 / 2 / 0 | 12 / 2 / 0 | 12 / 2 / 0 |

## SINE_orth_loc simulations (fixed fs9)

| class | v1 aaa | v2 ccc | expected |
|---|---|---|---|
| segmental duplications (copy + duplicate) | 20/20 twin1 | – | twin |
| twice-assembled region (haplotig) | – | 22/22 twin1 | twin |
| plain / close / flank-indel | 141 / – / – unique | 160 / 63 / 87 unique | unique |
| repeat-flank (young repeat as left flank) | 0 twins (39 masked, 5 unique) | 0 twins (40 masked, 4 unique) | not twin (before the fix: all twin) |
| satellite units | – | 55 array | array |
| nested inserts | – | 8 twin2 | not twin |
| hosts | – | 2 twin1 | not twin |

The remaining false twins all have a SINE inside the flank (nested inserts: flanks are host SINE pieces; two hosts
with young inserts at their 3' end). With the annotated SINE pieces (sine_nest elements) masked in the genome before
fs9: 0 false twins; haplotig 20/22 twin1 (2 masked: a close copy in the flank), nested 30/30 and hosts 9 "masked"
(flank untestable — handled by the compound-locus logic of sine_nest), satellites 56 array, all other classes unique.

fs9_dupregion on the simulations flags 20/20 segdup and 22/22 haplotig copies and no plain copy; it also flags
repeat-flank, satellite and nested copies because the simulated genomes are not soft-masked (in real, soft-masked
assemblies those stretches are not mapped).

## Decisions for gate (b)

- use the fixed fs9; mask sine_nest element pieces (all ≥ 20 nt pieces, incl. fragments) before the twin test;
- the Darevskia NCBI assemblies are soft-masked (SINE copies 99 % lower case): measure on nai how many flanks are
  testable with SOFTMASK=0 vs 1 and how many dar8 two-contig multicopy groups each explains, then choose.
