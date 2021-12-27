import os
from tqdm import tqdm
from transformers import AutoTokenizer

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_file', type=str)
parser.add_argument('--model_name_or_path', type=str)
parser.add_argument('--max_seq_length', type=int, default=512)
parser.add_argument('--add_sep', default=False, action='store_true')
args = parser.parse_args()


def get_num_lines(fname):
    res = os.popen(f'wc -l {fname}').read()
    lines = res.strip().split()[0]
    return int(lines)

def main(args):
    seq_length = args.max_seq_length - 2 # room for [CLS], [SEP]
    input_fs = open(args.input_file, 'r')

    model_name = args.model_name_or_path.replace('/', '-')
    output_file = args.input_file.split('.txt')[0] + f'_tokenized_{model_name}_{args.max_seq_length}.txt'
    output_fs = open(output_file, 'a')

    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path)
    buffer = []

    for doc in tqdm(input_fs):
        tokens = tokenizer.tokenize(doc)
        buffer += tokens
        if args.add_sep:
            buffer += [tokenizer.sep_token]

        while len(buffer) > seq_length:
            text = ' '.join(buffer[:seq_length])
            output_fs.write(text)
            output_fs.write('\n')
            buffer = buffer[seq_length:]

    input_fs.close()
    output_fs.close()

if __name__ == '__main__':
    main(args)