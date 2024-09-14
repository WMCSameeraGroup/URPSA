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

    def write_product(self, iter, molecules):
        if molecules ==None:
            print("No molecules are found")
            return
        self.create_if_not()
        new_data = self.create_json_string(molecules)
        try:
            data = self.read()
            data[iter] = new_data
        except:
            data ={iter:new_data}


        with open(self.file,"w") as file:
            file.write(json.dumps(data, indent=self.indent))


    def create_json_string(self, molecules):

        molecule_list =[]
        for molecule in molecules:
            molecule_list.append({f"RMSD":molecule.calculate_RMSD(), "molecule":molecule.to_str()})
        dict = { "num_of_mols": len(molecules), "mol": molecule_list}

        return dict