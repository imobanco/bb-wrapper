import json
import os


def dump_response(response, file_realpath):
    current_file_path = os.path.dirname(file_realpath)
    file_name = os.path.basename(file_realpath).split(".")[0]
    data_path = os.path.join(current_file_path, "data")

    file_path = os.path.join(data_path, f"{file_name}.json")
    with open(file_path, "w") as file:
        json.dump(response.data, file, indent=4)
