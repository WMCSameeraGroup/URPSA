def get_input_template(number):
    # gonna replace title value
     return """%nprocshared=1
%mem=500MB
%chk=test{0}.chk
# wb97xd/aug-cc-pvtz 

Title{0}
 
0   1	\n""".format(number)


if __name__ =="__main__":
    print(get_input_template(1))