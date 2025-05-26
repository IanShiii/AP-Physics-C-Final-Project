import math
from vpython import *

dt = 0.002
steps_per_second = 100

scene = canvas(width=600, height=600)

starting_rope_length = 1.5
initial_angle = 0
initial_angular_velocity = 0
distance_between_pivot_and_point = 0.75

def find_position_of_mass_about_pivot_1(angle: float) -> vector:
    pivot_1_to_mass = vector(cos(angle), sin(angle), 0) * starting_rope_length
    return pivot_1.pos + pivot_1_to_mass

def find_position_of_mass_about_pivot_2(angle: float, effective_rope_length: float) -> vector:
    pivot_2_to_mass = vector(cos(angle), sin(angle), 0) * effective_rope_length
    return pivot_2.pos + pivot_2_to_mass

pivot_1 = box(pos=vector(0,0.9,0), length=0.03, height=0.03, width=0.03, color=color.blue)
mass = sphere(pos=find_position_of_mass_about_pivot_1(initial_angle), radius=0.03, color=color.blue)
pivot_2 = sphere(pos=(pivot_1.pos-vector(0, distance_between_pivot_and_point, 0)), radius = 0.03, color=color.blue)
string_about_pivot_1 = box(pos = (pivot_1.pos + mass.pos)/2, width=0.005, height=0.005, axis=(mass.pos - pivot_1.pos))
string_about_pivot_2 = box(pos = (pivot_2.pos + mass.pos)/2, width=0.005, height=0.005, axis=vector(0,0,0))

angle_to_pivot_1 = initial_angle
angular_velocity_to_pivot_1 = initial_angular_velocity
angle_to_pivot_2 = -math.pi/2
angular_velocity_to_pivot_2 = 0

def convert_pivot_1_angular_velocity_to_pivot_2_angular_velocity():
    global angular_velocity_to_pivot_2
    angular_velocity_to_pivot_2 = ((starting_rope_length / (starting_rope_length - distance_between_pivot_and_point)) ** 2) * angular_velocity_to_pivot_1

def is_mass_pivoting_about_pivot_1() -> bool:
    return angle_to_pivot_1 > -math.pi/2

def get_effective_rope_length() -> float:
    if (is_mass_pivoting_about_pivot_1()):
        return starting_rope_length
    else:
        circumference_of_point = pivot_2.radius * 2 * math.pi
        rotations_around_point = abs((angle_to_pivot_2 + math.pi/2) / (2 * math.pi))
        return starting_rope_length - (circumference_of_point * rotations_around_point) - distance_between_pivot_and_point
    
def update_mass_angular_velocity() -> None:
    global angle_to_pivot_1
    global angular_velocity_to_pivot_1
    global angle_to_pivot_2
    global angular_velocity_to_pivot_2
    if (is_mass_pivoting_about_pivot_1()):
        alpha = -9.81 * cos(angle_to_pivot_1) / get_effective_rope_length()
        angular_velocity_to_pivot_1 += (alpha * dt)
    else:
        alpha = -9.81 * cos(angle_to_pivot_2) / get_effective_rope_length()
        angular_velocity_to_pivot_2 += (alpha * dt)
    
def update_mass_angle() -> None:
    global angle_to_pivot_1
    global angle_to_pivot_2
    if (is_mass_pivoting_about_pivot_1()):
        angle_to_pivot_1 += (angular_velocity_to_pivot_1 * dt)
        if (not is_mass_pivoting_about_pivot_1()):
            convert_pivot_1_angular_velocity_to_pivot_2_angular_velocity()
    else:
        angle_to_pivot_2 += (angular_velocity_to_pivot_2 * dt)

def update_mass_position() -> None:
    if (is_mass_pivoting_about_pivot_1()):
        mass.pos = find_position_of_mass_about_pivot_1(angle=angle_to_pivot_1)
    else:
        mass.pos = find_position_of_mass_about_pivot_2(angle=angle_to_pivot_2, effective_rope_length=get_effective_rope_length())

def update_string_about_pivot_1() -> None:
    if (is_mass_pivoting_about_pivot_1()):
        string_about_pivot_1.pos = (pivot_1.pos + mass.pos)/2
        string_about_pivot_1.axis = (mass.pos - pivot_1.pos)
    else:
        string_about_pivot_1.pos = (pivot_2.pos + pivot_1.pos)/2
        string_about_pivot_1.axis = (pivot_2.pos - pivot_1.pos)

def update_string_about_pivot_2() -> None:
    string_about_pivot_2.pos = (pivot_2.pos + mass.pos)/2
    if (is_mass_pivoting_about_pivot_1()):
        string_about_pivot_2.axis = vector(0,0,0)
    else:
        string_about_pivot_2.axis = (mass.pos - pivot_2.pos)

while True:
    rate(steps_per_second)
    if (get_effective_rope_length() > 0.05):
        update_mass_angular_velocity()
        update_mass_angle()
        update_mass_position()
        update_string_about_pivot_1()
        update_string_about_pivot_2()    