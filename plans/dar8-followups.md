# dar8 follow-ups: plan (for approval)

Status 2026-10-07. dar8 (`pan/dar8.*`, branch `actions/pairs21`) is built from all 21 pairs rerun with SINE_orth_loc v2.2.
This plan covers six follow-ups. Nothing below has been run yet. Every heavy step is gated:
**toy (known truth) → partial real data (one region or one genome) → full run**, and each gate has a pass criterion
that is checked before the next step starts. Compute: GitHub Actions on the public data repo (4 vCPU, 16 GB RAM,
~70 GB disk, 6 h per job, 20 jobs at a time). Steps that do not fit are marked **[KIT]**; for those I write a
ready-to-paste prompt for the local Claude, which runs them under the KIT rules (one persistent connection,
nothing written to `/data/V/toki/Darevskia_v2`).

## Facts the plan rests on (checked 2026-10-07)

| | dva | dvl | nai | mix | arm | unp | unm |
|---|---|---|---|---|---|---|---|
| assembly size (Gb) | 1.65 | 1.46 | 1.77 | 1.41 | **1.93** | 1.37 | 1.40 |
| sequences | 3,559 | 31,777 | 1,805 | 402 | 1,656 | 347 | 152 |
| X states in dar8 | 14.7k | 6.0k | 19.7k | 3.0k | 18.1k | 2.0k | 1.5k |
| … of which multicopy on 2 contigs | 13.7k | 3.9k | 18.9k | 1.7k | 17.2k | 0.8k | 0.3k |
| M states (window at a contig end) | 77 | **1,378** | 35 | 5 | 26 | 10 | 4 |
| satellite loci (nest scan) | 10 | 10 | 17 | 7 | 10 | 11 | 8 |

- The three large assemblies carry the two-contig multicopy groups; unp/unm (haplotype-resolved) and mix do not.
  The excess size (0.25–0.55 Gb) fits retained alternative haplotypes (haplotigs). arm is a valentini × mixta
  hybrid, so both parental haplotypes being assembled side by side is expected.
- 113 of 117 satellite loci have only 3 elements (a 3-unit "array" is also what a dimer next to a close copy looks
  like). In dar8, 32 groups carry the satellite flag.
- Dimers: 1,231 groups (3,778 species-level flags), 373–601 dimer loci per genome.
- M is almost all dvl, the fragmented legacy assembly, for which Illumina reads exist (v245, 10x, SRR16117178; used
  for genotyping).

## Order and dependencies

```
1a haplotig rule (toy)  ─┐
2  minimap2 synteny map ─┴─> 1b dar8.1 rebuild with haplotig map ─> 4, 5 (need correct states)
1c satellite re-check  ──────> dar8.1
6  M recovery (split contigs; sineclose on dvl) ──> dar8.1 / dar8.2
3  Cactus (independent truth layer; heaviest; last)
4  genes × SINE age (deep research first)
5  dimers (deep research first; subfamily library needed)
```

Proposed sequence: 2 and 1a together → 1b, 1c → 6 → 5 → 4 → 3. Each item ends with a commit, a short report and your go-ahead
for the next.

---

## 1. Registry: haplotigs, then satellites

### 1a. Haplotig rule, simulation (toy)
- Rule: two copies of one species in one group, **on different contigs**, both inside the same duplicated block (a run of
  ≥ 3 consecutive multicopy sites pairing the same two contigs, already in `dupblocks`), or inside a haplotig pair from
  item 2 once that exists → one species state (P if both carry the SINE, A if both are empty, X if they disagree:
  a heterozygous insertion, reported as flag `het`) plus flag `haplotig`. Copies on the same contig (tandem duplicates)
  stay X.
- Toy: the v2 simulation already has a twice-assembled 30 kb region (`ccc_chr9`). I add a larger case, 5 regions of
  50–200 kb at 0.2–1 % divergence, one with a heterozygous insertion, and a true segmental duplication at 5 %
  divergence that must not collapse.
- Pass: every simulated haplotig collapsed; the heterozygous site reported as `het`; the segmental duplication still X;
  nothing else changes (existing tests and the dar7 rebuild unchanged).

### 1b. Real data (dar8.1)
- Registry rebuild from the committed pair tables (minutes, cloud). Partial first: nai only, with the haplotig pairs from
  item 2 as the reference set: precision and recall of the rule against the minimap2 map, and a manual look at 20 loci.
- Pass: ≥ 90 % of two-contig multicopy groups explained by the minimap2 haplotig map; collapsed groups stop
  contradicting the other species (no new `inconsistent`).
- Expected: X in nai/arm/dva drops from ~15–20k to the 1–2k level of unp/unm. A `het` column for the parthenogens is a
  by-product (insertion heterozygosity inside a clonal genome).

### 1c. Satellites
- Re-check all 117 satellite loci (and the 32 flagged groups): Tandem Repeats Finder on ±5 kb, a self dot plot,
  unit length and copy number, and comparison across species (a real array changes unit number between lineages; a
  dimer + close copy does not).
- Rule change: a satellite needs ≥ 4 units with a constant period (± 10 %) or TRF support; 3-element loci become
  `dimer+close` or `close`. Simulation test: satellites with 3–20 units against dimers with a close copy.
- Pass: no false satellites in simulation; manually checked real loci confirm the new labels. Report what remains
  (possibly none).

## 2. minimap2 synteny: what the duplicated regions are

- Questions: are the two-contig duplicated blocks haplotigs (allelic, 98–99.9 % identical over long stretches,
  contig-scale), segmental duplications (lower identity, shorter), or collapsed or misjoined regions?
- Methods, cheapest first:
  1. **compleasm** (BUSCO genes, sauropsida_odb10) per assembly: duplicated-BUSCO rate as a whole-genome haplotig index
     (~20 min per genome).
  2. **Self-alignment** `minimap2 -x asm5 -DP` per assembly (diagonal excluded): duplicated blocks with identity and
     length; haplotigs = long (≥ 20 kb), ≥ 98 %, contig-to-contig, often a whole contig contained in another.
  3. **Against a haplotype-resolved reference** (unm, 152 sequences, and mix): `minimap2 -x asm5` of each assembly to
     unm; reference regions covered twice by one query assembly = duplicated in the query; coverage tracks per window.
  4. Cross-check with sineclose `end_twin` logic: a contig end with a long twin (≥ 0.8 kb at ≥ 97 %) on another contig
     marks a haplotig boundary.
- Gates: toy (simulated assembly with known haplotigs, from 1a) → one assembly against itself (nai; ~1 h) → all seven.
- Output: `synteny/<sp>.haplotigs.bed` (pairs of regions, identity, length), `synteny/<sp>-unm.paf.gz`, a dot-plot
  page per assembly, and a table: haplotig Mb per assembly against the size excess. These feed 1b.
- Resources: an asm5 self-alignment of a 1.8 Gb assembly needs ~10–15 GB RAM with `-I 4G` (fits; arm is the risk,
  splitting the target in halves if needed).

## 3. Cactus alignment as an independent truth layer

- Purpose: P/A at every SINE_orth_loc site lifted through a whole-genome alignment (`halLiftover`), so every group gets
  an independent call: agree / disagree / unaligned. It is not ground truth (Cactus also struggles in young repeats),
  but its errors are independent of flank-anchoring errors.
- Choice (deep research before deciding): **Minigraph-Cactus** (pangenome mode; designed for low divergence, as
  between these Darevskia, roughly 1–5 %) against **Progressive Cactus** (needs a guide tree; much heavier).
  Minigraph-Cactus is the likely choice, with unm as reference, split by unm sequence. Haplotig-rich assemblies
  (arm, nai, dva) are a known problem for both: use the item-2 map to mask or report haplotigs.
- Gates: toy (cactus test data, then the 4-species simulation, where every insertion is known) → one large unm
  sequence (~100 Mb) across all 7 assemblies on a runner, to measure time and memory and validate on the simulated
  truth → full genome.
- Resources: the full 7-genome run will not fit 16 GB / 6 h runners (the minigraph join and the per-chromosome align
  need tens of GB). The partial run tells us how much is needed; the full run is **[KIT]** or a bigger machine. Your
  decision after the partial run.
- Deliverable: `cactus/dar.hal` (on KIT or as a release asset), a per-group comparison table (SINE_orth_loc state ×
  Cactus state) and discordance cases for manual review. This also gives an independent test of the haplotig
  collapse in item 1.

## 4. Gene annotation from Podarcis and SINE–gene relationships by relative age

- Annotation, cheapest robust first:
  1. **miniprot**: Podarcis muralis RefSeq proteins (GCF_004329235.1; P. raffonei GCF_027172205.1 as a second
     reference, to be confirmed on NCBI) aligned to each Darevskia assembly → gene models with exon/intron structure
     (~1–2 h per genome, cloud).
  2. **TOGA** (skill available) with Podarcis as reference for orthology and gene loss: needs whole-genome chains
     (make_lastz_chains), which is heavy → **[KIT]**, only if item 4 questions need orthology classes or gene loss.
  3. Validation: compleasm/BUSCO completeness of the projected set, and miniprot models against the RefSeq
     annotation of Podarcis itself (toy: project P. muralis onto P. raffonei and score).
- Relative age per SINE group (available now): (a) phylogenetic depth of the P/A pattern (shared by all = old;
  one lineage or one parthenogen = young), (b) identity to consensus, (c) nesting order (host older than insert),
  later (d) subfamily age from TinT once the subfamily library is in.
- Analyses (exact list after the deep research):
  - Insertion density in exons/UTRs/introns/promoters (±2 kb)/intergenic, by age class, against a matched null
    (random positions with the same GC and mappability, gaps excluded, haplotigs collapsed).
  - Orientation bias in introns (antisense excess, as for Alu/L1) as a function of age.
  - Depletion near genes with age (purifying selection), per gene category (housekeeping vs tissue-specific via
    Podarcis/Anolis expression where available).
  - Parthenogen-specific insertions (P only in unp/unm or arm, A in both parents): genes hit, and whether they differ
    from parental young insertions (relaxed selection in clonal lineages?).
- Deep research first: literature on SINE/Alu genic distribution by age, intronic orientation bias, lacertid and
  squamate TE landscapes, parthenogen genomes (Darevskia, Aspidoscelis).
- Gates: toy (planted insertions in a simulated annotated genome, to check the enrichment code returns the planted
  bias) → one genome (mix, the cleanest) → all seven.

## 5. Dimers: chance pairs or dimeric elements; homo- or heterodimers

- Null model first: with ~100k copies in ~1.5 Gb, chance alone gives roughly 1 neighbour within 50 bp per 150
  copies, i.e. hundreds per genome, the same order as the 373–601 dimer loci observed. So the test has to be
  explicit:
  1. Expected count of adjacent pairs (by spacer and orientation) from shuffled copies (bedtools shuffle, gaps
     excluded), against observed: excess, and the spacer distribution.
  2. Target preference: does the second unit sit in the A-rich tail of the first (insertion into the tail = sequential
     insertions with a hot spot, not a dimeric element)?
  3. One event or two: TSDs (one around the whole dimer = inserted as a dimer; one per unit = sequential), and the P/A
     patterns of the two units across the 7 genomes (identical in all = consistent with one event; different =
     sequential, and the order is then known).
  4. Conserved junction: a dimeric source gene leaves copies with the same spacer and junction sequence; cluster the
     junctions across all copies and genomes.
  5. Homo vs heterodimer: subfamily of each unit. Needs the SINEderella subfamily library for dar_squam1 (on KIT; or
     rebuilt in the cloud with SINEderella from the copies, toy-tested first), plus orientation (head-to-tail vs
     inverted).
- Deep research first: dimeric SINEs (Alu from FLAM-C/FLAM-A, B1/ID, tRNA-tRNA and other dimeric SINEs, reptile
  examples), and how they are recognised.
- Gates: simulation with planted dimeric elements and chance pairs (both must be told apart) → one genome → all, then
  across species through the registry.

## 6. M (window at a contig end): recovery

1,378 of 1,535 M states are dvl (31,777 sequences); the rest are at haplotig or contig boundaries in the HiFi assemblies.
1. **Split-contig sites (assembly only, cloud).** For each M site, take the full locus (both flanks) from a species where
   it is complete and map it to the M genome: if the missing flank lies at another contig's end, the site is split
   across two contigs. Report it as a split-contig site; its state comes from whether SINE sequence sits at either end.
   Toy: the simulation already cuts ddd at 18 insertion sites. Pass: all 18 recovered, no false joins.
2. **sineclose on dvl (Illumina, v245 10x reads).** `scan` (N-runs at or near the sites) + `anchors` + `fish` + `close`,
   and for true contig ends the `link_extend`/`link_meet` prototype (two ends meeting) or a one-sided extension to
   read the missing site. Toy: sineclose's own toys plus 50 known dvl sites that are complete in dva (cut them
   artificially). Partial: 100 real M sites. The 10x R1 needs the 23 bp barcode clipped (done before for
   genotyping). Sizes: 30M-spot chunks, as in the genotype workflow.
3. **HiFi assemblies (the ~150 non-dvl M).** Raw HiFi reads, if deposited (to check per BioProject), spanning the site:
   a long read through both flanks settles it. A small "long-read span" check (fish reads by unique end k-mers, as
   in sineclose) rather than reassembly. Decide after 6.1, which may already explain most of them.
- Result: M → P/A where evidence is sufficient, otherwise kept M with a reason; dar8.2.

---

## What I need from you

1. Go-ahead for the order (2 + 1a → 1b, 1c → 6 → 5 → 4 → 3), or another priority.
2. Item 5: get the SINEderella dar_squam1 subfamily library from KIT (via the local Claude), or rebuild it in the
   cloud?
3. Item 3: OK to plan the full Cactus run on KIT if the partial run shows it does not fit runners?
4. Item 6.3: should I search SRA for the HiFi raw reads of the 2023 assemblies (and Illumina for the other species)?
5. Item 4: any gene sets of special interest (e.g. meiosis/parthenogenesis-related genes, MHC)?

Corrections to my last summary: the dimer flag is on 1,231 groups (3,778 species-level flags), satellite on 32
groups, close on 27,271 species-level flags.
