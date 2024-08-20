import os
import subprocess
home = os.getcwd()
for N in range(1,51):
        os.chdir(f'vector{N}')
        folder = os.getcwd()
        subfolders = [ f for f in os.scandir(folder) if f.is_dir() ]
        energies = []
        for fol in subfolders:
                fol = f'{fol}'
                energy = int(fol.split("'")[1])
                energies.append(energy)
        maxe = max(energies)
        path = os.path.join(folder, 'data.txt')
        if os.path.exists(path):
                conditions = []
                with open('data.txt', 'r') as infile:
                        lines = infile.readlines()
                        lines = lines[len(lines)-1]
                        check = int(lines.split()[0])
                        condition = str(lines.split()[1])
                        conditions.append(condition)
                if 'y' not in conditions:
                        if check != maxe:

                                with open ('job.slurm', 'r') as job:
                                        lines = job.read()
                                lines = lines.replace('submission.py',  'sub2.py')
                                lines = lines.replace('CP2K_test', f'vector{N}')
                               # lines = lines.replace(f'vector{N}', f'vector{N}(sub2)')
                                with open('job.slurm', 'w') as out:
                                        out.write(lines)
                                subprocess.run('sbatch job.slurm', shell= True)
                                os.chdir(home)
                        else:
                                with open ('job.slurm', 'r') as job:
                                        lines = job.read()
                                lines = lines.replace('sub2.py',  'submission.py')
                                lines = lines.replace('CP2K_test', f'vector{N}')
                               # lines = lines.replace(f'vector{N}', f'vector{N}(sub1)')
                                with open('job.slurm', 'w') as out:
                                        out.write(lines)
                                subprocess.run('sbatch job.slurm', shell= True)
                                os.chdir(home)
                else:
                        os.chdir(home)
        else:
                with open ('job.slurm', 'r') as job:
                        lines = job.read()
                lines = lines.replace('submission.py',  'sub2.py')
                lines = lines.replace('CP2K_test', f'vector{N}')
               # lines = lines.replace(f'vector{N}', f'vector{N}(sub2)')
                with open('job.slurm', 'w') as out:
                        out.write(lines)
                subprocess.run('sbatch job.slurm', shell= True)
                os.chdir(home)

