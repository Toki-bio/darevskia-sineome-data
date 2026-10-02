import re,collections
N='/data/V/toki/sol_v2_runs/dva-mix-v2/results/'
cl={}
for l in open(N+'clusters_dva-mix.tsv'):
    p=l.rstrip('\n').split('\t'); cl[p[0]]=p
orth={l.split('\t')[1] for l in open(N+'orth_dva-mix.tsv')}
c=collections.Counter(); ex=[]
for l in open(N+'stat_multi_dva-mix'):
    p=l.split(); n=re.search(r'(C\d+R)',p[0]).group(1)
    k=(cl[n][1] if n in cl else 'absent', cl[n][3].split(':')[0] if n in cl else '-', n in orth, p[1])
    c[k]+=1
    if not k[2] and len(ex)<3: ex.append(l.strip()[:200]+' | '+'\t'.join(cl.get(n,['?'])))
for k,v in sorted(c.items(),key=lambda x:-x[1]): print(v,k)
print(*ex,sep='\n')
