defaults = {
    "project": {
        "project_name": "test1",
        "input_file_name": "Test"
    },
    "controls": {
        "update_with_optimized_coordinates": "True",
        "step_size": 0.1,
        "step_count": 40,
        "stop_distance_factor": 0.4,
        "stress_release": "0:10:40",
        "sphere_radius": 4,
        "n_iterations": 100,
        "spherical_placement": "statistically_even",
        "ADD_COM_CONST": "False"
    },
    "gaussian": {
        "number_of_cores": 8,
        "memory": "8GB",
        "method": "#N opt(maxcycle=600,AddGIC) PM6 scf(maxcyc=600,xqc) nosymm"
    }
}
