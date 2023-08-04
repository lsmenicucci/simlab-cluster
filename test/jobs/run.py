#!/usr/bin/env python3
from subprocess import run
from tempfile import TemporaryDirectory
from pathlib import Path
from contextlib import contextmanager
import os, sys

try:
    from rich import print 
except ImportError:
    pass

script_exts = ['.sh', '.py']
PYBIN = sys.executable

@contextmanager
def in_dir(dirpath):
    old_dir = Path.cwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_dir)

def print_job_header(job, tempfolder):
    job_header = f"{job['sub_script']}"
    print(f"-- {job_header} {'-'*(80-len(job_header))}")
    print(f"  Running job: {job['sub_script']}")
    print(f"  Temp folder: {tempfolder}")

    files = ['sub_script', 'pre_script', 'check_script']
    for f in files:
        v = job.get(f, None)
        print(f"  {f}: {v}")


def run_test_job(test_job):
    script_src = test_job['sub_script']
    assert script_src.exists(), f'Jobscript {script_src} does not exist'

    with TemporaryDirectory(dir=Path.home(), prefix=".test-job-") as tmpdir:
        tmpdir = Path(tmpdir)
        print_job_header(test_job, tmpdir)
        print()

        job = with_temp_prefix(tmpdir, test_job)
     
        # copy folder to tmpdir
        if "copy_folder" in job:
            print(f"-- Copying folder: {job['copy_folder']}")
            for f in job['copy_folder'].glob('*'):
                run(['cp', '-R', f.as_posix(), tmpdir.as_posix()], check=True)

        # copy scripts to tmpdir
        path_keys = ['sub_script', 'pre_script', 'check_script']
        for k in path_keys:
            if k in job:
                job[k].write_text(test_job[k].read_text())

        # cd to tmpdir
        with in_dir(tmpdir):
            # run pre script if it exists
            if "pre_script" in job and job["pre_script"].exists():
                print(f"-- Runing pre script: {job['pre_script']}")
                run([PYBIN, job["pre_script"].as_posix()])
                print()

        with in_dir(tmpdir):
            # run job script
            print(f"-- Running job script: {job['sub_script']}")
            run(['sbatch', job["sub_script"].as_posix()])
            print()
        
        with in_dir(tmpdir):
            # run check script if it exists
            if "check_script" in job and job["check_script"].exists():
                print(f"-- Runing check script: {job['check_script']}")
                res = run([PYBIN, job["check_script"].as_posix()])

def with_temp_prefix(temp_path, job): 
    path_keys = ['sub_script', 'pre_script', 'check_script']
    temp_job = { **job }
    for k, v in job.items():
        if k in path_keys:
            temp_job[k] = temp_path / v.name

    return temp_job 


def find_auxiliary_scripts(job):
    # find pre script
    for ext in script_exts:
        pre_script = script.with_name(script.stem)
        pre_script = pre_script.with_suffix('.pre' + ext)
        if pre_script.exists():
            job["pre_script"] = pre_script
            break

    # find check script
    for ext in script_exts:
        check_script = script.with_name(script.stem)
        check_script = check_script.with_suffix('.check' + ext)
        print(check_script)
        if check_script.exists():
            job["check_script"] = check_script
            break

    return job

def find_folder_job(folder):
    files = {
        "sub_script": "job.sh",
        "pre_script": "pre.py",
        "check_script": "check.py"
    }
    job = { "copy_folder": folder }
    for k, v in files.items():
        path = folder / v
        if path.exists():
            job[k] = path

    if "sub_script" not in job:
        return None

    return job

if __name__ == '__main__':
    print("Discovering jobscripts...", end=' ')
    here = Path(__file__).parent
    
    test_jobs = {}
    
    for script in here.glob('*.sh'):
        test_jobs[script.name] = { "sub_script": script }
        find_auxiliary_scripts(test_jobs[script.name])

    # discover folders
    for folder in here.glob('*'):
        if not folder.is_dir():
            continue
        
        job = find_folder_job(folder)
        if job:
            test_jobs[folder.name] = job

    
    print(f"Found {len(test_jobs)} test jobs")

    for t in test_jobs.values():
        run_test_job(t)
        print("="*80)
