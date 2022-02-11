from tqdm import tqdm
from datasets import load_dataset

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--dataset_path', type=str, default='wikipedia')
parser.add_argument('--dataset_name', type=str, default='20200501.en')
parser.add_argument('--dataset_split', type=str, default='train')
parser.add_argument('--column_name', type=str, default='text')
parser.add_argument('--min_document_length', type=int, default=20)
parser.add_argument('--output_file', type=str, default='enwiki.txt')
args = parser.parse_args()


def main(args):
    if args.dataset_name:
        dataset = load_dataset(path=args.dataset_path, name=args.dataset_name, split=args.dataset_split)
    else:
        dataset = load_dataset(path=args.dataset_path, split=args.dataset_split)

    fs = open(args.output_file, 'a')
    for data in tqdm(dataset):
        text = data[args.column_name]
        text = text.replace('\n', ' ').strip()
        if len(text) >= args.min_document_length:
            fs.write(text)
            fs.write('\n')
    
    fs.close()

if __name__ == '__main__':
    main(args)