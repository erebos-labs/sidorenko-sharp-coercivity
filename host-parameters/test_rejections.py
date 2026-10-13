#!/usr/bin/env python3
"""Meaningful semantic rejection controls for the bounded host audit.

MIT License, copyright (c) 2026 Erebos Labs. Changes only temporary inputs.
"""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parent

def main():
    if not __debug__:raise RuntimeError('Optimized Python is refused.')
    original=json.loads((ROOT/'certificates/audit_inputs.json').read_text())
    controls=[]
    mutations=[
      ('inadmissible dimension',{'new_D':598,'new_r':299},'even_rank_reversal'),
      ('odd rank loses retained sign reversal',{'new_r':301},'even_rank_reversal'),
      ('mode-removal floor not reached',{'new_D':596,'new_r':298},'integer_mode_admission'),
      ('rank-layer prime floor only',{'prime_policy':'odd prime q >= 9600'},'complete_host_prime_condition'),
      ('missing factor two in field error budget',{'field_error_padding_power':5},'complete_kernel_error_padding'),
      ('dropped C_D polynomial exponent',{'rank_envelope_poly_power':255},'published_C_D_envelope'),
      ('one coordinate omitted',{'coordinate_count':65},'tensor_product_multiplicity'),
      ('invalid activation theta',{'theta':'3/2'},'activation_theta'),
      ('branch weights fail normalization',{'sign_branch_weights':['1/2','1/3']},'activation_branch_weights'),
      ('empty product replaced by zero',{'empty_product':0},'empty_product_normalization'),
      ('nonidentity pinning padding shortened',{'score_base_power':2458},'pinning_score_base'),
      ('all-map count replaced by injective bound',{'map_count_power':100},'all_type_map_count'),
      ('independent incidence draws removed',{'independent_incidence_draws':False},'independent_repeated_type_pairs'),
      ('repeated type pair thinned only once',{'incidence_reuse_count':1},'independent_repeated_type_pairs'),
      ('collision pair omitted',{'collisions':594},'all_map_collision_budget'),
      ('loop or collision budget underpaid',{'host_loss':660},'complete_sampling_budget'),
      ('half-gap host size shortened',{'host_half_gap_multiplier':1321},'half_gap_host_size'),
      ('kernel scaling power shortened',{'kernel_scale_multiplier':13},'bounded_kernel_scaling'),
      ('coin denominator undercounts rank powers',{'coin_matrix_multiplier':41},'exact_cloning_and_coins'),
      ('fixed host padding reduced to target gap',{'host_padding_power':10},'fixed_host_padding'),
      ('new host exponent corrupted',{'new_host_B':original['new_host_B']-1},'host_order_exponent'),
      ('injective-only host count',{'all_maps':False},'collapsed_original_H_homomorphisms'),
      ('robust fallback silently changed',{'fallback_residual':189},'fallback_1196_preserved'),
    ]
    with tempfile.TemporaryDirectory(prefix='host-audit-controls-') as td:
        for name,change,site in mutations:
            cfg=copy.deepcopy(original);cfg.update(change)
            data=(json.dumps(cfg,indent=2,sort_keys=True)+'\n').encode()
            p=Path(td)/'inputs.json';p.write_bytes(data)
            proc=subprocess.run([sys.executable,'-I','-B',str(ROOT/'check_audit.py'),'--inputs',str(p)],cwd=td,capture_output=True,timeout=60)
            expected=('AUDIT_FAILED: '+site+'\n').encode()
            if proc.returncode!=1 or proc.stdout or proc.stderr!=expected:
                raise RuntimeError('Wrong rejection site: '+name+' '+proc.stderr.decode(errors='replace'))
            controls.append({'name':name,'changed_fields':change,'rejection_site':site,'exit_code':1,
                             'input_sha256':hashlib.sha256(data).hexdigest(),'status':'REJECTED_AS_EXPECTED'})
        proc=subprocess.run([sys.executable,'-I','-B','-O',str(ROOT/'check_audit.py')],cwd=td,capture_output=True,timeout=10)
        if proc.returncode!=1 or proc.stdout or proc.stderr!=b'AUDIT_FAILED: optimized_python_not_accepted\n':
            raise RuntimeError('Optimized Python was not rejected')
        controls.append({'name':'optimized Python','rejection_site':'optimized_python_not_accepted','exit_code':1,'status':'REJECTED_AS_EXPECTED'})
        bad=Path(td)/'wrong_external.md';bad.write_bytes(b'not the retained source\n')
        proc=subprocess.run([sys.executable,'-I','-B',str(ROOT/'check_external_source.py'),str(bad)],cwd=td,capture_output=True,timeout=10)
        if proc.returncode==0 or proc.stdout or b'External source length mismatch' not in proc.stderr:
            raise RuntimeError('Incorrect external source accepted')
        controls.append({'name':'wrong optional external bytes','rejection_site':'External source length mismatch','status':'REJECTED_AS_EXPECTED'})
        bad.write_bytes(b'x'*80925)
        proc=subprocess.run([sys.executable,'-I','-B',str(ROOT/'check_external_source.py'),str(bad)],cwd=td,capture_output=True,timeout=10)
        if proc.returncode==0 or proc.stdout or b'External source SHA256 mismatch' not in proc.stderr:
            raise RuntimeError('Equal-length corrupted external source accepted')
        controls.append({'name':'equal-length wrong optional external bytes','rejection_site':'External source SHA256 mismatch','status':'REJECTED_AS_EXPECTED'})
    print(json.dumps({'status':'PASS','rejection_count':len(controls),'controls':controls,
          'limits':'These reject the specified corruptions only. Optional external positive byte binding remains NOT_RUN.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
