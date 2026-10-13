#!/usr/bin/env python3
"""Offline exact arithmetic support for THEOREM.md and DOWNSTREAM.md.

Python 3.9+ standard library only. Polynomial coefficients are Fractions.
No numerical optimization, source-program execution, or network access.
The sign/domain arguments are the conventional proof, not a formal theorem.
"""
import sys
if not __debug__:
    raise RuntimeError('Optimized Python is refused; use neither -O nor -OO.')
import argparse
import hashlib
import json
import re
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAIRS = tuple(combinations(range(3), 2))

class CheckError(Exception):
    pass

def need(ok, label):
    if not ok:
        raise CheckError(label)

class Poly:
    """Sparse Q-polynomial. A monomial is a sorted tuple of variable names."""
    def __init__(self, value=0):
        raw = value if isinstance(value, dict) else ({(): F(value)} if value else {})
        self.a = {tuple(m): F(c) for m, c in raw.items() if c}
    @staticmethod
    def cast(x):
        return x if isinstance(x, Poly) else Poly(x)
    def __add__(self, other):
        out = dict(self.a)
        for m,c in self.cast(other).a.items(): out[m] = out.get(m,F(0))+c
        return Poly(out)
    __radd__ = __add__
    def __neg__(self): return Poly({m:-c for m,c in self.a.items()})
    def __sub__(self, x): return self + (-self.cast(x))
    def __rsub__(self, x): return self.cast(x)-self
    def __mul__(self, x):
        out = {}
        for m,c in self.a.items():
            for n,d in self.cast(x).a.items():
                k=tuple(sorted(m+n));out[k]=out.get(k,F(0))+c*d
        return Poly(out)
    __rmul__ = __mul__
    def __truediv__(self, x): return self * (F(1)/F(x))
    def __pow__(self, n):
        need(isinstance(n,int) and n>=0,'polynomial power domain')
        out=Poly(1)
        for _ in range(n):out=out*self
        return out
    def sub(self, mapping):
        out=Poly()
        for m,c in self.a.items():
            term=Poly(c)
            for name in m:term=term*mapping.get(name, var(name))
            out=out+term
        return out
    def __repr__(self):
        return repr({('*'.join(m) or '1'):str(c) for m,c in sorted(self.a.items())})

def var(name): return Poly({(name,):F(1)})

def qform(c,d,z,v,p,t):
    P=sum(p);T=sum(t)
    return (F(1,4)*(c*(d+z)-z*d+2*z*z)
            +sum(F(1,6)*(2*a-b)**2+z*a-F(1,6)*c*(a+b) for a,b in zip(p,t))
            +v*(F(1,2)*(d-3*z)-P)+F(1,2)*v*v)

def variance(p,t):
    ss=[a+b for a,b in zip(p,t)]
    return sum((ss[i]-ss[j])**2 for i,j in PAIRS)

def ell(z,v,p,t): return F(1,2)*z+F(1,4)*(sum(p)-sum(t))+F(1,2)*v

def full_loss(c,z,v,p,t):return F(1,4)*c+F(1,2)*z+F(1,6)*(2*sum(p)-sum(t))+F(1,2)*v

def read_tuple(item):
    return F(item['c']),F(item['d']),F(item['delta']),F(item['v']),list(map(F,item['p'])),list(map(F,item['t']))

def feasible(values):
    c,d,z,v,p,t=values;P=sum(p);T=sum(t)
    margins={'c-abs(delta)':c-abs(z),'d-P-T':d-P-T,'v':v,
             'w':(d-3*z)/2-P+v}
    for i in range(3):
        margins['p'+str(i)]=p[i];margins['t'+str(i)]=t[i]
        margins['p+delta-t '+str(i)]=p[i]+z-t[i]
        margins['p+delta-v '+str(i)]=p[i]+z-v
    for key,val in margins.items():need(val>=0,'feasibility: '+key)
    return margins

def evaluate(item):
    c,d,z,v,p,t=read_tuple(item);feasible((c,d,z,v,p,t))
    Q=qform(c,d,z,v,p,t);V=variance(p,t);S=Q-full_loss(c,z,v,p,t)
    return {'Q':Q,'V':V,'S':S,'ell':ell(z,v,p,t),'remainder':Q-V/48-ell(z,v,p,t)}

PINNED_BLOBS={
 'sources/published/LICENSE':'fd53c72f02b17b6c660b9a95144175fc4178f8b3',
 'sources/published/variance/THEOREM.md':'caaf4fe3f77f266bb17ee69d500dac8c9921bd6d',
 'sources/published/variance/DOWNSTREAM.md':'922bebb56ffbef76723e048acd77848a61d1ee2f',
 'sources/published/variance/original_certificate.json':'75f203c1895e92aaa60eaa429ae4483d5dba850a',
 'sources/openai/tail.tex':'dc11e07a592e70d3a13e3a005c72378c88edc351',
 'sources/openai/planted.tex':'e1a4636e66361dae0f5918e1245950060535a83c',
 'sources/openai/complex.tex':'178b0e9da21867a727ea847dae8e537b9d719a70',
 'sources/openai/LICENSE':'261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64'}

def check_sources(root=ROOT, overrides=None):
    entries=json.loads((root/'SOURCES.json').read_text())['sources']
    need({e['bundled_path'] for e in entries}==set(PINNED_BLOBS),'source inventory')
    for entry in entries:
        path=entry['bundled_path'];b=(overrides or {}).get(path)
        if b is None:b=(root/path).read_bytes()
        git=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        need(git==PINNED_BLOBS[path]==entry['git_blob_sha1'],'source Git blob: '+path)
        need(hashlib.sha256(b).hexdigest()==entry['sha256'],'source SHA256: '+path)
        need(len(b)==entry['bytes'],'source byte length: '+path)
    return {'source_files':len(entries),'binding':'SHA-256 and immutable Git blob SHA-1'}

def check_local(cert, examples=None):
    C=F(cert['C']);beta=F(cert['coefficient']);kap=F(cert['variance_coefficient'])
    sharp=evaluate(cert['sharp_tuple'])
    need(sharp['remainder']>=-C,'sharp witness rejects C')
    for field in ('Q','S','V','remainder'):
        need(sharp[field]==F(cert['expected_sharp_'+field]),'sharp value: '+field)
    labels=[]
    def same(a,b,label):
        diff=Poly.cast(a)-b
        need(not diff.a,'identity: '+label+'; residual '+repr(diff))
        labels.append(label)
    c,d,z,v,e=map(var,('c','d','z','v','e'))
    p=[var('p'+str(i)) for i in range(3)];t=[var('t'+str(i)) for i in range(3)]
    P=sum(p);T=sum(t);ss=[p[i]+t[i] for i in range(3)]
    Q=qform(c,d,z,v,p,t);V=variance(p,t);S=Q-full_loss(c,z,v,p,t)
    E=ell(z,v,p,t);W=Q-V/48
    bfun=lambda x:x*(x+1)/2
    ambient=d+c;common_u=(c+z)/2;r=ambient/2
    gain=(r+c+1)*common_u-2*common_u**2+sum(bfun(x) for x in ss)-z*P-sum(x*x for x in p)-v*((d-3*z)/2-P+v)-sum(bfun(x) for x in t)+bfun(v)
    baseline=((ambient+1)*c+sum(bfun(x) for x in ss))/2-sum(bfun(c+x) for x in ss)/6
    same(S,baseline-gain,'published slack versus baseline and planted maximand')
    same(S-kap*V+beta*(3*c+P+T),W-E,'requested equivalence')
    A=(d+z)/4-(P+T)/6
    same(A,(d+3*z)/12+(d-P-T)/6,'c coefficient sign decomposition')
    same(d+3*z-2*T,(d-P-T)+(P-T+3*z),'d+3delta nonnegativity identity')
    same(Q-Q.sub({'c':z}),(c-z)*A,'positive c reduction')
    same(Q-Q.sub({'c':-z}),(c+z)*A,'negative c reduction')
    a,beta0=var('a'),var('beta0')
    ray={'c':0,'z':0,'v':0,'p0':a,'t0':a,'p1':0,'p2':0,'t1':0,'t2':0}
    same(Q.sub(ray),a*a/6,'sharp ray Q')
    same(V.sub(ray),8*a*a,'sharp ray V')
    same((S-V/48+beta0*(3*c+P+T)).sub(ray),2*a*(beta0-F(1,12)),'obstruction to smaller linear coefficient')
    qi=[var('q'+str(i)) for i in range(3)];q=sum(qi)/3
    sub0={'c':0,'z':0,'d':P+T+e}
    # Substitution is simultaneous; first replace d, then t_i=p_i-q_i.
    W0=W.sub(sub0).sub({'t'+str(i):p[i]-qi[i] for i in range(3)})
    E0=sum(qi)/4+v/2
    s0vec=[2*p[i]-qi[i] for i in range(3)]
    cross0=sum(s0vec[i]*s0vec[j] for i,j in PAIRS)
    rem0=sum((p[i]-v)*qi[i] for i in range(3))/2+v*e/2+cross0/24
    same(W0,sum(x*x for x in qi)/8+v*v/2+rem0,'delta-zero variable remainder')
    same(W0-E0+F(1,2),sum((x-1)**2 for x in qi)/8+(v-F(1,2))**2/2+rem0,'delta-zero affine completion')
    y=var('y')
    qp=qform(y,d+3*y,-y,v,[x+y for x in p],t)
    qb=qform(0,d,0,v,p,t)
    same(qp-qb,y*y/4+y*(2*P-T)/3+y*(d-P-T)/2,'negative delta shift Q')
    same(variance([x+y for x in p],t),V,'variance translation invariance')
    same(ell(-y,v,[x+y for x in p],t)-ell(0,v,p,t),y/4,'negative delta linear shift')
    same(y*y/4-y/4+F(1,16),(y-F(1,2))**2/4,'negative delta square')
    # Positive delta: expand 24W with q_i=p_i-t_i and e=d-P-T.
    posW=(24*W).sub({'c':z,'d':P+T+e}).sub({'t'+str(i):p[i]-qi[i] for i in range(3)})
    const=12*v*v+12*v*e+18*z*z-36*z*v
    Rexpr=sum((12*qi[i]+16*z)*p[i]+3*qi[i]**2+(4*z-12*v)*qi[i] for i in range(3))+const
    cross=sum(s0vec[i]*s0vec[j] for i,j in PAIRS)
    same(posW,Rexpr+cross,'positive delta 24W expansion')
    same(12*qi[0]+16*z,12*(qi[0]+z)+4*z,'strict p coefficient')
    rr=[var('r'+str(i)) for i in range(3)];aa=[var('a'+str(i)) for i in range(3)]
    sr=[2*rr[i]-qi[i] for i in range(3)]
    lhs=posW.sub({'p'+str(i):rr[i]+aa[i] for i in range(3)})-posW.sub({'p'+str(i):rr[i] for i in range(3)})
    rhs=sum((12*qi[i]+16*z)*aa[i] for i in range(3))+2*sum(sr[i]*aa[j]+sr[j]*aa[i] for i,j in PAIRS)+4*sum(aa[i]*aa[j] for i,j in PAIRS)
    same(lhs,rhs,'exact nonnegative p-reduction gap')
    h,b=var('h'),var('b');hi=[var('h'+str(i)) for i in range(3)]
    f=lambda x,hx:3*x*x+(12*b+4*z-12*v)*x+16*z*b+12*hx*hx+(12*b+16*z)*hx
    same(f(q,h),(12*q+16*z)*(b+h)+3*q*q+(4*z-12*v)*q+12*h*(b+h-q),'hinge form identity with zero hinge-complement product')
    # The last added product vanishes for h=(q-b)_+.
    si=[2*b+2*hi[i]-qi[i] for i in range(3)];sm=2*b+2*h-q;Ssum=sum(si)
    lhs=sum(f(qi[i],hi[i]) for i in range(3))+sum(si[i]*si[j] for i,j in PAIRS)-3*f(q,h)-3*sm*sm
    rhs=F(5,2)*sum((x-q)**2 for x in qi)+sum((qi[i]-qi[j])**2-(si[i]-si[j])**2 for i,j in PAIRS)/6+12*(sum(x*x for x in hi)-3*h*h)+(12*b+16*z)*(sum(hi)-3*h)+(Ssum-3*sm)*(Ssum+3*sm)/3
    same(lhs,rhs,'exact symmetrization gap')
    hbar=sum(hi)/3
    same(sum(x*x for x in hi)-3*h*h,sum((x-hbar)**2 for x in hi)+3*(hbar-h)*(hbar+h),'hinge squared Jensen sign identity')
    same(Ssum-3*sm,2*(sum(hi)-3*h),'s Jensen sign identity')
    x1,x2=var('x1'),var('x2')
    for sg1,sg2 in product((-1,1),repeat=2):
        same((sg1*x1-sg2*x2)**2-(x1-x2)**2,(2-2*sg1*sg2)*x1*x2,'absolute-value contraction '+str((sg1,sg2)))
    u,m=var('u'),var('m')
    H=9*u*u+36*(m-v)*u-42*z*u+12*z*m+3*z*z+12*v*v+12*v*e
    J=H+3*(2*m-z-u)**2;k=3*u-z+2*v
    symQ=qform(z,3*(2*m-z-u)+e,z,v,[m-z]*3,[m-u]*3)
    same(24*symQ,J,'symmetric residual J')
    same(ell(z,v,[m-z]*3,[m-u]*3),k/4,'symmetric linear functional')
    for name,bvalue in [('v<=delta',0),('v>=delta',v-z)]:
        # f evaluated at q=u-z and max(b,q)=m-z; verify via original expression.
        f_reduced=(12*(u-z)+16*z)*(m-z)+3*(u-z)**2+(4*z-12*v)*(u-z)
        same(3*f_reduced+const+3*(2*m-z-u)**2,J,'scalar reduction '+name)
    jm=F(cert['homogeneous_constants']['J_multiplier']);ks=F(cert['homogeneous_constants']['k_square_multiplier'])
    Dpoly=jm*J-ks*k*k
    same(Dpoly.sub({'m':u,'e':3*u-2*v}),6*u*u+(u-z)*(456*u-96*z)+(u-v)*(300*u+228*v-24*z),'m-u homogeneous certificate')
    zz=var('z0')
    for ev in (Poly(0),3*u-2*v):
        rz=Dpoly.sub({'m':z,'e':ev})
        same(rz-rz.sub({'z':zz}),(z-zz)*(300*(z+zz)-168*u+24*v),'m-delta reduction '+repr(ev))
    same(Dpoly.sub({'m':v,'e':3*u-2*v}),6*(5*u-4*v)**2+(v-z)*(576*u-96*z-120*v),'m-v positive-e certificate')
    gap=2*v/3-u
    same(Dpoly.sub({'m':v,'e':0}),F(8,3)*v*v+168*v*(v-z)+96*(v-z)**2+150*gap*gap+76*v*gap+576*z*gap,'m-v zero-e certificate')
    same(456*u-96*z,360*u+96*(u-z),'m-u bracket one positivity')
    same(300*u+228*v-24*z,276*u+228*v+24*(u-z),'m-u bracket two positivity')
    same(300*(z+zz)-168*u+24*v,300*(z-zz)+600*(zz-u)+432*u+24*v,'m-delta bracket positivity')
    same(576*u-96*z-120*v,576*(u-2*v/3)+168*v+96*(v-z),'m-v bracket positivity')
    same(J/24-k/4+C,(J-F(6,17)*k*k)/24+(k-F(17,2))**2/68,'sharp C affine completion')
    same(qform(a,a,a,a,[Poly(0)]*3,[a/5]*3),17*a*a/100,'sharp common-mode family Q')
    same(ell(a,a,[Poly(0)]*3,[a/5]*3),17*a/20,'sharp common-mode family ell')
    same(17*a*a/100-17*a/20+C,17*(a-F(5,2))**2/100,'sharp common-mode family completion')
    eps=var('eps')
    lQ=qform(F(5,2),F(5,2),F(5,2),F(5,2),[Poly(0)]*3,[F(1,2)+eps,F(1,2)-eps,Poly(F(1,2))])
    lV=variance([Poly(0)]*3,[F(1,2)+eps,F(1,2)-eps,Poly(F(1,2))])
    same(lV,6*eps*eps,'positive-variance limiting family V')
    same(lQ-lV/48-F(17,8),-F(17,16)+5*eps*eps/24,'positive-variance limiting family remainder')
    zero={'d':0,'z':0,'v':0,**{'p'+str(i):0 for i in range(3)},**{'t'+str(i):0 for i in range(3)}}
    same(S.sub(zero),-c/4,'fully coincident negative slack')
    n_examples=0;n_negative=0
    for ex in examples or []:
        val=evaluate(ex['tuple']);need(val['remainder']>=-C,'example bound: '+ex['name'])
        for fld,expected in ex['expected'].items():need(val[fld]==F(expected),'example value '+ex['name']+' '+fld)
        n_examples+=1;n_negative+=int(val['S']<0)
    return {'polynomial_identities':len(labels),'identity_labels':labels,'feasible_examples':n_examples,'negative_slack_examples':n_negative,'C':str(C),'sharp_remainder':str(sharp['remainder']),'sharp_V':str(sharp['V'])}

def connected(adj, subset=None):
    subset=set(range(len(adj))) if subset is None else set(subset)
    if not subset:return True
    seen={min(subset)};todo=list(seen)
    for x in todo:
        for y in adj[x]:
            if y in subset and y not in seen:seen.add(y);todo.append(y)
    return seen==subset

def check_downstream(cert, published, root=ROOT):
    faces=cert['template']['faces'];bits=cert['template']['bits']
    need(cert['template']==published['template'],'published template unchanged')
    need(len(faces)==22 and len(set(map(tuple,faces)))==22,'22 distinct faces')
    need(set(sum(faces,[]))==set(range(13)),'13 points')
    ef={}
    for j,f in enumerate(faces):
        need(f==sorted(set(f)) and len(f)==3,'face is sorted triple')
        for e in combinations(f,2):ef.setdefault(e,[]).append(j)
    edges=sorted(ef);n=len(edges)
    need(n==33 and all(len(js)==2 for js in ef.values()),'33 pairs, each twice')
    need(edges==list(map(tuple,cert['edge_order']))==list(map(tuple,published['edge_order'])),'edge ordering')
    dual=[set() for _ in faces]
    ds=[]
    for e in edges:
        j,k=ef[e];dual[j].add(k);dual[k].add(j)
        ds.append(sum(x!=y for x,y in zip(bits[j],bits[k]))-1)
    need(connected(dual),'dual connected')
    need(ds==cert['three_rho']==published['three_rho'],'exact coverages')
    need(min(ds)>=0 and sum(ds)==6,'nonnegative anchors sum rho=2')
    degree=[sum(i in e for e in edges) for i in range(13)]
    need(max(degree)==6,'retained transverse degree cap')
    # Check literal faces/bits against the pinned source table.
    text=(root/'sources/openai/complex.tex').read_text()
    pat=r'^\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*\d+\s*&\s*\d+\s*&\s*\d+\s*&\s*([01]{3})\\\\'
    rows={int(m[1]):([int(m[k]) for k in (2,3,4)],m[5]) for m in re.finditer(pat,text,re.M)}
    need(len(rows)==22 and [rows[i][0] for i in range(22)]==faces and [rows[i][1] for i in range(22)]==bits,'pinned source literal comparison')
    for bit in range(3):
        for val in range(2):
            order=cert['exposure_orders'][2*bit+val]
            selected={j for j in range(22) if int(bits[j][bit])==val}
            need(set(order)==selected and len(order)==11,'bit class order')
            exposed=set(faces[order[0]]);prior=[order[0]]
            for j in order[1:]:
                need(len(set(faces[j])-exposed)==1 and any(len(set(faces[j])&set(faces[k]))==2 for k in prior),'fresh-point exposure')
                exposed.update(faces[j]);prior.append(j)
            need(exposed==set(range(13)),'exposure covers all points')
    A=[[0]*n for _ in range(n)];adj=[set() for _ in range(n)]
    for f in faces:
        ix=[edges.index(e) for e in combinations(f,2)]
        for i,j in combinations(ix,2):
            A[i][i]+=1;A[j][j]+=1;A[i][j]-=1;A[j][i]-=1;adj[i].add(j);adj[j].add(i)
    need(connected(adj),'edge graph connected')
    for i in range(n):A[i][i]+=4*ds[i]
    need(A==cert['A']==published['A'],'unchanged K matrix')
    N=cert['inverse_numerator'];tau=cert['inverse_denominator']
    need(type(tau) is int and tau>0,'inverse denominator positive')
    need(len(N)==n and all(len(row)==n and all(type(x)is int for x in row) for row in N),'integer inverse shape')
    need(all(N[i][j]==N[j][i] for i in range(n) for j in range(n)),'inverse symmetry')
    for i in range(n):
        for j in range(n):need(sum(A[i][k]*N[k][j] for k in range(n))==(tau if i==j else 0),'inverse product '+str((i,j)))
    need(N==published['inverse_numerator'] and tau==published['inverse_denominator'],'inherited inverse reused unchanged')
    C=F(cert['face_constant']);need(C==F(17,16),'certified local constant')
    need(cert['worst_three_active_faces']==22,'all-activity constant count')
    Gamma=22*C;need(F(cert['Gamma'])==Gamma,'global constant Gamma')
    b=[2-x for x in ds];need(cert['b']==b,'new global linear vector')
    u=[sum(N[i][j]*b[j] for j in range(n)) for i in range(n)];H=sum(b[i]*u[i] for i in range(n))
    psi=H+12*Gamma*tau
    need(u==cert['u'] and H==cert['Hnum'],'new exact u and Hnum')
    need(psi==cert['Psi'],'radius includes additive constant')
    B=cert['strict_bound_B'];lm=[];qm=[]
    for i in range(n):
        lin=B*tau-2*u[i];quad=lin*lin-4*psi*N[i][i]
        need(lin>0 and quad>0,'coordinate inequality '+str(i))
        lm.append(lin);qm.append(quad)
    need(lm==cert['linear_margins'] and qm==cert['squared_margins'],'all literal margins')
    need(cert['M_bound']==B-1,'integer M threshold')
    mode=12*(B-1);need(cert['mode_removal_even_D']==mode,'integer mode removal D>=12M')
    D=cert['sufficient_even_D'];R=cert['retained_nondirect_remainder']
    need(R==1196,'retained residual constant unchanged')
    need(D%2==0 and D>=mode and D>=12,'even D and integer-mode premises')
    need(D-R>=F(1,6),'retained nondirect saving threshold')
    need(cert['nondirect_saving']==D-R and cert['minimum_field_threshold']==16*D,'retained analytic thresholds')
    need(D<cert['inherited_even_D']==3072 and cert['inherited_M_bound']==256,'strict improvement comparison')
    oldb=[12-x for x in ds];oldu=[sum(N[i][j]*oldb[j] for j in range(n)) for i in range(n)];oldH=sum(oldb[i]*oldu[i] for i in range(n))
    for i in range(n):
        lin=257*tau-2*oldu[i]
        need(lin>0 and lin*lin>4*oldH*N[i][i],'inherited bound regression '+str(i))
    allowed=[e for e,x in zip(edges,ds) if x==0]
    caps=[sum(i in e for e in allowed) for i in range(13)]
    need(len(allowed)==28 and sum((2*k)*(2*k-1)//2 for k in caps)==468,'retained 1196 combinatorial caps')
    need(28*28-2*28+468==1196,'1196 unchanged arithmetic')
    labels=[]
    def same(a,b,label):
        need(not (Poly.cast(a)-b).a,'downstream identity: '+label);labels.append(label)
    h,x,y=map(var,('h','x','y'));Vh=(h-x)**2+(h-y)**2+(x-y)**2
    same(2*h*h-Vh,2*(x*(h-x)+y*(h-y)+x*y),'range variance bound')
    same(h*h/24-h/12-(Vh/48-(h+x+y)/12),(2*h*h-Vh)/48+(x+y)/12,'all lower activity cases, no constant')
    masks=[]
    for mask in range(8):
        count=bin(mask).count('1');masks.append({'mask':mask,'active_count':count,'constant':str(C) if count==3 else '0','argument':'new all-real bound' if count==3 else 'inherited integer lower-activity bound plus exact comparison'})
    need(sum(m['active_count']==2 for m in masks)==3,'all two-active endpoints covered')
    c,d,z,v,M,Dp=map(var,('c','d','z','v','M','D'))
    p=[var('p'+str(i)) for i in range(3)];t=[var('t'+str(i)) for i in range(3)];P=sum(p);T=sum(t);nn=[2*a-b for a,b in zip(p,t)]
    slack=qform(c,d,z,v,p,t)-full_loss(c,z,v,p,t)
    base=3*c*(c-1)/4+sum(n*n+(c-1)*n+3*c*pi for n,pi in zip(nn,p))/6
    same(slack,base+(c-z)*(d-3*c-2*z+2-4*P)/4+v*(d-3*z-2*P+v-1)/2,'unchanged integer mode identity')
    same(Dp-4*c-2*z+2-4*P-(Dp-12*M+6*c+2),2*(c-z)+4*(3*(M-c)-P),'mode bracket one')
    same(Dp-c-3*z-2*P+v-1-(Dp-6*M+2*c+v-1),3*(c-z)+2*(3*(M-c)-P),'mode bracket two')
    same(base,(c-1)*(5*c+1)/8+sum((n+(c-1)/2)**2 for n in nn)/6+c*P/2,'unchanged integer base square')
    rho,hh=var('rho'),var('hh')
    same(-hh/6+rho*(hh*hh+hh)/4,rho*hh*hh/4-(F(1,6)-rho/4)*hh,'global linear term keeps excess')
    hv,tauv,Hv,Gv,Nv,uv=map(var,('hv','tau','Hnum','Gamma','Nii','uv'))
    same(48*(Hv/3+4*Gv*tauv)*Nv,16*(Hv+12*Gv*tauv)*Nv,'ellipsoid radius normalization')
    fractional=qform(0,Dp,0,0,[Poly(F(1,2))]*3,[Poly(F(1,2))]*3)-full_loss(0,0,0,[Poly(F(1,2))]*3,[Poly(F(1,2))]*3)
    same(fractional,-F(1,8),'fractional local slack control')
    same(22*fractional+1,-F(7,4),'fractional global counterprofile to real mode removal')
    return {'pair_coordinates':33,'inverse_entries':33**2,'new_coordinate_checks':33,'inherited_coordinate_checks':33,'activity_cases':masks,'symbolic_identities':len(labels),'identity_labels':labels,'Hnum':H,'Gamma':str(Gamma),'Psi':int(psi),'B':B,'M_bound':B-1,'mode_removal_D':mode,'sufficient_even_D':D,'retained_residual':R,'nondirect_saving':D-R,'min_linear_margin':min(lm),'min_squared_margin':int(min(qm))}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=ROOT)
    args=ap.parse_args();root=args.root.resolve()
    source=check_sources(root)
    local=check_local(json.loads((root/'certificates/local.json').read_text()),json.loads((root/'examples.json').read_text()))
    downstream=check_downstream(json.loads((root/'certificates/original.json').read_text()),json.loads((root/'sources/published/variance/original_certificate.json').read_text()),root)
    print(json.dumps({'status':'PASS','sources':source,'local':local,'downstream':downstream,'limits':'Finite exact arithmetic supports the separate conventional proofs; no Lean or independent human verification.'},indent=2,sort_keys=True))

if __name__=='__main__':
    try:main()
    except CheckError as err:
        print('FAIL: '+str(err),file=sys.stderr);sys.exit(1)
