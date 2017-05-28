import os
import sys
import traceback
import copy
import datetime
import glob
import pandas as pd

from data_utils import *


def sex(df, columns):
    """ values are in any range and described for both men and women
    """

    # define sort criteria
    sort_criteria = copy.deepcopy(columns)
    sort_criteria.remove('Sex')
    sort_criteria.remove('Value')

    # get avalaible sexs
    avalaible_sexs = list(set(df['Sex'].tolist()))
    if not len(avalaible_sexs) > 1:
        print "fail treatment by sex: %s" % df.Indicator.tolist()[0]
        raise ValueError("Need at least two keys in 'Sex' columns.")
    df = df[df['Sex'] != 'All']
    if 'All' in avalaible_sexs:
        avalaible_sexs.remove('All')
    if not len(avalaible_sexs) == 2:
        print "fail treatment by sex: %s" % df.Indicator.tolist()[0]
        raise ValueError("Wrong number of keys in 'Sex' columns.")
    sexA, sexB = avalaible_sexs

    # pre difference treatment
    df = add_hash(df, sort_criteria)

    sexA_df = df[df['Sex'] == sexA].sort_values('hash')
    sexA_df.rename(columns={u'Value': 'Value_A'}, inplace=True)
    sexB_df = df[df['Sex'] == sexB].sort_values('hash')
    sexB_df.rename(columns={u'Value': 'Value_B'}, inplace=True)

    merged_sex = pd.merge(sexA_df, sexB_df, on=sort_criteria+['hash'])

    # compute difference
    merged_sex['diff'] = (merged_sex['Value_A'] - merged_sex['Value_B']).apply(lambda x: abs(x))

    # scale difference to [0, 1] range
    merged_sex['diff'] = (merged_sex['diff'] - merged_sex['diff'].min()) / \
        (merged_sex['diff'].max() - merged_sex['diff'].min())

    # store in new dataframe
    merged_sex.rename(columns={u'diff': 'Value'}, inplace=True)
    sex_diff_df = merged_sex[sort_criteria + ['Value']].copy(deep=True)

    return sex_diff_df


def share(df, columns):
    """ values are in [0, 1] range with
            0.5 ~ no difference between men and women
              0 ~ maximal difference between men and women
    """
    df['Value'] = df['Value'].apply(lambda x: 1-2*x)
    return df


def no_treat(df, columns):
    """ values are in [0, 1] range with
            0 ~ no difference between men and women
            1 ~ maximal difference between men and women
    """
    return df


def percentage(df, columns):
    """ values are in [0, 100] range with
            0 ~ no difference between men and women
          100 ~ maximal difference between men and women
    """
    df['Value'] = df['Value'].apply(lambda x: x/100.)
    return df


def data_traitement(path, columns, treatment, new_indicator):

    try:

        print 'processing: %s' % path
        print 'treatment: %s' % treatment

        if isinstance(columns, basestring):
            columns = list(columns.split(','))

        if isinstance(treatment, basestring):
            treatment = globals()[treatment]

        # load and clean data
        df = pd.read_csv(path, delimiter=',', engine='python')[columns]
        df.dropna(axis='index', inplace=True, how='any')

        # normalize columns
        df = normalize_columns(df)

        # rename indicator
        df = rename_indicator(df, new_indicator)

        # specific data traitement
        processed_df = treatment(df, columns)
        export_ML4(processed_df, path)

    except Exception as e:
        print 'failed'
        print traceback.print_exc()
        os.system('open %s' % path)
        raise ValueError()


def create_database():

    if not os.path.exists(DATA_FOLDER):
        raise ValueError("Please provide set a valid path for the data to treat.")

    # create data dict
    data = {
        'development': {  # ok
            'columns': ['Country', 'Variables', 'Time', 'Value'],
            'paths':  glob.glob(os.path.join(DATA_FOLDER, "development/*.csv")),

        },
        'education': {  # ok
            'columns': COLUMNS + ['Sex'],
            'paths':  glob.glob(os.path.join(DATA_FOLDER, "education/*.csv")),

        },
        'employment': {
            'columns': COLUMNS + ['Sex'],
            'paths':  glob.glob(os.path.join(DATA_FOLDER, "employment/*.csv")),

        },
        'health': {
            'columns': COLUMNS,
            'paths':  glob.glob(os.path.join(DATA_FOLDER, "health/*.csv")),
        },
        'entrepreneurship': {  # ok
            'columns': COLUMNS + ['Sex'],
            'paths':  glob.glob(os.path.join(DATA_FOLDER, "entrepreneurship/*.csv")),

        },
    }

    for k, v in data.iteritems():
        print k
        verify_columns(v['paths'], v['columns'])

    records = []
    for kind, v in data.iteritems():
        for path in v['paths']:
            df = pd.read_csv(path, delimiter=',', engine='python')
            df = normalize_columns(df)
            records.append({
                'path': path,
                'columns': ','.join(v['columns']),
                'kind': kind,
                'name': df.Indicator.tolist()[0],
                'code': os.path.split(path)[-1].split('.')[0],
            })

    df_out = pd.DataFrame.from_records(records)
    columns = ['name', 'kind', 'code', u'columns', u'path']
    path = '/Users/JRLetelier/perso/sonification/data/oced/oced_all.csv'
    bk_path = '/Users/JRLetelier/perso/sonification/data/oced/oced_all_bk.csv'
    os.system('mv %s %s' % (path, bk_path))
    df_out.to_csv(path, sep=';', header=True, index=False, columns=columns)

    if sys.platform == 'darwin':
        os.system('open %s' % path)

    print 'db saved at %s' % path


def parse_database():

    path = '/Users/JRLetelier/perso/sonification/data/oced/oced_all.csv'
    db = pd.read_csv(path, delimiter=';', engine='python')

    for k, row in db.iterrows():
        data_traitement(row.path,
                        row['columns'],
                        TREATMENTS[row.code]['treatment'],
                        TREATMENTS[row.code]['new_indicator_name'])

if __name__ == '__main__':
    # create_database()
    parse_database()
