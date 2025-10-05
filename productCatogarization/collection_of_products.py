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

    def check_number_of_times_same_products_were_observed(self,iter,moleculs):
        """ check how many times the same products were observed using RMSD
        :param iter: int
            current iteration number
        :param moleculs: list of Molecule objects
            list of molecules to compare with the products in the file
        :return: int
            number of times the same products were observed
        :rtype: int
        :example: 3
        """

        if moleculs is None:
            return -1
        number_of_times = 0
        current_rmsds = [molecule.calculate_RMSD() for molecule in moleculs]
        data = self.read()


        for i in range(iter):
            rmsd_list = []
            try:
                for j in data[str(i)]['molecules']:
                    rmsd_list.append(j["RMSD"])
                    if self.almost_equal_RMSD(current_rmsds, rmsd_list):
                        number_of_times += 1
            except:
                    pass


        return number_of_times


    def almost_equal_RMSD(self, list1, list2,possible_change=0.05):
        """ check if two lists of RMSD values are almost equal
        :param list1: list of float
            first list of RMSD values
        :param list2: list of float
            second list of RMSD values
        :param possible_change: float
            maximum allowed difference between two RMSD values to be considered almost equal
        :return: bool
            True if the two lists are almost equal, False otherwise
        :rtype: bool
        """
        for i, j in zip(list1,list2):
            if i < j:
                if i+possible_change < j:
                    return False
            else:
                if i+possible_change > j:
                    return False
        return True

