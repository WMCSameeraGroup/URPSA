##Unbiased Reaction Path Search Algorithm (URPSA)
## How to install 

```bash 
git clone https://github.com/HesaraMahela/computationalChemistryProject15315.git
```
Use the command or download the file and extract the folder.

## How to Run 
To run the program you need to specify the path of the configuration file to the repeated.py python script.

the following command can be used to run the program
```bash
python3 repeated.py config.txt
```

## Input change
we have written a simple parser file for the organization of input parameters to the program.
The sections are *[SECTION]* defined with square brackets. 
predefined variables are placed on the left hand side and the values are defined by  

```buildoutcfg
[section]
variable = value
```
modify the config file to enter the inputs (*Molecules*, step_size, step_count, and etc )
```buildoutcfg
# This is a comment
[project]
#define project name this have to be change everytime to a non exisiting name 
project_name = stable code 4
input_file_name = Test

[controls]
# set this as false for now
update_with_optimized_coordinates = True
step_size = 0.2
step_count = 30
stop_distance_factor = 0.4

sphere_radius = 4
# number of iterations needs to run with different orientations
n_iterations = 10

# Total_random or statistically_even or False
spherical_placement = statistically_even


[gaussian]
number_of_cores = 10
memory = 2GB
#method = #N b3lyp/3-21g opt=AddGIC  nosymm
method =#N opt(maxcycle=1200,AddGIC) wb97xd/6-31g* scf(maxcyc=1200,xqc) nosymm
#method =#N opt(maxcycle=200,AddGIC) HF/3-21g* scf(maxcyc=200,xqc) nosymm
# use dft



[molecules]
charge = 0
multiplicity = 2
number_of_molecules = 2

0 = C -0.69272980 -0.81618654 0.00000000\
H -0.33605696 -0.31178835 0.87365150\
H -0.33605696 -0.31178835 -0.87365150\
H -1.76272980 -0.81617336 0.00000000\
O -0.21607949 -2.16440926 0.00000000\
H -0.53442410 -2.61684869 0.78457331

# add \ to the end of a line if the next line continues
1 = O -0.21607949 -2.16440926 0.00000000\
H -0.53442410 -2.61684869 0.7845733




```

## output data
project outputs are saved in the *Projects* directory 
