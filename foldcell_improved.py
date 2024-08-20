import numpy as np
import os

# lattice_vectors = np.array([
            #     [3.869, 0, 0],
            #     [0, 3.958, 0],
            #     [0, 0, 11.854]
            # ])
lattice_vectors = np.array([
    [3.9302, 0, 0],
    [0, 3.9513, 0],
    [0, 0, 11.9497]
])



tolerance_range = 0.04

i1_list = [(0.5, 0.5, 0), (0.5, 0.5, 1)]
i2_list = [(0.5, 0, 0), (0.5, 1, 0), (0.5, 0, 1), (0.5, 1, 1), (0.5, 1-(tolerance_range*2), 0), (0.5, 1-(tolerance_range*2), 1), (0.5, 0 + (tolerance_range*2), 0), (0.5, 0 + (tolerance_range*2), 1)]
i3_list = [(0, 0.5, 0.1584), (1, 0.5, 0.1584), (0, 0.5, 0.8416), (1, 0.5, 0.8416)]
i4_list = [((0.5, 0, 0.1584)), (0.5, 1, 0.1584), (0.5, 0, 0.8416), (0.5, 1, 0.8416)]
i5_list = [(1, 0, 0.5), (0, 0, 0.5), (1, 1, 0.5), (0, 1, 0.5)]
i6_list = [(0.5, 0, 0.5), (0.5, 1, 0.5)]
i7_list = [(0, 0.5, 0.5), (1, 0.5, 0.5)]
conditions = i1_list, i2_list, i3_list, i4_list, i5_list, i6_list, i7_list

list_names = ['i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7']

counts = {}
for name in list_names:
    counts[name + 'count'] = 0



def read_xyz(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        num_atoms = int(lines[0].strip())
        comment = lines[1].strip()
        atom_data = [line.strip().split() for line in lines[-num_atoms:]]
        atom_types = [data[0] for data in atom_data]
        positions = np.array([[float(data[1]), float(data[2]), float(data[3])] for data in atom_data])

        min_coords = positions[224]
        cell_size = np.array([6, 6, 2])
        supercell = cell_size * np.diag(lattice_vectors)

        # Subtract the minimum coordinates to shift the origin
        positions -= min_coords

        # Apply periodic boundary conditions using modulo operations
        for k in range(num_atoms):
            for i in range(3):
                positions[k][i] = positions[k][i] % supercell[i]
           
    return atom_types, positions


def write_xyz(file_path, atom_types, positions):
    with open(file_path, 'w') as file:
        file.write(f"{len(atom_types)}\n")
        file.write("Collapsed to unit cell\n")
        for atom, pos in zip(atom_types, positions):
            file.write(f"{atom} {pos[0]:.6f} {pos[1]:.6f} {pos[2]:.6f}\n")


def map_to_unit_cell(positions, lattice_vectors):
    inv_lattice = np.linalg.inv(lattice_vectors)
    reduced_positions = np.dot(positions, inv_lattice)
    reduced_positions %= 1.0  # Wrap positions to the unit cell (0 <= pos < 1)
    return np.dot(reduced_positions, lattice_vectors)

def collapse_supercell_to_unit_cell(xyz_file, lattice_vectors, output_file):
    atom_types, positions = read_xyz(xyz_file)
    reduced_positions = map_to_unit_cell(positions, lattice_vectors)
    write_xyz(output_file, atom_types, reduced_positions)
    return reduced_positions

def check_unit_cell_defect(reduced_positions):
    frac_positions = reduced_positions / np.diag(lattice_vectors)
    for coord in frac_positions:
        for index, condition in enumerate(conditions):
            for ref_coord in condition:
                if (ref_coord[0]-tolerance_range <= coord[0] <= ref_coord[0] + tolerance_range) and (ref_coord[1]-tolerance_range <= coord[1] <= ref_coord[1] + tolerance_range) and (ref_coord[2]-tolerance_range <= coord[2] <= ref_coord[2] + tolerance_range):
                    list_name = list_names[index]
                    list_name = list_name.split('_')[0]
                    check = list_name + 'count'
                    if check in counts:
                        counts[check] += 1

    return frac_positions, counts



parent = os.getcwd()
folders = []
for N in range(1, 51):
	string = f'vector_{N}'
	folders.append(string)



for folder in folders:
    path = os.path.join(parent, folder)
    if os.path.isdir(path) and not folder.startswith('.'):
        os.chdir(path)
        vec_dir = os.getcwd()
        folders2 = os.listdir()
        f_list = []
        for f in folders2:
            path2 = os.path.join(vec_dir, f)
            if os.path.isdir(path2) and not f.startswith('.'):
                f_list.append(float(f))
        folder2 = str(float(max(f_list)))



        path2 = os.path.join(vec_dir, folder2)
        if os.path.isdir(path2) and not folder2.startswith('.'):
            os.chdir(folder2)
               
                    


            # Path to your XYZ file
            xyz_file = 'prod.xyz'
            # Output file for the collapsed unit cell
            output_file = 'collapsed_cell.xyz'
            # atom_types, positions = read_xyz(xyz_file)
            # write_xyz('test.xyz', atom_types, positions)

            # Call the function to collapse the supercell
            reduced_positions = collapse_supercell_to_unit_cell(xyz_file, lattice_vectors, output_file)
            frac_positions, counts = check_unit_cell_defect(reduced_positions)
        
            
print(counts)