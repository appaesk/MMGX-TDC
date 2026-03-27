import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('results.txt', header=None, names=['log_folder_name', 'experiment_number', 'dataset', 'performance', 'std'])
    selected_model = "GIN_AR_0_pharmacophore"
    df_selected = df[df['log_folder_name'].str.contains(selected_model)]
    submission = {}
    for idx, row in df_selected.iterrows():
        submission[row['dataset']] = [row['performance'], row['std']]
    print(submission)
    with open('submission.txt', 'w') as f:
        f.write(str(submission))