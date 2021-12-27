import os
import ray
import shutil
from tqdm import tqdm
from glob import glob
from filelock import FileLock

from transformers import AutoTokenizer

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_file', type=str, default='modu-spoken.txt')
parser.add_argument('--model_name_or_path', type=str, default='klue/bert-base')
parser.add_argument('--max_seq_length', type=int, default=512)
parser.add_argument('--add_sep', default=False, action='store_true')
args = parser.parse_args()

tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path)


def get_num_lines(fname):
    res = os.popen(f'wc -l {fname}').read()
    lines = res.strip().split()[0]
    return int(lines)

def split(input_file):
    os.makedirs('temp')
    cmd = f'split -l 1000 {input_file} temp/'
    os.system(cmd)

def clean():
    shutil.rmtree('temp')

@ray.remote
def process(text_file, output_file, seq_length, add_sep=False):
    input_fs = open(text_file, 'r')    
    buffer = []
    for doc in input_fs:
        tokens = tokenizer.tokenize(doc)
        buffer += tokens
        if add_sep:
            buffer += [tokenizer.sep_token]

        while len(buffer) > seq_length:
            text = ' '.join(buffer[:seq_length])
            buffer = buffer[seq_length:]

            with FileLock(f'{output_file}.lock'):
                with open(output_file, 'a') as output_fs:
                    output_fs.write(text)
                    output_fs.write('\n')
            
    input_fs.close()
    output_fs.close()


def main(args):
    split(args.input_file)
    files = glob('temp/*')
    
    model_name = args.model_name_or_path.replace('/', '-')
    output_file = args.input_file.split('.txt')[0] + f'_tokenized_{model_name}_{args.max_seq_length}.txt'

    ray.init()
    ray.get([process.remote(f, output_file, args.max_seq_length) for f in files])
    ray.shutdown()

    clean()

if __name__ == '__main__':
    main(args)