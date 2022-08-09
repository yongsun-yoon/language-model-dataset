from tqdm import tqdm
from datasets import load_dataset

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--lang', type=str, default='en')
parser.add_argument('--column_name', type=str, default='text')
parser.add_argument('--min_document_length', type=int, default=20)
parser.add_argument('--output_file', type=str, default='en_cc100.txt')
args = parser.parse_args()


def main(args):
    dataset = load_dataset(path='cc100', lang=args.lang, split='train')
    print('loading dataset finished')

    fs = open(args.output_file, 'a')
    doc = ''
    for data in tqdm(dataset):
        text = data['text'].strip()
        if text:
            doc += text + ' '
        else:
            fs.write(doc + '\n')
            doc = ''
    
    fs.close()

if __name__ == '__main__':
    main(args)