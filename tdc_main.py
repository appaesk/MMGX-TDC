######################
### Import Library ###
######################

# My library
from molgraph.dataset import *
from molgraph.graphmodel import *
from molgraph.training import *
from molgraph.testing import *
from molgraph.visualize import *
from molgraph.experiment import *
# General library
import os
import argparse
import numpy as np
# pytorch
import torch
import pytorch_lightning as pl
os.environ["CUBLAS_WORKSPACE_CONFIG"]=":4096:8"
torch.set_default_dtype(torch.float64)
# Ensure that all operations are deterministic on GPU (if used) for reproducibility
torch.backends.cudnn.determinstic = True
torch.backends.cudnn.benchmark = False

from tdc.benchmark_group import admet_group
group = admet_group(path = 'data/')

#####################
### Argument List ###
#####################

####################
### Main Program ###
####################

if __name__ == '__main__':
    print(os.environ["CUBLAS_WORKSPACE_CONFIG"])
    parser = ArgumentParser()
    args = parser.getArgument()
    print(args)

    file = args.file
    smiles = args.smiles 
    task = args.task
    splitting = args.splitting 
    splitting_fold = args.fold
    splitting_seed = args.splitting_seed

    # get validated dataset
    datasets = getDataset(file, smiles, task, splitting, skip_validation=True)
    # compute positive weight for classification
    if args.graphtask == 'classification':
        args.pos_weight = getPosWeight(datasets)
        print('pos_weight:', args.pos_weight)
    # generate dataset splitting
    datasets_splitted = generateDatasetSplitting(file, splitting, splitting_fold, splitting_seed)
    # generate all graph dataset
    datasets_graph = generateGraphDataset(file)
    # generate all reduced graph dataset
    dict_reducedgraph = dict()
    for g in args.reduced:
        if g == 'substructure':
            for i in range(splitting_fold):
                vocab_file = file+'_'+str(i)
                if not os.path.exists('vocab/'+vocab_file+'.txt'):
                    generateVocabTrain(file, splitting_seed, splitting_fold, vocab_len=args.vocab_len)
                dict_reducedgraph[g] = generateReducedGraphDict(file, g, vocab_file=vocab_file)
        else:
            dict_reducedgraph[g] = generateReducedGraphDict(file, g)
        
    trainer = Trainer(args)
    trainer.train()
    print("TRAINING COMPLETED!")

    args_test = dict()
    predictions_list = []
    for fold in [0, 1, 2, 3, 4]:
        print(f'FOLD {fold} TESTING...')
        args_test['log_folder_name'] = trainer.log_folder_name
        args_test['exp_name'] = args.experiment_number
        args_test['fold_number'] = fold
        args_test['seed'] = args.seed

        test_loader, datasets_test =  generateDataLoaderTesting(args.file, args.batch_size)
        print('length of test_loader:', len(test_loader))
        print('length of datasets_test:', len(datasets_test))

        tester = Tester(args, args_test)
        y_pred = tester.test(test_loader)
        print('length of y_pred:', len(y_pred))

        x_embed = tester.getXEmbed()
        y_test = tester.getYTest()
        print('length of x_embed:', len(x_embed))
        print('length of y_test:', len(y_test))

        predictions = {}
        predictions[args.file] = y_pred
        predictions_list.append(predictions)
        
        # path = 'dataset/'+trainer.log_folder_name+'/results'
        # legend = getLegend(args.graphtask, y_test)
        # visualize_pca(x_embed, y_test, title=args.file, path=path, legend=legend)
        # visaulize_tsne(x_embed, y_test, title=args.file, path=path, legend=legend)
        # visualize_umap(x_embed, y_test, title=args.file)

    results = group.evaluate_many(predictions_list)
    # {'caco2_wang': [6.328, 0.101], 'hia_hou': [0.5, 0.01], ...}

    # export results with log_folder_name and experiment_number
    path = 'results.txt'
    # if not exists, create file and write header
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write('log_folder_name,experiment_number,dataset,performance,std\n')
    with open(path, 'a') as f:
        for dataset in results:
            metric = results[dataset][0]
            std = results[dataset][1]
            f.write(f'{trainer.log_folder_name},{args.experiment_number},{dataset},{metric},{std}\n')


    print('COMPLETED!')