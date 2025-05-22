import math
from vpython import *

scene = canvas(width=600, height=600)

starting_rope_length = 1.5
initial_angle = 0
initial_velocity = 0
distance_between_pivot_and_point = 1.0

def findStartingPositionForMass() -> vector:
    pivot_to_mass = vector(cos(initial_angle), sin(initial_angle), 0) * starting_rope_length
    return pivot.pos + pivot_to_mass

pivot = box(pos=vector(0,0.9,0), length=0.03, height=0.03, width=0.03, color=color.blue)
mass = sphere(pos=findStartingPositionForMass(), radius=0.03, color=color.blue)
point = sphere(pos=(pivot.pos-vector(0, distance_between_pivot_and_point, 0)), radius = 0.03, color=color.blue)
string = box(pos = (pivot.pos + mass.pos)/2, width=0.005, height=0.005, axis=(mass.pos - pivot.pos))

# angle_to_pivot = initial_angle
# angle_around_point = -math.pi/2

# def get_effective_rope_length() -> float:
#     if (angle_to_pivot > -math.pi/2):
#         return starting_rope_length
#     else:


while True:
    string.axis=(mass.pos - pivot.pos)
    