import torch

from datasets import load_dataset
from transformers import AutoTokenizer, BatchEncoding


def get_token_type_ids(input_ids, sep_token_id):
    token_type_ids = []

    curr = 0
    for i in input_ids:
        token_type_ids.append(curr)
        if i == sep_token_id:
            curr = 1 - curr
    
    return token_type_ids


def prep(example, tokenizer):
    tokens = example['text'].split()
    tokens = [tokenizer.cls_token] + tokens + [tokenizer.sep_token]

    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    attention_mask = [1] * len(input_ids)
    token_type_ids = get_token_type_ids(input_ids, tokenizer.sep_token_id)
    
    return {'input_ids': input_ids, 'attention_mask': attention_mask, 'token_type_ids': token_type_ids}


def main():
    dataset = load_dataset('text', data_files='modu-spoken.txt')['train']
    print(dataset)
    # dataset = load_dataset('text', data_files='modu-spoken-tokenized.txt')['train']
    # tokenizer = AutoTokenizer.from_pretrained('klue/bert-base')
    # dataset = dataset.map(lambda x: prep(x, tokenizer))
    # dataset.set_format('torch', columns=['input_ids', 'attention_mask', 'token_type_ids'])
    
    # dataloader = torch.utils.data.DataLoader(dataset, batch_size=16, shuffle=True)
    # batch = next(iter(dataloader))
    # print(batch['input_ids'].size(), batch['attention_mask'].size(), batch['token_type_ids'].size())
    # print(batch['token_type_ids'].sum())
    # for i in range(16):
    #     print(batch['token_type_ids'][i])
    #     print('=' * 100)


if __name__ == '__main__':
    main()