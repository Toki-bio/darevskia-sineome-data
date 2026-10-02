#!/bin/bash
R=/data/V/toki/sol_v2_runs
O=/data/V/toki/Darevskia_v2
N=dva-mix-v2
mkdir -p $R/scratch-v2
T0=$(date +%s); echo "START $(date +%F\ %T)" > $R/$N.timing
cd /data/V/toki/SINE_orth_loc_v2 && echo "COMMIT $(git rev-parse HEAD)" >> $R/$N.timing
PYTHON=/usr/local/bin/python3.12 /data/V/toki/SINE_orth_loc_v2/SINE_orth_loc_flexible.sh \
  -g1 $O/genomes/dva.fna -g2 $O/genomes/mix.fna -s $R/inputs/dar_squam1.fa \
  -b1 $R/inputs/dva-dar_squam1.bed -b2 $R/inputs/mix-dar_squam1.bed -n1 dva -n2 mix \
  -o $R/$N -t 24 --scratch $R/scratch-v2 --force 2>&1 \
 | tee $R/$N.stdout \
 | gawk '!/INFO|M::|BWTInc|bwa_index|^Processing|^C[0-9]+R|^[[:space:]]*$/ { print strftime("%T"), $0; fflush() }' > $R/$N.stages.log
echo "EXIT ${PIPESTATUS[0]} $(date +%F\ %T) elapsed=$(( $(date +%s)-T0 ))s" >> $R/$N.timing
