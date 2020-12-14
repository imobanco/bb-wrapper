import json
import os


def dump_response(response, file_name):
    current_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(current_path, "data")

    file_path = os.path.join(data_path, f"{file_name}.json")
    with open(file_path, "w") as file:
        json.dump(response.data, file, indent=4)
