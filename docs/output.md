## Output format 


Each reaction path is saved with a folder named as Pathway_0001 and gaussian calculations files(input file, output files) are stored. 
further a scatter plot of the energy of converged structures as scatter.jpg and a xyz file is produced to see the trajectory. 

in the xzy file the reaction path is recorded as follows 

```
<Number of atoms>
Energy = <energy in Hartree> 
<element1> <x1> <y1> <z1>
<element2> <x2> <y2> <z2>
...<elementN> <xN> <yN> <zN>
<Number of atoms>
Energy = <energy in Hartree>
<element1> <x1> <y1> <z1>
<element2> <x2> <y2> <z2>
...<elementN> <xN> <yN> <zN>
...
```
this can be visualized using any molecular visualization program that supports xyz format.
(IQmol, VMD, etc)
---