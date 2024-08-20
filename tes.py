import numpy as np 
import pyvoro
from scipy.spatial import Delaunay


result = []
with open ('prod.xyz', 'r') as inp:
    
    lines = inp.readlines()
    natoms = int(63999)
    for i in range(0, len(lines), (natoms + 2)):
        sublist = lines[i + 16:i+938]
        result.append(sublist)




#reference configuration
reference_config = []
for i in result[0]:
    ele = i.split()
    points = [float(ele[2]), float(ele[3]), float(ele[4])] 
    reference_config.append(points)

reference_points = np.array(reference_config)
reference_points = reference_points.astype(float) 

result = []
with open ('prod.xyz', 'r') as inp:
    
    lines = inp.readlines()
    natoms = int(63999)
    for i in range(0, len(lines), (natoms + 16)):
        sublist = lines[i + 16:i+(natoms + 16)]
        result.append(sublist)


n = float(0.5)

xmin = min(reference_points[:, 0]) - n
xmax = max(reference_points[:, 0]) + n

ymin = min(reference_points[:, 1]) - n
ymax = max(reference_points[:, 1]) + n

zmin = min(reference_points[:, 2]) - n
zmax = max(reference_points[:, 2]) + n

voronoi = pyvoro.compute_voronoi(reference_points,[[xmin, xmax],[ymin, ymax],[zmin, zmax]],1)




def wigner_seitz(voronoi, step_number):

    list_of_vertices = [np.array(vnoicel['vertices']) for vnoicel in voronoi]

    triangulations = [Delaunay(np.array(polyhedra).reshape(-1, 3)) for polyhedra in list_of_vertices]

    new_points = [
        np.array(
            element.strip().replace('\n', '').split()[1:],
            dtype=float
        )
        for element in result[step_number]
    ]
    #how many points in polyhedron? 
    counts = []

    for triangulation in triangulations:

        count = 0
        for point in new_points:
            point1 = (triangulation.points[1])
            point2 = point
            dist = np.linalg.norm(point1 - point2)
            if dist < 6:
                if triangulation.find_simplex(point) >= 0:
                    count += 1
        counts.append(count)

    return counts, new_points




for step_number in range(1, 2, 1):  #in brackets first number means the step number the script starts from,
    #second number means step number it ends on (note that if you want it to end on step 50, you must enter 
    #51 because python things). The last number indicates how regularly the check is performed, in this case
    #every 10 steps. The step number relates to 
    counts, new_points = wigner_seitz(voronoi, step_number)

    all_defects_false = True
    for i, count in enumerate(counts):
        defect = count != 1
        if defect:
            print(f"Polyhedron {i + 1}: {count} points inside at step {step_number}")
            all_defects_false = False 

    if all_defects_false:
        print(f"No defects found in any polyhedron at step {step_number}")
    

   




