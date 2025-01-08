
# The data required for training and testing in the offline learning process, 
# and the data needed for unknown object parameter estimation.

def load_data(data_name):
    
    data_config = {
        

        # The data from 4500 to 54500 seconds is the data needed for SINDy learning, 
        # and the data from 50 to 70 seconds is the data for testing the identified unmodeled dynamics.
        "train": {  
            "path": "../data/train/",
            "start_point": 0,
            "end_point": 50000
        },
        "test": {  
            "path": "../data/test/",
            "start_point": 0,
            "end_point": 20000
        },
        

        # Six types of data used to verify the robustness of the proposed methodology and the accuracy of estimation.
        "obj1_1": {  
            "path": "../data/obj1_1/",
            "start_point": 0,
            "end_point": 10000
        },
        "obj1_2": {  
            "path": "../data/obj1_2/",
            "start_point": 0,
            "end_point": 10000
        },
        "obj1_3": {  
            "path": "../data/obj1_3/",
            "start_point": 0,
            "end_point": 10000
        },
        "obj1_4": {  
            "path": "../data/obj1_4/",
            "start_point": 0,
            "end_point": 10000
        },
        "obj2": {  
            "path": "../data/obj2/",
            "start_point": 0,
            "end_point": 10000
        },
        "obj3": {  
            "path": "../data/obj3/",
            "start_point": 0,
            "end_point": 10000
        }
    }

    if data_name not in data_config:
        print("error")
        return None

    data_info = data_config[data_name]
    path = data_info["path"]
    files = {
        "franka_ft": f"{path}Fext_local_forObjectEstimation.csv",
        "g": f"{path}robot_g_local.csv",
        "v": f"{path}object_velocity.csv",
        "a": f"{path}object_acceleration.csv",
        "sensor_cali": f"{path}ft_data_cali.csv"
    }

    start_point = data_info["start_point"]
    end_point = data_info["end_point"]

    return start_point, end_point, *files.values()
