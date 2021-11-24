import os
from glob import glob
from tqdm.auto import tqdm

from utils import read_json

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, default='')
parser.add_argument('--output_file', type=str, default='modu_written.txt')
parser.add_argument('--min_document_length', type=int, default=20)
args = parser.parse_args()


def extract_text(data):
    assert len(data['document']) == 1
    paragraph = data['document'][0]['paragraph']
    text = [i['form'] for i in paragraph]
    text = ' '.join(text)
    return text


def main(args):
    fpaths = glob(os.path.join(args.input_dir, '*.json'))

    fs = open(args.output_file, 'a') 
    for fpath in tqdm(fpaths):
        data = read_json(fpath)
        text = extract_text(data)
        
        if len(text) >= args.min_document_length:
            fs.write(text)
            fs.write('\n')
    
    fs.close()


if __name__ == '__main__':
    main(args)