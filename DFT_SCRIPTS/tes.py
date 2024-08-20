import numpy as np
import pyvoro
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import Delaunay
import sys
range_no = int(sys.argv[1])
rng = np.random.default_rng(11)
result = []
with open ('MD-pos-1.xyz', 'r') as inp:

    lines = inp.readlines()
    for i in range(0, len(lines), 938):
        sublist = lines[i + 2:i+938]
        result.append(sublist)


#reference configuration
reference_config = []
for i in result[0]:


    lines = i.strip().replace('\n', '').replace('Cu', '').replace('Ba', '').replace('O', '').replace('Y', '').split()
    a = reference_config.append(lines)

reference_points = np.array(reference_config)
reference_points = reference_points.astype(float)

n = float(1.0)

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
            element.strip().replace('\n', '').replace('Cu', '').replace('Ba', '').replace('O', '').replace('Y', '').split(),
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
            if dist < 8:
                if triangulation.find_simplex(point) >= 0:
                    count += 1
        counts.append(count)
    return counts, new_points




for step_number in range(25, range_no, 25):
    counts, new_points = wigner_seitz(voronoi, step_number)

    all_defects_false = True
    for i, count in enumerate(counts):
        defect = count != 1
        if defect:
            print(f"Polyhedron {i + 1}: {count} points inside at step {step_number}")
            all_defects_false = False
    if all_defects_false:
        print(f"No defects found in any polyhedron at step {step_number}")





fig = plt.figure()
fig.set_size_inches(8, 8)
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_zlim(zmin, zmax)

ax.view_init(elev=0, azim=90)
for vnoicell in voronoi:

    faces = []

    list_of_vertices = np.array(vnoicell['vertices'])
    for face in vnoicell['faces']:
        faces.append(list_of_vertices[np.array(face['vertices'])])

    # join the faces into a 3D polygon
    polygon = Poly3DCollection(faces, alpha=0.5,
                               facecolors=rng.uniform(0,1,3),
                               linewidths=0.5,edgecolors='black')
    ax.add_collection3d(polygon)
#ax.scatter(new_points[:, 0], new_points[:, 1], new_points[:, 2], c='red', marker='o')
plt.show()
