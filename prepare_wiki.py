import os
import json
import shutil
from glob import glob
from tqdm import tqdm

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_file', type=str)
parser.add_argument('--output_file', type=str)
parser.add_argument('--min_document_length', type=int, default=1)
args = parser.parse_args()


def main(args):
    os.system(f'python -m wikiextractor.WikiExtractor {args.input_file} -o temp --json')
    fs = open(args.output_file, 'a') 

    files = glob('temp/*/*')
    for file in tqdm(files):
        for line in open(file, 'r'):
            data = json.loads(line)
            text = data['text']
            text = text.replace('\n', ' ').strip()
            if len(text) >= 20:
                fs.write(text)
                fs.write('\n')
    
    fs.close()

if __name__ == '__main__':
    main(args)