# Example Input File: HNO2

This example shows the structure of an input file for the HNO2 project. Sections, comments, and parameters are included for clarity.

## Sample Input

```ini
[project]
project_name = HNO2

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
method =#N B3LYP/3-21G scf=(xqc,maxcon=128,maxcyc=512,conver=8) nosymm

[molecules]
charge = 0
multiplicity = 1
number_of_molecules = 4

0 = H 0.000 0.000 0.0000
1 = N 0.000 0.000 0.000
2 = O 0.000 0.0000 0.0000
3 = O 0.0000 0.00 0.000

[Additional]

```







