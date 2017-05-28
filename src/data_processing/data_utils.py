import os
import pandas as pd

DATA_FOLDER = '/Users/JRLetelier/perso/sonification/data/oced'

COLUMNS = ['Country', 'Indicator', 'Time', 'Value']
COLUMNS_RENAME_MAPPING = {'Variables': 'Indicator'}

TREATMENTS_PATH = os.path.join(DATA_FOLDER, 'oced_code_treatment.csv')
TREATMENTS = pd.read_csv(TREATMENTS_PATH, delimiter=';').set_index(['code']).to_dict('index')


def rename_indicator(df, new_indicator):
    df['Indicator'] = new_indicator
    return df


def normalize_columns(df):
    return df.rename(columns=COLUMNS_RENAME_MAPPING, inplace=False)


def verify_columns(paths, columns):
    if paths:
        columns_0 = pd.read_csv(paths[0], delimiter=',', engine='python').columns
        for path in paths:
            this_columns = pd.read_csv(path, delimiter=',', engine='python').columns
            assert (columns_0 == this_columns).all()
            assert not set(columns) - set(this_columns.tolist())
    return True


def export_ML4(df, path):
    """ Export data to ML4 table format. """

    # get colums for maxforlive format
    df = df[COLUMNS]

    # randomize rows
    df = df.sample(frac=1)

    # for OSC format
    for column in df.columns:
        df[column] = df[column].apply(lambda x: str(x).replace(' ', '_'))

    pre_path, name = os.path.split(path.split('.')[0])
    path_out = os.path.join(pre_path, name+'_m4l.tsv')

    df.to_csv(path_out, sep='\t', header=False, index=False, encoding='utf-8', decimal=',')

    print 'data saved at \n\t %s' % path_out


def add_hash(df, hash_criteria):

    df['hash'] = ''
    for c in hash_criteria:
        df['hash'] = df['hash'] + df[c].apply(lambda x: str(x))
    df['hash'] = df['hash'].apply(lambda x: hash(x))
    return df
