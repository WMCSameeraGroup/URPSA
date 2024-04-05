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


0 2
```

## How to run the program 
```bash
python3 grogu.py inputfile.txt
```






