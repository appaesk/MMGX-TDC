from tdc.benchmark_group import admet_group
import pandas as pd
import os
import random

if __name__ == '__main__':

    group = admet_group(path = 'data/')
    column_name = {'Drug_ID': 'ids', 'Drug': 'X', 'Y': 'y'}
    predictions_list = []
    default_number = 0

    for fold_seed in [0, 1, 2, 3, 4]:
        for benchmark in group:
            name = benchmark['name']
            # all benchmark names in a benchmark group are stored in group.dataset_names
            predictions = {}
            name = benchmark['name']
            train_val, test = benchmark['train_val'], benchmark['test']
            train, valid = group.get_train_valid_split(benchmark = name, split_type = 'default', seed = fold_seed)
            # scaffold, random, combination, group

            # save to csv file with ids, smiles, y, split
            os.makedirs(f'dataset/{name}', exist_ok=True)
            train['s'] = 'train'
            valid['s'] = 'valid'
            test['s'] = 'test'
            train = train.rename(columns=column_name)
            valid = valid.rename(columns=column_name)
            test = test.rename(columns=column_name)
            train.to_csv(f'dataset/{name}/train_{default_number}_{fold_seed}.csv', index=False)
            valid.to_csv(f'dataset/{name}/val_{default_number}_{fold_seed}.csv', index=False)
            test.to_csv(f'dataset/{name}/test.csv', index=False)

            # combine train and valid and test
            combined = pd.concat([train, valid, test], ignore_index=True)
            combined.to_csv(f'dataset/{name}.csv', index=False)
