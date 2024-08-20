import numpy as np
import os
import math
import shutil
import subprocess
import sys
from numpy import pi, cos, sin, arccos, arange
import re
import random
from ovito.io import *
from ovito.modifiers import *
from ovito.pipeline import *

#import mpl_toolkits.mplot3d
#import matplotlib.pyplot as plt


n = int(sys.argv[1])
restart_check = str(sys.argv[2]) #y/n
num_pts = n

thetas = np.random.uniform(0, 2*np.pi, num_pts)
phis = np.arccos(np.random.uniform(0, 1, num_pts))
x = np.sin(phis) * np.cos(thetas)
y = np.sin(phis) * np.sin(thetas)
z = np.cos(phis)
points = []
points.append((x, y, z))


angle = float(pi/2) #direct random points along correct axis
def rotate_points_x(points, angle):
    points_array = np.array(points)
    rotation_matrix = np.array([[np.cos(angle), 0, np.sin(angle)],
                            [0, 1, 0],
                            [-np.sin(angle), 0, np.cos(angle)]])
    return np.dot(rotation_matrix, points_array.T).T


points_rotated = np.array(rotate_points_x(points, angle))



print(points_rotated)

coords = np.array(points_rotated[0])


# #Plot
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# #Unpack the coordinates
# x, y, z = coords[:, 0], coords[:, 1], coords[:, 2]
# ax.scatter(x, y, z)
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# plt.show()


starting_configs = int(sys.argv[3])
starting_range = [element for element in range (1, starting_configs + 1)]
start = int(1)
SEED = [random.randint(1, 10000) for _ in range(starting_configs)]

points_rotated = np.array(points_rotated[0])

file_check = ['starting_vectors.txt', 'seeds.txt']
for line in starting_range:
    file_check.append(str(line))

if restart_check == 'n':
    for file in file_check:
        if os.path.exists(file):
            if os.path.isfile(file):
                os.remove(file)
            elif os.path.isdir(file):
                shutil.rmtree(file)

    last_vector = int(1)
    with open('starting_vectors.txt', 'w') as vecs:
        for line in points_rotated:
            vecs.write(f'{line[0]} {line[1]} {line[2]}\n')

    with open('seeds.txt', 'w') as sed:
        for bit in SEED:
            sed.write(f'{bit}\n')

elif restart_check == 'y':
    current_directory = os.getcwd()


    directories = [name for name in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, name))]
    numbers = []
    for directory in directories:
        start_no = int(directory)
        numbers.append(start_no)
    if len(numbers) > 0:
        start = max(numbers)
    else:
        start = int(1)
        last_vector = int(1)




current = os.getcwd()
files_to_copy = ['in.YBCO', 'TABLE_s', 'YBa2Cu3O7.lmp']
for k in range(start, starting_configs + 1):
    with open('seeds.txt', 'r') as sed:
        lines = sed.readlines()
        seed =  int(lines[k-1])
    print(f'STARTING CONFIGURATION {k}')
    if os.path.exists(f'starting_vectors.txt'):
        with open('starting_vectors.txt', 'r') as inp:
            lines = inp.readlines()
            arr = []
            for line in lines:
                part = line.split()
                var = part[0], part[1], part[2]
                arr.append(var)
            points_rotated = np.array(arr,dtype= float)



    if os.path.exists(f'{k}'):
        os.chdir(f'{k}')
        current_directory = os.getcwd()
        directories = [name for name in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, name))]
        numbers = []
        for directory in directories:
            parts = directory.split('_')
            vecno = int(parts[1])
            numbers.append(vecno)
        if len(numbers) > 0:
            last_vector = max(numbers)
        else:
            last_vector = int(1)



    else:
        os.makedirs(str(k))
        for file in files_to_copy:
            path = os.path.join(current, str(k))
            shutil.copy(file, path)
        os.chdir(str(k))
        last_vector = int(1)




    for index, vector in enumerate(points_rotated[last_vector - 1:], start = (last_vector - 1)):
        print(f'STARTED VECTOR {index+1}')
        with open ('vectors.txt', 'a') as file:
            text = f'{index + 1} {vector[0]} {vector[1]} {vector[2]} \n'
            file.write(text)

        directory_name = f'vector_{index+1}'
        if os.path.exists(directory_name):
            shutil.rmtree(directory_name)

        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
            parent_dir = os.getcwd()
            path = os.path.join(directory_name, os.path.basename('in.YBCO'))
            shutil.copy('in.YBCO', path)
            os.chdir(directory_name)






        def generate_vector(vector, energy):
            print('Calculating vector...')
            scaled_vector = []
            O_mass = float(2.657E-26)
            electron_charge = float(1.602E-19)
            scale_factor = np.sqrt((2* energy * electron_charge)/(O_mass)) /100 #note first divisor is mass of one O atom, the 100 divisor is to conver to angstroms per picosecond
            scaled = [element * scale_factor for element in vector]
            scaled_vector.append(scaled)

            return scaled_vector






        def run_cascade(vector, energy):
            print('Running cascade...')
            directory_name = f'{energy}'
            if os.path.exists(directory_name):
                shutil.rmtree(directory_name)

            if not os.path.exists(directory_name):
                os.makedirs(directory_name)
                parent_dir = os.getcwd()
                directory_name2 = os.path.join(directory_name, os.path.basename('in.YBCO'))
                shutil.copy('in.YBCO', directory_name2)
                os.chdir(directory_name)
                with open('in.YBCO', 'r') as infile:
                    lines = infile.readlines()
                    for i, line in enumerate(lines):
                        if 'VAR' in line:
                            x = vector[0][0]
                            y = vector[0][1]
                            z = vector[0][2]
                            lines[i] = line.replace('VAR', f'{x} {y} {z}')
                        if 'SEED' in line:
                            lines[i] = line.replace('SEED', str(seed))

                with open('in.YBCO', 'w') as outfile:
                    outfile.writelines(lines)


                #subprocess.run('srun --cpu-bind=cores lmp_intel_cpu < in.YBCO', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run('mpirun lmp-mpi -in in.YBCO', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                os.chdir(parent_dir)
                path_to_out = os.path.join(directory_name, os.path.basename('prod.xyz'))

            return path_to_out



        def defect_check(a):
            print('Checking for defects..')
            # Load the final frame
            pipeline = import_file(f"{a}")

            # Perform Wigner-Seitz analysis using the reference frame as a seperate file
            ws_modifier = WignerSeitzAnalysisModifier(
                per_type_occupancies = True
                #eliminate_cell_deformation = True,
                #affine_mapping = ReferenceConfigurationModifier.AffineMapping.ToReference
            )


            pipeline.modifiers.append(ws_modifier)

            for frame in range(1, pipeline.source.num_frames + 1):
                data = pipeline.compute(frame)
                occupancies = data.particles['Occupancy'].array
                occupancy2 = 0 #total num interstitial
                occupancy0 = 0 #total num vacancies
                # Get the site types as additional input:
                site_type = data.particles['Particle Type'].array
                # Calculate total occupancy of every site:
                total_occupancy = np.sum(occupancies, axis=1)
                #print(total_occupancy)
                for element in total_occupancy:
                    if element == 0:
                        occupancy0 +=1
                    if element >= 2:
                        occupancy2 += (1 + (element-2))
                # Set up a particle selection by creating the Selection property:
                selection = data.particles_.create_property('Selection')

                # Select A-sites occupied by exactly one B, C, or D atom
                # (the occupancy of the corresponding atom type must be 1, and all others 0)
                selection[...] =((site_type == 1) & (occupancies[:, 1] == 1) & (total_occupancy == 1)) | \
                                ((site_type == 1) & (occupancies[:, 2] == 1) & (total_occupancy == 1)) | \
                                ((site_type == 1) & (occupancies[:, 3] == 1) & (total_occupancy == 1)) | \
                                ((site_type == 2) & (occupancies[:, 2] == 1) & (total_occupancy == 1)) | \
                                ((site_type == 2) & (occupancies[:, 3] == 1) & (total_occupancy == 1)) | \
                                ((site_type == 4) & (occupancies[:, 2] == 1) & (total_occupancy == 1))

                # Count the total number of antisite defects
                antisite_count = np.count_nonzero(selection[...])

                # Output the total number of antisites as a global attribute:
                data.attributes['Antisite_count'] = antisite_count
                tot_num_defects = antisite_count + occupancy0 + occupancy2


            return tot_num_defects

        def select_energy(results_list):
            num_rows = len(results_list) // 2
            results_list = (np.array(results_list)).reshape(num_rows, 2)




            prev_two_energies = results_list[-1:]
            energy_column = [float(row[1]) for row in prev_two_energies]

            new_energy = float(max(energy_column)) + 1


            return new_energy

        energy = float(1)
        initial_vector = generate_vector(vector, energy = 1)
        cascade1 = run_cascade(initial_vector, energy = 1)
        check = defect_check(cascade1)
        results_list = []
        if check != 0:
            results_list.append('y')
            results_list.append(energy)

        else:
            results_list.append('n')
            results_list.append(energy)

        print(f'Finished step 1')

        if 'n' in results_list:
            energy = float(2)
            initial_vector = generate_vector(vector, energy = 2)
            cascade1 = run_cascade(initial_vector, energy = 2)
            check = defect_check(cascade1)
            if check != 0:
                results_list.append('y')
                results_list.append(energy)

            else:
                results_list.append('n')
                results_list.append(energy)
            print(f'Finished step 2')


        i = 1
        if 'y' not in results_list:
            while i <= 100:
                energy = select_energy(results_list)
                PKA_vector = generate_vector(vector, energy)
                initiate_cascade = run_cascade(PKA_vector, energy)
                WS_analysis = defect_check(initiate_cascade)
                if WS_analysis != 0:
                    results_list.append('y')
                    results_list.append(energy)
                    i = 100

                else:
                    results_list.append('n')
                    results_list.append(energy)

                print(f'Finished step {i+2}')
                i += 1

            with open ('data.txt', 'w') as outfile:
                num_rows = len(results_list) // 2
                results_list = (np.array(results_list)).reshape(num_rows, 2)
                for row in results_list:
                    outfile.write(f'{row[0]} {row[1]}\n')


            os.chdir(parent_dir)
        else:
            with open ('data.txt', 'w') as outfile:
                num_rows = len(results_list) // 2
                results_list = (np.array(results_list)).reshape(num_rows, 2)
                for row in results_list:
                    outfile.write(f'{row[0]} {row[1]}\n')
            os.chdir(parent_dir)





        parent = os.getcwd()
        directories = [d for d in os.listdir(parent) if os.path.isdir(os.path.join(parent, d))]
        vector_directories = [d for d in directories if "vector" in d]

        threshold_displacement_energies = []
        energy_for_average = []
        directory_name = f'vector_{index+1}'
        if directory_name in vector_directories:
        # Change the current working directory to the vector directory
            os.chdir(os.path.join(parent, directory_name))
            energies = []
            with open('data.txt', 'r') as infile:
                lines = infile.readlines()


                for line in lines:
                    element = line.split()
                    if 'y' in line:
                        energies.append(float(element[1]))
                    else:
                        None
            threshold_displacement = np.min(energies)
            var = f'{threshold_displacement} {directory_name}'
            energy_for_average.append(threshold_displacement)
            threshold_displacement_energies.append(var)
            os.chdir(parent)


        running_sum = 0
        count = 0

        averaged_energies = []

        for energy in energy_for_average:

            count += 1
            running_sum += energy


            average = running_sum / count


            averaged_energies.append(average)
        #threshold_displacement_energies = [x + (f' {y}') for x, y in zip(threshold_displacement_energies, averaged_energies)]

        average_td = np.average(np.array(energy_for_average))
        name = f'{n}vectors.txt'
        with open(name, 'a') as out, open('vectors.txt', 'r') as vec:
            lines = vec.readlines()
            for line in threshold_displacement_energies:

                part = re.split(r'[_\s]+', line)
                vector_coord = []
                for line2 in lines:
                    part2 = re.split(r'[_\s]+', line2)
                    if float(part2[0]) == float(part[2]):

                        x, y, z = part2[1], part2[2], part2[3]
                        string = f'{x} {y} {z}'
                        vector_coord.append(string)
                    else:
                        None
                for bit in vector_coord:
                    out.write(f'{line} {bit}\n')

    os.chdir(current)
