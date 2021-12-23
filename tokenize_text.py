from tqdm import tqdm
from transformers import AutoTokenizer

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_file', type=str, default='modu-spoken.txt')
parser.add_argument('--model_name_or_path', type=str, default='klue/bert-base')
parser.add_argument('--max_seq_length', type=int, default=512)
args = parser.parse_args()


def main(args):
    seq_length = args.max_seq_length - 2 # room for [CLS], [SEP]

    input_fs = open(args.input_file, 'r')
    output_file = args.input_file.split('.txt')[0] + '-tokenized.txt'
    output_fs = open(output_file, 'a')

    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path)
    buffer = []

    for doc in tqdm(input_fs):
        tokens = tokenizer.tokenize(doc)
        buffer += tokens
        buffer += [tokenizer.sep_token]

        if len(buffer) > seq_length:
            text = ' '.join(buffer[:seq_length])
            output_fs.write(text)
            output_fs.write('\n')
            buffer = buffer[seq_length:]

    input_fs.close()
    output_fs.close()

if __name__ == '__main__':
    main(args)