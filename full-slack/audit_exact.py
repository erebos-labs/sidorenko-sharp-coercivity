#!/usr/bin/env python3
"""Same-session adversarial arithmetic replay using separate formulations.

Uses no primary-checker import: exact Gaussian elimination reconstructs K^-1;
full slack is evaluated from its n(n-1) formula rather than Q minus loss.
Finite cases below are regression tests, not the proof of the universal claim.
"""
import sys
if not __debug__:
    raise RuntimeError('Optimized Python is refused.')
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent

def require(ok,label):
    if not ok:raise RuntimeError(label)

def full_slack_tuple(data):
    c,d,z,v=(F(data[k]) for k in ('c','d','delta','v'))
    p=list(map(F,data['p']));t=list(map(F,data['t']));P=sum(p);T=sum(t)
    w=(d-3*z)/2-P+v
    require(c>=abs(z) and d>=P+T and v>=0 and w>=0,'audit feasibility scalar')
    require(all(a>=0 and b>=0 and b<=a+z and v<=a+z for a,b in zip(p,t)),'audit individual feasibility')
    n=[2*a-b for a,b in zip(p,t)];ss=[a+b for a,b in zip(p,t)]
    S=(c*(d+z-1)-z*(d+2)+2*z*z)/4+sum(nn*(nn-1)/6+z*a-c*(a+b)/6 for nn,a,b in zip(n,p,t))+v*w-v*(v+1)/2
    V=sum((ss[i]-ss[j])**2 for i,j in combinations(range(3),2))
    R=S-V/48+(3*c+P+T)/12
    return S,V,R

def inverse(matrix):
    n=len(matrix)
    a=[[F(matrix[i][j]) for j in range(n)]+[F(i==j) for j in range(n)] for i in range(n)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        require(pivot is not None,'audit singular matrix')
        a[j],a[pivot]=a[pivot],a[j]
        z=a[j][j];a[j]=[x/z for x in a[j]]
        for i in range(n):
            if i!=j:
                z=a[i][j]
                if z:a[i]=[x-z*y for x,y in zip(a[i],a[j])]
    return [row[n:] for row in a]

def main():
    examples=json.loads((ROOT/'examples.json').read_text())
    for ex in examples:
        S,V,R=full_slack_tuple(ex['tuple'])
        require((S,V,R)==tuple(F(ex['expected'][k]) for k in ('S','V','remainder')),'independent slack specialization '+ex['name'])
        require(R>=-F(17,16),'audit new bound example')
    # Fixed mixed triples straddling q_i=b, with no optimization or search.
    mixed=0
    for z,v in [(F(1),F(0)),(F(1),F(1,2)),(F(1),F(1)),(F(1),F(2)),(F(5,2),F(5,2)),(F(1,2),F(3,2))]:
        b=max(F(0),v-z)
        for qq in [(-z,0,b+z),(-z,-z/2,b),(b,b,b),(-z,b-z/4,b+z/4)]:
            p=[max(F(0),q,v-z) for q in qq];t=[p[i]-qq[i] for i in range(3)]
            e=max(F(0),sum(qq)+3*z-2*v);d=sum(p)+sum(t)+e
            S,V,R=full_slack_tuple({'c':z,'d':d,'delta':z,'v':v,'p':p,'t':t})
            require(R>=-F(17,16),'mixed max/hinge regression')
            mixed+=1
    pub=json.loads((ROOT/'sources/published/variance/original_certificate.json').read_text())
    new=json.loads((ROOT/'certificates/original.json').read_text())
    faces=pub['template']['faces'];bits=pub['template']['bits'];ef={}
    for j,f in enumerate(faces):
        for pair in combinations(f,2):ef.setdefault(pair,[]).append(j)
    edges=sorted(ef);idx={e:i for i,e in enumerate(edges)};n=len(edges)
    K=[[F(0) for _ in edges] for _ in edges]
    for f in faces:
        loc=[idx[p] for p in combinations(f,2)]
        for i,j in combinations(loc,2):
            K[i][i]+=F(1,48);K[j][j]+=F(1,48);K[i][j]-=F(1,48);K[j][i]-=F(1,48)
    rho=[]
    for e in edges:
        j,k=ef[e];rho.append(F(sum(a!=b for a,b in zip(bits[j],bits[k]))-1,3))
    for i in range(n):K[i][i]+=rho[i]/4
    KI=inverse(K)
    require(all(KI[i][j]==F(48*new['inverse_numerator'][i][j],new['inverse_denominator']) for i in range(n) for j in range(n)),'independent inverse comparison')
    ell=[F(1,6)-r/4 for r in rho]
    zvec=[sum(KI[i][j]*ell[j] for j in range(n)) for i in range(n)]
    H=sum(a*b for a,b in zip(ell,zvec));Gamma=F(187,8)
    margins=[]
    for i in range(n):
        lhs=2*F(new['strict_bound_B'])-zvec[i]
        rhs=(H+4*Gamma)*KI[i][i]
        require(lhs>0 and lhs*lhs>rhs,'independent direct ellipsoid bound '+str(i))
        margins.append(lhs*lhs-rhs)
    require(new['sufficient_even_D']%2==0 and new['sufficient_even_D']>=12*new['M_bound'] and new['sufficient_even_D']-1196>=F(1,6),'independent final dimension gates')
    print(json.dumps({'status':'PASS','full_slack_examples':len(examples),'additional_mixed_hinge_regressions':mixed,'independent_Fraction_Gaussian_inverse_entries':n*n,'direct_rational_ellipsoid_coordinates':n,'H':str(H),'Gamma':str(Gamma),'minimum_direct_squared_margin':str(min(margins)),'final_even_D':new['sufficient_even_D'],'review_status':'Same-session separate implementation, not independent human acceptance or a formal proof.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
