def get_input_template(number, system):
    # gonna replace title value
     return """%nprocshared=1
%mem=500MB
%chk=test{0}.chk
# wb97xd/aug-cc-pvtz 

Title{0}
 
{1}   {2}	\n""".format(number,system.charge,system.multiplicity)


if __name__ =="__main__":
    print(get_input_template(1))