import numpy as np
from scipy.spatial import SphericalVoronoi, geometric_slerp
import os

parent = os.getcwd()
results = []
for directory in os.listdir(parent):
    if os.path.isdir(os.path.join(parent, directory)):
        os.chdir(directory)


        points = []
        with open('50vectors.txt', 'r') as xyz:
            lines = xyz.readlines()
            for line in lines:
                element = line.split()
                var = float(element[2]), float(element[3]), float(element[4])
                points.append(var)

        points1 = np.array(points)




        # Generate sample points on a sphere
        radius = 1
        center = np.array([0, 0, 0])
        i = 0


        sv = SphericalVoronoi(points1, radius, center)

        i = 1
        v = []

        for vertex in sv.vertices:
            if vertex[0] < 1:
                v.append(int(i))
            i += 1
        i = 1

        change = []
        for polyhdron in sv.regions:
            for element in v:
                if element in polyhdron:
                    change.append(int(i))


            i += 1

        change = list(dict.fromkeys(change))

        new_points = []
        for element in change:
            xyz = points1[element - 1]
            newx= -xyz[0]
            y, z = xyz[1], xyz[2]
            new_points.append((newx, y, z))


        new_points = np.array(new_points)
        new_points2 = np.concatenate((points1, new_points))
        sv1 = SphericalVoronoi(new_points2, radius, center)





        rows_to_remove = len(change)
        areas = (SphericalVoronoi.calculate_areas(sv1)).reshape(-1, 1)
        points = sv1.points
        string = np.concatenate((areas[:-rows_to_remove], points[:-rows_to_remove]), axis = 1)
        with open('vector_weights.txt', 'w') as out:
            for line in string:
                out.write(f'{line[0]} {line[1]} {line[2]} {line[3]}\n')
        print(np.sum(areas[:-rows_to_remove]))


        with open('vector_weights.txt', 'r') as inp1, open('50vectors.txt', 'r') as inp2:
            lines1 = inp1.readlines()
            xyz = []
            weights =[]
            for line in lines1:
                element = line.split()
                weight = element[0]
                x, y, z = element[1], element[2], element[3]
                var = f'{x} {y} {z}'
                xyz.append(var)
                weights.append(weight)

            lines2 = inp2.readlines()
            weighted_cont = []
            for line in lines2:
                i = 0
                for part in xyz:
                    if part in line:
                        stuff = line.split()
                        energy = float(stuff[0])
                        weight = float(weights[i])
                        bit = energy * weight
                        weighted_cont.append(bit)
                    i += 1
            var = np.sum(weighted_cont) / (2 * np.pi)
            results.append(var)
            os.chdir(parent)
            print(f'{np.sum(weighted_cont) / (2 * np.pi)} config {directory}')
            print(np.mean(results))
print(results)
for line in results:
    print(line)
