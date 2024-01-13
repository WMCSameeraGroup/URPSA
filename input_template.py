def get_input_template(number):
    # gonna replace title value
     return """
%Chk=heavy
# HF/6-31G(d) Opt=ModRedun	
 
Opt job	Title{0}
 
0   1	\n""".format(number)


