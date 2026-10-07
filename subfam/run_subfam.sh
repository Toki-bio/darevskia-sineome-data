#!/bin/bash
# run_subfam.sh SAMPLE.fa (copy names <species>_<locus>; no '|': it makes EMBOSS cons hang) REF.fa OUTDIR [BATCH=50]
# SubFam (github.com/Toki-bio/SubFam, SubFam.sh unchanged, on PATH as SUBFAM) on the sample, then:
#   OUTDIR/subfam_input.aln.fa   reference + chunk consensi in SubFam's final alignment (reference first)
#   OUTDIR/chunks/<chunk>.aln.fa each chunk's copies, aligned (MAFFT)
#   OUTDIR/chunks.tsv, chunks.copies.tsv  (chunk_table.py)
set -euo pipefail
SAMPLE=$(readlink -f "$1"); REF=$(readlink -f "$2"); OUT=$(readlink -m "$3"); BATCH=${4:-50}
HERE=$(dirname "$(readlink -f "$0")"); SUBFAM=${SUBFAM:?path to SubFam.sh}
mkdir -p "$OUT/run" "$OUT/chunks"
cd "$OUT/run"
cp "$SAMPLE" sample.fa
bash "$SUBFAM" sample.fa "$BATCH" > subfam.log 2>&1 || { tail -20 subfam.log; exit 1; }
seqret -sequence sample.msf -outseq stdout -osformat2 fasta -auto > input.aln.fa
mafft --quiet --add "$REF" --keeplength input.aln.fa > with_ref.aln.fa
refname=$(head -1 "$REF" | sed 's/^>//; s/ .*//')
seqkit grep -p "$refname" with_ref.aln.fa > "$OUT/subfam_input.aln.fa"
seqkit grep -v -p "$refname" with_ref.aln.fa >> "$OUT/subfam_input.aln.fa"
ls sample_*.bnk | xargs -P "$(nproc)" -I % sh -c "mafft --quiet --thread 1 % > '$OUT/chunks/%.aln.fa'"
python3 "$HERE/chunk_table.py" --dir . --prefix sample --ref "$REF" -o "$OUT/chunks.tsv"
echo "$(ls sample_*.bnk | wc -l) chunks, $(grep -c '>' "$OUT/subfam_input.aln.fa") sequences in subfam_input.aln.fa"
