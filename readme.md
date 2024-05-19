## silicon.py 
This program  can converge N number of atoms randomly placed on a sphere of radius R and converged to center step by step and SCF energies are calculated and plotted.

### input file format

```
<symbol of the atom> <number of atoms>  # multiple lines can be used 
<symbol of the atom> <number of atoms>
                                        # 2 line 

<step size> <step count>

                                        # 2 line
---------- # line without spaces 

                                        # 2 line  
<charge> <multiplicity>

                                        # 2 lines
radius <radius of the sphere>                                   
```

### example 1

```bash
python3 silicon.py silicon.txt
```
This example file has 3 silicon atoms on a sphere of radius 12 ten steps with a step size of 1.

```
Si 3 


1.0 10.0


--------


0 1


radius 12
```

## example 2
```bash
python3 silicon.py carbonSilicon.txt
```

```
Si 2
C 2


1.0 5.0


--------


0 1


radius 12
```



## Hi this is grogu program 
You can use me to get the energies of molecular pairs in a specific reaction coordinate by moving one molecule to a molecule where another stationary molecule stays at the origin. 
## prerequisites 

 * gaussian 16
 * Python 3.10 above
#How to get started
clone the repository or download the files as a zip and extract them.\
enter this line on cli
```bash
git clone https://github.com/HesaraMahela/computationalChemistryProject15315.git
```
and now its possible to write your own input file or run an example file already written
so H2.txt is a simple two hydrogen atom based model which requires less calculation time.
```bash
python3 grogu.py H2.txt
```
After calculations are complete, 
plot of energies are saved in same directory named **output.jpg**\
and all the relevant files are saved in **inputFiles/** directory (or **archives/** )
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
"""
general values and configurations are written here
"""

input_file_directory = 'inputFiles'
output_file_directory = 'inputFiles'
input_file_name = 'Test'
data_file_name = "data.txt"
backend = "g16"

method = "wb97xd/aug-cc-pvtz"

""" ** these values are overwritten by input file ** """
# distance in angstroms gravity point of the molecules are decreased  
step_size = 0.5 
# number of steps 
step_count = 21
""" ** ** """
stop_distance_factor = 0.4 # factor that multiplies sum of vandervals radius

```
# where to find the output files (com, log, chk)
default all the files of the current calculations are stored in **inputFile** directory and previous calculations are moved to **archives** folder


### how to use with more than two molecules 

well, change 1 molecule at a time while keeping others as stationary.

## points of improvement

* use gauss view to generate molecules in order to achieve a better result

* if the distance is smaller  than the specified then other steps of that iterations are skiped.

* only data for first 30 atoms are provided. if you are to use other molecules you have to update **atoms/constants**


### Examples 
There are 4 example input files 
```bash
H2.txt
```
Two hydrogen molecules are analyzed without changing orientation

```bash
test.txt
```
Two water molecules are analysed using the program 3 incremental orientations and 1 x 10

```bash
example1.txt
```
Two water molecules are analysed using the program in 3 random orientations 6 random orientations 0.5 times 5 distance 
```bash
example2.txt
```
One water molecule and carbon dioxide molecule are analysed using the program 6 random orientations 5 times 0.5 distance 
