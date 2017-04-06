from os import path
import yaml

def load():
    map_path = path.join(path.dirname(__file__), 'mapping.yaml')
    mapp = open(map_path, 'rb')
    data = yaml.safe_load(mapp)['mappings']
    return data
