import shutil
import subprocess
import os
import sys
import numpy as np


parent = os.getcwd()
files = os.listdir(parent)

filelist = []
for file in files:
    filepath = os.path.join(parent, file)
    if os.path.isdir(filepath):
        filelist.append(int(file))
new_energy = str(np.max(np.array(filelist)))
os.chdir(new_energy)




subprocess.run('python3 ../tes.py 201 > out.txt', shell = True)
with open('out.txt', 'r') as data:
    lines = data.readlines()
    defect_check = []
for line in lines:
    if 'Poly' in line:
        defect_check.append(line)
if len(defect_check) != 0:
    with open ('MD-1.restart', 'r') as inp:
        lines = inp.readlines()
        start_index = -1
        end_index = -1
        start_string = '&CASCADE'
        end_string = '&END CASCADE'
        for i, line in enumerate(lines):
            if start_string in line:
                start_index = i
            if end_string in line:
                end_index = i
        if start_index != -1 and end_index != -1:
            del lines[start_index:end_index + 1]
    with open('MD-1.restart', 'w') as out:
        out.writelines(lines)
    subprocess.run('srun --hint=nomultithread --distribution=block:block cp2k.psmp -i MD-1.restart -o result.out', shell=True)
    subprocess.run('python3 ../tes.py 401 > out.txt', shell = True)
    with open('out.txt', 'r') as data:
        lines = data.readlines()
        defect_check = []
        for line in lines:
            if 'step 400' in line:
                if 'No' in line:
                    defect_check.append('no')
        if len(defect_check) != 0:
            os.chdir(parent)
            with open('data.txt', 'a') as out:
                out.write(f'{new_energy} n\n')
        else:
            os.chdir(parent)
            with open('data.txt', 'a') as out:
                out.write(f'{new_energy} y\n')

else:
    os.chdir(parent)
    with open('data.txt', 'a') as out:
        out.write(f'{new_energy} n\n')
