import os
from glob import glob
from tqdm.auto import tqdm

from utils import read_json

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, default='')
parser.add_argument('--output_file', type=str, default='modu_newspaper.txt')
parser.add_argument('--min_document_length', type=int, default=20)
args = parser.parse_args()


def extract_text(data):
    text = []
    documents = data['document']
    for doc in documents:
        _text = [p['form'] for p in doc['paragraph']]
        _text = ' '.join(_text)
        text.append(_text)
    
    text = '\n'.join(text)
    return text


def main(args):
    fpaths = glob(os.path.join(args.input_dir, '*.json'))

    fs = open(args.output_file, 'a') 
    for fpath in tqdm(fpaths):
        data = read_json(fpath)
        text = extract_text(data)        
        fs.write(text)
        fs.write('\n')
    fs.close()


if __name__ == '__main__':
    main(args)