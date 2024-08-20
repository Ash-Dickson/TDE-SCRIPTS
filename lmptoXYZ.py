with open('YBCO.lmp', 'r') as f:
    lines = f.readlines()
    list = []
    for line in lines[12:]:
        element = line.split()
        var = num, type, charge, x, y, z = element[0], element[1], element[2],  element[3], element[4], element[5]
        list.append(f'{type} {x} {y} {z}\n')
    with open('YBa2Cu3O7.xyz', 'w') as o:
        o.write('936\n')
        o.write('comment\n')
        for line in list:
            o.write(str(line))

