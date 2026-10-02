import random, re, subprocess, collections, os, sys, statistics
R='/data/V/toki/sol_v2_runs/'
W=R+'dup_test/'; os.makedirs(W,exist_ok=True)
G='/data/V/toki/Darevskia_v2/genomes/'
PAD=5000
def fai(p):
    d={}
    for l in open(p+'.fai'):
        f=l.split('\t'); d[f[0]]=int(f[1])
    return d
mixl=fai(G+'mix.fna'); dval=fai(G+'dva.fna')
def fetch(fa,c,s,e):
    out=subprocess.run(['samtools','faidx',fa,f'{c}:{s+1}-{e}'],capture_output=True,text=True).stdout.split('\n',1)[1].replace('\n','').upper()
    return out
def rc(s): return s.translate(str.maketrans('ACGTN','TGCAN'))[::-1]
rows=[l.rstrip('\n').split('\t') for l in open(R+'dva-mix-v2/results/rescue_dva-mix.tsv')][1:]
amb=[r for r in rows if r[0].startswith('mix|') and r[2]=='ambiguous:2']
print('mix ambiguous:2 copies',len(amb))
random.seed(1); samp=random.sample(amb,int(os.environ.get('NS','200')))
q=open(W+'q.fa','w'); meta={}
for i,r in enumerate(samp):
    m=re.match(r'mix\|(.+):(\d+)-(\d+)\(([+-])\)',r[0]); c,s,e=m.group(1),int(m.group(2)),int(m.group(3))
    a,b=max(0,s-PAD),min(mixl[c],e+PAD)
    seq=fetch(G+'mix.fna',c,a,b); q.write(f'>q{i}\n{seq}\n'); meta[f'q{i}']=(r[0],len(seq))
q.close()
if not os.path.exists(W+'dva.nsq') and not os.path.exists(W+'dva.00.nsq'):
    subprocess.run(['makeblastdb','-in',G+'dva.fna','-dbtype','nucl','-out',W+'dva'],check=True,stdout=subprocess.DEVNULL)
subprocess.run(['blastn','-task','megablast','-query',W+'q.fa','-db',W+'dva','-outfmt','6 qseqid sseqid pident length qstart qend sstart send bitscore','-evalue','1e-10','-num_threads','24','-max_target_seqs','50','-out',W+'q_vs_dva.tsv'],check=True)
hits=collections.defaultdict(list)
for l in open(W+'q_vs_dva.tsv'):
    f=l.split('\t'); hits[f[0]].append((f[1],float(f[2]),int(f[3]),int(f[4]),int(f[5]),int(f[6]),int(f[7]),float(f[8])))
def loci(hs):
    L=[]  # [chr,strand,lo,hi,bits,alnlen]
    for h in sorted(hs,key=lambda h:-h[7]):
        st='+' if h[5]<h[6] else '-'; lo,hi=min(h[5],h[6]),max(h[5],h[6])
        for l in L:
            if l[0]==h[0] and l[1]==st and lo<=l[3]+15000 and hi>=l[2]-15000:
                l[2]=min(l[2],lo); l[3]=max(l[3],hi); l[4]+=h[7]; l[5]+=h[2]; break
        else: L.append([h[0],st,lo,hi,h[7],h[2]])
    return sorted(L,key=lambda l:-l[4])
res=[]
for qn,(cid,qlen) in meta.items():
    L=loci(hits.get(qn,[]))
    if len(L)<2: res.append((qn,cid,len(L),None)); continue
    A,B=L[0],L[1]
    regs=[]
    for l in (A,B):
        mid=(l[2]+l[3])//2; lo,hi=max(0,mid-PAD),min(dval[l[0]],mid+PAD)
        s=fetch(G+'dva.fna',l[0],lo-1 if lo>0 else 0,hi); regs.append((l,lo,hi,s))
    open(W+'a.fa','w').write(f'>A\n{regs[0][3]}\n'); open(W+'b.fa','w').write(f'>B\n{regs[1][3]}\n')
    out=subprocess.run(['blastn','-task','megablast','-query',W+'a.fa','-subject',W+'b.fa','-outfmt','6 pident length qstart qend sstart send','-evalue','1e-10','-dust','no','-max_hsps','50'],capture_output=True,text=True).stdout
    cov=set(); idn=0; tl=0; n=0
    for l in out.splitlines():
        f=l.split('\t'); p,ln,qs,qe=float(f[0]),int(f[1]),int(f[2]),int(f[3]); n+=1
        new=set(range(min(qs,qe),max(qs,qe)+1))-cov; cov|=new; idn+=p*len(new); tl+=len(new)
    same=(A[0]==B[0] and abs((A[2]+A[3])-(B[2]+B[3]))//2<200000)
    res.append((qn,cid,len(L),dict(A=f'{A[0]}:{A[2]}-{A[3]}({A[1]})',B=f'{B[0]}:{B[2]}-{B[3]}({B[1]})',lenA=len(regs[0][3]),lenB=len(regs[1][3]),cov=len(cov),ident=(idn/tl if tl else 0),hsps=n,bitsA=A[4],bitsB=B[4],sameChr=A[0]==B[0],dist=(abs((A[2]+A[3])-(B[2]+B[3]))//2 if A[0]==B[0] else None))))
with open(W+'dup_results.tsv','w') as o:
    o.write('query\tmix_copy\tn_dva_loci\tdvaA\tdvaB\tregionLenA\tregionLenB\taligned_bp_of_A\tfrac_aligned\tpident\tn_hsps\tbitsA\tbitsB\tsame_chr\tdist\n')
    for qn,cid,n,d in res:
        if d: o.write('\t'.join(map(str,[qn,cid,n,d['A'],d['B'],d['lenA'],d['lenB'],d['cov'],round(d['cov']/d['lenA'],3),round(d['ident'],2),d['hsps'],round(d['bitsA']),round(d['bitsB']),d['sameChr'],d['dist']]))+'\n')
        else: o.write(f'{qn}\t{cid}\t{n}\t\t\t\t\t\t\t\t\t\t\t\t\n')
ok=[d for _,_,_,d in res if d]
print('queries',len(res),'with >=2 dva loci',len(ok),'with <2 loci',len(res)-len(ok))
fr=[d['cov']/d['lenA'] for d in ok]; idl=[d['ident'] for d in ok if d['cov']>0]
def q(v): 
    v=sorted(v); return [round(v[int(p*(len(v)-1))],3) for p in (0,.1,.25,.5,.75,.9,1)]
print('frac of A aligned to B  [min,10,25,50,75,90,max]',q(fr))
print('identity of aligned part',q(idl),'n with any alignment',len(idl))
print('aligned bp',q([d['cov'] for d in ok]))
for t in (0.1,0.5,0.8):
    print(f'frac aligned >= {t}:',sum(1 for x in fr if x>=t),'; of which ident>=95:',sum(1 for d in ok if d['cov']/d['lenA']>=t and d['ident']>=95))
print('same chromosome',sum(d['sameChr'] for d in ok),' <100kb apart',sum(1 for d in ok if d['dist'] is not None and d['dist']<100000))
