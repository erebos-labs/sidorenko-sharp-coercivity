#!/usr/bin/env python3
"""Independent exact reconstruction. Imports no submitted Python modules."""
from fractions import Fraction as F
from itertools import combinations, product
from collections import defaultdict, Counter
from pathlib import Path
from datetime import datetime, timezone
from math import lcm, sqrt
import json
import re

PKG = Path(__file__).resolve().parent.parent

def now():
    return datetime.now(timezone.utc).isoformat()

def inverse(mat):
    size = len(mat)
    a = [[F(x) for x in row] + [F(i == j) for j in range(size)]
         for i, row in enumerate(mat)]
    for j in range(size):
        assert a[j][j] > 0, ('positive elimination pivot', j)
        scale = a[j][j]
        a[j] = [x / scale for x in a[j]]
        for i in range(size):
            if i != j:
                q = a[i][j]
                a[i] = [x - q*y for x,y in zip(a[i],a[j])]
    return [row[size:] for row in a]

def b(x):
    return F(x*(x+1),2)

def connected(adj):
    seen = {next(iter(adj))}
    todo = list(seen)
    while todo:
        x = todo.pop()
        for y in adj[x] - seen:
            seen.add(y); todo.append(y)
    return len(seen) == len(adj)

def main():
    report = {'started_utc':now(), 'method':'Parse source complex.tex; exact rational inversion; independently evaluate source gain and beta, no submitted code imports.'}
    text = (PKG/'sources/openai/complex.tex').read_text()
    # Parse the seven integer columns and literal three-bit code in source Table 1.
    table = re.findall(r'^\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*([01]{3})\\\\',text,re.M)
    assert [int(row[0]) for row in table] == list(range(22))
    faces = [tuple(map(int,row[1:4])) for row in table]
    bits = [row[7] for row in table]
    literal = json.loads((PKG/'sources/global/experiment/template_data.json').read_text())['original']
    assert literal == {'faces':list(map(list,faces)), 'bits':bits}
    edgefaces = defaultdict(list)
    for j,f in enumerate(faces):
        for e in combinations(f,2): edgefaces[e].append(j)
    edges = sorted(edgefaces)
    assert len(edges)==33 and all(len(js)==2 for js in edgefaces.values())
    edgeidx = {e:i for i,e in enumerate(edges)}
    rho = [F(sum(a!=b for a,b in zip(bits[js[0]],bits[js[1]]))-1,3) for e,js in sorted(edgefaces.items())]
    assert sum(rho)==2 and min(rho)>=0
    K = [[F(0) for e in edges] for e in edges]
    adj = {i:set() for i in range(33)}
    dual = {i:set() for i in range(22)}
    for js in edgefaces.values():
        a,c = js; dual[a].add(c); dual[c].add(a)
    for face in faces:
        ids = [edgeidx[e] for e in combinations(face,2)]
        for i,j in combinations(ids,2):
            K[i][i]+=F(1,48); K[j][j]+=F(1,48)
            K[i][j]-=F(1,48); K[j][i]-=F(1,48)
            adj[i].add(j); adj[j].add(i)
    assert connected(adj) and connected(dual)
    for i,r in enumerate(rho): K[i][i] += r/4
    inv = inverse(K)
    cert = json.loads((PKG/'original_certificate.json').read_text())
    assert [[int(48*x) for x in row] for row in K]==cert['A']
    assert all(inv[i][j]==F(48*cert['inverse_numerator'][i][j],cert['inverse_denominator']) for i in range(33) for j in range(33))
    ell = [1-r/4 for r in rho]
    z = [sum(inv[i][j]*ell[j] for j in range(33)) for i in range(33)]
    H = sum(ell[i]*z[i] for i in range(33))
    def margin(B,i):
        linear = 2*B-z[i]
        return linear,linear*linear-H*inv[i][i]
    allmargins = [margin(257,i) for i in range(33)]
    assert all(a>0 and c>0 for a,c in allmargins)
    fail256 = [list(edges[i]) for i in range(33) if any(x<=0 for x in margin(256,i))]
    assert fail256
    numerator = [[x/48 for x in row] for row in inv]
    tau = lcm(*(x.denominator for row in numerator for x in row))
    assert tau == 270558215904 == cert['inverse_denominator']
    N = [[int(x*tau) for x in row] for row in numerator]
    bv = [int(12-3*r) for r in rho]
    u = [sum(N[i][j]*bv[j] for j in range(33)) for i in range(33)]
    Hnum = sum(bv[i]*u[i] for i in range(33))
    assert Hnum==3716263103433120==cert['Hnum']
    first = [257*tau-2*x for x in u]
    second = [first[i]**2-4*Hnum*N[i][i] for i in range(33)]
    assert [24*x for x in first]==cert['coordinate_linear_margins']
    assert [576*x for x in second]==cert['coordinate_squared_margins']
    ext = [(z[i]+sqrt(float(H*inv[i][i])))/2 for i in range(33)]
    report['matrix']={'all_inverse_entries_matched':1089,'coordinate_inequalities_passed':33,'tau':tau,'Hnum':Hnum,'minimum_unscaled_linear_margin':min(first),'minimum_unscaled_squared_margin':min(second),'threshold_256_rejected_edges':fail256,'maximum_real_coordinate_bound_approx':max(ext),'maximum_bound_edge':list(edges[ext.index(max(ext))]),'M':256,'D':3072,'positive_pivots':33}
    oldK = [[(K[i][j]-(rho[i]/4 if i==j else 0))/3+(rho[i]/4 if i==j else 0) for j in range(33)] for i in range(33)]
    oldinv=inverse(oldK)
    old=json.loads((PKG/'sources/global/experiment/certificates.json').read_text())['templates']['original']
    assert all(oldinv[i][j]==F(144*old['adjugate'][i][j],old['denominator']) for i in range(33) for j in range(33))
    oldz=[sum(oldinv[i][j]*ell[j] for j in range(33)) for i in range(33)]
    oldH=sum(ell[i]*oldz[i] for i in range(33))
    assert all(2*609-oldz[i]>0 and (2*609-oldz[i])**2>oldH*oldinv[i][i] for i in range(33))
    assert any(2*608-oldz[i]<=0 or (2*608-oldz[i])**2<=oldH*oldinv[i][i] for i in range(33))
    report['baseline']={'all_inverse_entries_matched':1089,'coordinate_inequalities_passed':33,'strict_threshold':609,'threshold_608_rejected':True,'M':608,'D':7296}
    # Count all seven lower-activity masks separately, including their pair identity.
    counters=Counter(); eqs=Counter()
    for hs in product(range(7),repeat=3):
        for c in range(min(hs)+1):
            s = [h-c for h in hs]
            D0 = c+sum(s)
            Ds = {D0+(D0%2),12*max(hs)}
            for D in Ds:
                if D<c+sum(s):continue
                C=(D+1)*c+sum(b(x) for x in s)
                beta=C/2-sum(b(h) for h in hs)/6
                V=sum((hs[i]-hs[j])**2 for i,j in combinations(range(3),2))
                for mask in range(7):
                    active=[i for i in range(3) if mask&(1<<i)]
                    gain=b(hs[next(i for i in range(3) if i not in active)]//2) if len(active)==2 else F(0)
                    S=beta-gain
                    assert S>=0 and S>=F(max(hs)**2,24)-F(max(hs),12)
                    assert S>=F(V,48)-F(sum(hs),2)
                    expected=c==0 and (all(h==0 for h in hs) or (len(active)==2 and hs[next(i for i in range(3) if i not in active)]==2 and sum(hs)==2))
                    assert (S==0)==expected
                    counters[str(mask)]+=1
                    if S==0:eqs[str(mask)]+=1
    # Fully active: evaluate beta minus SOURCE GAIN, not author's slack rewrite.
    full=0; full_eq=0
    for M in range(5):
        D=12*M; r=D//2
        for hs in product(range(M+1),repeat=3):
            if max(hs)!=M:continue
            for c in range(min(hs)+1):
                d=D-c;s=[h-c for h in hs]
                for u0 in range(min(c,r)+1):
                    rp=r-u0; delta=2*u0-c
                    if not 0<=rp<=d or sum(s)>d:continue
                    for ps in product(*(range(x+1) for x in s)):
                        ts=[s[i]-ps[i] for i in range(3)];P=sum(ps)
                        if any(ts[i]>ps[i]+delta for i in range(3)):continue
                        for v in range(min(ps)+delta+1):
                            w=F(d-3*delta,2)-P+v
                            if w<0:continue
                            gain=(r+c+1)*u0-2*u0*u0+sum(b(x) for x in s)-delta*P-sum(x*x for x in ps)-v*w-sum(b(x) for x in ts)+b(v)
                            beta=F((D+1)*c+sum(b(x) for x in s),2)-sum(b(h) for h in hs)/6
                            S=beta-gain
                            eta=F(c-delta,2);ns=[2*ps[i]-ts[i] for i in range(3)]
                            S0=F(3*c*(c-1),4)+F(sum(n*n+(c-1)*n+3*c*p for n,p in zip(ns,ps)),6)
                            bc=d-3*c-2*delta+2-4*P;bv0=d-3*delta-2*P+v-1
                            assert S==S0+eta*bc/2+F(v*bv0,2)
                            assert bc>=D-12*M+6*c+2
                            assert bv0>=D-6*M+2*c+v-1
                            assert S>=0
                            expected=eta==v==0 and ((c==1 and all(x==0 for x in ps+tuple(ts))) or (c==0 and all((p,t) in {(0,0),(1,1)} for p,t in zip(ps,ts))))
                            assert (S==0)==expected
                            V=sum((hs[i]-hs[j])**2 for i,j in combinations(range(3),2))
                            assert S>=F(V,48)-F(sum(hs),2)
                            full+=1;full_eq+=S==0
    counters['7']=full;eqs['7']=full_eq
    report['activity_tests']={'lower_domains':'h_i=0..6; 0<=c<=min h_i; minimal even feasible D and D=12 max h','full_domain':'M=max h=0..4; D=12M; all integer source necessary gain tuples','tests_by_mask':dict(counters),'zero_slacks_by_mask':dict(eqs),'all_equality_classifications_matched':True}
    deg=[sum(i in e for e,rho0 in zip(edges,rho) if rho0==0) for i in range(13)]
    assert deg==[3,6,3,6,4,2,4,4,4,6,4,6,4]
    count=sum((2*x)*(2*x-1)//2 for x in deg)
    assert count==468
    exp=max(-k*k+2*m*k-2*m+count for m in range(1,29) for k in range(2,2*m))
    assert exp==1196
    report['residual']={'zero_excess_degrees':deg,'sum_binomial_caps':count,'maximum_count_exponent':exp,'nondirect_exponent_saving_at_D3072':3072-exp,'support_span_prefactor_less_than_2_pow_63':2**28*55*2**29<2**63}
    report['finished_utc']=now(); report['status']='PASS'
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
