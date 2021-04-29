import json

def load_json(file):
    '''Loads a data structure from JSON file'''
    json_data = dict()
    try:
        with open(file, mode='r') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        print(f"{file} does not exist!")
    
    return json_data