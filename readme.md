## How to Run 
```
python3 repeated.py config.txt
```

## Input change
modify the config file to enter the inputs 
```buildoutcfg
# This is a comment
[project]
project_name = test4
input_file_name = Test

[controls]
# set this as false for now
update_with_optimized_coordinates = True
step_size = 0.05
step_count = 75
stop_distance_factor = 0.4

sphere_radius = 5
# number of iterations needs to run with different orientations
n_iterations = 1

# Total_random or statistically_even or False
spherical_placement = statistically_even


[gaussian]
number_of_cores = 2
memory = 2GB
method = opt(maxcycle=1200) B3LYP/6-31++g



[molecules]
charge = 0
multiplicity = 2
number_of_molecules = 2

# add the number from 0 to n-1 and put equal sign to declair the moolecule 
0 = C -0.69272980 -0.81618654 0.00000000 fixed\
H -0.33605696 -0.31178835 0.87365150\
H -0.33605696 -0.31178835 -0.87365150\
H -1.76272980 -0.81617336 0.00000000\
O -0.21607949 -2.16440926 0.00000000\
H -0.53442410 -2.61684869 0.78457331

# add \ to the end of a line if the next line continues
# add fixed at the end of an atom to optimize while 
1 = O -0.21607949 -2.16440926 0.00000000 fixed\
H -0.53442410 -2.61684869 0.7845733

```

## output data
project outputs are saved in the *Projects* directory 
