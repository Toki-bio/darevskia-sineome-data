import collections, csv, re, sys
N='/data/V/toki/sol_v2_runs/dva-mix-v2/results/'
OLD='/data/V/toki/sol_v2_runs/dva-mix/results/'
def rows(p):
    with open(p) as f:
        r=[l.rstrip('\n').split('\t') for l in f]
    return r[0], r[1:]
hn,new=rows(N+'orth_dva-mix.tsv'); ho,old=rows(OLD+'orth_dva-mix.tsv')
print('orth rows new',len(new),'old',len(old),'header same',hn==ho)
cl={}
for l in open(N+'clusters_dva-mix.tsv'):
    p=l.rstrip('\n').split('\t'); cl[p[0]]=p
dbl={c for c,p in cl.items() if p[1]=='double'}
mul={c for c,p in cl.items() if p[1]=='multi'}
isM=lambda r:r[1].startswith('M')
print('\n== a. stat_multi')
cnt=collections.Counter(); names=collections.defaultdict(set)
for l in open(N+'stat_multi_dva-mix'):
    p=l.split(); c=re.search(r'(C\d+R)',p[0]).group(1); cnt[p[1]]+=1; names[p[1]].add(c)
print('stat_multi lines',sum(cnt.values()),dict(cnt)); print('distinct clusters per class',{k:len(v) for k,v in names.items()},'union',len(set().union(*names.values())))
fate=collections.Counter(p[3] for c,p in cl.items() if p[1]=='multi'); print('clusters.tsv multi fates',dict(fate),'total multi clusters',len(mul))
print('\n== b. doubles regression')
nd=[r for r in new if not isM(r) and r[1] in dbl]; od=[r for r in old if not isM(r)]
print('new doubles rows',len(nd),'old non-M rows',len(od))
print('identical as multiset',collections.Counter(map(tuple,nd))==collections.Counter(map(tuple,od)),'identical in order',nd==od)
nm=[r for r in new if not isM(r) and r[1] in mul]; oth=[r for r in new if not isM(r) and r[1] not in dbl and r[1] not in mul]
print('new multi-resolved rows',len(nm),'non-M rows in neither double nor multi',len(oth))
print('\n== c. rescued rows')
nr=[r for r in new if isM(r)]
print('M rows',len(nr),'species1 counts',dict(collections.Counter(r[3] for r in nr)),'species2',dict(collections.Counter(r[6] for r in nr)))
print('\n== d. totals')
def recount(rs):
    c=collections.Counter()
    for r in rs:
        a,b=int(r[5])>0,int(r[8])>0
        c['SINE' if a and b else 'PM' if a else 'MP' if b else 'neither']+=1
    return c
print('file',open(N+'MP_PM_SINE_dva-mix.txt').read().split())
print('orth status col',dict(collections.Counter(r[2] for r in new)))
print('recount by species cols',dict(recount(new)))
for nm_,rs in (('doubles',nd),('multi',nm),('rescue',nr)):
    print(' ',nm_,'status',dict(collections.Counter(r[2] for r in rs)),'recount',dict(recount(rs)))
mism=sum(1 for r in new if r[2]!=('SINE' if int(r[5])>0 and int(r[8])>0 else 'PM' if int(r[5])>0 else 'MP')); print('rows where status != species recount:',mism)
print('\n== e. rescue outcomes by species')
res=[l.rstrip('\n').split('\t') for l in open(N+'rescue_dva-mix.tsv')][1:]
t=collections.Counter(); amb=collections.Counter()
for r in res:
    sp=r[0].split('|')[0]; o=r[2].split(':')[0]; t[(sp,o)]+=1
    if o=='ambiguous': amb[(sp,r[2])]+=1
for k in sorted(t): print(' ',k,t[k])
print('  per species total',{s:sum(v for (a,_),v in t.items() if a==s) for s in {a for a,_ in t}})
print('  ambiguous detail',dict(sorted(amb.items())))
print('\n== f. reconcile')
print('copies',len(res),'resolved',sum(1 for r in res if r[2].startswith('resolved')))
cp=collections.Counter(r[2].split(':')[1] for r in res if r[2].startswith('resolved:'))
print('distinct pairs referenced',len(cp),'copies sharing a pair (sum n-1)',sum(v-1 for v in cp.values()),'pairs with 2 copies',sum(1 for v in cp.values() if v==2),'>2',sum(1 for v in cp.values() if v>2))
sr={}
for l in open(N+'stat_rescue_dva-mix'):
    p=l.split(); sr[re.match(r'\./(M\d+R)',p[0]).group(1)]=p[1]
print('stat_rescue pairs',len(sr),dict(collections.Counter(sr.values())))
mrows=collections.Counter(r[1] for r in nr); print('orth M rows',len(nr),'distinct M clusters',len(mrows),'status',dict(collections.Counter(r[2] for r in nr)))
inorth=set(mrows); print('stat_rescue pairs in orth',len(inorth&set(sr)),'pairs not in orth',len(set(sr)-inorth),'orth M not in stat_rescue',len(inorth-set(sr)))
print('not-in-orth by stat class',dict(collections.Counter(sr[m] for m in set(sr)-inorth)))
cf=collections.Counter(p[3] for c,p in cl.items() if p[1]=='multi' or True)
print('clusters.tsv rescue column values (top)',collections.Counter(p[4] if len(p)>4 else '' for p in cl.values()).most_common(6))
