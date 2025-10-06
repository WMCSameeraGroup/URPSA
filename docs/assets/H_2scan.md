# Lattice optimization of H2 in a fixed benzene lattice

```ini


[project]
project_name = lattice-non-opt


[controls]
step_size = 0.1
step_count = 40
stop_distance_factor = 0.9
update_with_optimized_coordinates = True
dynamic_fragment_replacement = True
sphere_radius = 2.0

# Total_random or statistically_even or False
spherical_placement = statistically_even


# add COM constraints = True
ADD_TRUE_COM = True


[gaussian]
method =#N PM6 scf(maxcyc=300,xqc)


[molecules]
charge = 0
multiplicity = 1
number_of_molecules = 2

0 = H 0.000 0.0000 0.00000000

# add \ to the end of a line if the next line continues
1 = H 0.00000 0.00000 0.00000000



lattice =  C                 1.31988500    0.91615000    0.00000000 fixed\
 H                   1.89112600    0.00761400    0.00000000 fixed\
 H                   1.88382200    1.82866300    0.00000000 fixed\
 C                    0.00000000    0.92731700    0.00000000 fixed\
 H                   -0.50664600    1.87544200    0.00000000 fixed\
 C                   -0.89261300   -0.25132100    0.00000000 fixed\
 H                   -1.94256100   -0.02059200    0.00000000 fixed\
 C                   -0.52415000   -1.51877900    0.00000000 fixed\
 H                   0.50520000   -1.82241000    0.00000000 fixed\
 H                   -1.24967100   -2.30892300    0.00000000 fixed


[Additional]

```


