import json

def read_json(fpath, encoding='utf-8'):
    with open(fpath, 'r', encoding=encoding) as f:
        data = json.load(f)
    return data