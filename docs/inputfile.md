
## Input file configuration
we have written a simple parser file for the organization of input parameters to the program.
The sections are **[SECTION]** defined with square brackets. 
predefined variables are placed on the left hand side and the values are defined by  

```buildoutcfg
[section]
variable = value
```
modify the input file to enter the inputs (*Molecules*, step_size, step_count, and etc )

- **update_with_optimized_coordinates**: keep the optimized configuration of molecules to the next method.
- **step size:** distance moved towards the center 
- **step_count:** number of steps should move towards the center
- **stop_distance_factor:** the factor that determines distance that the calculation should stop ; factor x (sum of covalent radius)
- **stress_release:** iterations that should be optimized without constraints. input is given as  start: step :end
- **spherical_placement:** how to place the molecular fragments on the hypothetical spherical.
- **ADD_COM_CONST:** whether to add center of mass constraints
- **dynamic_fragment_replacement:** if atoms are closer than given number value.


```buildoutcfg
# This is a comment
[project]
project_name = Project1

[controls]
# set this as false for now
update_with_optimized_coordinates = True
# in angstrum 
step_size = 0.1
step_count = 40
stop_distance_factor = 0.4


# add COM constraints = True
ADD_COM_CONST = False
dynamic_fragment_replacement = True

[gaussian]
number_of_cores = 8
memory = 8GB
method =#N opt(maxcycle=600,AddGIC) PM6 scf(maxcyc=600,xqc) nosymm



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

[Additional]
# use /- instead of = sign when using inside values

constraints = XCm1 (Inactive) /- XCntr(1-6) \
YCm1 (Inactive) /- YCntr(1-6) \
ZCm1 (Inactive) /- ZCntr(1-6)\
XCm2 (Inactive)  /- XCntr(7)\
YCm2 (Inactive)  /- YCntr(7) \
ZCm2 (Inactive) /- ZCntr(7)\
F1F2(FREEZE) /- sqrt[(XCm1-XCm2)^2+(YCm1-YCm2)^2+(ZCm1-ZCm2)^2]*0.529177

```
---

## Output data
Project outputs are saved in a directory inside the pwd with the project name that you specified in the input file.
Successfully observed reaction paths would be saved as **Pathways_xxxx** directories.
And inside those folders all the files related to the calculation would be saved.
Summary of a path is recorded by **output2.xyz** file.

If a pathway was unsuccessful that pathway is either removed or moved to the Archived folder depending on the input option that is given.
By default, it is Archived.

---
## Default values 
the default values are stored as a dictionary 

```python
defaults = {
    "project": {
        "project_name": "new-project",
    },
    "controls": {
        "update_with_optimized_coordinates": "True",
        "step_size": 0.1,
        "step_count": 40,
        "stop_distance_factor": 0.8,
        "stress_release": "0:1:-1",
        "sphere_radius": 3,
        "n_iterations": 10,
        "spherical_placement": "statistically_even",
        "ADD_COM_CONST": "True",
        "ADD_SPHERICAL_CONST": "False",
        "dynamic_fragment_replacement": "False",
        "cutoff_energy_gap":120.0,
        "energy_surpass_options":"exit",
        "optimize_the_final_particle":"True",
        "convergence_error":"exit",
        "consecutive_duplicates_threshold":5,
        "unsuccessful_pathway":"archive"


    },
    "gaussian": {
        "number_of_cores": 1,
        "memory": "1GB",
        "method": "#N opt(maxcycle=200,AddGIC) WB97XD/6-31G* scf(maxcyc=300,xqc) nosymm"
    }
}

```