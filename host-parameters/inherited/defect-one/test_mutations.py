#!/usr/bin/env python3
"""Require rejection of specified corruptions; only temporary local files change."""
from __future__ import annotations
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent

def digest(data):return hashlib.sha256(data).hexdigest()

def main():
    if not __debug__: raise RuntimeError('run without -O or -OO')
    src={'certificate':json.loads((ROOT/'certificates/template_and_budget.json').read_text()),
         'coefficients':json.loads((ROOT/'certificates/proof_coefficients.json').read_text()),
         'controls':json.loads((ROOT/'certificates/controls.json').read_text())}
    tests=[
        ('gain_removed','coefficients',['gain_per_plane'],0,'identity:robust_actual_defect_exponent'),
        ('wrong_basis_power','coefficients',['basis_power_per_plane'],3,'identity:gain_after_full_basis_division'),
        ('missing_intersection_allowance','coefficients',['step_cost_coefficients','111'],[2,-1,-1,0,0],'identity:step_cost_111'),
        ('missing_dependent_endpoint_cost','coefficients',['step_cost_coefficients','001'],[0,0,0,0,0],'identity:step_cost_001'),
        ('two_sided_defect_misclassified','coefficients',['defect_values','011'],1,'defect_value:011'),
        ('unsupported_smaller_remainder','certificate',['defect_one_remainder'],240,'defect_one_remainder'),
        ('missing_pattern_prefactor','certificate',['defect_one_prefactor_power'],117,'complete_pattern_prefactor'),
        ('corrupted_robust_remainder','certificate',['robust_remainder'],1195,'retained_1196'),
        ('actual_defect_dropped','coefficients',['higher_defect_D_multiplier'],1,'actual_defect_two_multiplier'),
        ('integer_mode_threshold_lowered','certificate',['new_sufficient_even_D'],598,'integer_mode_removal_threshold'),
        ('field_threshold_lowered','certificate',['minimum_field_size'],9599,'retained_field_threshold'),
        ('full_bases_assumed_in_line_pattern','controls',['q13_first_line_bases'],26208,'control_line_basis_count'),
    ]
    records=[]
    with tempfile.TemporaryDirectory(prefix='sidorenko-defect-mutations-') as td:
        tmp=Path(td)
        for name,which,path,value,site in tests:
            data=deepcopy(src[which]);obj=data
            for key in path[:-1]:obj=obj[key]
            old=obj[path[-1]];obj[path[-1]]=value
            text=(json.dumps(data,indent=2)+'\n').encode();fp=tmp/(name+'.json');fp.write_bytes(text)
            cmd=[sys.executable,'-I','-B',str(ROOT/'check_exact.py'),'--'+which,str(fp)]
            run=subprocess.run(cmd,capture_output=True,timeout=60)
            err=run.stderr.decode()
            if run.returncode==0 or 'CHECK_FAILED: '+site not in err:
                raise RuntimeError(f'mutation {name} was not rejected at {site}: {run.returncode} {err}')
            records.append({'test':name,'changed_field':'.'.join(map(str,path)),
                'old':old,'new':value,'input_sha256':digest(text),'exit_code':run.returncode,
                'expected_failure':site,'stderr':err.strip(),'stdout_sha256':digest(run.stdout),
                'status':'REJECTED_AS_EXPECTED'})
        # Copy only the material needed for this source-integrity mutation.
        cp=tmp/'source_mutation';cp.mkdir()
        shutil.copy2(ROOT/'check_exact.py',cp/'check_exact.py')
        shutil.copy2(ROOT/'SOURCES.json',cp/'SOURCES.json')
        shutil.copytree(ROOT/'sources',cp/'sources')
        shutil.copytree(ROOT/'certificates',cp/'certificates')
        f=cp/'sources/published/THEOREM.md';f.write_bytes(f.read_bytes()+b'\n')
        run=subprocess.run([sys.executable,'-I','-B',str(cp/'check_exact.py')],capture_output=True,timeout=60)
        err=run.stderr.decode();site='source_length:sources/published/THEOREM.md'
        if run.returncode==0 or site not in err: raise RuntimeError('source corruption not detected')
        records.append({'test':'pinned_source_byte_corruption','exit_code':run.returncode,
                        'expected_failure':site,'stderr':err.strip(),'status':'REJECTED_AS_EXPECTED'})
        run=subprocess.run([sys.executable,'-I','-B','-O',str(ROOT/'check_exact.py')],capture_output=True,timeout=60)
        err=run.stderr.decode();site='optimized_python_not_accepted'
        if run.returncode==0 or site not in err:raise RuntimeError('optimized invocation not rejected')
        records.append({'test':'optimized_python','exit_code':run.returncode,
                        'expected_failure':site,'stderr':err.strip(),'status':'REJECTED_AS_EXPECTED'})
    print(json.dumps({'status':'PASS','mutations_rejected':len(records),'tests':records,
          'limit':'These controls detect the stated corruptions, not every possible checker or proof error.'},indent=2))
if __name__=='__main__':main()
