import os, glob, csv
import numpy as np
import pandas as pd

ww_path = '/Users/JRLetelier/perso/sonification'

def export_ML4(path,rows=[]):

    # load data
    df = pd.read_csv(path, delimiter=',')

    # select rows
    rows_ = list(set(rows) & set(df.columns.tolist()))
    df = df[rows_]

    # clean data
    df.dropna(axis='index',inplace=True,how='any')

    # data traitement
    tt = 'Sex'
    if tt in rows_:
        try:
            if (len(set(df[tt].tolist()))>1):
                to_treats = list(set(df[tt].tolist()))
                print to_treats
                if 'All' in to_treats:
                    to_treats.remove('All')
                tt0 = to_treats[0]
                tt1 = to_treats[1]
                new_df = df[df[tt]==tt0].copy()
                del new_df[tt]
                to_replace_df = pd.DataFrame(np.abs(df[df[tt]==tt0]['Value'].as_matrix()  - df[df[tt]==tt1]['Value'].as_matrix()))
                new_df['Value'] = to_replace_df.values
                df = new_df
        except:
            return 

    # normalise
    # cols_to_norm = ['Value']
    # df[cols_to_norm] = df[cols_to_norm].apply(lambda x: (x + x.min()))
    # df[cols_to_norm] = df[cols_to_norm].apply(lambda x: (100*(x/x.max())))


    # monitoring data
    # for i,column in enumerate(df.columns.tolist()):
    #     print column
    #     if column=='Value':
    #         values = np.array([row[1].tolist()[i] for row in df.iterrows()])
    #         print  "min %s | max %s  | mean %s "%  (values.min(),values.max(),values.mean())
    #     else:
    #         set_ = set([ row[1].tolist()[i] for row in df.iterrows()])
    #         print "%s" % ' | '.join([str(s) for s in set_])
    #     print ""




    # export data to ML4
    rows_out = []
    for row in df.iterrows():
        idx = row[0]
        tup = row[1]
        tup[1] = '_'.join(tup[1].split(' '))
        for i in range(len(tup)):
            if isinstance(tup[i],str):
                tup[i] = '_'.join(tup[i].split(' '))
                tup[i] = '_'.join(tup[i].split(','))
        str_ = ' '.join([str(t) for t in tup])+";\n"
        rows_out.extend([str_])

    # name = path.split('.')[0].split('/')[-1]
    # path_out = os.path.join(ww_path,'data','oced',name+'.txt')
    path_out = path.split('.')[0]+'.txt'
    with open(path_out,'w') as f_out:
        f_out.writelines([r for r in rows_out])

    print 'data saved at \n\t %s' % path_out

if __name__=='__main__':

    kinds = {
        'education'           : ['Indicator','Country','Value','Time','Sex'],
        'development'         : ['Variables','Country','Value','Time','Sex'],
        'employment'          : ['Indicator','Country','Value','Time','Sex'],
        'health'              : [],
        'entrepreneurship'    : ['Indicator','Country','Value','Time','Sex'],
        }

    for kind,rows in kinds.iteritems():
        print "\n\n**** %s *****\n\n" % kind
        path_list = glob.glob(os.path.join(ww_path,'data','oced',"%s/*.csv"%kind))
        for path in path_list:
            print "\n\t %s " % path
            export_ML4(path,rows)
