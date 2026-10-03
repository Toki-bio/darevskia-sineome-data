# Genotyping D. valentini individuals from Illumina reads

Pan-SINEome built without dvl (15 pairs), templates from dva, nai, mix, arm, unp, unm.

## Individual 245 (the dvl assembly) vs its own assembly

GQ >= 0:

| assembly state | 0/0 | 0/1 | 1/1 | no call |
|---|---|---|---|---|
| P | 245 | 749 | 74180 | 7076 |
| A | 18097 | 242 | 98 | 2143 |
| U | 2431 | 170 | 7258 | 13283 |
| X | 259 | 23 | 269 | 142 |
| new | 16 | 7 | 620 | 1631 |

homozygous calls agreeing with the assembly: 92277, contradicting: 343 (0.37%), heterozygous: 991

GQ >= 20:

| assembly state | 0/0 | 0/1 | 1/1 | no call |
|---|---|---|---|---|
| P | 187 | 554 | 52601 | 28908 |
| A | 14942 | 148 | 27 | 5463 |
| U | 1848 | 110 | 3048 | 18136 |
| X | 220 | 16 | 166 | 291 |
| new | 7 | 3 | 349 | 1915 |

homozygous calls agreeing with the assembly: 67543, contradicting: 214 (0.32%), heterozygous: 702

## Genotype counts per individual

| individual | 0/0 | 0/1 | 1/1 | no call |
|---|---|---|---|---|
| v245 | 21048 | 1191 | 82425 | 24275 |
| v5_38 | 19936 | 970 | 78857 | 29176 |
| atis | 19163 | 992 | 77460 | 31324 |
| teg | 18468 | 1160 | 76824 | 32487 |

## Agreement between individuals (loci called in both, GQ >= 20)

| | v245 | v5_38 | atis | teg |
|---|---|---|---|---|
| v245 | 100.0% of 74226 | 97.3% of 23843 | 96.5% of 13939 | 96.4% of 9481 |
| v5_38 | 97.3% of 23843 | 100.0% of 31277 | 98.4% of 8739 | 98.3% of 6285 |
| atis | 96.5% of 13939 | 98.4% of 8739 | 100.0% of 18102 | 98.4% of 4615 |
| teg | 96.4% of 9481 | 98.3% of 6285 | 98.4% of 4615 | 100.0% of 12403 |
