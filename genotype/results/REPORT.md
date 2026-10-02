# Genotyping D. valentini individuals from Illumina reads

Pan-SINEome built without dvl (15 pairs), templates from dva, nai, mix, arm, unp, unm.

## Individual 245 (the dvl assembly) vs its own assembly

GQ >= 0:

| assembly state | 0/0 | 0/1 | 1/1 | no call |
|---|---|---|---|---|
| P | 0 | 0 | 0 | 82250 |
| A | 0 | 0 | 0 | 20580 |
| U | 0 | 0 | 0 | 23142 |
| X | 0 | 0 | 0 | 693 |
| new | 0 | 0 | 0 | 2274 |

homozygous calls agreeing with the assembly: 0, contradicting: 0 (0.00%), heterozygous: 0

GQ >= 20:

| assembly state | 0/0 | 0/1 | 1/1 | no call |
|---|---|---|---|---|
| P | 0 | 0 | 0 | 82250 |
| A | 0 | 0 | 0 | 20580 |
| U | 0 | 0 | 0 | 23142 |
| X | 0 | 0 | 0 | 693 |
| new | 0 | 0 | 0 | 2274 |

homozygous calls agreeing with the assembly: 0, contradicting: 0 (0.00%), heterozygous: 0

## Genotype counts per individual

| individual | 0/0 | 0/1 | 1/1 | no call |
|---|---|---|---|---|
| v245 | 0 | 0 | 0 | 128939 |
| v5_38 | 885 | 131 | 5583 | 122340 |
| atis | 13544 | 834 | 64948 | 49613 |
| teg | 10710 | 829 | 57581 | 59819 |

## Agreement between individuals (loci called in both, GQ >= 20)

| | v245 | v5_38 | atis | teg |
|---|---|---|---|---|
| v245 | 0.0% of 0 | 0.0% of 0 | 0.0% of 0 | 0.0% of 0 |
| v5_38 | 0.0% of 0 | 100.0% of 93 | 100.0% of 78 | 98.6% of 70 |
| atis | 0.0% of 0 | 100.0% of 78 | 100.0% of 2424 | 96.9% of 387 |
| teg | 0.0% of 0 | 98.6% of 70 | 96.9% of 387 | 100.0% of 1261 |
