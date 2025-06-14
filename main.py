from vpython import *
#Web VPython 3.2

dt = 0.005
time = 0
steps_per_second = 100

scene = canvas(width=1000, height=400)
scene.userzoom = False
scene.userspin = False
scene.userpan = False
scene.autoscale = False
scene.camera.pos = vector(0,0,-12) 
# scene.camera.pos = vector(0,0,3) 

simulation_started = False
simulation_ended = False

starting_rope_length = 1.5
distance_between_pivot_and_point = 1.0

angle_to_pivot_1 = 0
angular_velocity_to_pivot_1 = 0
angle_to_pivot_2 = 0
angular_velocity_to_pivot_2 = 0

radius_of_pivot_2 = 0.05
radius_of_mass = 0.05

def set_radius_of_pivot_2(evt):
    global radius_of_pivot_2
    if (not simulation_started):
        radius_of_pivot_2 = evt.value

def set_starting_rope_length(evt):
    global starting_rope_length
    if (not simulation_started):
        starting_rope_length = evt.value

def set_distance_between_pivot_and_point(evt):
    global distance_between_pivot_and_point
    if (not simulation_started):
        distance_between_pivot_and_point = evt.value

def set_initial_angle(evt):
    global angle_to_pivot_1
    if (not simulation_started):
        angle_to_pivot_1 = evt.value

def set_initial_angular_velocity(evt):
    global angular_velocity_to_pivot_1
    if (not simulation_started):
        angular_velocity_to_pivot_1 = -evt.value

spacing = wtext(text='\n')

starting_rope_length_slider = slider(bind=set_starting_rope_length, max=2, min=0.5, step=0.05, value=1.5)
starting_rope_length_slider_text = wtext(text='Rope Length: ' + str(starting_rope_length_slider.value) + '\n')

distance_between_pivot_and_point_slider = slider(bind=set_distance_between_pivot_and_point, max=2.0, min=0.5, step=0.05, value=1)
distance_between_pivot_and_point_slider_text = wtext(text='Distance Between Two Pivots: ' + str(distance_between_pivot_and_point_slider.value) + '\n')

radius_of_second_pivot_slider = slider(bind=set_radius_of_pivot_2, max=0.15, min=0.05, step=0.01, value=radius_of_pivot_2)
radius_of_second_pivot_slider_text = wtext(text='Radius of Second Pivot\n')

initial_angle_slider = slider(bind=set_initial_angle, max=0, min=-pi/4, step=0.05, value=0)
initial_angle_slider_text = wtext(text='Initial Angle\n')

initial_angular_velocity_slider = slider(bind=set_initial_angular_velocity, max=3, min=0, step=0.01, value=0)
initial_angular_velocity_slider_text = wtext(text='Initial Angular Velocity\n\n')

def update_text():
    starting_rope_length_slider_text.text = 'Rope Length: ' + str(starting_rope_length_slider.value) + '\n'
    distance_between_pivot_and_point_slider_text.text = 'Distance Between Two Pivots: ' + str(distance_between_pivot_and_point_slider.value) + '\n'

def find_position_of_mass_about_pivot_1():
    pivot_1_to_mass = vector(cos(angle_to_pivot_1), sin(angle_to_pivot_1), 0) * starting_rope_length
    return pivot_1.pos + pivot_1_to_mass

def find_position_of_mass_about_pivot_2(effective_rope_length: float):
    pivot_2_to_mass = vector(cos(angle_to_pivot_2), sin(angle_to_pivot_2), 0) * effective_rope_length
    return pivot_2.pos + pivot_2_to_mass

pivot_1 = box(pos=vector(0,0.9,0), length=0.1, height=0.1, width=0.1, texture=textures.metal)
mass = sphere(pos=find_position_of_mass_about_pivot_1(), radius=radius_of_mass, texture=textures.wood)
pivot_2 = sphere(pos=(pivot_1.pos-vector(0, distance_between_pivot_and_point, 0)), radius = radius_of_pivot_2, texture=textures.metal)
string_about_pivot_1 = box(pos = (pivot_1.pos + mass.pos)/2, width=0.005, height=0.005, axis=(mass.pos - pivot_1.pos), texture=textures.rough)
string_about_pivot_2 = box(pos = (pivot_2.pos + mass.pos)/2, width=0.005, height=0.005, axis=vector(0,0,0), texture=textures.rough)

def convert_pivot_1_angle_to_pivot_2():
    global angle_to_pivot_2
    angle_to_pivot_2 = atan((mass.pos.y - pivot_2.pos.y) / (mass.pos.x - pivot_2.pos.x))

def convert_pivot_1_angular_velocity_to_pivot_2_angular_velocity():
    global angular_velocity_to_pivot_2
    angular_velocity_to_pivot_2 = angular_velocity_to_pivot_1 * starting_rope_length / (starting_rope_length - distance_between_pivot_and_point)

def is_mass_pivoting_about_pivot_1():
    return angle_to_pivot_1 > (-pi/2 + atan(radius_of_pivot_2 / distance_between_pivot_and_point))

def get_effective_rope_length():
    if (is_mass_pivoting_about_pivot_1()):
        return starting_rope_length
    else:
        circumference_of_point = pivot_2.radius * 2 * pi
        rotations_around_point = abs((angle_to_pivot_2 + pi/2) / (2 * pi))
        return starting_rope_length - (circumference_of_point * rotations_around_point) - distance_between_pivot_and_point
    
def update_mass_angular_velocity():
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
    
def update_mass_angle():
    global angle_to_pivot_1
    global angle_to_pivot_2
    global angular_velocity_to_pivot_2
    if (is_mass_pivoting_about_pivot_1()):
        angle_to_pivot_1 += (angular_velocity_to_pivot_1 * dt)
        if (not is_mass_pivoting_about_pivot_1()):
            convert_pivot_1_angle_to_pivot_2()
            convert_pivot_1_angular_velocity_to_pivot_2_angular_velocity()
    else:
        initial_radius = get_effective_rope_length()
        initial_linear_velocity = angular_velocity_to_pivot_2 * initial_radius

        angle_to_pivot_2 += (angular_velocity_to_pivot_2 * dt)

        new_radius = get_effective_rope_length()
        new_linear_velocity = initial_radius * initial_linear_velocity / new_radius
        angular_velocity_to_pivot_2 = (new_linear_velocity + initial_linear_velocity) / 2 / new_radius
        

def update_mass_position():
    if (is_mass_pivoting_about_pivot_1()):
        mass.pos = find_position_of_mass_about_pivot_1()
    else:
        mass.pos = find_position_of_mass_about_pivot_2(effective_rope_length=get_effective_rope_length())

def update_string_about_pivot_1():
    if (is_mass_pivoting_about_pivot_1()):
        string_about_pivot_1.pos = (pivot_1.pos + mass.pos)/2
        string_about_pivot_1.axis = (mass.pos - pivot_1.pos)
    else:
        rope_angle_from_horizontal = -pi/2 + atan(radius_of_pivot_2 / distance_between_pivot_and_point)
        length_of_pivot_1_string = sqrt(distance_between_pivot_and_point ** 2 + pivot_2.radius ** 2)
        target_point_on_second_pivot = pivot_1.pos + vector(cos(rope_angle_from_horizontal), sin(rope_angle_from_horizontal), 0) * length_of_pivot_1_string
        string_about_pivot_1.pos = (pivot_1.pos + target_point_on_second_pivot)/2
        string_about_pivot_1.axis = (target_point_on_second_pivot - pivot_1.pos)

def update_string_about_pivot_2():
    target_angle_from_pivot_2 = angle_to_pivot_2 + acos(pivot_2.radius / (pivot_2.pos - mass.pos).mag)
    start_pos = pivot_2.pos + vector(cos(target_angle_from_pivot_2), sin(target_angle_from_pivot_2), 0) * radius_of_pivot_2
    string_about_pivot_2.pos = (start_pos + mass.pos)/2
    if (is_mass_pivoting_about_pivot_1()):
        string_about_pivot_2.axis = vector(0,0,0)
    else:
        string_about_pivot_2.axis = (mass.pos - start_pos)

def update_pivot_2():
    pivot_2.pos = pivot_1.pos-vector(0, distance_between_pivot_and_point, 0)
    pivot_2.radius = radius_of_pivot_2

def get_minimum_magnitude_angular_velocity_required_to_keep_string_taut_top_half():
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

def is_rope_taut():
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

def hide_strings():
    string_about_pivot_1.axis = vector(0,0,0)
    string_about_pivot_2.axis = vector(0,0,0)

mass_linear_velocity = vector(0,0,0)

def convert_mass_angular_velocity_to_linear_velocity():
    global mass_linear_velocity
    if (is_mass_pivoting_about_pivot_1()):
        ccw_velocity_magnitude = angular_velocity_to_pivot_1 * starting_rope_length
        mass_linear_velocity = vector(ccw_velocity_magnitude * -sin(angle_to_pivot_1), ccw_velocity_magnitude * cos(angle_to_pivot_1), 0)
    else:
        ccw_velocity_magnitude = angular_velocity_to_pivot_2 * get_effective_rope_length()
        mass_linear_velocity = vector(ccw_velocity_magnitude * -sin(angle_to_pivot_2), ccw_velocity_magnitude * cos(angle_to_pivot_2), 0)

def update_mass_velocity_free_fall():
    mass_linear_velocity.y -= (9.81 * dt)

def update_mass_position_free_fall():
    mass.pos += (mass_linear_velocity * dt)

rope_has_become_slack = False
last_effective_rope_length_before_going_slack = 0
mass_was_last_pivoting_around_pivot_1 = True

def has_mass_reached_end_of_string():
    if (mass_was_last_pivoting_around_pivot_1):
        distance_to_pivot_1 = (mass.pos - pivot_1.pos).mag
        return distance_to_pivot_1 > last_effective_rope_length_before_going_slack * 1
    else:
        distance_to_pivot_2 = (mass.pos - pivot_2.pos).mag
        return distance_to_pivot_2 > last_effective_rope_length_before_going_slack * 1
    
def is_mass_touching_pivot_2():
    return (mass.pos - pivot_2.pos).mag <= (radius_of_mass + radius_of_pivot_2)

rope_is_too_short_error = wtext(text='\n')

def attempt_start_simulation(evt):
    global simulation_started
    if (starting_rope_length <= distance_between_pivot_and_point):
        rope_is_too_short_error.text = 'ROPE IS TOO SHORT (Must be longer than the distance between the two pivots)\n'
    else:
        simulation_started = True
        rope_is_too_short_error.text = '\n'

start_button = button(bind=attempt_start_simulation, text='Start Simulation')

pivot_1_angular_velocity_graph = graph(title='Angular Velocity (about the top pivot)', xtitle='time', ytitle='Angular Velocity', xmin=0)
pivot_1_angular_velocity_curve = gcurve(graph=pivot_1_angular_velocity_graph, color=color.red, label='Angular Velocity')

pivot_2_angular_velocity_graph = graph(title='Angular Velocity (about the bottom pivot)', xtitle='time', ytitle='Angular Velocity', xmin=0)
pivot_2_angular_velocity_curve = gcurve(graph=pivot_2_angular_velocity_graph, color=color.red, label='Angular Velocity')

def reset(evt):
    global simulation_started, simulation_ended
    global time
    global angle_to_pivot_1, angular_velocity_to_pivot_1, angle_to_pivot_2, angular_velocity_to_pivot_2
    global mass_linear_velocity
    global rope_has_become_slack, last_effective_rope_length_before_going_slack
    global mass_was_last_pivoting_around_pivot_1
    global rope_is_too_short_error
    global radius_of_pivot_2
    global angular_velocity_curve

    simulation_started = False
    simulation_ended = False

    time = 0

    angle_to_pivot_1 = initial_angle_slider.value
    angular_velocity_to_pivot_1 = -initial_angular_velocity_slider.value
    angle_to_pivot_2 = 0
    angular_velocity_to_pivot_2 = 0

    radius_of_pivot_2 = radius_of_second_pivot_slider.value

    mass_linear_velocity = vector(0,0,0)

    rope_has_become_slack = False
    last_effective_rope_length_before_going_slack = 0
    mass_was_last_pivoting_around_pivot_1 = True

    rope_is_too_short_error.text = '\n'

    pivot_1_angular_velocity_graph.delete()
    pivot_2_angular_velocity_graph.delete()

reset_button = button(bind=reset, text='Reset Simulation')

def disable_enable_sliders():
    if (simulation_started):
        starting_rope_length_slider.disabled = True
        distance_between_pivot_and_point_slider.disabled = True
        radius_of_second_pivot_slider.disabled = True
        initial_angle_slider.disabled = True
        initial_angular_velocity_slider.disabled = True
    else:
        starting_rope_length_slider.disabled = False
        distance_between_pivot_and_point_slider.disabled = False
        radius_of_second_pivot_slider.disabled = False
        initial_angle_slider.disabled = False
        initial_angular_velocity_slider.disabled = False
        

while True:
    rate(steps_per_second)
    update_text()
    if (simulation_started and not simulation_ended):
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
            elif (is_mass_touching_pivot_2()):
                simulation_ended = True

            time += dt
            if (is_mass_pivoting_about_pivot_1()):
                pivot_1_angular_velocity_curve.plot(time, angular_velocity_to_pivot_1)
            else:
                pivot_2_angular_velocity_curve.plot(time, angular_velocity_to_pivot_2)
        else:
            update_mass_velocity_free_fall()
            update_mass_position_free_fall()
            if (has_mass_reached_end_of_string()):
                simulation_ended = True
    elif (not simulation_started and not simulation_ended):
        update_string_about_pivot_1()
        update_string_about_pivot_2()
        update_mass_position()
        update_pivot_2()
