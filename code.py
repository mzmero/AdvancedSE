import os
import sys
import pandas as pd
import numpy as np
import matplotlib. pyplot as plt
from os import listdir
from os.path import isfile, join

## calculate box plot parameters
def get_box_plot_data(labels, bp):
    rows_list = []
    for i in range(len(labels)):
        dict1 = {}
        dict1['label'] = labels[i]
        dict1['lower_whisker'] = bp['whiskers'][i * 2].get_ydata()[1]
        dict1['lower_quartile'] = bp['boxes'][i].get_ydata()[1]
        dict1['median'] = bp['medians'][i].get_ydata()[1]
        dict1['upper_quartile'] = bp['boxes'][i].get_ydata()[2]
        dict1['upper_whisker'] = bp['whiskers'][(i * 2) + 1].get_ydata()[1]
        rows_list.append(dict1)
    return pd.DataFrame(rows_list)


# remove noise and normalize reuse score
def reuseScore(dataset_name):
    matrix = os.path.join(ROOT_PATH + '/data', dataset_name)
    data = pd.read_csv(matrix)

    ## drop first column and calculate threshold
    df = data.copy()
    df = df.drop(df.columns[0], axis=1)
    arr = df.values.flatten()
    median = np.mean(arr)
    threshold = median * 0.1

    data_frame = data.copy()
    data_frame.drop(data_frame.columns[0], axis=1, inplace=True)
    data_frame[data_frame < 0] = 0

    ## normalize reuse score
    for i, row in data_frame.iterrows():
        count = 0
        summary = 0
        for col in data_frame.columns:
            cell = data_frame.loc[df.index[i], col]
            if cell > threshold:
                count = count + 1
                summary = summary + cell
        if count > 0:
            data_frame.at[i, 'score'] = summary / count
        else:
            data_frame.at[i, 'score'] = 0

    repos_id = data_frame.columns
    lst = repos_id[:len(repos_id) - 1]

    reuse_score = pd.DataFrame({
        "repo_id": lst,
        "reuse_score": data_frame['score']
    })
    return reuse_score

# calculate quality score for each dataset
def scoring_quality(dataset_name):
    matrix = os.path.join(ROOT_PATH + '\\repository', dataset_name)
    score = pd.read_csv(matrix)
    matrix = os.path.join(ROOT_PATH + '\\commits', dataset_name)
    commits = pd.read_csv(matrix, header=0)
    arr = commits['committer'].groupby(commits['repo_id']).agg(['nunique'])
    arr.columns = ['contributors']
    score = score.merge(arr, on='repo_id')

    labels = ['stargazers', 'subscribers', 'forks', 'contributors']
    bp = plt.boxplot([score['stargazers_count'], score['subscribers_count'],
                      score['forks_count'], score['contributors']], labels=labels, showfliers=False)
    plt.close()

    dictionary = get_box_plot_data(labels, bp)
    upper_stars = dictionary['upper_whisker'][0]
    upper_subs = dictionary['upper_whisker'][1]
    upper_forks = dictionary['upper_whisker'][2]
    upper_contributors = dictionary['upper_whisker'][3]

    for i, row in score.iterrows():
        s = {}
        has_wiki = 0.1
        if upper_stars != 0:
            s['s1'] = 1 if row['stargazers_count'] > upper_stars else row['stargazers_count'] / upper_stars
        if upper_subs != 0:
            s['s2'] = 1 if row['subscribers_count'] > upper_subs else row['subscribers_count'] / upper_subs
        if upper_forks != 0:
            s['s3'] = 1 if row['forks_count'] > upper_forks else row['forks_count'] / upper_forks
        if upper_contributors != 0:
            s['s5'] = 1 if row['contributors'] > upper_contributors else row['contributors'] / upper_contributors
        if row['has_wiki'] == 0:
            has_wiki = 0

        score.at[i, 'quality_score'] = ((sum(s.values()) / 0.9) + has_wiki)

    result = score['quality_score'].groupby(score['repo_id']).unique().apply(pd.Series)
    result.columns = ['quality_score']
    return result

def correlation(dataset_name, quality_score, reuse_score):
    merge = reuse_score.merge(quality_score,on='repo_id')
    merge = merge.drop(["repo_id"], axis=1)
    corr= merge.corr()
    print("Correlation for Database "+ dataset_name+" :" )
    print(corr)
    print()

ROOT_PATH = os.path.abspath(os.getcwd())
onlyfiles = [f for f in listdir(ROOT_PATH+'//data') if isfile(join(ROOT_PATH+'//data', f)) and  f.endswith(".csv")]

for f in onlyfiles:
    q = scoring_quality(f)
    r = reuseScore(f)
    correlation(f,q,r)