#!/bin/bash
# run_pair.sh C1WITHC2   e.g. run_pair.sh dva-nai
# one SINE_orth_loc v2 pairwise run: guarded, prelinked indexes, logged, idempotent
set -u
PROJ=/data/V/toki/Darevskia_v2
cd "$PROJ"; set -a; source "$PROJ/conf.sh"; set +a
pair="$1"
c1="${pair%-*}"; c2="${pair#*-}"
out="$PROJ/pairs/$pair"
log() { echo "[$(date +%F\ %T)] [$pair] $*"; }

[ -f "$PROJ/logs/STOP" ] && { log "STOP requested - exiting"; exit 0; }
[ -f "$out/.done" ] && { log "already done"; exit 0; }
[ -f "$out/.skipped_chrom" ] && { log "previously skipped (chrom clash)"; exit 0; }

mkdir -p "$out"

for f in "$PROJ/genomes/$c1.fna" "$PROJ/genomes/$c2.fna" \
         "$PROJ/beds/$c1-$SINE_NAME.bed" "$PROJ/beds/$c2-$SINE_NAME.bed"; do
  if [ ! -s "$f" ]; then log "MISSING INPUT $f"; exit 1; fi
done

# chromosome-name clash guard (species labels would silently corrupt the orth table)
comm -12 <(cut -f1 "$PROJ/genomes/$c1.fna.fai" | sort) \
         <(cut -f1 "$PROJ/genomes/$c2.fna.fai" | sort) > "$out/chrom_overlap.txt"
if [ -s "$out/chrom_overlap.txt" ]; then
  n=$(wc -l < "$out/chrom_overlap.txt")
  log "!! CHROMOSOME-NAME CLASH ($n shared names) - SKIPPING pair"
  touch "$out/.skipped_chrom"
  echo -e "$pair\tskipped_chrom_clash\t$n\t-" >> "$PROJ/summary_pairs.tsv"
  exit 0
fi

t0=$(date +%s)

# prelink genome + indexes into work dir so the run skips re-indexing
WD="$out/work"
mkdir -p "$WD" "$PROJ/scratch/$pair"
for g in "$c1" "$c2"; do
  ln -sf "$PROJ/genomes/$g.fna" "$WD/$g.bnk"
  for ext in fai sa pac bwt ann amb; do
    ln -sf "$PROJ/genomes/$g.fna.$ext" "$WD/$g.bnk.$ext"
  done
done
ln -sf "$PROJ/$SINE_NAME.q" "$WD/$SINE_NAME.q"

log "launching SINE_orth_loc_v2 (t=$THREADS_PER_PAIR, scratch=$PROJ/scratch/$pair)"
if bash "$PROJ/repo/SINE_orth_loc-main/SINE_orth_loc_flexible.sh" \
    -g1 "$PROJ/genomes/$c1.fna" -g2 "$PROJ/genomes/$c2.fna" \
    -s "$PROJ/$SINE_NAME.q" \
    -b1 "$PROJ/beds/$c1-$SINE_NAME.bed" -b2 "$PROJ/beds/$c2-$SINE_NAME.bed" \
    -n1 "$c1" -n2 "$c2" \
    -o "$out" --scratch "$PROJ/scratch/$pair" -t "$THREADS_PER_PAIR" --force \
    > "$out/run.log" 2>&1 && [ -f "$out/results/orth_$c1-$c2.tsv" ]; then
  cnt=$(tr '\n' ' ' < "$out/results/MP_PM_SINE_$c1-$c2.txt" 2>/dev/null | cut -c1-80)
  dt=$(( $(date +%s) - t0 ))
  echo -e "$pair\tok\t${dt}s\t$cnt" >> "$PROJ/summary_pairs.tsv"
  touch "$out/.done"
  rm -rf "$PROJ/scratch/$pair"
  log "DONE in ${dt}s"
  exit 0
fi
dt=$(( $(date +%s) - t0 ))
echo -e "$pair\tFAIL\t${dt}s\t-" >> "$PROJ/summary_pairs.tsv"
log "FAILED after ${dt}s - tail of run.log:"; tail -5 "$out/run.log"
exit 1
