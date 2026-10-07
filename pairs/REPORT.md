# 21 pairs, SINE_orth_loc v2.2 (SOL bdc2134, run 37462585105, registry 37559304934)

| pair | rows v2.0 (SINE/PM/MP) | rows v2.2 (SINE/PM/MP/MISSING) | nested rows | superseded | shard s (max) |
|---|---|---|---|---|---|
| arm-dvl | 77122/1173/5784 | 123051/2052/6165/855 | 9927 | 1111 | 3033 |
| arm-unm | 54072/2728/6188 | 96218/4309/6759/23 | 7975 | 956 | 2554 |
| arm-unp | 35324/9469/11848 | 75137/13673/13845/25 | 4654 | 768 | 2941 |
| dva-arm | 53893/4177/927 | 112669/4845/1312/58 | 9685 | 1057 | 2694 |
| dva-dvl | 84078/455/2203 | 121441/677/2410/807 | 9970 | 1054 | 2738 |
| dva-mix | 41001/9325/10935 | 68375/15577/12922/60 | 4520 | 737 | 2931 |
| dva-nai | 42627/4279/7889 | 100531/7625/9598/75 | 7714 | 1090 | 3042 |
| dva-unm | 58398/2704/2700 | 91380/4375/3041/49 | 7683 | 894 | 2381 |
| dva-unp | 38888/10679/8999 | 65893/17010/10649/52 | 4292 | 701 | 2718 |
| mix-arm | 39711/11003/7953 | 82419/13922/9748/26 | 5589 | 846 | 3095 |
| mix-dvl | 58975/12663/11776 | 72324/15654/13712/984 | 4711 | 634 | 3161 |
| mix-unm | 46993/10598/10871 | 60736/13902/12551/7 | 4547 | 736 | 2584 |
| mix-unp | 49496/7835/7740 | 64763/10310/8993/9 | 4606 | 707 | 2506 |
| nai-arm | 39012/7438/7349 | 107708/10318/9088/53 | 8044 | 1145 | 3286 |
| nai-dvl | 63904/6038/9023 | 107519/8541/10165/943 | 7912 | 1041 | 3362 |
| nai-mix | 39186/8797/11177 | 80657/12914/13329/26 | 5393 | 913 | 3017 |
| nai-unm | 55055/2886/6288 | 99717/4300/6865/23 | 9858 | 1062 | 2570 |
| nai-unp | 49173/4495/7528 | 93806/6213/8298/25 | 8777 | 1059 | 2718 |
| unm-dvl | 82996/3735/3948 | 97843/4496/4622/882 | 7879 | 839 | 2710 |
| unp-dvl | 56607/12304/11531 | 69188/14928/13530/986 | 4497 | 607 | 3203 |
| unp-unm | 45276/10606/10276 | 57794/13547/11985/7 | 4390 | 702 | 2657 |

## Registry dar8

```
Traceback (most recent call last):
  File "/home/runner/work/darevskia-sineome-data/darevskia-sineome-data/sol/sine_registry.py", line 833, in <module>
    main()
  File "/home/runner/work/darevskia-sineome-data/darevskia-sineome-data/sol/sine_registry.py", line 829, in main
    args.func(args)
  File "/home/runner/work/darevskia-sineome-data/darevskia-sineome-data/sol/sine_registry.py", line 436, in cmd_build
    with open_text(path) as fh:
         ^^^^^^^^^^^^^^^
  File "/home/runner/work/darevskia-sineome-data/darevskia-sineome-data/sol/sine_registry.py", line 58, in open_text
    return gzip.open(path, 'rt') if path.endswith('.gz') else open(path)
                                                              ^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'nest/nest_dva.caution.bed'

```
