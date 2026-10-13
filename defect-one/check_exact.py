#!/usr/bin/env python3
"""Offline exact checks for the defect-one handoff; Python standard library.

The conventional proofs in PROOF.md and DOWNSTREAM.md establish the universal
claims. This program checks their algebra, fixed template, budgets, and controls.
It does not enumerate supports, construct the theorem-sized field, or prove Lean.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import json
from math import isqrt
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
class CheckFailure(Exception):
    pass

def need(condition, site):
    if not condition:
        raise CheckFailure(site)

class Poly:
    """Small sparse polynomial ring over Q, monomials are sorted name tuples."""
    def __init__(self, value=0):
        if isinstance(value, Poly): self.terms = dict(value.terms)
        elif isinstance(value, dict): self.terms = {m:F(c) for m,c in value.items() if c}
        else: self.terms = {(): F(value)} if value else {}
    def __add__(self, other):
        out=dict(self.terms)
        for m,c in Poly(other).terms.items(): out[m]=out.get(m,F(0))+c
        return Poly(out)
    __radd__=__add__
    def __neg__(self): return Poly({m:-c for m,c in self.terms.items()})
    def __sub__(self, other): return self+-Poly(other)
    def __rsub__(self, other): return Poly(other)+-self
    def __mul__(self, other):
        out={}
        for m,c in self.terms.items():
            for n,d in Poly(other).terms.items():
                z=tuple(sorted(m+n));out[z]=out.get(z,F(0))+c*d
        return Poly(out)
    __rmul__=__mul__
    def __truediv__(self, other): return self*F(1,F(other))
    def __pow__(self,n):
        need(isinstance(n,int) and n>=0,'polynomial_power_domain')
        out=Poly(1)
        for _ in range(n): out=out*self
        return out

def sym(name): return Poly({(name,):1})
def b2(x): return x*(x-1)/2

def symbolic(coeff):
    D,m,k,a,r,x,y,mu,z,t,tau = map(sym,'D m k a r x y mu z t tau'.split())
    checks=[]
    def same(lhs,rhs,label):
        need(not (Poly(lhs)-rhs).terms,'identity:'+label);checks.append(label)
    gain=coeff['gain_per_plane']; basis=coeff['basis_power_per_plane']
    same(k*(2*D-k)+2*m*(k-2)+gain*m-D*(2*k+a)+r,
         -D*a-k*k+2*m*k-2*m+r,'robust_actual_defect_exponent')
    same(-k*k+2*m*k-2*m+468,
         m*m-2*m+468-(k-m)**2,'robust_complete_square')
    same(1196-(m*m-2*m+468),(28-m)*(m+26),'robust_uniform_1196')
    same((gain-basis)*m,-2*m,'gain_after_full_basis_division')
    for inc in (0,1):
        same(b2(x+inc)-b2(x),inc*x,'endpoint_binomial_increment_'+str(inc))
    expected_costs={'111':2*D-x-y+mu,'000':mu,'001':x,'010':y,'011':z}
    expected_local={'111':mu,'000':mu,'001':x+y,'010':x+y,'011':z+x+y}
    for code,expected in expected_costs.items():
        vals=coeff['step_cost_coefficients'][code]
        need(len(vals)==5,'cost_vector_shape')
        cost=sum(c*v for c,v in zip(vals,(D,x,y,mu,z)))
        same(cost,expected,'step_cost_'+code)
        g,li,lj=map(int,code)
        need(coeff['defect_values'][code]==li+lj-2*g,'defect_value:'+code)
        same(cost+li*x+lj*y-2*D*g,expected_local[code],
             'containment_telescoping_'+code)
    same(-2*m+(t-tau)/2+tau,-2*m+(t+tau)/2,'defect_one_prefix_budget')
    same((468+22)/F(2)-2*m,245-2*m,'coarse_degree_envelope')
    same(241-(245-2*m),2*(m-2),'uniform_defect_one_remainder')
    same(4*D*m-4*x-m-4*m-4*D*m+(4*x+2*m)+2*m,-m,
         'inherited_direct_exponent')
    same(299+22*(D+47)+88,22*D+1421,'rank_layer_prefactor')
    same(22*5+55,165,'rank_layer_polynomial_power')
    same((32*D+2048-1)-(22*D+1421),10*D+626,'retained_envelope_second_half')
    same((32*D+2048-1)-170,32*D+1877,'retained_envelope_first_half')
    same((D-241)-1-62,D-304,'defect_one_absorption_margin')
    return checks

def blob_hash(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def source_bindings():
    pins=json.loads((ROOT/'SOURCES.json').read_text())
    for item in pins['bundled_sources']:
        data=(ROOT/item['local_path']).read_bytes()
        need(len(data)==item['bytes'],'source_length:'+item['local_path'])
        need(hashlib.sha256(data).hexdigest()==item['sha256'],'source_sha256:'+item['local_path'])
        need(blob_hash(data)==item['git_blob_sha1'],'source_git_blob:'+item['local_path'])
    return len(pins['bundled_sources'])

def connected(adj):
    if not adj: return True
    start=next(iter(adj));seen={start};todo=[start]
    for v in todo:
        for w in adj[v]:
            if w not in seen: seen.add(w);todo.append(w)
    return seen==set(adj)

def template_and_budget(c, coeff):
    text=(ROOT/'sources/openai/complex.tex').read_text()
    pattern=r'^\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*\d+\s*&\s*\d+\s*&\s*\d+\s*&\s*([01]{3})\\\\'
    parsed={int(m[1]):([int(m[i]) for i in (2,3,4)],m[5]) for m in re.finditer(pattern,text,re.M)}
    need(set(parsed)==set(range(22)),'source_face_table_parse')
    faces=[parsed[i][0] for i in range(22)];bits=[parsed[i][1] for i in range(22)]
    need(c['faces']==faces and c['bits']==bits,'fixed_template_source_binding')
    ef={}
    for j,f in enumerate(faces):
        for e in combinations(f,2): ef.setdefault(e,[]).append(j)
    edges=sorted(ef)
    need(len(edges)==33 and all(len(v)==2 for v in ef.values()),'pair_incidence_count')
    need(max(sum(i in e for e in edges) for i in range(13))==6,'retained_transverse_degree_cap')
    need(c['edge_order']==[list(e) for e in edges],'edge_order')
    dual={j:set() for j in range(22)};eadj={e:set() for e in edges}
    for e,(j,k) in ef.items(): dual[j].add(k);dual[k].add(j)
    for face in faces:
        for e,f in combinations(list(combinations(face,2)),2): eadj[e].add(f);eadj[f].add(e)
    need(connected(dual) and connected(eadj),'fixed_connected_graphs')
    d=[sum(x!=y for x,y in zip(bits[ef[e][0]],bits[ef[e][1]]))-1 for e in edges]
    need(c['three_rho']==d and min(d)>=0 and sum(d)==6,'coverage_and_total_excess')
    e0=[e for e,de in zip(edges,d) if de==0]
    deg=[sum(i in e for e in e0) for i in range(13)]
    need(c['zero_excess_edges']==[list(e) for e in e0],'zero_excess_support')
    need(c['degree_caps']==deg,'degree_caps')
    need(len(e0)==28 and c['pair_support_cap']==28,'support_cap')
    prefix=sum((2*x)*(2*x-1)//2 for x in deg)
    last=2*max(deg)-1
    need(c['endpoint_prefix_budget']==prefix==468,'prefix_budget')
    need(c['per_endpoint_last_prefix_cap']==last==11,'exceptional_prefix_budget')
    need(c['robust_remainder']==28**2-2*28+prefix==1196,'retained_1196')
    remainder=(prefix+2*last)//2-2*2
    need(c['defect_one_remainder']==remainder==241,'defect_one_remainder')
    for pos in range(3):
        for val in (0,1):
            order=c['exposure_orders'][2*pos+val]
            need(len(order)==11 and len(set(order))==11,'exposure_length')
            need(set(order)=={j for j,s in enumerate(bits) if int(s[pos])==val},'exposure_class')
            seen=set(faces[order[0]]);earlier=[order[0]]
            for j in order[1:]:
                need(len(set(faces[j])-seen)==1,'exposure_fresh_point')
                need(any(len(set(faces[j])&set(faces[k]))==2 for k in earlier),'exposure_old_pair')
                seen.update(faces[j]);earlier.append(j)
            need(seen==set(range(13)),'exposure_point_cover')
    # Pure arithmetic envelopes, not a sweep of supports or realizable ranks.
    for m in range(2,29):
        n=2*m
        patterns=n*2**n
        need(patterns<=56*2**56,'pattern_count_monotonic')
        need((prefix+2*last)//2-2*m<=remainder,'all_support_sizes_remainder')
    pattern_num=2**28*(56*2**56)*2**28
    need(pattern_num<2**c['defect_one_prefactor_power'],'complete_pattern_prefactor')
    need(2**28*55*2**29<2**c['higher_defect_prefactor_power'],'robust_prefactor')
    need(coeff['higher_defect_D_multiplier']==2,'actual_defect_two_multiplier')
    D=c['new_sufficient_even_D']
    need(D%2==0 and D>=12*c['M_inherited'],'integer_mode_removal_threshold')
    need(c['mode_removal_even_D']==12*c['M_inherited']==600,'mode_removal_ledger')
    need(c['inherited_final_even_D']==1198,'fallback_threshold_preserved')
    need(c['minimum_field_size']==16*D,'retained_field_threshold')
    need(D>=12,'retained_transverse_dimension')
    one_saving=D-remainder;high_saving=2*D-c['robust_remainder']
    need(one_saving>=1 and high_saving>=4,'residual_exponent_budget')
    # For q>=2, 2^118 q^(-D+241) <= 2^56 q^-1 at all D>=600.
    need((c['defect_one_prefactor_power']-c['direct_prefactor_power'])<=one_saving-1,
         'defect_one_prefactor_absorption')
    need(2**(c['direct_prefactor_power']+1)+2**c['higher_defect_prefactor_power']<
         2**c['saving_profile_prefactor_power'],'retained_tail_envelope')
    need(c['collapsed_tail_prefactor_power']==c['saving_profile_prefactor_power']+1,
         'tail_envelope_power')
    need(10*D+626>=0 and 32*D+1877>=0,'retained_rank_layer_envelope')
    return {'points':13,'faces':22,'point_pairs':33,'zero_excess_pairs':28,
            'degree_caps':deg,'prefix_budget':prefix,'last_prefix_cap':last,
            'six_exposures_checked':6,'support_sizes_arithmetic_only':27,
            'defect_one_remainder':remainder,'defect_one_prefactor_power':c['defect_one_prefactor_power'],
            'higher_defect_prefactor_power':c['higher_defect_prefactor_power'],
            'D':D,'one_saving':one_saving,'higher_saving':high_saving,
            'field_lower_bound':16*D,'rank_layer_envelope_power_at_D':32*D+2048}

def rref(rows,p,width=None):
    width=width if width is not None else (len(rows[0]) if rows else 0)
    A=[[int(x)%p for x in row] for row in rows];r=0;piv=[]
    for j in range(width):
        pivot=next((i for i in range(r,len(A)) if A[i][j]),None)
        if pivot is None: continue
        A[r],A[pivot]=A[pivot],A[r]
        inv=pow(A[r][j],-1,p);A[r]=[(x*inv)%p for x in A[r]]
        for i in range(len(A)):
            if i!=r and A[i][j]:
                v=A[i][j];A[i]=[(a-v*b)%p for a,b in zip(A[i],A[r])]
        piv.append(j);r+=1
        if r==len(A): break
    return A[:r],piv

def rank(rows,p): return len(rref(rows,p)[0])

def nullspace(rows,p,width):
    A,piv=rref(rows,p,width);free=[j for j in range(width) if j not in piv];out=[]
    for j in free:
        v=[0]*width;v[j]=1
        for row,col in zip(A,piv): v[col]=-row[j]%p
        out.append(v)
    return out

def intersection(U,V,p,width):
    eq=[[u[i] for u in U]+[-v[i] for v in V] for i in range(width)]
    ker=nullspace(eq,p,len(U)+len(V))
    out=[[sum(a[j]*U[j][i] for j in range(len(U)))%p for i in range(width)] for a in ker]
    return rref(out,p,width)[0]

def omega(x,y,D,p):
    return sum(x[i]*y[D+i]-x[D+i]*y[i] for i in range(D))%p

def plane_bases(U,p):
    for a,b,c,d in product(range(p),repeat=4):
        if (a*d-b*c)%p:
            yield [[(a*x+b*y)%p for x,y in zip(U[0],U[1])],
                   [(c*x+d*y)%p for x,y in zip(U[0],U[1])]]

def gl2(q): return (q*q-1)*(q*q-q)
def theta(D,k,q):
    need(0<=k<=D,'theta_domain')
    out=F(1)
    for j in range(D-k+1,D+1): out/=q**j+1
    return out

def trace_list(support, bases,D,q):
    G=[];local={i:[] for i in range(13)};hist=[];cactual=0;cupper=0
    for (i,j),plane in zip(support,bases):
        for vec in plane:
            x=len(local[i]);y=len(local[j]);w=len(G)
            pi=x+y-rank(local[i]+local[j],q);mu=min(x,y)
            Gn=rref(G+[vec],q)[0];Un=rref(local[i]+[vec],q)[0];Vn=rref(local[j]+[vec],q)[0]
            g=len(Gn)-w;li=len(Un)-x;lj=len(Vn)-y
            code=f'{g}{li}{lj}'
            need(code in ('111','000','001','010','011'),'geometric_increment_type')
            if code=='111': ca=2*D-x-y+pi;cu=2*D-x-y+mu
            elif code=='000': ca=pi;cu=mu
            elif code=='001': ca=cu=x
            elif code=='010': ca=cu=y
            else: ca=cu=w
            cactual+=ca;cupper+=cu
            hist.append({'code':code,'x':x,'y':y,'pi':pi,'mu':mu,'w':w})
            G=Gn;local[i]=Un;local[j]=Vn
    kis=[len(local[i]) for i in range(13)];k=len(G);a=sum(kis)-2*k;m=len(support)
    need(a==sum(sum(map(int,h['code'][1:]))-2*int(h['code'][0]) for h in hist),
         'trace_defect_telescoping')
    correction=sum(v*(v-1)//2 for v in kis)+2*m-4*m-D*sum(kis)
    if a==1:
        need(sum(h['code'] in ('001','010') for h in hist)==1 and all(h['code']!='011' for h in hist),
             'trace_defect_one_structure')
        R=-2*m+sum(h['pi'] if h['code'] in ('111','000') else h['x']+h['y'] for h in hist)
        Ru=-2*m+sum(h['mu'] if h['code'] in ('111','000') else h['x']+h['y'] for h in hist)
        need(cactual+correction==-D+R,'trace_exact_exponent')
        need(cupper+correction==-D+Ru,'trace_uniform_exponent')
        need(R<=Ru<=245-2*m,'trace_remainder_envelope')
    else: R=Ru=None
    return tuple(h['code'] for h in hist),{'k':k,'sum_ki':sum(kis),'a':a,'R_actual':R,'R_uniform':Ru}

def geometric_controls(c,controls):
    D=4;width=8
    E=[[int(j==i) for j in range(width)] for i in range(D)]
    Fv=[[int(j==D+i) for j in range(width)] for i in range(D)]
    out=[]
    for q in (13,67):
        need(q%2==1 and all(q%d for d in range(2,isqrt(q)+1)),'small_control_field_prime')
        add=lambda x,y:[(a+b)%q for a,b in zip(x,y)]
        L={1:E,0:[E[0],E[1],Fv[2],Fv[3]],7:[E[0],Fv[1],E[2],add(E[3],Fv[3])]}
        for i,lam in zip([i for i in range(13) if i not in L],range(2,12)):
            L[i]=[[(a+lam*b)%q for a,b in zip(E[t],Fv[t])] for t in range(D)]
        for U in L.values():
            need(rank(U,q)==D,'example_lagrangian_dimension')
            need(all(omega(x,y,D,q)==0 for x in U for y in U),'example_isotropy')
        H={}
        for edge in map(tuple,c['edge_order']):
            U=intersection(L[edge[0]],L[edge[1]],q,width)
            if U:H[edge]=U
        need(set(H)=={(0,1),(1,7)} and all(len(U)==2 for U in H.values()),'adjacent_exact_support')
        need(len(intersection(L[0],L[7],q,width))==1 and [0,7] not in c['edge_order'],
             'adjacent_nonedge_line')
        for i,j,k in c['faces']:
            need(not intersection(intersection(L[i],L[j],q,width),L[k],q,width),
                 'adjacent_face_common_zero')
        k=rank(H[(0,1)]+H[(1,7)],q)
        kis=[rank([v for edge,U in H.items() if i in edge for v in U],q) for i in range(13)]
        need((k,sum(kis),sum(kis)-2*k)==(3,7,1),'adjacent_rank_data')
        out.append({'q':q,'D':D,'k':k,'sum_ki':sum(kis),'a':1,
                    'all_pair_checks':33,'all_common_checks':22,'q_ge_16D':q>=16*D})
    P=[E[0],E[1]];T=[E[0],E[2]]
    count=0;line=0
    for basis in plane_bases(T,13):
        count+=1
        if all(basis[0][j]==0 for j in range(width) if j!=0): line+=1
    need(count==gl2(13)==controls['q13_gl2'],'control_GL2_count')
    need(line==(13-1)*(13**2-13)==controls['q13_first_line_bases'],'control_line_basis_count')
    need(F(line,count)==F(1,14),'control_line_basis_fraction')
    counts=Counter();sample=None
    basesP=list(plane_bases(P,3));basesT=list(plane_bases(T,3))
    for bp in basesP:
        for bt in basesT:
            pat,tr=trace_list([(0,1),(1,7)],[bp,bt],D,3)
            counts[pat]+=1;sample=tr
    need(sum(counts.values())==gl2(3)**2==controls['q3_complete_pairs']==2304,'complete_partition_total')
    need(sorted(counts.values())==sorted([controls['q3_line_pattern'],controls['q3_other_pattern']])==[576,1728],'complete_partition_counts')
    weight=3**4*theta(D,2,3)**2*theta(D,3,3)
    weighted=sum(F(n,gl2(3)**2)*weight for n in counts.values())
    need(weighted==weight,'weighted_complete_partition_identity')
    need(min(F(n,gl2(3)**2)*weight for n in counts.values())==weight/4,
         'forbidden_per_pattern_division_control')
    # A locally isotropic enlarged family with a 000 step, NOT a c_j=0 residual family.
    pat,tr=trace_list([(0,1),(0,3),(1,3)],[[E[0],E[1]],[E[0],E[2]],[E[0],E[3]]],D,3)
    need(tr['a']==1 and tr['k']==4 and tr['sum_ki']==9 and '000' in pat,
         'enlargement_000_control')
    # These three planes share a line, so their face has positive common dimension.
    need([0,1,3] in c['faces'],'enlargement_control_is_source_face')
    return {'actual_adjacent_plane_controls':out,'q13_GL2':count,'q13_first_line_bases':line,
            'q3_complete_basis_pairs':2304,'q3_pattern_counts':{','.join(k):v for k,v in sorted(counts.items())},
            'weighted_control':str(weight),'enlarged_not_residual_control':{'pattern':pat,**tr}}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate',type=Path,default=ROOT/'certificates/template_and_budget.json')
    parser.add_argument('--coefficients',type=Path,default=ROOT/'certificates/proof_coefficients.json')
    parser.add_argument('--controls',type=Path,default=ROOT/'certificates/controls.json')
    args=parser.parse_args()
    if not __debug__: raise CheckFailure('optimized_python_not_accepted')
    c=json.loads(args.certificate.read_text());coeff=json.loads(args.coefficients.read_text())
    controls=json.loads(args.controls.read_text())
    nsrc=source_bindings();ids=symbolic(coeff);budget=template_and_budget(c,coeff)
    geo=geometric_controls(c,controls)
    print(json.dumps({'status':'PASS','source_files_bound':nsrc,'polynomial_identities':len(ids),
                     'identity_labels':ids,'budget':budget,'controls':geo,
                     'limitations':'Finite exact support for separate conventional proofs; no formal verification or template/host search.'},indent=2))
if __name__=='__main__':
    try: main()
    except (CheckFailure,ValueError,KeyError,OSError) as exc:
        print('CHECK_FAILED: '+str(exc),file=sys.stderr);sys.exit(1)
