import json
from tqdm.auto import tqdm
from namuwiki.extractor import extract_text

from utils import read_json

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_file', type=str)
parser.add_argument('--output_file', type=str, default='namuwiki.txt')
parser.add_argument('--min_document_length', type=int, default=20)
args = parser.parse_args()


def main(args):
    namu_wiki = read_json(args.input_file)
    fs = open(args.output_file, 'a') 
    for idx, document in enumerate(tqdm(namu_wiki)):
        text = extract_text(document['text'])
        text = text.replace('\n', '  ')

        if len(text) >= args.min_document_length:
            fs.write(text)
            fs.write('\n')

    fs.close()

if __name__ == '__main__':
    main(args)