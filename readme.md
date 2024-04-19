## Hi this is grogu program 
You can use me to get the energies of molecular pairs in a specific reaction coordinate by moving one molecule to a molecule where another stationary molecule stays at the origin. 
## prerequisites 

 * gaussian 16
 * Python 3.10 above

# input file format 
At the beginning you can include **symbol x y z** one line for one atom then after first molecule is written two empty lines has to be written to say molecule is completely written.
Then step size and step count is to be expressed eg: **1 10** \
Then another 2 lines to indicate new section and stationary molecules **symbol x y z ** coordinates are written. then another two empty lines to indicate the end of the stationary molecule and charge and multiplicity is written finally.

## Example input file for two H<sub>2</sub>O molecules
```
O -0.78947368 -2.06766914 0.00000000
H 0.17052632 -2.06766914 0.00000000
H -1.10992827 -1.16273331 0.00000000


1.0 10.0


O 4.28571428 0.63909773 0.00000000
H 5.24571428 0.63909773 0.00000000
H 3.96525969 1.54403357 0.00000000


0 3


3 step 10 0 1
```
the last line indicates run the calculations for three times changing rotation in (xy,xz,yz)
or random orentations can be taken by using random word instead of step
```
3 random
```
## How to run the program 
Create an input file as described above then give the path to the input file
Note: stay in the same directory as grogu.py

```bash
python3 grogu.py inputfile.txt
```


## change configuration using settings.py file
the parameters can be changed as you fit
```python
input_file_directory = 'inputFiles'
output_file_directory = 'inputFiles'
input_file_name = 'Test'
data_file_name = "data.txt"
backend = "g16"

# distance in angstroms gravity point of the molecules are decreased  
step_size = 0.5 
# number of steps 
step_count = 21

stop_distance_factor = 0.4 # factor that multiplies sum of vandervals radius

```
# where to find the output files (com, log, chk)
default all the files of the current calculations are stored in **inputFile** directory and previous calculations are moved to **archives** folder


### how to use with more than two molecules 

well, change 1 molecule at a time while keeping others as stationary.

## points to improve 
# use gauss view to generate molecules in order to achieve a better result

#! if the distance is smaller  than the specified then other steps of that iterations are skiped.