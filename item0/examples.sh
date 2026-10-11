#!/bin/bash
# examples.sh GENOME.fa NAMED.bed FLANK_GROUPS.tsv N OUTDIR : N random twin pairs (class twin), each copy with 200 bp on both
# sides in element orientation, aligned with MAFFT -> OUTDIR/pair_<k>.aln.fa (upper case = SINE copy)
set -euo pipefail
G=$1; B=$2; P=$3; N=$4; O=$5; mkdir -p "$O"
awk -F'\t' 'NR > 1 && $7 == "twin"' "$P" | shuf --random-source=<(yes) -n "$N" | awk -F'\t' '{print NR"\t"$1"\t"$2"\t"$3"\t"$4"\t"$5}' > "$O/pairs.tsv"
while IFS=$'\t' read k a b side id len; do
  : > "$O/p.fa"
  for c in $a $b; do
    read ch s e st < <(awk -F'\t' -v n="$c" '$4 == n {print $1, $2, $3, $6; exit}' "$B")
    l=$(( s > 200 ? s - 200 : 0 )); r=$(( e + 200 ))
    if [ "$st" = "-" ]; then samtools faidx -i "$G" "$ch:$((l+1))-$r"; else samtools faidx "$G" "$ch:$((l+1))-$r"; fi | sed "1s/.*/>$c/" >> "$O/p.fa"
  done
  mafft --quiet --auto "$O/p.fa" > "$O/pair_$k.aln.fa"
done < "$O/pairs.tsv"; rm -f "$O/p.fa"
