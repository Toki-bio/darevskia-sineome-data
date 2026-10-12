# Item 0, gate (c): within-genome uniqueness in all seven assemblies (runs 38201844513, 38202962397)

fs9_twins (fixed, SOFTMASK=0) per genome; dar8 multicopy groups compared; contig pairs carrying ≥ 5 twin pairs
aligned with minimap2 -c (identity = 1 - gap-compressed divergence, weighted by aligned length).

| genome | size Gb | copies with a twin | dar8 multicopy groups (2+ contigs) | explained as twin pair | untestable | unexplained | duplicated blocks aligned | block identity (share of aligned bp) |
|---|---|---|---|---|---|---|---|---|
| dva | 1.65 | 24.0 % | 11,712 | 90.9 % | 8.6 % | 0.4 % | 160 Mb (992 contig pairs) | ≥ 99 %: 79 %; 98–99: 15 %; 95–98: 6 % |
| dvl | 1.46 | 7.9 % | 2,906 | 87.9 % | 11.3 % | 0.7 % | 8.6 Mb (188; whole small contigs) | ≥ 99.5 %: 79 %; 99–99.5: 18 % |
| nai | 1.77 | 29.2 % | 16,193 | 82.5 % | 14.7 % | 2.4 % | 320 Mb (926) | 95–97 %: 93 %; 97–98: 5 % |
| arm | 1.93 | 28.7 % | 14,742 | 90.3 % | 7.3 % | 2.2 % | 505 Mb (526) | 97–98 %: 86 %; 95–97: 14 % |
| mix | 1.41 | 4.6 % | 1,248 | 89.0 % | 10.7 % | 0.2 % | 45 Mb (129) | spread 95–100 % |
| unp | 1.37 | 2.9 % | 509 | 86.2 % | 10.0 % | 3.7 % | 16 Mb (12) | 95–97 %: 70 % |
| unm | 1.40 | 2.2 % | 154 | 74.0 % | 21.4 % | 3.2 % | 33 Mb (18) | 95–97 %: 100 % |

## Reading

Three different things hide behind "multicopy":

1. **dva, dvl: retained haplotigs.** Blocks 99–100 % identical (allelic differences of one individual); in dvl whole
   small contigs duplicated. These copies are one locus: collapse them (the planned haplotig rule), disagreeing
   P/A between them = heterozygous insertion.
2. **arm (505 Mb at 97–98 %) and nai (320 Mb at 95–97 %): two divergent haplotypes side by side.** 2–5 % divergence is
   far above allelic variation inside an individual and in the range between species (flank p-distance in the BPP
   test: nai–val 2.2 %, val–mix 3.3 %). For arm (mixta × valentini parthenogen) this is expected — the primary assembly
   holds both parental subgenomes in large blocks, which also explains the BPP test (arm's primary sequence val-like,
   the mixta alleles elsewhere). For nai (a bisexual species) it is unexpected: the sequenced individual may carry a
   divergent second haplotype (hybrid or introgressed ancestry) or the assembly may join material of different
   origin. These copies must NOT be collapsed as haplotigs: each block is a separate haplotype whose orthology to the
   parental species differs.
3. **mix, unp, unm: a small, ordinary level** (2–5 % of copies; tens of Mb), a mix of segmental duplications and some
   divergent blocks.

## Consequences for the pipeline (item 0 design, revised)

- within-genome status per copy as planned, plus a block class per twin pair from block identity: `haplotig`
  (≥ 99 %), `homeolog` (two divergent haplotypes, 94–98.5 % over large blocks), `segdup` (short or older);
- haplotig twins collapsed before the pairwise step; homeolog twins kept as two loci and assigned to a haplotype
  (parent) by block — the per-block affinity test of the BPP notes — so that arm (and nai, if confirmed) enter the
  pan-SINEome as two haplotypes;
- the reads (next week) test it directly: a haplotig pair or a homeolog pair has half the read depth on each copy;
  a segmental duplication has full depth on both.
