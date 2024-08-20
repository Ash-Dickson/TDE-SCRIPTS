start_string = ''' #YBa2Cu3O7 unitcell

         936  atoms
           4  atom types

      0.76      23.86  xlo xhi
      1.4     24.8  ylo yhi
      1.36      24.86  zlo zhi
	0 0 0 xy xz yz

Atoms
'''
import sys
filename = str(sys.argv[1])
with open(f'{filename}.xyz', 'r') as f:
    lines = f.readlines()
    list = []
    for line in lines[2:]:
        element = line.split()
        type, x, y, z = element[0], element[1], element[2], element[3]
        if type == 'Ba':
            type = f'1 1.3' 
        elif type == 'Y':
            type = f'2 1.9' 
        elif type == 'Cu':
            type = f'3 1.4' 
        elif type == 'O':
            type = f'4 -1.3' 
        list.append(f'{type} {x} {y} {z}\n')
    with open(f'{filename}.lmp', 'w') as o:
        o.write(f'{start_string}\n')
        for index, line in enumerate(list, start = 1):
            o.write(f'{index} {line}')

