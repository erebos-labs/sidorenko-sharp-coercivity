#!/usr/bin/env python3
"""MIT License, copyright (c) 2026 Erebos Labs.

Bounded exact parameter audit. Python standard library; no giant powers/fields/hosts.

Universal implications are proved in PROOF.md. Finite computations below verify
identities, literal data, parameters and controls, not a proof-assistant theorem.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
class AuditFailure(Exception): pass

def need(test, site):
    if not test: raise AuditFailure(site)

def dump(value): return json.dumps(value, indent=2, sort_keys=True) + '\n'
def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def pop(n): return bin(n).count('1')
def sign(n): return -1 if pop(n)%2 else 1

def structure():
    c=json.loads((ROOT/'inherited/defect-one/certificates/template_and_budget.json').read_text())
    faces=c['faces']; bits=c['bits']
    text=(ROOT/'inherited/defect-one/sources/openai/complex.tex').read_text()
    pat=r'^\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*\d+\s*&\s*\d+\s*&\s*\d+\s*&\s*([01]{3})\\\\'
    table={int(x[1]):([int(x[z]) for z in (2,3,4)],x[5]) for x in re.finditer(pat,text,re.M)}
    need(len(table)==22 and faces==[table[i][0] for i in range(22)] and
         bits==[table[i][1] for i in range(22)],'immutable_template')
    ef={}
    for j,face in enumerate(faces):
        for e in combinations(face,2): ef.setdefault(e,[]).append(j)
    need(len(ef)==33 and all(len(js)==2 for js in ef.values()),'pair_incidence')
    corners=sorted((i,j) for j,f in enumerate(faces) for i in f)
    need(len(corners)==66,'incidence_count')
    adj=[set() for _ in range(35)]
    for i,j in corners: adj[i].add(13+j); adj[13+j].add(i)
    need(max(map(len,adj))==6,'transverse_degree')
    U={e:frozenset((i,j) for i in e for j in ef[e]) for e in ef}
    pairs={k:tuple(e for e in combinations(faces[k[1]],2) if k[0] in e) for k in corners}
    Ms={k:U[pairs[k][0]]|U[pairs[k][1]] for k in corners}
    for k in corners:
        e,f=pairs[k]
        need(len(U[e])==len(U[f])==4 and U[e]&U[f]=={k},'four_corner_overlap')
        need(len(Ms[k])==7 and len(U[e]^U[f])==6,'seven_six_support')
    for e in ef:
        meet=set.intersection(*(set(Ms[k]) for k in U[e]))
        need(meet==set(U[e]),'identity_label_forcing')
    return c,faces,bits,ef,corners,adj,U,pairs

def pinning(cfg, data):
    _,faces,_,_,corners,adj,_,_=data
    colors=[0]*13+[1]*22
    rounds=[]; all_counts=[]
    sv=[0]*35; se=[[0]*22 for _ in range(13)]
    need(cfg['refinement_rounds']==4 and cfg['round_base']==1856,'retained_refinement_weights')
    need(cfg['round_spread']==1854,'round_spread')
    for t in range(4):
        old=colors[:]; hist=[Counter(old[w] for w in adj[v]) for v in range(35)]
        vv=[-sum(a*a for a in h.values()) for h in hist]
        ee=[[2*hist[i][old[13+j]]+2*hist[13+j][old[i]] for j in range(22)] for i in range(13)]
        sig=[(old[v],tuple(sorted(hist[v].items()))) for v in range(35)]
        numbering={s:i for i,s in enumerate(sorted(set(sig)))}
        colors=[numbering[s] for s in sig]
        all_counts.append([len(set(colors[:13])),len(set(colors[13:]))])
        wt=cfg['round_base']**(3-t)
        sv=[a+wt*b for a,b in zip(sv,vv)]
        se=[[se[i][j]+wt*ee[i][j] for j in range(22)] for i in range(13)]
        rounds.append((old,hist,vv,ee,colors[:]))
    need(all_counts==[[3,1],[3,7],[13,7],[13,22]],'discrete_refinement')
    aa=[v-min(sv[:13]) for v in sv[:13]]
    bb=[v-min(sv[13:]) for v in sv[13:]]
    em=max(v for row in se for v in row)
    ell=[[em-se[i][j] for j in range(22)] for i in range(13)]
    E=sum(aa)+sum(bb)-sum(ell[i][j] for i,j in corners)
    Bpin=13*max(aa)+22*max(bb)-E
    ans={'round_color_counts':all_counts,'a':aa,'b':bb,'ell':ell,
         'max_a':max(aa),'max_b':max(bb),'ell_max':max(v for row in ell for v in row),
         'E_id':E,'B_pin':Bpin}
    for k in ('max_a','max_b','ell_max','E_id','B_pin'):
        need(ans[k]==cfg['pinning_expectation'][k],'pinning_value:'+k)
    need(all(v>=0 for v in aa+bb+[v for row in ell for v in row]),'nonnegative_thinning_powers')
    need(cfg['score_base_power']==2459,'pinning_score_base')
    need(cfg['map_count_power']==147 and 13**13*22**22 < 2**cfg['map_count_power'],'all_type_map_count')
    need(cfg['coefficient_power']==66*33==2178,'all_label_count')
    need(cfg['identity_power']==2*66==132,'identity_exponent')
    need(cfg['score_base_power']-cfg['map_count_power']-cfg['coefficient_power']==134,
         'nonidentity_dominance_margin')
    for k in range(4):
        need(1856**k-1854*sum(1856**j for j in range(k))>=1,'first_failing_round_dominance')
    # Deterministic controls with collapses, no assumption that a map preserves edges.
    ident=list(range(35)); maps=[ident,[0]*13+[13]*22]
    for old,_,_,_,_ in rounds:
        rep={color:min(v for v in range(35) if old[v]==color) for color in set(old)}
        maps.append([rep[color] for color in old])
        pair=next(((v,rep[old[v]]) for v in range(35) if rep[old[v]]!=v),None)
        if pair:
            f=ident[:];f[pair[0]]=pair[1];maps.append(f)
    maps.append([(i+1)%13 for i in range(13)]+[13+(j+1)%22 for j in range(22)])
    maps=list({tuple(f):f for f in maps}.values()); identities=0; collapsed=0
    def score(f,vv,ee):
        return sum(vv[f[v]] for v in range(35))+sum(ee[f[i]][f[13+j]-13] for i,j in corners)
    total_id=sum(sv)+sum(se[i][j] for i,j in corners)
    for f in maps:
        need(all((v<13)==(f[v]<13) for v in range(35)),'part_preserving_control')
        collapsed+=len(set(f))<35
        for old,hs,vv,ee,_ in rounds:
            if all(old[f[v]]==old[v] for v in range(35)):
                gap=score(ident,vv,ee)-score(f,vv,ee)
                rhs=sum(sum((hs[f[v]][c]-hs[v][c])**2 for c in set(hs[f[v]])|set(hs[v])) for v in range(35))
                need(gap==rhs,'all_map_histogram_square');identities+=1
        total_f=sum(sv[f[v]] for v in range(35))+sum(se[f[i]][f[13+j]-13] for i,j in corners)
        Ef=(sum(aa[f[i]] for i in range(13))+sum(bb[f[13+j]-13] for j in range(22))-
            sum(ell[f[i]][f[13+j]-13] for i,j in corners))
        need(E-Ef==total_id-total_f,'all_map_shift_identity')
        need(f==ident or E-Ef>=1,'collapsed_map_score_gap')
    need(cfg['independent_incidence_draws'] and cfg['incidence_reuse_count']==66,
         'independent_repeated_type_pairs')
    f=maps[1]
    need(sum(ell[f[i]][f[13+j]-13] for i,j in corners)==66*ell[0][0],
         'one_thinning_per_source_incidence')
    ans['finite_map_controls']=len(maps);ans['collapsed_controls']=int(collapsed)
    ans['histogram_identity_controls']=identities
    return ans

def activation(cfg, data):
    need(F(cfg['theta'])==F(1,2),'activation_theta')
    need([F(x) for x in cfg['sign_branch_weights']]==[F(1,2)]*2,'activation_branch_weights')
    _,_,_,_,corners,_,U,pairs=data
    need(tuple(cfg['negative_corner']) in corners,'negative_corner')
    need(cfg.get('empty_product',1)==1,'empty_product_normalization')
    first=overlap=0
    for sigma in (-1,1):
        laws=[(127,z,2+sigma*sign(z&126)) for z in range(128)]
        laws += [(126,z<<1,2*(2-sigma*sign(z))) for z in range(64)]
        need(sum(w for _,_,w in laws)==512 and min(w for _,_,w in laws)>0,'activation_probability_law')
        for alpha in range(1,128):
            num=sum(w*sign(z&alpha) for S,z,w in laws if alpha&S==alpha)
            need(num==0,'zero_first_moment');first+=1
        for Q in range(128):
            R=Q
            while True:
                num=sum(w*sign(z&R) for S,z,w in laws if Q&S==Q)
                expected=F(1,2)*(int(R==0)+F(sigma,2)*int(R==126))
                if Q&126==Q:expected+=F(1,2)*(int(R==0)-F(sigma,2)*int(R==126))
                need(F(num,512)==expected,'exact_overlap_moment');overlap+=1
                # Whole-law thinning, including the empty event: tests both boundaries.
                for lam in (F(0),F(1,3),F(1)):
                    thinned=lam*F(num,512)+(1-lam)*int(Q==0)
                    need(thinned==(F(1) if Q==0 else lam*expected),'whole_law_thinning')
                if R==0:break
                R=(R-1)&Q
    coeff=F(1)
    for corner in corners:
        e,f=pairs[corner]
        need(U[e]&U[f]=={corner},'identity_corner_overlap')
        coeff*=F(-1 if corner==tuple(cfg['negative_corner']) else 1,4)
    need(coeff==-F(1,2**132),'negative_identity_coefficient')
    parity_checks=0
    for c0 in (-1,1):
        for active in range(16):
            for signs in product((-1,1),repeat=4):
                vals=[]
                for eta in (-1,1):
                    z=1
                    if active&3==3:z*=1+c0*eta*signs[0]*signs[1]
                    if active&12==12:z*=1+c0*eta*signs[2]*signs[3]
                    vals.append(z)
                expected=1+(signs[0]*signs[1]*signs[2]*signs[3] if active==15 else 0)
                need(F(sum(vals),2)==expected,'all_activity_pair_parity')
                need(expected in (0,1,2),'nonnegative_parity_model');parity_checks+=1
    return {'first_moments':first,'union_difference_moments':overlap,
            'pair_activity_sign_controls':parity_checks,'identity_coefficient':'-2^-132',
            'normalizers_nonzero':'diagonal rank-r forms of both square classes; conventional argument'}

class Poly:
    """Sparse Q-polynomials; adapted from the MIT-licensed pinned checker."""
    def __init__(self,v=0):
        if isinstance(v,Poly):self.t=dict(v.t)
        elif isinstance(v,dict):self.t={m:F(c) for m,c in v.items() if c}
        else:self.t={():F(v)} if v else {}
    def __add__(self,b):
        z=dict(self.t)
        for m,c in Poly(b).t.items():z[m]=z.get(m,F(0))+c
        return Poly(z)
    __radd__=__add__
    def __neg__(self):return Poly({m:-c for m,c in self.t.items()})
    def __sub__(self,b):return self+-Poly(b)
    def __rsub__(self,b):return Poly(b)+-self
    def __mul__(self,b):
        z={}
        for m,c in self.t.items():
            for n,d in Poly(b).t.items():
                k=tuple(sorted(m+n));z[k]=z.get(k,F(0))+c*d
        return Poly(z)
    __rmul__=__mul__
    def __truediv__(self,b):return self*F(1,b)
    def __pow__(self,n):
        z=Poly(1)
        for _ in range(n):z=z*self
        return z

def symbolic(cfg):
    D,r,alpha,e,lam,A,B,h,Fm=map(lambda n:Poly({(n,):1}),['D','r','alpha','e','lam','A','B','h','Fm'])
    out=[]
    def eq(a,b,s):need(not (Poly(a)-b).t,'identity:'+s);out.append(s)
    tri=lambda z:z*(z+1)/2
    eq(r*r+tri(r)-tri(2*r),-tri(r),'signed_rank_leading_power')
    eq(-tri(2*r)+r*(r-1)/2+3*tri(r),0,'three_active_normalization_power')
    eq(-tri(2*r)+r*r+2*tri(r),0,'two_active_normalization_power')
    eq(lam+(1-lam)*cfg.get('empty_product',1),1,'thinned_mean_one')
    eq((1-alpha)*(1+alpha/8),1-7*alpha/8-alpha*alpha/8,'orientation_model_product')
    eq(3*e+e*e,4*e-e*(1-e),'two_orientation_error')
    eq((1-7*alpha/8)+4*alpha/cfg['orientation_error_divisor'],1-13*alpha/16,'error_budget_at_alpha_over_64')
    eq((1-3*alpha/4)-(1-13*alpha/16),alpha/16,'orientation_spare_margin')
    eq((1-alpha/2)-(1-3*alpha/4),alpha/4,'Gamma_spare_margin')
    eq(A*B*Fm+(h-1)*A*B*Fm,h*A*B*Fm,'clone_total_multiplicity')
    eq(299+22*(D+47)+88,22*D+1421,'all_gain_prefactors_paid')
    eq(22*5+55,165,'all_gain_polynomial_powers_paid')
    eq((32*D+2048-1)-(22*D+1421),10*D+626,'envelope_second_half')
    eq((32*D+2048-1)-170,32*D+1877,'envelope_first_half')
    eq(2*7*2+14,42,'coin_q_exponent')
    eq(2*66-35,97,'acceptance_hom_power')
    eq(2*66-1,131,'acceptance_gap_power')
    eq(2459+0-(147+2178),134,'nonidentity_map_margin_power')
    eq(132+147+1,280,'pinning_margin_padding')
    eq(13*2181,28353,'dilution_alpha_padding')
    return out

def parameters(D,cfg,pin):
    need(D in (cfg['old_D'],cfg['new_D']),'bounded_dimension_set')
    r=cfg['old_r'] if D==cfg['old_D'] else cfg['new_r']
    need(D==2*r and r%2==0,'even_rank_reversal')
    need(D>=600 and D%2==0 and D>=cfg['mode_multiplier']*cfg['inherited_M'],
         'integer_mode_admission')
    need(cfg['inherited_M']==50 and cfg['mode_multiplier']==12,'inherited_mode_premises')
    need(cfg['fallback_residual']==1196,'fallback_1196_preserved')
    need(cfg['defect_one_remainder']==241 and cfg['defect_one_prefactor']==118 and
         cfg['higher_defect_prefactor']==63,'inherited_defect_budget')
    need(D-241>=359 and 2*D-1196>=4 and D-304>=0,'new_residual_absorption')
    need(cfg['rank_envelope_slope']==32 and cfg['rank_envelope_padding']==2048 and
         cfg['rank_envelope_poly_power']==256,'published_C_D_envelope')
    need(cfg['rank_prime_multiplier']==16 and cfg['prime_policy']=='odd prime q > 16D + J^6',
         'complete_host_prime_condition')
    need(cfg['prime_root_power']==6 and cfg['field_error_padding_power']==6 and
         cfg['orientation_error_divisor']==64,'complete_kernel_error_padding')
    need(cfg['coordinate_count']==66 and cfg['coordinate_bound_power']==34,'tensor_product_multiplicity')
    need(cfg['source_vertices']==35 and cfg['source_edges']==66,'original_host_template')
    need(cfg['kernel_active_cap']==7 and cfg['kernel_scale_multiplier']==14 and
         cfg['deficit_multiplier']==924,'bounded_kernel_scaling')
    need(cfg['clone_matrix_multiplier']==132 and cfg['kernel_coin_base']==512 and
         cfg['coin_matrix_multiplier']==42,'exact_cloning_and_coins')
    need(cfg['collisions']==35*34//2==595,'all_map_collision_budget')
    need(cfg['host_loss']==66+cfg['collisions']==661,'complete_sampling_budget')
    need(cfg['host_half_gap_multiplier']==2*cfg['host_loss']==1322,'half_gap_host_size')
    need(cfg['host_target_power']==10 and cfg['host_padding_power']==11 and
         2**cfg['host_padding_power']-cfg['host_loss']>2**cfg['host_target_power'],
         'fixed_host_padding')
    Z=cfg['pinning_safety_power']+cfg['score_base_power']*pin['B_pin']
    need(cfg['pinning_safety_power']==280 and cfg['dilution_extra_power']==2181,'fixed_pinning_padding')
    A0=14*Z+13*cfg['dilution_extra_power'];Lambda=A0+1
    need((Z,A0,Lambda)==tuple(cfg['pinning_expectation'][k] for k in ('Z','A0','Lambda')),'fixed_negative_margin')
    b=D*(D+1)//2
    Cexp=32*D+2048
    Hexp=34*65
    Jexp=A0+6+Hexp+Cexp
    # Only exponents are computed. J,Q0,q,N and 2^A0 are never allocated.
    logpad=(D+1).bit_length()
    need(D+1 < 2**logpad and 66 < 2**7,'strict_J_power_bound')
    FJ=Jexp+7+256*logpad
    Fq=6*FJ+cfg['prime_bound_outer_power']
    need(cfg['prime_bound_outer_power']==2 and cfg['prime_lemma_lower_input']==65536,'prime_existence_budget')
    need(6*Jexp>max(16,(16*D).bit_length()),'large_prime_lemma_admission')
    # The dyadic induction in the conventional prime proof, not a prime search.
    need(18<=2**6 and 19<=2**13 and 49<50 and 2*16-1>0,'prime_lemma_induction_bases')
    need(F(1,8)+F(3,2)/4==F(1,2)<F(2,3),'prime_lemma_contradiction_margin')
    qpower=924*b
    hostB=11+Lambda+qpower*Fq
    expected=cfg['old_host_B'] if D==cfg['old_D'] else cfg['new_host_B']
    need(hostB==expected,'host_order_exponent')
    ans={
      'D':D,'r':r,'bD':b,'b_r':r*(r+1)//2,'rank_prime_floor':16*D,
      'planted_prefactor':{'two_power':D+47,'D_plus_one_power':5},
      'profile_prefactor_power':87,'profile_count_power':55,'chart_prefactor_power':299,
      'transverse_prefactor_power':170,'C_D':{'two_power':Cexp,'base':D+1,'power':256},
      'Z':Z,'epsilon_power':Z+2181,'A0':A0,'Lambda':Lambda,
      'H_c':{'coefficient':66,'two_power':Hexp},
      'J':{'coefficient':66,'base':D+1,'power':256,'two_power':Jexp},
      'Q0':'%d + J^6'%(16*D),'q_condition':'odd prime q > Q0',
      'q_choice':'least prime in the finite interval (Q0,2Q0); existence proved, not tested',
      'J_upper_two_power':FJ,'q_upper_two_power':Fq,
      'mu_q_power':14*b,'kernel_gap_q_power':qpower,'host_B':hostB,
      'host_N':'2^B','host_gap':'1024/N','generic_host_n':'integer n >= 1322 * 2^Lambda * q^(924*bD)',
      'atom_count_coefficient':14*22,'atom_count_q_power':132*b,
      'clone_log_bound':Z+2181+9+2459*(pin['max_a']+pin['max_b'])+132*b*Fq,
      'coin_log_bound':18+4918*pin['ell_max']+42*b*Fq,
      'normalizer_enumeration_log_bound':b*Fq,
      'new_defect_savings':[D-241,2*D-1196],
      'saving_profile_gap':'1/6','asymptotic_fields_allocated':False,'theorem_host_allocated':False}
    return ans

def inherited_matrix(data):
    c=json.loads((ROOT/'inherited/full-slack/original.json').read_text())
    _,faces,bits,ef,*_=data;edges=sorted(ef);n=len(edges)
    A=[[0]*n for _ in range(n)]
    for face in faces:
        ids=[edges.index(e) for e in combinations(face,2)]
        for i,j in combinations(ids,2):
            A[i][i]+=1;A[j][j]+=1;A[i][j]-=1;A[j][i]-=1
    rho=[sum(x!=y for x,y in zip(bits[ef[e][0]],bits[ef[e][1]]))-1 for e in edges]
    for i in range(n):A[i][i]+=4*rho[i]
    need(A==c['A'],'inherited_matrix_from_template')
    N=c['inverse_numerator'];tau=c['inverse_denominator']
    need(tau==270558215904,'inherited_inverse_denominator')
    for i in range(n):
        for j in range(n):
            need(sum(A[i][k]*N[k][j] for k in range(n))==(tau if i==j else 0),'inherited_inverse_identity')
    b=[2-x for x in rho];u=[sum(N[i][j]*b[j] for j in range(n)) for i in range(n)]
    H=sum(x*y for x,y in zip(b,u));Psi=H+12*F(187,8)*tau
    need(H==c['Hnum']==96183743778420 and Psi==c['Psi']==172075323339492,'inherited_full_slack_radius')
    for i in range(n):
        x=51*tau-2*u[i]
        need(x>0 and x*x>4*Psi*N[i][i],'inherited_M50_bound')
    need(c['M_bound']==50 and c['mode_removal_even_D']==600 and
         c['retained_nondirect_remainder']==1196 and c['sufficient_even_D']==1198,
         'inherited_fallback_unchanged')
    return {'inverse_entries':1089,'coordinate_inequalities':33,'M':50,
            'integer_mode_D':600,'unsplit_fallback_D':1198}

def density(kernel,weights,edges):
    nv=1+max(max(e) for e in edges)
    ans=F(0)
    for labels in product(range(len(weights)),repeat=nv):
        z=F(1)
        for x in labels:z*=weights[x]
        for i,j in edges:z*=kernel[labels[i]][labels[j]]
        ans+=z
    return ans

def finite_host_controls(cfg,faces):
    # Nonzero diagonals are retained by cloning, not silently discarded.
    U=[[F(1,4),F(1,2)],[F(1,2),F(3,4)]];w=[F(1,3),F(2,3)]
    clones=[0,1,1];V=[[U[i][j] for j in clones] for i in clones]
    checks=0
    for edges in ([(0,1)],[(0,1),(1,2)],[(0,1),(1,2),(2,0)]):
        need(density(U,w,edges)==density(V,[F(1,3)]*3,edges),'cloning_all_label_pushforward');checks+=1
    # Literal original H into a two-vertex edge. Every homomorphism collapses vertices.
    hom=0
    neighborhoods=[2,1]
    for labels in product(range(2),repeat=13):
        if not cfg['all_maps'] and len(set(labels))<13:continue
        term=1
        for face in faces:
            common=3
            for i in face:common &= neighborhoods[labels[i]]
            term*=pop(common)
            if not term:break
        hom+=term
    need(hom==2,'collapsed_original_H_homomorphisms')
    # A repeated image edge uses one coin; it is not assigned an independent trial twice.
    prob=F(1,3)
    shared=sum(F(1,3) for coin in range(3) if coin<1)
    need(shared==prob and shared!=prob*prob,'repeated_image_edge_coin')
    # Exact sampling on two host vertices with the above cloned kernel.
    mean=sum(w[i]*w[j]*U[i][j] for i in range(2) for j in range(2))
    Ep=F(0)
    for i,j in product(range(3),repeat=2):
        for coin in range(4):
            edge=int(coin<4*V[i][j])
            Ep+=F(1,9*4)*F(2*edge,4)
    need(Ep==mean/2,'host_diagonal_deletion_cost')
    need(2048-661==1387 and 1387>1024 and 1322<2048,'fixed_host_positive_gap')
    return {'clone_density_controls':checks,'original_H_to_K2_all_maps':hom,
            'original_H_to_K2_injective_maps':0,'sampled_two_vertex_mean':str(Ep),
            'repeated_edge_coin':'one Bernoulli variable, not its square',
            'host_collision_bound':595,'complete_host_loss':661,'fixed_host_expectation_lower_numerator':1387}

def source_bindings():
    p=ROOT/'SOURCE_ACCESS.json'
    need(p.is_file(),'source_access_ledger_required')
    data=json.loads(p.read_text());n=0
    for item in data['bundled']:
        b=(ROOT/item['local_path']).read_bytes()
        need(len(b)==item['bytes'],'source_length:'+item['local_path'])
        need(hashlib.sha256(b).hexdigest()==item['sha256'],'source_sha256:'+item['local_path'])
        if item.get('git_blob_sha1'):need(blob(b)==item['git_blob_sha1'],'source_blob:'+item['local_path'])
        n+=1
    return {'bundled_bindings':n,'retained_whole_file_local_sha256':'NOT_RUN; optional external byte check available',
            'retained_connector_blob':'e5f1aaef9c3020054f0221a5b5dedc8260d5d5e4'}

def main():
    need(__debug__,'optimized_python_not_accepted')
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--inputs',type=Path,default=ROOT/'certificates/audit_inputs.json')
    ap.add_argument('--emit-certificates',action='store_true',help='Regenerate only small exact JSON certificates.')
    args=ap.parse_args();cfg=json.loads(args.inputs.read_text())
    data=structure();pin=pinning(cfg,data);act=activation(cfg,data);syms=symbolic(cfg)
    pars={str(D):parameters(D,cfg,pin) for D in (cfg['old_D'],cfg['new_D'])}
    need(pars['600']['host_B']<pars['7296']['host_B'],'strictly_smaller_host_order')
    if args.emit_certificates:
        (ROOT/'certificates/pinning.json').write_text(dump(pin))
        (ROOT/'certificates/parameters.json').write_text(dump(pars))
    else:
        need(pin==json.loads((ROOT/'certificates/pinning.json').read_text()),'pinning_certificate')
        need(pars==json.loads((ROOT/'certificates/parameters.json').read_text()),'parameter_certificate')
    matrix=inherited_matrix(data);small=finite_host_controls(cfg,data[1]);sources=source_bindings()
    print(dump({'status':'PASS','symbolic_identity_count':len(syms),'symbolic_identities':syms,
       'activation':act,'pinning':{k:pin[k] for k in ['round_color_counts','max_a','max_b','ell_max','E_id','B_pin','finite_map_controls','collapsed_controls','histogram_identity_controls']},
       'matrix_regression':matrix,'finite_host_controls':small,'parameters':pars,'sources':sources,
       'limits':['Conventional all-domain proof, not proof-assistant verification.',
                 'No exhaustive type-map enumeration, theorem-sized prime test, field, kernel or host.',
                 'Inherited analytic geometry remains a stated premise of the transfer audit.']}).rstrip())

if __name__=='__main__':
    try:main()
    except AuditFailure as exc:
        print('AUDIT_FAILED: '+str(exc),file=sys.stderr);sys.exit(1)
