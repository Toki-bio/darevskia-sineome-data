# /data/V/toki/Darevskia_v2/conf.sh - project configuration, sourced by master + workers
# sourced with `set -a` so all settings export to subshells. Edit only this file to tune.

PROJ=/data/V/toki/Darevskia_v2
PY=/usr/local/bin/python3.12
SEAR2KLOOP_BIN=/data/V/toki/bin/sear2kloop
REPO_URL=https://codeload.github.com/Toki-bio/SINE_orth_loc/zip/refs/heads/main
THREADS_PER_PAIR=16
MAX_CONC_PAIRS=3
MAX_CONC_BEDS=2
MAX_CONC_INDEX=3

# code -> raw download
#   dva = GCA_034642135.1  D. valentini   Dar_val_2.0    (new 2025 assembly)
#   dvl = GCA_024498535.1  D. valentini   Dval_245       (legacy; genome+bed ready on /data/W)
#   nai = GCA_034642065.1  D. nairensis   Dar_nair_1.0   (maternal parent of D. unisexualis)
#   arm = GCA_034641395.1  D. armeniaca   Dar_arm_1.0    (parthenogen, valentini x mixta)
#   mix = GCA_034641385.1  D. mixta       Dar_mix_1.0    (maternal parent of D. armeniaca)
#   unp = GCA_032766555.1  D. unisexualis D.uni.pHiFi.1.0 (parthenogen, PATERNAL haplotype)
#   unm = GCA_032766585.1  D. unisexualis D.uni.mHiFi.1.0 (parthenogen, MATERNAL haplotype)
GZ_RAW=(
  "dva,GCA_034642135.1_Dar_val_2.0_genomic.fna.gz"
  "nai,GCA_034642065.1_Dar_nair_1.0_genomic.fna.gz"
  "arm,GCA_034641395.1_Dar_arm_1.0_genomic.fna.gz"
  "mix,GCA_034641385.1_Dar_mix_1.0_genomic.fna.gz"
  "unp,GCA_032766555.1_D.uni.pHiFi.1.0_genomic.fna.gz"
  "unm,GCA_032766585.1_D.uni.mHiFi.1.0_genomic.fna.gz"
)

DVL_GENOME=/data/W/toki/Dval/dval.fna
DVL_BED=/data/W/toki/Dval/dval-darsquam1.bed

SINE_Q_SRC=/data/W/toki/Roma/darsquam1.q
SINE_NAME=dar_squam1

# order: parent-parent first, then parent-parthenogen, same-species/QA (dvl) pairs last
PAIRS=(
  "dva-nai" "dva-mix" "nai-mix"
  "dva-unp" "dva-unm" "nai-unp" "nai-unm" "dva-arm" "mix-arm"
  "unp-unm" "arm-unp" "arm-unm" "mix-unp" "mix-unm" "nai-arm"
  "dva-dvl" "nai-dvl" "mix-dvl" "arm-dvl" "unp-dvl" "unm-dvl"
)

SPECIES_ALL=dva,dvl,nai,mix,arm,unp,unm
SPECIES_CORE=dva,nai,mix,arm,unp,unm
