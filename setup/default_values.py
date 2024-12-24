
defaults = {
    "project": {
        "project_name": "test1",
        "input_file_name": "Test"
    },
    "controls": {
        "update_with_optimized_coordinates": "True",
        "step_size": 0.1,
        "step_count": 40,
        "stop_distance_factor": 0.5,
        "stress_release": "0:1:-1",
        "sphere_radius": 3,
        "n_iterations": 10,
        "spherical_placement": "statistically_even",
        "ADD_COM_CONST": "True",
        "ADD_SPHERICAL_CONST": "False",
        "dynamic_fragment_replacement": "False",
        "cutoff_energy_gap":3.0
    },
    "gaussian": {
        "number_of_cores": 1,
        "memory": "1GB",
        "method": "#N opt(maxcycle=200,AddGIC) WB97XD/6-31G* scf(maxcyc=300,xqc) nosymm"
    }
}
