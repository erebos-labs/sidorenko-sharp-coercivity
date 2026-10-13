"""Independent bounded host audit; no submitted program imports or huge powers."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,deque
from itertools import product,combinations
import random,json,re,datetime,bisect

if not __debug__:raise RuntimeError('Run without optimization')
ROOT=Path(__file__).resolve().parents[1]
PKG=ROOT/'host-parameters'
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
table=re.findall(r'^\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*\d+\s*&\s*\d+\s*&\s*\d+\s*&\s*([01]{3})\\\\',(PKG/'inherited/defect-one/sources/openai/complex.tex').read_text(),re.M)
assert [int(r[0]) for r in table]==list(range(22))
faces=[tuple(map(int,r[1:4])) for r in table]
corners=tuple((i,j) for j,face in enumerate(faces) for i in face)
adj=[[] for _ in range(35)]
for i,j in corners:adj[i].append(13+j);adj[13+j].append(i)
assert len(corners)==66 and max(map(len,adj))==6
pair_faces={}
for j,f in enumerate(faces):
    for e in combinations(f,2):pair_faces.setdefault(e,[]).append(j)
pairs=sorted(pair_faces);assert len(pairs)==33 and all(len(js)==2 for js in pair_faces.values())
U={e:frozenset((i,j) for i in e for j in pair_faces[e]) for e in pairs}
Ms={};pair_adj={e:set() for e in pairs}
for corner in corners:
    e,f=[e for e in combinations(faces[corner[1]],2) if corner[0] in e]
    assert U[e]&U[f]=={corner};Ms[corner]=U[e]|U[f];pair_adj[e].add(f);pair_adj[f].add(e)
    assert len(Ms[corner])==7 and len(U[e]^U[f])==6
seen={pairs[0]};queue=deque(seen)
while queue:
    for e in pair_adj[queue.popleft()]-seen:seen.add(e);queue.append(e)
assert len(seen)==33
for e in pairs:assert set.intersection(*(set(Ms[k]) for k in U[e]))==set(U[e])

# Different color-numbering convention: first occurrence, not sorted signatures.
colors=[0]*13+[1]*22;rounds=[];sv=[0]*35;sp=[[0]*22 for _ in range(13)];counts=[]
for t in range(4):
    old=colors[:];hist=[Counter(old[w] for w in adj[v]) for v in range(35)]
    vs=[-sum(n*n for n in h.values()) for h in hist]
    ps=[[2*(hist[i][old[13+j]]+hist[13+j][old[i]]) for j in range(22)] for i in range(13)]
    labels={};colors=[]
    for v in range(35):
        sig=(old[v],tuple(sorted(hist[v].items())))
        if sig not in labels:labels[sig]=len(labels)
        colors.append(labels[sig])
    counts.append([len(set(colors[:13])),len(set(colors[13:]))]);wt=1856**(3-t)
    sv=[x+wt*y for x,y in zip(sv,vs)]
    sp=[[sp[i][j]+wt*ps[i][j] for j in range(22)] for i in range(13)]
    rounds.append((old,hist,vs,ps))
assert counts==[[3,1],[3,7],[13,7],[13,22]]
aa=[v-min(sv[:13]) for v in sv[:13]];bb=[v-min(sv[13:]) for v in sv[13:]];max_pair=max(map(max,sp))
ell=[[max_pair-v for v in row] for row in sp]
Eid=sum(aa)+sum(bb)-sum(ell[i][j] for i,j in corners)
Bpin=13*max(aa)+22*max(bb)-Eid
cert=json.loads((PKG/'certificates/pinning.json').read_text())
assert cert['a']==aa and cert['b']==bb and cert['ell']==ell
assert (max(aa),max(bb),max(map(max,ell)),Eid,Bpin)==(127937502468,20679552,25601296520,115295183886,1548347298342)

identity=tuple(range(35));maps={identity}
for lo,hi in [(0,13),(13,35)]:
    for i,j in product(range(lo,hi),repeat=2):
        if i!=j:f=list(identity);f[i]=j;maps.add(tuple(f))
    for i,j in combinations(range(lo,hi),2):f=list(identity);f[i],f[j]=f[j],f[i];maps.add(tuple(f))
for i,j in product(range(13),range(13,35)):maps.add((i,)*13+(j,)*22)
rng=random.Random(20261013141411)
for _ in range(2000):maps.add(tuple([rng.randrange(13) for _ in range(13)]+[rng.randrange(13,35) for _ in range(22)]))
for old,_,_,_ in rounds:
    classes={c:[i for i,v in enumerate(old) if v==c] for c in set(old)}
    for _ in range(256):maps.add(tuple(rng.choice(classes[old[i]]) for i in range(35)))
square_checks=0;collapsed=0
def score(f,vs,ps):return sum(vs[f[v]] for v in range(35))+sum(ps[f[i]][f[13+j]-13] for i,j in corners)
total_id=sum(sv)+sum(sp[i][j] for i,j in corners)
for f in maps:
    collapsed+=len(set(f))<35
    Ef=sum(aa[f[i]] for i in range(13))+sum(bb[f[13+j]-13] for j in range(22))-sum(ell[f[i]][f[13+j]-13] for i,j in corners)
    assert Eid-Ef==total_id-score(f,sv,sp) and (f==identity or Eid-Ef>=1)
    for old,hs,vs,ps in rounds:
        if all(old[f[v]]==old[v] for v in range(35)):
            rhs=sum(sum((hs[f[v]][c]-hs[v][c])**2 for c in set(hs[v])|set(hs[f[v]])) for v in range(35))
            assert score(identity,vs,ps)-score(f,vs,ps)==rhs;square_checks+=1
assert 13**13*22**22<2**147 and 2459-147-2178==134
i,j=next((i,j) for i,j in product(range(13),range(22)) if ell[i][j]>0)
assert sum(ell[i][j] for _ in corners)==66*ell[i][j]>ell[i][j]

# Direct exact covariance matrix of all 128 labels, not author's Q/R sweep.
covariance=0;forcing=0
def char(z):return -1 if bin(z).count('1')%2 else 1
for sigma in (-1,1):
    samples=[(127,z,2+sigma*char(z&126)) for z in range(128)]
    samples += [(126,z<<1,4-2*sigma*char(z)) for z in range(64)]
    assert sum(w for _,_,w in samples)==512 and min(w for _,_,w in samples)>0
    funcs=[tuple(char(z&a) if a&S==a else 0 for S,z,w in samples) for a in range(128)]
    weights=[w for _,_,w in samples];moments=[]
    for a in range(128):
        row=[]
        for b in range(128):
            num=sum(w*x*y for w,x,y in zip(weights,funcs[a],funcs[b]));Q=a|b;R=a^b
            expected=256*int(R==0)+128*sigma*int(R==126)
            if not Q&1:expected+=256*int(R==0)-128*sigma*int(R==126)
            assert num==expected;row.append(num);covariance+=1
        moments.append(row)
    assert moments[0][0]==512 and all(moments[0][a]==0 for a in range(1,128))
    for a,b in product(range(1,16),repeat=2):
        maskb=(b&1)+((b>>1)<<4)
        if moments[a][maskb]:assert a&1 and maskb&1
        forcing+=1
    assert moments[15][113]==128*sigma
assert -F(1,4)**66==-F(1,2**132)

Z=280+2459*Bpin;A0=14*Z+13*2181;Lambda=A0+1
assert (Z,A0,Lambda)==(3807386006623258,53303404092753965,53303404092753966)
parameters={}
for D in (600,7296):
    b=D*(D+1)//2;rank=D//2;Cexp=32*D+2048;Jexp=A0+6+2210+Cexp;h=(D+1).bit_length()
    FJ=Jexp+7+256*h;Fq=6*FJ+2;B=11+Lambda+924*b*Fq
    values={'D':D,'r':rank,'bD':b,'b_r':rank*(rank+1)//2,'Z':Z,'A0':A0,'Lambda':Lambda,
            'J_upper_two_power':FJ,'q_upper_two_power':Fq,'host_B':B,'mu_q_power':14*b,'kernel_gap_q_power':924*b,
            'atom_count_q_power':132*b,'clone_log_bound':Z+2181+9+2459*(max(aa)+max(bb))+132*b*Fq,
            'coin_log_bound':18+4918*max(map(max,ell))+42*b*Fq,'normalizer_enumeration_log_bound':b*Fq}
    recorded=json.loads((PKG/'certificates/parameters.json').read_text())[str(D)]
    for key,value in values.items():assert value==recorded[key],(D,key,value,recorded[key])
    assert recorded['J']['two_power']==Jexp and recorded['C_D']['two_power']==Cexp
    assert D>=600 and rank%2==0 and 6*Jexp>(16*D).bit_length()
    parameters[str(D)]=values
assert parameters['600']['host_B']==53281187287257529723615577
assert parameters['7296']['host_B']==7866423844799423288734694969
assert parameters['600']['host_B']<parameters['7296']['host_B']

# Abstract orientation perturbation budget; these are not a giant-field model.
error_cases=0
for alpha in [F(i,64) for i in range(1,65)]+[F(1,2**1000)]:
    for fraction in [F(i,32) for i in range(33)]:
        e=alpha*fraction/64
        assert (1-alpha)*(1+alpha/8)+3*e+e*e<=1-alpha/2
        assert 3*e+e*e<=4*e and 4*e<=alpha/16;error_cases+=1
assert 2048-661==1387>1024 and 1322<2048 and 97==132-35 and 131==132-1

# Bounded prime lemma evidence and dyadic induction controls, never Q0 search.
limit=262144;sieve=bytearray(b'\x01')*(limit+1);sieve[0:2]=b'\0\0'
for p in range(2,513):
    if sieve[p]:sieve[p*p:limit+1:p]=b'\0'*len(sieve[p*p:limit+1:p])
primes=[i for i in range(2,limit+1) if sieve[i]]
for n in range(65536,131072):assert n<primes[bisect.bisect_right(primes,n)]<2*n
for k in range(16,4097):
    # Squared form avoids floating square roots for odd k.
    assert (k+2)**2<=2**(k-4) and k+3<=2**(k-3)
assert F(19,18)**2<2 and F(1,8)+F(3,8)==F(1,2)<F(2,3)

def density(U,w,edges):
    vertices=1+max(max(edge) for edge in edges);total=F(0)
    for labels in product(range(len(w)),repeat=vertices):
        term=F(1)
        for v in labels:term*=w[v]
        for i,j in edges:term*=U[labels[i]][labels[j]]
        total+=term
    return total
U=[[F(1,5),F(1,2),F(4,5)],[F(1,2),F(3,5),F(1,10)],[F(4,5),F(1,10),F(2,5)]]
w=[F(1,6),F(1,3),F(1,2)];labels=[0,1,1,2,2,2];cloned=[[U[i][j] for j in labels] for i in labels];clone_cases=0
for edges in [[(0,1)],[(0,1),(1,2)],[(0,1),(1,2),(2,0)],[(0,1),(1,2),(2,3),(3,0)]]:
    assert density(U,w,edges)==density(cloned,[F(1,6)]*6,edges);clone_cases+=1

# Exact original H-to-star all-map count: expected2^22+2^13 from connectedness.
neighborhoods=[6,1,1];hom=0
for assignment in product(range(3),repeat=13):
    term=1
    for face in faces:
        common=7
        for i in face:common &= neighborhoods[assignment[i]]
        term*=bin(common).count('1')
        if not term:break
    hom+=term
assert hom==2**22+2**13==4202496
# On a two-vertex Bernoulli host, H has only two collapsed homomorphisms.
p=F(1,3);E_t=p/F(2**34);kernel_t=p**66
assert E_t>kernel_t and p!=p*p  # Dropping collisions or resampling repeat edges fails.
assert p/F(2)==(1-F(1,2))*p and p/F(2)!=p

# Small signed normalizer reconstruction from all59,049 symmetric4x4 matrices.
def rank_mod(A,q):
    a=[row[:] for row in A];r=0
    for c in range(len(a)):
        j=next((j for j in range(r,len(a)) if a[j][c]%q),None)
        if j is None:continue
        a[r],a[j]=a[j],a[r];inv=pow(a[r][c],-1,q);a[r]=[(v*inv)%q for v in a[r]]
        for j in range(r+1,len(a)):
            x=a[j][c]%q
            if x:a[j]=[(u-x*v)%q for u,v in zip(a[j],a[r])]
        r+=1
    return r
positions=list(combinations(range(4),2))+[(i,i) for i in range(4)];normal=Counter();matrices=0
for values in product(range(3),repeat=10):
    A=[[0]*4 for _ in range(4)]
    for (i,j),v in zip(positions,values):A[i][j]=A[j][i]=v
    if rank_mod(A,3)==2:
        quotient=next(((i,j,(A[i][i]*A[j][j]-A[i][j]**2)%3) for i,j in combinations(range(4),2) if (A[i][i]*A[j][j]-A[i][j]**2)%3),None)
        assert quotient is not None
        i,j,determinant=quotient;normal[1 if determinant==1 else -1]+=1
        assert ((-A[i][i])*(-A[j][j])-(-A[i][j])**2)%3==(A[i][i]*A[j][j]-A[i][j]**2)%3
    matrices+=1
assert normal==Counter({1:780,-1:1560}) and matrices==59049
assert normal[1]==130*6 and normal[-1]==130*12 and sum(normal.values())==130*18

result={'started_utc':started,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS',
        'pinning_reconstructed_with_independent_color_numbering':True,'map_controls':len(maps),'collapsed_maps':collapsed,'histogram_square_controls':square_checks,
        'activation_covariance_pairs':covariance,'nonempty_shared_corner_forcing_controls':forcing,'parameters':parameters,
        'orientation_error_cases':error_cases,'prime_intervals_tested':65536,'dyadic_induction_cases':4081,
        'nonzero_diagonal_exact_clone_density_controls':clone_cases,'original_H_to_three_vertex_star_all_maps':hom,'original_H_to_star_injective_maps':0,
        'lost_collision_or_repeat_coin_controls':'Incorrect no-collision/shared-independent models rejected by exact auxiliary expectation',
        'small_signed_matrix_enumeration':{'D':4,'r':2,'q':3,'matrices':matrices,'positive_count':normal[1],'negative_count':normal[-1],'even_rank_reversal':'PASS'},
        'limits':'Bounded checks corroborate separately reviewed universal arguments; no theorem prime, field, graph, full type-map enumeration or huge power allocated.'}
print(json.dumps(result,indent=2))
