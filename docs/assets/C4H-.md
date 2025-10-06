# Configuration file for C4H- cluster generation
# Comments start with a # symbol and are ignored by the parser
# Sections are defined in square brackets []
# Key-value pairs are defined with an equals sign (=)
# Use backslashes (\) to continue lines if necessary    


```ini
[project]
project_name = C4H-



[controls]
# set this as false for now
update_with_optimized_coordinates = True
step_size = 0.1
step_count = 30
stop_distance_factor = 0.8
dynamic_fragment_replacement = True
ADD_COM_CONST = True

sphere_radius = 3
# number of iterations needs to run with different orientations
n_iterations = 100

# Total_random or statistically_even or False
spherical_placement = statistically_even


[gaussian]
number_of_cores = 4
memory = 6GB

method =#N pm6 scf=(xqc) nosymm


[molecules]
charge = -1
multiplicity = 1
number_of_molecules = 5 

0 = C 0.000 0.000 0.0000

1 = C 0.000 0.000 0.000

2 = C 0.000 0.0000 0.0000

3 = C 0.0000 0.00 0.000

4 = H 0.000 0.000 0.000




[Additional]





```