import json
from tqdm.auto import tqdm
from namuwiki.extractor import extract_text

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--namuwiki_dump_path', type=str)
parser.add_argument('--min_document_length', type=int, default=20)
args = parser.parse_args()


def load_namuwiki_dump(namuwiki_dump_path):
    with open(namuwiki_dump_path, 'r', encoding='utf-8') as f:
        namu_wiki = json.load(f)
    
    print(f'Loaded {len(namu_wiki)} documents')
    return namu_wiki


def main(args):
    namu_wiki = load_namuwiki_dump(args.namuwiki_dump_path)
    fs = open('namuwiki.txt', 'a') 
    for idx, document in enumerate(tqdm(namu_wiki)):
        text = extract_text(document['text'])
        text = text.replace('\n', '  ')

        if len(text) >= args.min_document_length:
            fs.write(text)
            fs.write('\n')

    fs.close()

if __name__ == '__main__':
    main(args)