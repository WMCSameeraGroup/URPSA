import json

class productsManager:
    def __init__(self, dir, name="products.json"):
        self.file = dir+name
        self.indent=4

    def read(self):
        with open(self.file, "r") as file:
            data = json.load(file)
        return data


    def create_if_not(self):
        try:
            with open(self.file, "a") as _:
                pass
        except:
            with open(self.file, "w") as _:
                pass

    def write_product(self, iter, molecules,energy=0):
        """ write the products to products.txt file"""
        #todo: pass energy
        if molecules == [] or molecules is None:
            print("No molecules are found")
            return
        self.create_if_not()
        new_data = self.create_json_string(molecules,energy)
        try:
            data = self.read()
            data[int(iter)] = new_data
        except:
            data ={int(iter):new_data}


        with open(self.file,"w") as file:
            file.write(json.dumps(data, indent=self.indent))


    def create_json_string(self, molecules,energy):
        """ create a json string from the molecules list
        where each molecule is represented by its RMSD and xyz coordinates
        1. number of molecules
        2. energy of the system
        3. list of molecules with their RMSD and xyz coordinates
        4. return the json string
        5. example:
        {
            "num_of_molecules": 2,
            "energy": -150.0,
            "molecules": [
                {"RMSD": 0.5, "molecule": "3\n\nC 0.0 0.0 0.0\nH 0.0 0.0 1.0\nH 1.0 0.0 0.0\n"},
                {"RMSD": 0.7, "molecule": "2\n\nO 0.0 0.0 0.0\nH 0.0 0.0 1.0\n"}
            ]
        }
        :return: dict to be converted to json string
        :rtype: dict
        """


        molecule_list =[]
        for molecule in molecules:
            molecule_list.append({f"RMSD":molecule.calculate_RMSD(), "molecule":molecule.to_str()})
        dict = { "num_of_molecules": len(molecules),"energy":energy , "molecules": molecule_list}

        return dict

    def check_number_of_times_same_products_were_observed(self, iter, molecules, energy,
                                                          rmsd_tol=0.05, energy_tol=1e-3):
        """
        Check how many times equivalent products have appeared before,
        comparing both RMSDs and energies.

        :param iter: int
            Current iteration number.
        :param molecules: list[Molecule]
            Newly generated product molecules.
        :param energy: float
            Total energy of the new product set.
        :param rmsd_tol: float
            Allowed RMSD deviation.
        :param energy_tol: float
            Allowed energy deviation.
        :return: int
            Count of previous matching product sets.
        """

        if molecules is None:
            return -1

        # Compute RMSDs for the current products
        current_rmsds = [m.calculate_RMSD() for m in molecules]

        number_of_times = 0
        data = self.read()

        for i in range(iter):
            try:
                entry = data[str(i)]
                stored_molecules = entry["molecules"]
                stored_energy = entry.get("energy", None)

                # Collect RMSDs from stored molecules
                stored_rmsds = [mol["RMSD"] for mol in stored_molecules]

                # RMSD match?
                rmsd_match = self.lists_almost_equal(current_rmsds, stored_rmsds, rmsd_tol)

                # Energy match?
                energy_match = (stored_energy is not None and
                                abs(float(stored_energy) - float(energy)) <= float(energy_tol))

                if rmsd_match and energy_match:
                    number_of_times += 1

            except KeyError:
                continue

        return number_of_times

    def lists_almost_equal(self, list1, list2, tol):
        """
        Check whether two lists of values match within a tolerance.
        Lengths must match.
        """
        if len(list1) != len(list2):
            return False

        for a, b in zip(list1, list2):
            if abs(a - b) > tol:
                return False

        return True


