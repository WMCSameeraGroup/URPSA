def center_of_mass(atoms):
    """
    Calculate the center of mass for a list of atoms.
    1. Multiply each atom's mass by its coordinates to get the weighted position.
    2. Sum these weighted positions for all atoms.
    3. Divide the summed weighted positions by the total mass of all atoms to get the center of mass coordinates.
    4. Return the center of mass as a list of [x, y, z].
    :return: center of mass coordinates [x, y, z]
    :rtype: list
    :example: [1.234, 2.345, 3.456]
    :param atoms:
    """
    sum_of_gravity_vector_x_dir = 0
    sum_of_gravity_vector_y_dir = 0
    sum_of_gravity_vector_z_dir = 0
    sum_of_mass = 0

    for atom in atoms:
        sum_of_gravity_vector_x_dir += atom.mass * atom.x
        sum_of_gravity_vector_y_dir += atom.mass * atom.y
        sum_of_gravity_vector_z_dir += atom.mass * atom.z
        sum_of_mass += atom.mass

    return [sum_of_gravity_vector_x_dir / sum_of_mass,
            sum_of_gravity_vector_y_dir / sum_of_mass,
            sum_of_gravity_vector_z_dir / sum_of_mass
            ]
