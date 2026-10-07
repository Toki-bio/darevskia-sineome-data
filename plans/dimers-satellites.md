# Dimers and SINE satellites: study design (after the CLsat workflow)

Status 2026-10-07. Design only; runs wait for the subfamily structure (SubFam peeling), except the simulation.

## What the data say so far

- sine_nest.py scan (dar8): 373–601 dimer loci and 7–17 "satellite" loci per assembly. 113 of the 117 satellites have
  3 elements, which is also what a dimer next to a close copy looks like; 1,231 dar8 groups carry the dimer flag
  and 32 the satellite flag.
- Against the CLsat/DarSat catalogue (CLsat-viewer `MASTER.merged.bed`, 634 intervals, 68 Mb, six assemblies):
  **0 of 714,365 dar_squam1 copies lie inside a CLsat array, 9 lie within 5 kb of one.** The SINE "satellites" are a
  separate phenomenon (CLsat arrays are SINE-free), so they need their own evidence.
- Chance pairs: with ~100k copies per ~1.5 Gb, about 1 copy in 150 has another copy within 50 bp by chance alone,
  so a few hundred adjacent pairs per genome are expected without any dimeric element. Dimer counts have to be
  tested against that.

## Borrowed from the CLsat workflow

| CLsat step | use here |
|---|---|
| TRF discovery, period window, ≥ N copies (Step 3), simple-repeat filter (Step 4) | independent satellite discovery: TRF on ±5 kb around every multi-element SINE locus, period 300–1,500 bp (SINE + spacer), ≥ 3 copies; reject units dominated by simple repeats (the A-rich SINE tail must not drive the period) |
| canonical rotation of monomers (Step 5) + vsearch 0.90 per species, then pooled across species anchored on the reference consensus (Steps 6–8) | units of all SINE arrays rotated to start at the SINE 5′ end, clustered per assembly and across assemblies, so the same array type is recognised in every genome |
| seed → boundary expansion with a monomer-resolution scan (min bits, aligned fraction 0.67, dense walk then probe; Step 11) | every 3-element locus is extended unit by unit until the unit signal is lost: a real array grows past 3 units or shows regular phase; a dimer plus close copy stops |
| symmetric rescan of every locus against every family with bit-score deltas (DELTA 20, ambiguous 15; Step 12–14) | after peeling: each unit of a dimer or array scored against every subfamily consensus; homo- vs heterodimer called only when Δbits ≥ 20 for both units, otherwise "ambiguous" |
| curated family table deposited as data, not a threshold (Step 9) | the subfamily structure from peeling is the input table; nothing re-derived automatically |
| flank orthology with the overlap guard and all-vs-all orientation (04): flanks may not fall into another locus; left flank of one array may match the right flank of an inverted ortholog | compound loci (dimers, arrays) compared across assemblies through flanks outside the whole locus (already in sine_nest orth), plus the overlap guard and inverted orthologs checked explicitly; flank classes unique / low-complexity / scaffold-truncated |
| terminal monomers and boundary phase (05) | for dimers: which part of each unit is present at the junction (5′ truncation of the second unit, length of the first unit's tail), and whether that junction is the same in many copies (a dimeric source gene) or random (independent insertions) |
| chunked TRF for scaffolds beyond TRF's practical size (06) | same if any array sits on a > 80 Mb sequence |

## Tests

Satellites:
1. TRF ± 5 kb on all 117 loci and on every locus with ≥ 3 elements (any class): period, copy number, identity between
   units, unit = SINE + spacer or SINE only.
2. Unit-by-unit boundary expansion (above): array length in units.
3. Across assemblies, through the registry and flanks: unit number per lineage (a real array varies; a fixed
   3-element locus with identical P/A pattern of all three units is three insertions or a dimer + 1).
4. Call: satellite = ≥ 4 units with constant period (± 10 %) or TRF support with ≥ 3 full periods; otherwise relabel as
   dimer+close or close. Report every real array with its coordinates, unit consensus and copy number per assembly.

Dimers:
1. Null: shuffled copies (bedtools shuffle within the same sequences, gaps and haplotigs excluded) → expected adjacent
   pairs by spacer and orientation; observed / expected per spacer bin and per orientation (head-to-tail,
   head-to-head, tail-to-tail).
2. Target preference: position of the second unit relative to the first unit's 3′ A-rich tail (insertion into the
   tail = sequential, with a hot spot).
3. One event or two: TSD around the whole dimer vs one TSD per unit (tsd_check in sine_nest.py); P/A patterns of the
   two units across the seven assemblies (dimer groups in the registry: identical patterns in all assemblies vs
   different, which also orders the two insertions).
4. Conserved junction: junction ± 30 bp of all dimers clustered (vsearch 0.90) within and across assemblies; a large
   cluster with the same truncation pattern = copies of a dimeric source gene.
5. Homo vs heterodimer: subfamily of each unit by the symmetric bit-score rescan (needs the peeled subfamilies).

## Gates

1. Simulation (extends tests/simulate_genomes2.py): planted dimeric source elements (one junction, copied), chance
   pairs, sequential insertions into A-tails, true arrays of 3–20 units, dimer + close copy. Pass: every class told
   apart (confusion table), observed/expected recovers the planted excess.
2. One assembly (mix, the cleanest): all tests, manual look at 20 dimers and every satellite call.
3. All seven, then through the registry.
