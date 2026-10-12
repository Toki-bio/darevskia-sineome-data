# Item 0, gate (b): within-genome uniqueness of dar_squam1 copies in nai (run 38167697948)

fs9_twins (SINEderella `claude/fs9-5prime-kmer-mask`, 73f1b56); SINE pieces of the nest scan masked with N; genome
20-mers counted with KMC (733,875 flank 20-mers occur > 20 times). Genome soft-masked 37.4 %. fs9_dupregion not run
(its minimap2 index of 1.8 Gb exceeds a 16 GB runner). Run time: twins 8.5 min (SOFTMASK 0), 5 min (1).

## Copies (116,276)

| status | SOFTMASK=0 | SOFTMASK=1 |
|---|---|---|
| twin1 (≥ 85 %) | 34,002 (29.2 %) | 27,634 (23.8 %) |
| twin2 (70–85 %) | 569 | 124 |
| array | 34 | 35 |
| masked (flank untestable) | 26,858 (23.1 %) | 45,505 (39.1 %) |
| unique | 54,799 (47.1 %) | 42,960 (36.9 %) |

SOFTMASK=0 is the better mode here: it tests more flanks and explains more multicopy groups (below).

## dar8 multicopy groups of nai (16,328; 16,193 with copies on two contigs)

| class | SOFTMASK=0 | SOFTMASK=1 |
|---|---|---|
| twin_pair (the group's copies are twins of each other) | 13,443 (82.3 %) | 11,080 (67.9 %) |
| untestable (a copy's flanks masked) | 2,420 (14.8 %) | 4,663 (28.6 %) |
| twin_other | 60 | 60 |
| unexplained | 401 (2.5 %) | 520 (3.2 %) |

## The twins

- 19,588 twin pairs; 8,892 similar on both sides; 93.9 % on two different contigs.
- 82 % of the cross-contig pairs lie in contig pairs that carry ≥ 5 twin pairs (2,526 contig pairs; top: 111 twin pairs
  between JAWWNI010000175.1 and JAWWNI010000452.1) — duplicated blocks, not scattered copies.
- Proximal flank identity (≤ 100 bp, coarse): 100 % 3,586; 99–99.9 % 2,809; 98–98.9 % 4,459; 95–97.9 % 6,044;
  90–94.9 % 1,668; < 90 % 1,022.
- 20 random pairs aligned with ± 200 bp (`examples/`): 15 similar over both 200 bp flanks and the SINE (94–100 %), so the
  whole neighbourhood is duplicated; 4 similar on one side only (duplication breakpoint at the copy); 1 weak (77 %).

## Reading

The X/multicopy problem of dar8 in nai is a within-genome duplication problem, and fs9 identifies it before any
comparison between genomes. Open question: the twins are mostly 95–100 % identical over the flanks — more divergent
than allelic differences inside one individual usually are, less than between species. Whether the blocks are
retained haplotigs, segmental duplications or something else (e.g. a hybrid/introgressed haplotype) needs
block-level identity (minimap2 of the paired contigs, item 2) and read depth (the reads coming next week: a haplotig
pair has half depth on each copy).
