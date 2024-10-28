import numpy as np
from random import uniform

class Particle:
    def __init__(self, x, y, ang_vel):
        self.x = x
        self.y = y
        self.ang_vel = ang_vel
        
class ParticleSimulator:
    def __init__(self, particles):
        self.particles = particles
        
    def evolve(self, dt):
        timestep = 0.00001
        nsteps = int(dt/timestep)
        
        for i in range(nsteps):
            for p in self.particles:
                # 1. calculate the direction
                norm = (p.x**2 + p.y**2)**0.5
                v_x = -p.y/norm
                v_y = p.x/norm
                # 2. calculate the displacement
                d_x = timestep * p.ang_vel * v_x
                d_y = timestep * p.ang_vel * v_y
                p.x += d_x
                p.y += d_y
                # 3. repeat for all the time steps
                
    def evolve_fast(self, dt):
        timestep = 0.00001
        nsteps = int(dt/timestep)
        # Loop order is changed
        for p in self.particles:
            t_x_ang = timestep * p.ang_vel
            for i in range(nsteps):
                norm = (p.x**2 + p.y**2)**0.5
                p.x, p.y = (p.x - t_x_ang * p.y/norm,p.y + t_x_ang * p.x/norm)

    def evolve_numpy(self, dt):
        timestep = 0.00001
        nsteps = int(dt/timestep)

        r_i = np.array([[p.x, p.y] for p in self.particles])
        t_ang_vel_i = np.array([p.ang_vel for p in self.particles])*timestep

        for i in range(nsteps):
            norm_i = np.sqrt((r_i ** 2).sum(axis=1))
            v_i = r_i[:, [1, 0]]
            v_i[:, 0] *= -1
            v_i /= norm_i[:, np.newaxis]
            r_i += t_ang_vel_i[:, np.newaxis] * v_i

        for i, p in enumerate(self.particles):
            p.x, p.y = r_i[i]
                
def benchmark(npart=1000,method='python'):
    particles = [Particle(uniform(-1.0, 1.0),
                    uniform(-1.0, 1.0),
                    uniform(-1.0, 1.0))
                    for i in range(npart)]
    simulator = ParticleSimulator(particles)

    if method=='python':
        simulator.evolve(0.1)
    elif method=='pythonfast':
        simulator.evolve_fast(0.1)
    elif method=='numpy':
        simulator.evolve_numpy(0.1)
    simulator.evolve(0.1)
    
if __name__ == '__main__':
    benchmark()