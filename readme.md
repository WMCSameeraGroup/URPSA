## How to Run 
```
python3 repeated.py config.txt
```

## Input change
modify the config file to enter the inputs 
```buildoutcfg
# This is a comment
[project]
project_name = Benzene_HCl_1
input_file_name = Test

[controls]
update_with_optimized_coordinates = False
step_size = 0.1
step_count = 100
stop_distance_factor = 0.5

sphere_radius = 6
# number of iterations needs to run with different orientations
n_iterations = 3

# Total_random or statistically_even or False
spherical_placement = statistically_even


[gaussian]
number_of_cores = 2
method = opt(maxcycle=300) HF/3-21g



[molecules]
charge = 0
multiplicity = 1
number_of_molecules = 2
# number the molecules from 0 to n-1 
0 = C                 -2.46415780    0.75268816    0.00000000\
 C                 -1.06899780    0.75268816    0.00000000\
 C                 -0.37145980    1.96043916    0.00000000\
 C                 -1.06911380    3.16894816   -0.00119900\
 C                 -2.46393880    3.16887016   -0.00167800\
 C                 -3.16153980    1.96066416   -0.00068200\
 H                 -3.01391680   -0.19962884    0.00045000\
 H                 -0.51948980   -0.19982484    0.00131500\
 H                  0.72822020    1.96051916    0.00063400\
 H                 -0.51891380    4.12109116   -0.00125800\
 H                 -3.01406080    4.12115116   -0.00263100\
 H                 -4.26114380    1.96084716   -0.00086200


# add \ to the end of a line if the next line continues
1 = Cl                 4.18458797   -4.30107520   -0.00056443\
 H                  2.89458797   -4.30107520   -0.00056443

```

## output data
project outputs are saved in the *Projects* directory 