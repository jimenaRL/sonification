import os
import copy
import glob
import pandas as pd


def export_ML4(df, path):
    """ Export data to ML4 table format. """

    re_order_columns = [df.columns[1], df.columns[0]] + df.columns[2:].tolist()
    df = df[re_order_columns]

    for column in df.columns:
        df[column] = df[column].apply(lambda x: str(x).replace(' ', '_'))

    pre_path, name = os.path.split(path.split('.')[0])
    path_out = os.path.join(pre_path, name+'_m4l.txt')

    # df.to_csv(path_out, sep='\t', header=False, index=False, encoding='ascii',
    #           decimal=',')

    print df.head(5)
    print 'data saved at \n\t %s' % path_out


def sex(df):
    """ Sex difference data traitement. """

    sex = 'Sex'
    if not sex in df.columns:
        return
    sort_criteria = copy.deepcopy(rows)
    sort_criteria.remove(sex)
    sort_criteria.remove('Value')
    avalaible_sexs = list(set(df[sex].tolist()))
    if not len(avalaible_sexs) > 1:
        return
    df = df[df[sex] != 'All']
    if 'All' in avalaible_sexs:
        avalaible_sexs.remove('All')
    sex0, sex1 = avalaible_sexs
    sex0_df = df[df[sex] == sex0].sort_values(sort_criteria)
    sex1_df = df[df[sex] == sex1].sort_values(sort_criteria)
    assert sex0_df.shape == sex1_df.shape
    sex0_df = sex0_df.reset_index().drop('index', axis=1)
    sex1_df = sex1_df.reset_index().drop('index', axis=1)
    for sc in sort_criteria:
        assert sex0_df[sc].tolist() == sex1_df[sc].tolist()

    # compute difference
    diff = (sex0_df['Value'] - sex1_df['Value']).abs()

    # scale difference to [0, 1] range
    diff = (diff - diff.min()) / (diff.max() - diff.min())

    # store in new dataframe
    sex_diff_df = sex0_df[sort_criteria].copy(deep=True)
    sex_diff_df['Value'] = diff

    return sex_diff_df


def data_traitement(path, rows=[]):

    # load data
    df = pd.read_csv(path, delimiter=',', engine='python')

    # select rows
    avalaible_rows = list(set(rows) & set(df.columns.tolist()))
    df = df[avalaible_rows].copy(deep=True)

    # clean data
    df.dropna(axis='index', inplace=True, how='any')

    # specific data traitement
    sex_diff_df = sex(df)
    export_ML4(sex_diff_df, path)


if __name__ == '__main__':

    kinds = {
        # 'education': ['Indicator', 'Country', 'Value', 'Time', 'Sex'],
        # 'development': ['Variables', 'Country', 'Value', 'Time', 'Sex'],
        # 'employment': ['Indicator', 'Country', 'Value', 'Time', 'Sex'],
        # 'health': [],
        'entrepreneurship': ['Indicator', 'Country', 'Value', 'Time', 'Sex'],
    }

    # data_path = 'path/to/sonification/data/oced'
    data_path = '/Users/JRLetelier/perso/sonification/data/oced'

    if not os.path.exists(data_path):
        raise ValueError("Please provide set a valid path for the data to treat !!! ")

    for kind, rows in kinds.iteritems():
        print "\n\n**** %s *****\n\n" % kind
        path_list = glob.glob(os.path.join(data_path, "%s/*.csv" % kind))
        for path in path_list:
            print "\n\t %s " % path
            data_traitement(path, rows)
