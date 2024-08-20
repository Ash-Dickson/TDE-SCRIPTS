import shutil
import subprocess
import os
import sys


parent = os.getcwd()
files = os.listdir(parent)
if os.path.exists('data.txt'):

    with open('data.txt', 'r') as inp:
        lines = inp.readlines()
        newe = []
        for line in lines:
            element = line.split()
            energy = int(element[0])
            marker = element[1]
            if str(marker) == 'n':
                newe.append(energy)
            if str(marker) == 'y':
                sys.exit()
        var = max(newe) + 2
        new_energy = str(var)
        dir_name = str(new_energy)
        directory_path = os.path.join(parent, dir_name)
        os.makedirs(directory_path)
        filelist = ['YBCO.inp', 'GTH_POTENTIALS', 'BASIS_MOLOPT_UZH', 'supercell-6-6-2.xyz']

        for file in filelist:
            src = os.path.join(parent, file)
            dst = os.path.join(parent, directory_path)
            if os.path.isfile(src):

                shutil.copy(src, dst)

        os.chdir(directory_path)
        with open ('YBCO.inp', 'r') as inp:
            lines = inp.readlines()
            for i, line in enumerate(lines):
                if 'VAR_E' in line:
                    lines[i] = line.replace('VAR_E', str(new_energy))
        with open('YBCO.inp', 'w') as out:
            out.writelines(lines)



    # Define the batch job submission command
        batch_job_command = "srun --hint=nomultithread --distribution=block:block cp2k.psmp -i YBCO.inp -o result.out"

    # Submit the batch job
        subprocess.run(batch_job_command, shell=True)

        subprocess.run('python3 ../tes.py 201 > out.txt', shell = True)
        with open('out.txt', 'r') as data:
                lines = data.readlines()
                defect_check = []
        for line in lines:
            if 'Poly' in line:
                defect_check.append(line)
        if len(defect_check) == 0:
            os.chdir(parent)
            with open('data.txt', 'a') as out:
                out.write(f'{new_energy} n\n' )
else:
    new_energy = str(1)
    dir_name = str(new_energy)
    directory_path = os.path.join(parent, dir_name)
    os.makedirs(directory_path)
    filelist = ['YBCO.inp', 'GTH_POTENTIALS', 'BASIS_MOLOPT_UZH', 'supercell-6-6-2.xyz']

    for file in filelist:
        src = os.path.join(parent, file)
        dst = os.path.join(parent, directory_path)
        if os.path.isfile(src):

            shutil.copy(src, dst)

    os.chdir(directory_path)
    with open ('YBCO.inp', 'r') as inp:
        lines = inp.readlines()
        for i, line in enumerate(lines):
            if 'VAR_E' in line:
                lines[i] = line.replace('VAR_E', str(new_energy))
    with open('YBCO.inp', 'w') as out:
        out.writelines(lines)



# Define the batch job submission command
    batch_job_command = "srun --hint=nomultithread --distribution=block:block cp2k.psmp -i YBCO.inp -o result.out"

# Submit the batch job
    subprocess.run(batch_job_command, shell=True)

    subprocess.run('python3 ../tes.py 201 > out.txt', shell = True)
    with open('out.txt', 'r') as data:
            lines = data.readlines()
            defect_check = []
    for line in lines:
        if 'Poly' in line:
            defect_check.append(line)
    if len(defect_check) == 0:
        os.chdir(parent)
        with open('data.txt', 'a') as out:
            out.write(f'{new_energy} n\n' )
