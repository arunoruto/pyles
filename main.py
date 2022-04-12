import wave
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from particles import Particles
from initial_field import InitialField
from parameters import Parameters
from numerics import Numerics
from simulation import Simulation

spheres = pd.read_csv('data/sphere_parameters.txt', names = ['x', 'y', 'z', 'r', 'n', 'k'])
wavelength = pd.read_csv('data/lambda.csv', header=None).to_numpy()

particles = Particles(spheres.values[:,0:3], spheres.values[:,3], spheres.values[:,4:])
initial_field = InitialField(beam_width=2000,
  focal_point=np.array((0,0,0)),
  polar_angle=0,
  azimuthal_angle=0,
  polarization='TE'
  )
inputs = Parameters(
  wavelength=wavelength,
  medium_mefractive_index=np.ones(wavelength.shape) * 1.63,
  particles=particles,
  initial_field=initial_field)
numerics = Numerics(4,
  np.arange(0, np.pi * (1 + 1/5e3), np.pi / 5e3),
  np.arange(0, np.pi * (2 + 1/1e2), np.pi / 1e2),
  gpu=True)

simulation = Simulation(particles, numerics)
simulation.compute_mie_coefficients()

# fig = go.Figure()
# fig.add_trace(go.Scatter3d(
#   x = spheres.x,
#   y = spheres.y,
#   z = spheres.z,
#   mode = 'markers',
#   marker = dict(
#     sizemode = 'diameter',
#     sizeref = 10,
#     size = spheres.r * 2,
#     color = spheres.r,
#     opacity = 0.5
#   )
# ))
# fig.add_trace(go.Scatter3d(
#   x = particles.hull[:,0],
#   y = particles.hull[:,1],
#   z = particles.hull[:,2],
#   mode = 'markers',
#   marker = dict(
#     color = "red",
#     opacity = 1
#   )
# ))
# fig.show()