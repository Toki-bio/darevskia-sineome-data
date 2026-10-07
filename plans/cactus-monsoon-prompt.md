# Prompt for Claude Code (VS Code, Monsoon): Minigraph-Cactus alignment of the 7 Darevskia assemblies

Paste everything below the line into Claude Code in the VS Code session that is connected to Monsoon.

---

You are working on NAU Monsoon (Slurm) for the Darevskia pan-SINEome project (Sergei Kosushkin, user `sk4386`).
Goal: a whole-genome alignment of 7 Darevskia assemblies with **Minigraph-Cactus** (`cactus-pangenome`), used as an
independent check of SINE presence/absence calls from SINE_orth_loc (pan-SINEome dar8). Work in gates: **do not
start a gate before the previous one has passed its check, and stop and report to me at every gate.**

## Rules

- Work under `/scratch/sk4386/darcactus/` (create it). Never write outside it except your conda/env caches there.
- Everything heavy runs as Slurm jobs (`--partition=core`; up to 28 CPUs and up to 480G per job have been used on
  this account before), chained with `--dependency=afterok` and `--kill-on-invalid-dep=yes`, so nothing depends on
  the login session (the Monsoon proxy drops now and then). Logs go to `/scratch/sk4386/darcactus/logs/`.
- Before the first job, read the current Cactus docs (github.com/ComparativeGenomicsToolkit/cactus, `doc/pangenome.md`
  and the release notes) and use the **latest release**. Prefer the Apptainer/Singularity image
  (`docker://quay.io/comparative-genomics-toolkit/cactus:<version>`) if `apptainer` or `singularity` exists on Monsoon;
  otherwise the release binary tarball with its Python venv, as the docs describe. Record the exact version.
- Run Cactus on a single node per job (`--maxCores` and `--maxMemory` set to the Slurm allocation, Toil jobStore and
  `--workDir` on /scratch); do not use the Toil Slurm batch system unless a single node proves too small.
- Keep every command in scripts under `/scratch/sk4386/darcactus/code/` (sbatch files + one submit script), so the run
  is reproducible. Write a `README.md` there as you go: versions, commands, wall time and peak memory per step
  (`sacct -j <id> --format=JobID,Elapsed,MaxRSS,ReqMem,State`).

## Data

Assemblies (NCBI GenBank FTP, `https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/<3>/<3>/<3>/<acc>_<name>/`; find the
directory name by listing the accession directory). Keep only the first word of each FASTA header (the GenBank
accession), as in the SINE_orth_loc runs, so coordinates match dar8:

| code | accession | assembly |
|---|---|---|
| dva | GCA_034642135.1 | Dar_val_2.0 (D. valentini) |
| dvl | GCA_024498535.1 | Dval_245 (D. valentini, fragmented legacy assembly, 31,777 sequences) |
| nai | GCA_034642065.1 | Dar_nair_1.0 (D. nairensis) |
| mix | GCA_034641385.1 | Dar_mix_1.0 (D. mixta) |
| arm | GCA_034641395.1 | Dar_arm_1.0 (D. armeniaca, parthenogen, valentini × mixta) |
| unp | GCA_032766555.1 | D.uni.pHiFi.1.0 (D. unisexualis paternal haplotype) |
| unm | GCA_032766585.1 | D.uni.mHiFi.1.0 (D. unisexualis maternal haplotype, 152 sequences) |

Use **unm** as the reference (`--reference unm`). Known issue to keep in mind: arm (1.93 Gb), nai (1.77 Gb) and dva (1.65 Gb)
are larger than unm/unp/mix (~1.4 Gb) and probably retain haplotigs; Minigraph-Cactus will see these as duplications.
Do not try to fix that; report it.

SINE annotation and the pan-SINEome (public repo github.com/Toki-bio/darevskia-sineome-data):
- copies: `old/beds/<code>-dar_squam1.bed.gz` (branch `main`)
- pan-SINEome dar8: `pan/dar8.groups.tsv.gz` (branch `actions/pairs21`); columns `group, family, subfamily, pattern,
  n_P, n_A, n_U, n_X, n_M, pairs, flags`, then one column per genome (dva dvl nai mix arm unp unm). A cell is a copy
  `chrom:start-end(strand)` (state P), an empty insertion site `chrom:pos(strand)` (state A), or empty. `pattern` is
  the 7 states in that column order (P present, A empty site, U no data, X ambiguous, M window at a contig end).
- the simulation used for gate 1: github.com/Toki-bio/SINE_orth_loc, `tests/simulate_genomes2.py` (writes 4 genomes
  aaa/bbb/ccc/ddd, `truth.tsv` with every insertion and the lineage it happened on, `<sp>.sites.tsv` with coordinates).

## Gate 0: installation

1. Install Cactus (latest release) as above; run the docs' own small pangenome example (evolverPrimates) as a Slurm job.
2. Check: it finishes, writes `.full.hal`, `.gfa.gz`, `.vcf.gz`; `halStats` on the HAL lists the genomes.
Report: version, how it is installed, time and memory of the example.

## Gate 1: toy with a known answer (the SINE_orth_loc simulation)

1. Clone SINE_orth_loc, run `python3 tests/simulate_genomes2.py` in an empty directory (it writes the 4 genomes and the
   truth tables; read its docstring).
2. `cactus-pangenome` on aaa, bbb, ccc, ddd (reference aaa), producing a HAL.
3. Write `code/hal_sine_check.py`: for every true insertion in `truth.tsv`, take its insertion junction in a genome that
   has it, `halLiftover` a few bp on each side of the junction to every other genome, and call P (lifted onto a
   copy of the SINE, i.e. the other genome has the element there), A (both junction sides land adjacent, no element
   between), or unaligned. Compare with the truth (which genomes carry the insertion).
4. Check: at least 95 % of insertions recover the true presence/absence pattern in all four genomes; list every
   failure by event class (`plain, repflank, flankindel, host, nested, close, satellite`) and by whether ddd's
   contig ends or ccc's duplicated region are involved. Report these numbers before going on.

## Gate 2: partial real run (one reference chromosome)

1. Download the 7 assemblies (one sbatch, with checksums from NCBI's `md5checksums.txt`), simplify headers, `samtools faidx`.
2. `cactus-pangenome` with `--reference unm --refContigs <the longest unm sequence>` (all 7 genomes as input; see the
   docs for how other contigs are handled), HAL output.
3. Run `hal_sine_check.py` in its real-data mode: for every dar8 group with a site on that unm sequence, lift the
   insertion junction from each genome that has a copy (P) or an empty site (A) to every other genome; per group and
   genome compare the HAL call with the dar8 state. Output a table (group, genome, dar8 state, HAL call, lifted
   coordinate) and a summary: agreement per state (P/A), per genome pair, and for the flags `multicopy`, `close`,
   `dimer`, `nested`, `satellite`, `unannotated`.
4. Check: the job finished; record wall time and peak memory, and extrapolate to the whole genome. **Stop and send
   me the numbers.** I decide whether the full run goes ahead and with which resources.

## Gate 3: full run (only after my go-ahead)

All unm sequences, the same settings; then `hal_sine_check.py` on all dar8 groups. Keep the HAL, GFA and VCF on /scratch.

## Deliverables

- `/scratch/sk4386/darcactus/` with `code/`, `logs/`, `README.md`, the HAL files, and `results/`:
  `gate1_truth_check.tsv`, `gate2_dar8_vs_hal.tsv(.gz)`, `summary.md`.
- If git with push access to github.com/Toki-bio/darevskia-sineome-data is set up on Monsoon, put `code/`, `README.md`
  and the small result tables (not the HAL/GFA/VCF) on a new branch `cactus` in a folder `cactus/`; otherwise leave them
  on /scratch and tell me the paths.
- At each gate, a short report: what ran, versions, time and memory, the check numbers, problems, and the next step.
