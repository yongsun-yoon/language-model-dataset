from tqdm import tqdm
from datasets import load_dataset

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--dataset_name', type=str, default='bookcorpus')
parser.add_argument('--column_name', type=str, default='text')
parser.add_argument('--min_document_length', type=int, default=1)
args = parser.parse_args()


def main(args):
    dataset = load_dataset(args.dataset_name)
    print(dataset)

    for k, data in dataset.items():
        fname = f'{args.dataset_name}-{k}.txt'
        fs = open(fname, 'a') 

        for doc in tqdm(data):
            text = doc[args.column_name]
            if len(text) >= args.min_document_length:
                fs.write(text)
                fs.write('\n')
        
        fs.close()


if __name__ == '__main__':
    main(args)