#!/usr/bin/env python3
"""Targeted corruption controls; rejection proves only detection of these changes."""
import sys
if not __debug__:
    raise RuntimeError('Optimized Python is refused.')
import copy
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('full_slack_checker',ROOT/'checker.py')
ch=importlib.util.module_from_spec(spec);spec.loader.exec_module(ch)

def main():
    lc=json.loads((ROOT/'certificates/local.json').read_text())
    dc=json.loads((ROOT/'certificates/original.json').read_text())
    pub=json.loads((ROOT/'sources/published/variance/original_certificate.json').read_text())
    ch.check_sources(ROOT);ch.check_local(lc);ch.check_downstream(dc,pub,ROOT)
    controls=[]
    def reject(name,fn,expected):
        try:fn()
        except ch.CheckError as err:
            message=str(err)
            if not message.startswith(expected):raise RuntimeError('Wrong failure site for '+name+': '+message)
            controls.append({'name':name,'expected_prefix':expected,'observed':message,'status':'REJECTED_AS_EXPECTED'})
        else:raise RuntimeError('Corruption not detected: '+name)
    x=copy.deepcopy(lc);x['C']='1'
    reject('C lowered from 17/16 to 1',lambda:ch.check_local(x),'sharp witness rejects C')
    x=copy.deepcopy(lc);x['coefficient']='1/13'
    reject('linear coefficient changed to 1/13',lambda:ch.check_local(x),'identity: requested equivalence')
    x=copy.deepcopy(lc);x['homogeneous_constants']['J_multiplier']=16
    reject('homogeneous certificate 17 changed to 16',lambda:ch.check_local(x),'identity: m-u homogeneous certificate')
    x=copy.deepcopy(lc);x['sharp_tuple']['v']='3'
    reject('sharp tuple violates the individual v bounds',lambda:ch.check_local(x),'feasibility: p+delta-v')
    x=copy.deepcopy(lc);x['expected_sharp_S']='-9/16'
    reject('incorrect full-slack sign/value',lambda:ch.check_local(x),'sharp value: S')
    path='sources/published/variance/THEOREM.md'
    reject('published source byte appended',lambda:ch.check_sources(ROOT,{path:(ROOT/path).read_bytes()+b'\n'}),'source Git blob:')
    x=copy.deepcopy(dc);x['Gamma']='0'
    reject('additive global constant omitted',lambda:ch.check_downstream(x,pub,ROOT),'global constant Gamma')
    x=copy.deepcopy(dc);x['b']=[12-a for a in x['three_rho']]
    reject('old linear vector substituted',lambda:ch.check_downstream(x,pub,ROOT),'new global linear vector')
    x=copy.deepcopy(dc);x['inverse_numerator'][0][0]+=1
    reject('inverse diagonal entry changed by one',lambda:ch.check_downstream(x,pub,ROOT),'inverse product')
    x=copy.deepcopy(dc);x['strict_bound_B']=50
    reject('strict coordinate threshold lowered to 50',lambda:ch.check_downstream(x,pub,ROOT),'coordinate inequality')
    x=copy.deepcopy(dc);x['sufficient_even_D']=600
    reject('mode-removal dimension used as final dimension',lambda:ch.check_downstream(x,pub,ROOT),'retained nondirect saving threshold')
    x=copy.deepcopy(dc);x['retained_nondirect_remainder']=189
    reject('1196 replaced by unretained 189',lambda:ch.check_downstream(x,pub,ROOT),'retained residual constant unchanged')
    print(json.dumps({'status':'PASS','mutations':len(controls),'controls':controls,'limits':'Only these targeted corruptions were tested; this is not checker completeness or formal verification.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
