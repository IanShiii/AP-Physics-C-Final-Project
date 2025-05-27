import math
from turtle import pos
from vpython import *

dt = 0.003
steps_per_second = 100

scene = canvas(width=600, height=600)

starting_rope_length = 1.5
initial_angle = 0
initial_angular_velocity = 0
distance_between_pivot_and_point = 1.0

radius_of_pivot_2 = 0.03
radius_of_mass = 0.03

def find_position_of_mass_about_pivot_1(angle: float) -> vector:
    pivot_1_to_mass = vector(cos(angle), sin(angle), 0) * starting_rope_length
    return pivot_1.pos + pivot_1_to_mass

def find_position_of_mass_about_pivot_2(angle: float, effective_rope_length: float) -> vector:
    pivot_2_to_mass = vector(cos(angle), sin(angle), 0) * effective_rope_length
    return pivot_2.pos + pivot_2_to_mass

pivot_1 = box(pos=vector(0,0.9,0), length=0.03, height=0.03, width=0.03, color=color.blue)
mass = sphere(pos=find_position_of_mass_about_pivot_1(initial_angle), radius=radius_of_mass, color=color.blue)
pivot_2 = sphere(pos=(pivot_1.pos-vector(0, distance_between_pivot_and_point, 0)), radius = radius_of_pivot_2, color=color.blue)
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

def get_minimum_magnitude_angular_velocity_required_to_keep_string_taut_top_half() -> float:
    global angle_to_pivot_1
    global angle_to_pivot_2
    if (is_mass_pivoting_about_pivot_1()):
        magnitude_perpendicular_accel_from_gravity = abs(9.81 * sin(angle_to_pivot_1))
        minimum_linear_velocity = sqrt(magnitude_perpendicular_accel_from_gravity * starting_rope_length)
        minimum_angular_velocity = minimum_linear_velocity / starting_rope_length
        return minimum_angular_velocity
    else:
        magnitude_perpendicular_accel_from_gravity = abs(9.81 * sin(angle_to_pivot_2))
        minimum_linear_velocity = sqrt(magnitude_perpendicular_accel_from_gravity * get_effective_rope_length())
        minimum_angular_velocity = minimum_linear_velocity / get_effective_rope_length()
        return minimum_angular_velocity

def is_rope_taut() -> bool:
    if (is_mass_pivoting_about_pivot_1()):
        if (sin(angle_to_pivot_1) <=0):
            return True
        else:
            return abs(angular_velocity_to_pivot_1) >= get_minimum_magnitude_angular_velocity_required_to_keep_string_taut_top_half()
    else:
        if (sin(angle_to_pivot_2) <=0):
            return True
        else:
            return abs(angular_velocity_to_pivot_2) >= get_minimum_magnitude_angular_velocity_required_to_keep_string_taut_top_half()

def hide_strings() -> None:
    string_about_pivot_1.axis = vector(0,0,0)
    string_about_pivot_2.axis = vector(0,0,0)

mass_linear_velocity = vector(0,0,0)

def convert_mass_angular_velocity_to_linear_velocity() -> None:
    global mass_linear_velocity
    if (is_mass_pivoting_about_pivot_1()):
        ccw_velocity_magnitude = angular_velocity_to_pivot_1 * starting_rope_length
        mass_linear_velocity = vector(ccw_velocity_magnitude * -sin(angle_to_pivot_1), ccw_velocity_magnitude * cos(angle_to_pivot_1), 0)
    else:
        ccw_velocity_magnitude = angular_velocity_to_pivot_2 * get_effective_rope_length()
        mass_linear_velocity = vector(ccw_velocity_magnitude * -sin(angle_to_pivot_2), ccw_velocity_magnitude * cos(angle_to_pivot_2), 0)

def update_mass_velocity_free_fall() -> None:
    mass_linear_velocity.y -= (9.81 * dt)

def update_mass_position_free_fall() -> None:
    mass.pos += (mass_linear_velocity * dt)

rope_has_become_slack = False
last_effective_rope_length_before_going_slack = 0
mass_was_last_pivoting_around_pivot_1 = True

def has_mass_reached_end_of_string() -> bool:
    if (mass_was_last_pivoting_around_pivot_1):
        distance_to_pivot_1 = (mass.pos - pivot_1.pos).mag
        return distance_to_pivot_1 > last_effective_rope_length_before_going_slack * 1
    else:
        distance_to_pivot_2 = (mass.pos - pivot_2.pos).mag
        return distance_to_pivot_2 > last_effective_rope_length_before_going_slack * 1
    
def is_mass_touching_pivot_2() -> bool:
    return (mass.pos - pivot_2.pos).mag <= (radius_of_mass + radius_of_pivot_2)

simulation_ended = False

while True:
    rate(steps_per_second)
    if (not simulation_ended):   
        if (is_mass_touching_pivot_2()):
            simulation_ended = True
        if (not rope_has_become_slack):
            update_mass_angular_velocity()
            update_mass_angle()
            update_mass_position()
            update_string_about_pivot_1()
            update_string_about_pivot_2()
            if (not is_rope_taut()):
                rope_has_become_slack = True
                last_effective_rope_length_before_going_slack = get_effective_rope_length()
                if (not is_mass_pivoting_about_pivot_1()):
                    mass_was_last_pivoting_around_pivot_1 = False
                hide_strings()
                convert_mass_angular_velocity_to_linear_velocity()
        else:
            update_mass_velocity_free_fall()
            update_mass_position_free_fall()
            if (has_mass_reached_end_of_string()):
                simulation_ended = True
