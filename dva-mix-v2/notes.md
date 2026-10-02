# dva vs mix, rerun with fixed code (2026-10-02/03)

**Code:** Toki-bio/SINE_orth_loc, branch `claude/wonderful-tesla-x39s12`, commit **a53c4eb4573d73aeddd152ead434544b2152e5e7** (includes 8ff1ecf per-copy rescue + chromosome-list species detection, and a53c4eb genome-1-first pair order). The earlier run in `../dva-mix/` used 11771e3.
**Where:** KIT `/data/V/toki/sol_v2_runs/dva-mix-v2` (old `dva-mix` untouched). Same inputs and settings as before: `dva.fna`, `mix.fna`, `dar_squam1.fa`, dva/mix beds from `Darevskia_v2`, `-t 24`, `PYTHON=/usr/local/bin/python3.12`, `--force`. Only the scratch dir differs (`scratch-v2`). Launcher: `run_dva-mix-v2.sh`. Exit 0.
All numbers below come from `checks_v2.py` / `gap_v2.py` (outputs in `checks_v2.out`, `gap_v2.out`).

## Layout
Like `../dva-mix/`: `summary.txt`, `MP_PM_SINE_dva-mix.txt`, `orth_dva-mix.tsv.gz`, `clusters_dva-mix.tsv`, `rescue_dva-mix.tsv`, `stat_*`, `statbed_*.gz`, `alignments/aln_dva-mix_*.aln.gz`, `pipeline.log.gz`. Extra: `stage_timestamps.txt` (key stage lines with times), `stages.log.gz` (every non-noise log line with a timestamp), `dva-mix-v2.timing`, check scripts and outputs, `dup_test/` (item 4).

## Timing (MSK, 2026-10-02 21:09:41 -> 2026-10-03 00:50:37)
Total **13,256 s (3 h 40 m 56 s)**; old run 12,624 s (+632 s). Stage starts are logged timestamps; the resolve step does not log its own start, so its start is taken as the end of the bwa step.

| stage | start | end | duration |
|---|---|---|---|
| bwa index dva.bnk | 21:09:56 | 21:39:37 | 29 m 41 s |
| bwa index mix.bnk | 21:39:37 | 22:04:27 | 24 m 50 s |
| mapping flanks (both directions) | 22:04:27 | 22:04:49 | 22 s |
| clustering, stage 1+2 | 22:04:49 | 22:05:36 | 47 s |
| doubles alignment | 22:05:36 | 22:47:13 | 41 m 37 s |
| multi stage (align multi clusters) | 22:47:13 | 23:44:57 | 57 m 44 s |
| rescue: prepare | 23:44:57 | 23:45:13 | 16 s |
| rescue: bwa mem -a (2 directions) | 23:45:13 | ~23:45:27 | ~15 s |
| rescue: resolve (python local alignment) | ~23:45:27 | 00:38:03 | ~52 m 36 s |
| rescue: alignment of rescued pairs | 00:38:04 | 00:50:08 | 12 m 04 s |
| bundle compression | 00:50:08 | 00:50:24 | 16 s |
| gathering statistics, orth table | 00:50:24 | 00:50:37 | 13 s |

Indexing is 55 min of the total; resolve is the slowest rescue step.

## Checks
**a. stat_multi** is non-empty: 11,174 lines (SINE 8,796, PM 1,782, MP 595, badRF 1). Clusters actually resolved in the multi stage (final alignment, in the orth table): **10,346 of 20,530** multi clusters, **SINE 8,011, PM 1,765, MP 570**; 10,184 stay `multi_unresolved`. The 828 extra stat_multi lines (SINE 785, MP 25, PM 17, badRF 1) belong to clusters that have a stat line but no final alignment, so they are not in the orth table; their copies went to rescue. I did not find out why those alignments are not kept as final. Not investigated.

**b. Doubles regression: identical.** New orth rows for double clusters (classes from `clusters_dva-mix.tsv`) = 61,261; old non-M rows = 61,261; identical as a multiset and in the same order. Note that the new orth also has 10,346 multi-resolved rows with `C…R` names, so "cluster name not starting with M" alone gives 71,607 rows; the 61,261 doubles are selected by cluster class. No non-M row falls in neither class. Total 91,690 = 61,261 + 10,346 + 20,083.

**c. Rescued rows:** 20,083 `M…R` rows; species1 = dva in **all 20,083**, species2 = mix in all. Exceptions: **0**.

**d. Totals (MP / PM / SINE)**

| | MP | PM | SINE |
|---|---|---|---|
| old run (main) | 10,935 | 9,325 | 41,001 |
| previous new run, corrected | 12,786 | 14,349 | 63,673 |
| **this run, MP_PM_SINE file** | **12,941** | **14,514** | **64,235** |
| recount from orth (dva+ mix- = PM, dva- mix+ = MP) | 12,941 | 14,514 | 64,235 |

File and recount agree; 0 rows where the status column differs from the species columns. By origin (MP / PM / SINE): doubles 10,935 / 9,325 / 41,001 (same as old), multi 570 / 1,765 / 8,011, rescue 1,436 / 3,424 / 15,223. Versus the previous corrected run: +155 MP, +165 PM, +562 SINE. The rescue contribution fell from 29,547 rows (old, per-cluster rescue) to 20,083 because the multi stage now resolves 10,346 clusters first and rescue only handles the 40,678 copies left (58,169 before).

**e. Rescue outcomes by the copy's species** (40,678 copies):

| species of copy | resolved | no_concordant_pair | ambiguous | no_hit | total |
|---|---|---|---|---|---|
| dva | 18,078 | 6,523 | 1,471 | 191 | 26,263 |
| mix | 6,846 | 3,719 | 3,802 | 48 | 14,415 |
| both | 24,924 | 10,242 | 5,273 | 239 | 40,678 |

ambiguous:2 specifically: mix 3,365, dva 973 (previous run: 6,997 and 1,026).

**f. Reconciliation: no remaining gap.**
- 24,924 resolved copies map to **22,968 distinct pairs**: 1,956 pairs were found from both a dva copy and a mix copy (exactly 2 copies each, none with more) and are written once. That is `stat_rescue` = 22,968 lines.
- 22,968 pairs = **20,083** that passed ComPair.sh and are in the orth table (SINE 15,223, PM 3,424, MP 1,436; all 20,083 present, none extra) + **2,885** rejected by ComPair.sh (badRF 2,268, shortRF 319, badLF 288, lfSINE 10).
- `clusters_dva-mix.tsv` counts per copy: rescued SINE 17,014 + PM 3,425 + MP 1,437 = 21,876, plus qc_failed 3,048 = 24,924. The differences are the duplicate-pair copies: 21,876 - 20,083 = 1,793 (1,791 SINE, 1 PM, 1 MP) and 3,048 - 2,885 = 163; 1,793 + 163 = 1,956.
- The old 3,397 vs 3,572 is the same mechanism (pairs rejected vs copies whose pair was rejected; difference 175). I did not recheck that on the old data.

**g. Run time:** see Timing above.

## Item 4: duplicated regions in dva?
Method: the resolver's intermediates (SAMs, bwa indexes, prepare files) were deleted at the end of the run, so its exact placements are not recoverable. Instead: 200 random mix copies (seed 1) with outcome `ambiguous:2` (of 3,365); mix copy ±5 kb vs the dva genome with megablast; hits merged into loci (same scaffold and strand, within 15 kb); the two best loci by summed bit score; a 10 kb window centred on each; the two dva windows aligned to each other with megablast (dust off); aligned bases counted as union of HSPs on window A (minimap2 is not installed on KIT). Per copy: `dup_test/dup_results.tsv`; code: `dup_v2.py`.

Results (200 copies; all had ≥2 dva loci; 197 had any alignment between the two windows):
- Fraction of window A aligned to B: min 0.00, 10th pct 0.08, 25th 0.32, **median 0.92**, 75th 1.00, 90th 1.00.
- Identity of the aligned part: min 82.3, 25th 97.6, **median 99.4**, 75th 99.8, max 100.
- ≥10% aligned: 176; ≥50% aligned: 136 (135 of them ≥95% identity); ≥80% aligned: **111 (55.5%), all ≥95% identity**.
- All 200 pairs are on different scaffolds (none on the same one), so this is not tandem duplication.

Reading: for about half or more of these ambiguous copies, the two "equally good" dva placements lie in nearly identical (median 99.4%) ~10 kb regions on different scaffolds. That fits uncollapsed haplotigs or segmental duplications in the dva assembly. Whether they are haplotigs or true duplications cannot be told from this test; read coverage or ploidy information would be needed.
Caveats: the loci come from re-mapping with blastn, not from the resolver, so they may not be exactly its placements. No control set was run (for example copies with a unique placement). The 64 copies with <50% aligned are not explained: they could be short duplications or different placements.

## Operational note
The SSH tunnel from the Windows machine dropped twice during the run ("Software caused connection abort"); the run is `setsid`/`nohup` on KIT and was not affected. The tunnel was re-established through a saved PuTTY session with keepalives.
