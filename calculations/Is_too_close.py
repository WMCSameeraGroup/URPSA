
def is_too_close(origin_atoms,moving_atoms):
    for i in origin_atoms:
        for j in moving_atoms:
            if i.distance_between(j) < i.v_radius +j.v_radius:
                return False
    return True




