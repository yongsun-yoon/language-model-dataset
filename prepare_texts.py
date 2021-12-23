import os
from glob import glob
from tqdm import tqdm

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str)
parser.add_argument('--output_file', type=str)
parser.add_argument('--min_document_length', type=int, default=1)
args = parser.parse_args()





def main(args):
    fpaths = glob(os.path.join(args.input_dir, '*.txt'))
    wfs = open(args.output_file, 'a') 
    for fpath in tqdm(fpaths):
        rfs = open(fpath)
        for doc in tqdm(rfs):
            doc = doc.strip()
            if len(doc) >= args.min_document_length:
                wfs.write(doc)
                wfs.write('\n')

    
        rfs.close()
    wfs.close()

if __name__ == '__main__':
    main(args)