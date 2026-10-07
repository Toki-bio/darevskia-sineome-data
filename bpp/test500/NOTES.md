# BPP test, 500 loci (run 37600708479)

- Loci: 500 selected (10,540 candidate groups), 471 kept with all 7 genomes (29 dropped: a pair < 85 % identity).
- Time on a 4-core runner: genome downloads + flanks 2 min, alignments 3 min, A01 7.5 min (100k iterations),
  A00 5.3 min (90k). A full run of 3,000–5,000 loci scales to ~1–2.5 h per analysis: fits a runner.
- Mean p-distance of the flanks: dva–dvl 0.26 %, nai–val 2.2 %, nai–mix 3.1 %, val–mix 3.3 %, unp–unm 3.3 %.

## A01 (val = dva + dvl, nai, mix, unp, unm)

Best tree (mix, (((nai, unm), unp), val)), posterior 0.99995. unp does not group with val.

## Why: the parthenogen assemblies are not clean parental haplotypes

Closest bisexual genome per locus (lowest p-distance):

| genome | nai | val | mix | tie |
|---|---|---|---|---|
| unm | 266 | 158 | 18 | 29 |
| unp | 241 | 62 | 148 | 20 |
| arm | 25 | 400 | 16 | 30 |

- unm: nai- and val-like loci alternate along the same chromosome-scale sequences (e.g. JAWDKO010000018.1: 9 nai,
  14 val), so the "maternal" assembly switches haplotype within chromosomes; 30 of its sequences with ≥ 4 loci
  have no ≥ 80 % majority.
- unp: nai-like loci dominate, with mix-like rather than val-like loci as the second class; also mosaic within
  sequences (39 sequences without a majority).
- arm: val-like at 400 of 471 loci; the mixta-derived alleles are mostly absent from the primary assembly (possibly
  in the retained haplotigs, item 2 of the plan).

So the hybrid genomes cannot enter BPP as simple tips. A00/A01 estimates with them (θ of internal nodes 0.02–0.04)
reflect that misspecification and are not interpreted. Next: BPP on the bisexual species only (val ×2, nai, mix) for
τ and θ; the parthenogens through MSC-I with hybridisation nodes, or per-locus/per-block parental assignment first
(affinity along chromosomes), and the label question (unp mix-like) checked against the assembly papers.
