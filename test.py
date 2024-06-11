import configparser

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the file
# with open('exmInp.cfg', 'r') as file:
# Manually process the molecules section
# molecules_section = False
# molecules_data = []
# for line in file:
#     line = line.strip()
#     if line.startswith("[molecules]"):
#         molecules_section = True
#     elif molecules_section:
#         if line.startswith("[") and line.endswith("]"):
#             molecules_section = False
#         else:
#             molecules_data.append(line)
#     if not molecules_section:
#         config.read_string(line + "\n")

# Add the molecules data to the config object
# if molecules_data:
#     config.add_section("molecules")
#     config.set("molecules", "data", "\n".join(molecules_data))

# Accessing values from standard sections

config.read('exmInp.cfg')
number_of_cores = config.getint('gaussian', 'number_of_cores')
method_and_keywords = config.get('gaussian', 'method_and_keywords')
project_name = config.get('project', 'project_name')

# Accessing the molecules data
# molecules = config.get('molecules', 'data').split('\n')
#
# # Display the parsed values
# print("Number of cores:", number_of_cores)
# print("Method and keywords:", method_and_keywords)
# print("Project name:", project_name)
# print("Molecules:")
# for molecule in molecules:
#     print(molecule)
"""

[molecules]
O -9.39415821 15.41711766 3.76007085
H -8.43415821 15.41711766 3.76007085
H -9.71461280 16.32205349 3.76007085
;
C -1.07142857 1.31567670 -0.01722315
O 0.18697143 1.31567670 -0.01722315
O -2.32982857 1.31567670 -0.01722315
"""