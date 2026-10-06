#!/bin/bash
# tools for SINE_orth_loc on a GitHub runner; SOL_REF = SINE_orth_loc commit
set -euo pipefail
sudo rm -rf /usr/share/dotnet /usr/local/lib/android /opt/ghc /opt/hostedtoolcache/CodeQL || true
sudo apt-get update -q
sudo apt-get install -y -q mafft hmmer bwa samtools bedtools bedops gawk pigz > /dev/null
sudo apt-get install -y -q seqkit > /dev/null 2>&1 || true
sudo update-alternatives --set awk /usr/bin/gawk || sudo ln -sf /usr/bin/gawk /usr/local/bin/awk
mkdir -p "$HOME/bin"
if ! command -v seqkit > /dev/null; then
    curl -sSfL --retry 5 https://github.com/shenwei356/seqkit/releases/download/v2.8.2/seqkit_linux_amd64.tar.gz | tar xz -C "$HOME/bin"
fi
if ! command -v esl-alipid > /dev/null; then
    # easel miniapps are not in every hmmer package: build them
    curl -sSfL --retry 5 http://eddylab.org/software/hmmer/hmmer-3.4.tar.gz | tar xz -C /tmp
    (cd /tmp/hmmer-3.4 && ./configure -q > /dev/null && make -j4 > /dev/null && cp easel/miniapps/esl-alipid "$HOME/bin/")
fi
git clone -q https://github.com/Toki-bio/SINE_orth_loc sol && git -C sol checkout -q "$SOL_REF"
echo "$HOME/bin" >> "$GITHUB_PATH"; echo "$PWD/sol" >> "$GITHUB_PATH"
export PATH="$HOME/bin:$PWD/sol:$PATH"
for t in mafft esl-alipid seqkit bedtools samtools sam2bed bwa nhmmer ComPair.sh; do printf '%s: %s\n' "$t" "$(command -v $t)"; done
awk --version | head -1; seqkit version; mafft --version 2>&1 | head -1; df -h / | tail -1; nproc; free -g | head -2
