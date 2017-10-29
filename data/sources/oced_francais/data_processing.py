import os
import pandas as pd

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

SORT_CRITERIA = ['Pays', 'Indicateur', 'TIME']

def ecart(df):
    pass

def ecart_pourcentage(df):
    pass


def all_pourcentage(df):
    pass

def women_pourcentage(df):
    pass

def by_sex_pourcentage(df):

    # remove unuseful entries
    if 'Age Group' in df:
        df = df[df['Age Group'] == 'Total']

    # get avalaible sexs
    df = df[df['SEX'] != 'ALL_PERSONS']
    df = df[df['SEX'] != 'ALL']
    avalaible_sexs = list(set(df['SEX'].tolist()))
    sexA, sexB = avalaible_sexs

    # compute difference treatment
    hash_criteria = df.columns.tolist()
    for c in [u'Value', u'Sexe', u'SEX']:
        hash_criteria.remove(c)
    df['hash'] = ''
    for c in hash_criteria:
        df['hash'] = df['hash'] + df[c].apply(lambda x: str(x))
    df['hash'] = df['hash'].apply(lambda x: hash(x))


    sexA_df = df[df['SEX'] == sexA].sort_values('hash')
    sexA_df.rename(columns={u'Value': 'Value_A'}, inplace=True)
    sexB_df = df[df['SEX'] == sexB].sort_values('hash')
    sexB_df.rename(columns={u'Value': 'Value_B'}, inplace=True)
    merged_sex = pd.merge(sexA_df, sexB_df, on=SORT_CRITERIA+['hash'])

    # compute difference
    merged_sex['Pourcentage difference'] = (merged_sex['Value_A'] - merged_sex['Value_B']).apply(lambda x: abs(x))
    merged_sex['Value'] = merged_sex['Pourcentage difference']

    # store in new dataframe
    sex_diff_df = merged_sex[SORT_CRITERIA + ['Value', 'Pourcentage difference']].copy(deep=True)

    # sex_diff_df.head()
     
    return sex_diff_df

BASE_PATH = "/Users/JRLetelier/perso/sonification/data/sources/oced_francais"
ENCODING = 'utf-8'
TO_DROP = [
    "Flags",
    "Flag Codes",
    "Reference Period Code",
    "Reference Period",
    "PowerCode",
    "PowerCode Code",
]

FILES = [
    'emploi/GENDER_EMP_29102017131217738.csv',
    'entreprenariat/GENDER_ENT1_29102017131256176.csv',
    'education/GENDER_EDU_29102017131322363.csv',
]

TO_USE = {

    'EMP1': {'treatment': 'all_pourcentage'},
    'EMP3': {'treatment': 'all_pourcentage'},
    'EMP5': {'treatment': 'all_pourcentage'},
    'EMP8': {'treatment': 'all_pourcentage'},
    'EMP9': {'treatment': 'ecart_pourcentage'},
    'EMP10': {'treatment': 'by_sex_pourcentage'},
    'EMP12_P': {'treatment': 'women_pourcentage'},
    'EMP12_T': {'treatment': 'women_pourcentage'},
    'EMP13_A': {'treatment': 'by_sex_pourcentage'},
    'EMP13_I': {'treatment': 'by_sex_pourcentage'},
    'EMP13_S': {'treatment': 'by_sex_pourcentage'},
    'EMP17': {'treatment': 'women_pourcentage'},

    'ENT1': {'treatment': 'by_sex_pourcentage'},
    'ENT2': {'treatment': 'by_sex_pourcentage'},
    'ENT3': {'treatment': 'women_pourcentage'},
    'ENT4': {'treatment': 'women_pourcentage'},
    'ENT5': {'treatment': 'by_sex_pourcentage'},
    'ENT7': {'treatment': 'ecart'},
    'ENT8': {'treatment': 'by_sex_pourcentage'},
    'ENT9': {'treatment': 'by_sex_pourcentage'},
    'ENT10': {'treatment': 'by_sex_pourcentage'},
    'ENT11': {'treatment': 'by_sex_pourcentage'},
    'ENT12': {'treatment': 'by_sex_pourcentage'},
    'ENT13': {'treatment': 'by_sex_pourcentage'},
    'SELF_TERTIARY_EDU': {'treatment': 'by_sex_pourcentage'},
    'GAL_TRAINING': {'treatment': 'by_sex_pourcentage'},
    'GAL_MONEY': {'treatment': 'by_sex_pourcentage'},
    'SELF_YOUNG_SELF': {'treatment': 'by_sex_pourcentage'},
    'GAL_RISK': {'treatment': 'by_sex_pourcentage'},

    'EDU_11_READ': {'treatment': 'by_sex_pourcentage'},
    'EDU_11_MATH': {'treatment': 'by_sex_pourcentage'},
    'EDU_11_SCI': {'treatment': 'by_sex_pourcentage'},
    'EDU_12_READ': {'treatment': 'by_sex_pourcentage'},
    'EDU_12_MATH': {'treatment': 'by_sex_pourcentage'},
    'EDU_12_SCI': {'treatment': 'by_sex_pourcentage'},

}

for f in FILES:
    df = pd.read_csv(os.path.join(BASE_PATH, f), encoding=ENCODING)
    df.rename(index=str, columns={'INDICATOR': 'IND'}, inplace=True)
    df.drop(TO_DROP, axis=1, inplace=True)

    indicatives = {tuple(_) for _ in df[['Indicateur', 'IND', 'Unit']].as_matrix().tolist()}
    for ind_name, ind_code, unit in indicatives:
        # print "'%s'," % ind_code
        if ind_code in TO_USE.keys():
            # print ""
            # print ind_code
            # print ind_name
            # print unit
            # print df[df.IND == ind_code].SEX.unique()
            locals()[TO_USE[ind_code]['treatment']](df[df.IND == ind_code])
