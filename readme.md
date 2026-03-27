# MMGX: Multiple Molecular Graph eXplainable Discovery for TDC Benchmark
This is the fork repository for MMGX for TDC benchmarking.

Please kindly see main repository of [MMGX](https://github.com/ohuelab/MMGX) for more detail.

![graphical abstract](https://github.com/ohuelab/mmgx/blob/main/blob/graphicalabstract.png?raw=true)

## Benchmarking 💻

### 1. Installing MMGX and TDC

- Install [MMGX](https://github.com/ohuelab/MMGX) by following the MMGX installation guidelines.
- Install [TDC](https://tdc.readthedocs.io/en/main/install.html) using `pip install PyTDC`

### 2. Configuring datasets

Copy and paste the following lines into `dataset/_dataset.csv`:

```csv
caco2_wang,X,y,s,regression,1
hia_hou,X,y,s,classification,1
pgp_broccatelli,X,y,s,classification,1
bioavailability_ma,X,y,s,classification,1
lipophilicity_astrazeneca,X,y,s,regression,1
solubility_aqsoldb,X,y,s,regression,1
bbb_martins,X,y,s,classification,1
ppbr_az,X,y,s,regression,1
vdss_lombardo,X,y,s,regression,1
cyp2d6_veith,X,y,s,classification,1
cyp3a4_veith,X,y,s,classification,1
cyp2c9_veith,X,y,s,classification,1
cyp2d6_substrate_carbonmangels,X,y,s,classification,1
cyp3a4_substrate_carbonmangels,X,y,s,classification,1
cyp2c9_substrate_carbonmangels,X,y,s,classification,1
half_life_obach,X,y,s,regression,1
clearance_microsome_az,X,y,s,regression,1
clearance_hepatocyte_az,X,y,s,regression,1
ld50_zhu,X,y,s,regression,1
herg,X,y,s,classification,1
ames,X,y,s,classification,1
dili,X,y,s,classification,1
```

### 3. Downloading and constructing datasets

1. Run `tdc_dataset.py` to download and construct dataset splits.
2. The default split uses 5 seeds (0-4) as different folds for training.
3. Datasets are saved in the `dataset` folder. Each dataset folder contains `train_0_*.csv`, `val_0_*.csv`, and `test.csv`, where `*` is the fold number.

### 4. Training the model

Run `tdc_main.py` with the command below. This loops through datasets in the list and trains three model variants:

- MMGX_A+F (atom + functional)
- MMGX_A+P (atom + pharmacophore)
- MMGX_A+J (atom + junction tree)

The reported TDC benchmark result is from MMGX_A+P.

> Note: Most datasets use the same settings below, but `cyp3a4_substrate_carbonmangels` and `ppbr_az` use `batch_size 16`.

```bash
list_file=(ames ...)
list=(functional pharmacophore junctiontree)

for name in "${list_file[@]}"; do
    echo "Processing $name ..."
    for item in "${list[@]}"; do
        python3 tdc_main.py \
            -f "$name" \
            -m GIN \
            --schema AR_0 \
            --reduced "$item" \
            --vocab_len 100 \
            --mol_embedding 256 \
            --batch_normalize \
            --fold 5 \
            --seed 0 \
            --batch_size 32 \
            --num_layers 3 \
            --num_layers_reduced 2 \
            --in_channels 128 \
            --hidden_channels 128 \
            --out_channels 128 \
            --num_layers_self 3 \
            --num_layers_self_reduced 2
    done
done
```

### 5. Collecting results

Run `tdc_submit.py` to generate the submission format for the TDC benchmark.

> Note: The selected model was set to `GIN_AR_0_pharmacophore` for MMGX_A+P.

## Result analysis 📈
As of: 2026 March 23, 20:07

Only ADMET Group Leaderboard

- Only models appear in all benchmarks
- X-axis ordered by subcategory then size of dataset

![rank comparison](https://github.com/appaesk/MMGX-TDC/blob/main/tdc_results/tdc_leaderboard_bump_chart_grouped.png?raw=true)

![zscore comparison](https://github.com/appaesk/MMGX-TDC/blob/main/tdc_results/tdc_leaderboard_bump_chart_grouped_zscore.png?raw=true)

## Citation 📃
> - Kengkanna A, Ohue M. **Enhancing property and activity prediction and interpretation using multiple molecular graph representations with MMGX**. *Communications Chemistry*, 7: 74, 2024. [doi: 10.1038/s42004-024-01155-w](https://doi.org/10.1038/s42004-024-01155-w)
