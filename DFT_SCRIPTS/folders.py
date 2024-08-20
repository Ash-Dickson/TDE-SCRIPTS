import os
import shutil
import subprocess


parent = os.getcwd()
files = os.listdir(parent)

vectors = []
with open('vectors.txt', 'r') as vec:
    lines = vec.readlines()
    for line in lines:
        element = line.split()
        vec_no = element[0]
        x, y, z = element[1], element[2], element[3]
        vectors.append((x, y, z))

for N in range(34, 40, 1):
    dir_name = str(f'vector{N}')
    directory_path = os.path.join(parent, dir_name)
    os.makedirs(directory_path)
    #dir_name2 = str(5)
    #directorypath2 = os.path.join(directory_path, dir_name2)
    #os.makedirs(directorypath2)

    files = ['YBCO.inp', 'sub2.py', 'tes.py', 'submission.py', 'job.slurm', 'GTH_POTENTIALS', 'BASIS_MOLOPT_UZH', 'supercell-6-6-2.xyz']
    for file in files:
        src = os.path.join(parent, file)
        dst = os.path.join(parent, directory_path)
        shutil.copy(src, dst)

    os.chdir(directory_path)
    with open ('YBCO.inp', 'r') as inp:
        lines = inp.readlines()
        for i, line in enumerate(lines):
            if 'VECTOR' in line:
                var = vectors[int(N - 1)]
                text = f'{var[0]} {var[1]} {var[2]}'
                lines[i] = line.replace('VECTOR', str(text))
        with open('YBCO.inp', 'w') as out:
            out.writelines(lines)

    with open('job.slurm', 'r') as inp:
        lines = inp.readlines()
        for i, line in enumerate(lines):
            if '#SBATCH --job-name=CP2K_test' in line:
                name = f'vector{N}'
                lines[i] = line.replace('CP2K_test', str(name))
        with open('job.slurm', 'w') as out:
            out.writelines(lines)

# Define the batch job submission command
    batch_job_command = "sbatch job.slurm"

# Submit the batch job
    subprocess.run(batch_job_command, shell=True)
    os.chdir(parent)
