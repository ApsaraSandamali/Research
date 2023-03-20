import subprocess

def run_instance(factFile,time=1800,memory=8000):
    cmd = f"singularity run ./image.sif New/domain.hddl New/fact{factFile}.hddl New/output/output{factFile}.txt {time} {memory}"
    return cmd

for i in range(500):
    cmd = run_instance(i)
    # get the output(i).txt
    # ['total_time']
    subprocess.run(cmd, shell=True)       