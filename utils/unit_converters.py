
def hatree2kjmol(val: float) -> float:
    """Convert Hartree to kJ/mol.
     :param val: Value in Hartree.
     :return: Value in kJ/mol.
     """
    return 2625.5 * val

def hatree2kcalMol(val: float) -> float:
    """Convert Hartree to kcal/mol.
    :param val: Value in Hartree.
    """
    return 627.5 * val