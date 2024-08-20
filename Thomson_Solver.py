import numpy as np
import os 


'''TO DO:
        - Comment lines
        - Add convergence criteria
        - Add read me and how to run, allow acces to all variables from terminal
        - RDF pre and post min
        '''

def random_sphere_points(num_points):
    theta = np.random.uniform(0, 2 * np.pi, num_points)  
    phi = np.arccos(1 - 2 * np.random.uniform(0, 1, num_points)) 
    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)
    return np.column_stack((x, y, z))


def initialise(num_points):
    velocities = np.zeros((int(num_points), 3))
    acceleration = np.zeros((int(num_points), 3))
    positions = random_sphere_points(num_points)
    return velocities, acceleration, positions

def predictor(velocities, acceleration, positions, timestep):
    #move atoms 
    num_points = velocities.shape[0]
    for i in range (0, num_points):
        positions[i] = positions[i] + (velocities[i] * int(timestep)) + (1/2 * acceleration[i] * timestep**2)
        velocities[i] = positions[i] + (velocities[i] * int(timestep)) + (1/2 * acceleration[i] * timestep**2)
        #normalise to sphere surface
        positions[i] = positions[i] / np.linalg.norm(positions[i])
    return positions, velocities



def pair_potential(positions, mass):
    num_points = positions.shape[0]
    forces = np.zeros(((num_points), 3)) # Initialize force array
    potential_energy = np.zeros(((num_points), 1))

    for i in range(0, num_points):
        for j in range(0, num_points):
            if i != j:
                r_ij = positions[i] - positions[j]
                potential_energy[i] += 1/(np.linalg.norm(r_ij))
                distance = np.linalg.norm(r_ij)
                force_magnitude = 1 / distance**3
                forces[i] += force_magnitude * r_ij
    acceleration = forces / mass
    potential_energy = np.sum(potential_energy)
    return acceleration, potential_energy

def propogator(positions, acceleration, velocities, timestep, mass):
    num_points = velocities.shape[0]
    #step 1 
    for i in range (0, num_points):
        positions[i] = positions[i] + (velocities[i] * timestep) + (1/2 * acceleration[i] * timestep**2)
        #velocities for t + dt/2
        velocities[i] = velocities[i] + (1/2 * acceleration[i] * timestep)
    #step 2
    acceleration, potential_energy = pair_potential(positions, mass)
    for i in range(0, num_points):
        velocities[i] = velocities[i] + (1/2 * acceleration[i] * timestep)
        #normalise to sphere surface
        positions[i] = positions[i] / np.linalg.norm(positions[i])
    return positions, acceleration, velocities, potential_energy



num_points = int(input('How many points to minimise?'))
timestep = 1.0E-2
mass = 1
time = 0
positions = random_sphere_points(num_points) 
print('Initialising random positions....')
velocities, acceleration, positions = initialise(num_points)
print('Initialising velocities...')
print('Initialising acceleration...')


def MD(positions, velocities, acceleration, timestep, mass):
    positions, velocities = predictor(velocities, acceleration, positions, timestep)
    positions, acceleration, velocities, potential_energy = propogator(positions, acceleration, velocities, timestep, mass)
    return positions, velocities, acceleration, potential_energy

def print_xyz (positions, time):
    with open('pos.xyz', 'a') as f:
        f.write(f'{num_points}\ntime = {time}\n')
        for i in range(0, positions.shape[0]):
            x, y, z = positions[i]
            string = f'1 {x} {y} {z}\n'
            f.write(f'{string}')

def tot_ener(velocities, potential_energy, mass):
    KE = np.zeros(((num_points), 1))
    for i in range(0, num_points):
        KE[i] += 1/2 * mass * (np.linalg.norm(velocities[i]))**2
    KE = np.sum(KE)
    tot_E = KE + potential_energy
    return tot_E

        
    

parent = os.getcwd()
pos_filename = 'pos.xyz'
filepath = os.path.join(parent, pos_filename)
if os.path.exists(filepath):
    os.remove(filepath)

for t in range(1, 10000):
    positions, velocities, acceleration, potential_energy = MD(positions, velocities, acceleration, timestep, mass)
    tot_E = tot_ener(velocities, potential_energy, mass)
    if t % 10 == 0:  
        print(f'Timestep = {t}, time (s) = {time:.3g}, Total Energy = {tot_E:.9g}')
    print_xyz(positions, time)
    time += timestep






        



    



