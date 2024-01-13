
def generate_coordinates(atom='H', initial_cords_atom1=[10,0,0], initial_cords_atom2=[0,0,0], step_size=1, num_of_steps=10):
    """ returns the list of coordinates in string format"""
    list_of_coordinates = []
    for i in range(num_of_steps):
        new_coordinates = [initial_cords_atom1[0] - i * step_size, *initial_cords_atom1[1:]]
        coordinates = print_coordinates(atom, new_coordinates, initial_cords_atom2)
        list_of_coordinates.append(coordinates)
    return list_of_coordinates



def print_coordinates(atom, cords_atom1, cords_atom2):
    x1 = cords_atom1[0]
    y1 = cords_atom1[1]
    z1 = cords_atom1[2]
    x2 = cords_atom2[0]
    y2 = cords_atom2[1]
    z2 = cords_atom2[2]
    str = f"{atom} {x1} {y1} {z1} \n{atom} {x2} {y2} {z2} "

    return str

#print(generate_coordinates())