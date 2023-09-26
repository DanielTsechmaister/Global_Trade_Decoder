import pandas as pd
import numpy as np

class Data_Preprocess():
    def __init__(self,fname):
        self.df = pd.read_pickle(fname)


    def intro(self):
        print(self.df.columns)
        print(self.df.shape)
        print(self.df.info())

    def describe_object(self, colname):
        print(self.df[colname].nunique())
        print(self.df[colname].value_counts())


    def describe_all(self,num):
        col = self.df.iloc[:, num]
        if np.issubdtype(col.dtype, np.number):
            print(col.describe())
        else:
            print(self.describe_object(self.df.columns[num]))


    def omit_zeros(self):
        self.df = self.df[(self.df['Value'] != 0) & (~self.df['Value'].isna())]
        self.df.index = [i for i in range(self.df.shape[0])]
        return True


    def filt_top_areas_by_unit(self,u,n):
        gr1 = self.df[self.df['Unit'] == u]
        area_df = gr1['Area'].value_counts()
        top = area_df.nlargest(n).index.tolist()
        self.df = gr1[gr1['Area'].isin(top)]
        self.df.index = [i for i in range(self.df.shape[0])]


    def drop_cols(self, list):
        self.df.drop(list, axis=1, inplace=True)


    def calc_stats_by_factors(self,df, factors, vals, funcs):
        dataf = df.groupby(factors)
        dataf = dataf[vals].agg(funcs)
        return dataf


    def norm_by_factors(self,cols):
        self.df['val_normed'] = self.df.groupby(cols)['Value'].transform(lambda x: (x - x.mean()) / x.std())


    def split_by_factor(self, factor, val):
        df_copy = self.df.copy()
        df_copy = df_copy[(df_copy[factor]==val)]
        df_copy.reset_index(drop=True, inplace=True)
        return df_copy


    def merge_dfs(self, s1, s2, colnames):
        s_1 = pd.DataFrame(s1)
        s_2 = pd.DataFrame(s2)
        dfs = pd.concat([s_1, s_2], axis=1, join='inner')
        dfs.columns = colnames
        return dfs


    def diff_cols(self,det, col1, col2):
        return det[col2] - det[col1]

    def apply_diff_cols(self, d, c1, c2, newcol):
        d[newcol] = d.apply(lambda row: self.diff_cols(row, c1, c2), axis=1)
        return d


def main():
    data = Data_Preprocess('data.pickle')

    # 1.
    data.intro()

    # 2. + 3.
    data.describe_all(0)

    # 4.
    data.omit_zeros()
    print("4. after omitting zeros df shape is ", data.df.shape)
    print(data.df.head())


    #  5.
    data.filt_top_areas_by_unit('tonnes',5)
    print("5. After filtering product tonnes from 5 most reported areas, df shape is ", data.df.shape)
    print(data.df.head(30))

    # 6.
    data.drop_cols(["Item","Unit"])
    print("df shape after cols reduction",data.df.shape)

    # 7.
    # group by year+element, calculate annual mean and std of export and import quantities
    print("annual mean and std of export and import quantities")
    print(data.calc_stats_by_factors(data.df,["Year","Element"],"Value",[np.mean,np.std]))

    # 8.
    # apply z-score normalization by Year
    data.norm_by_factors(["Year"])
    print("after z-score normalization by Year\n")
    print(data.df.head(10))
    print(data.df.shape)

    # 9.
    data.export_df = data.split_by_factor("Element","Export Quantity")
    print("Export dataframe shape is ",data.export_df.shape)
    print("Export dataframe head:\n", data.export_df.head())
    data.import_df = data.split_by_factor("Element", "Import Quantity")
    print("Import dataframe shape is ",data.import_df.shape)
    print("Import dataframe head:\n", data.import_df.head())

    # Additional tests on export/import data
    data.export_df = data.calc_stats_by_factors(data.export_df,["Area","Year"],"Value",np.mean)
    print("export dataframe stats shape is ",data.export_df.shape)
    print(data.export_df.head())
    data.import_df = data.calc_stats_by_factors(data.import_df,["Area","Year"],"Value",np.mean)
    print("import dataframe stats shape is ",data.import_df.shape)
    print(data.import_df.head())

    # 10.
    data.merged = data.merge_dfs(data.import_df,data.export_df,["Import","Export"])
    print("merged Export-Import dataframe shape is ",data.merged.shape)
    print("merged Export-Import head:\n",data.merged.head())


    # 11.
    data.merged = data.apply_diff_cols(data.merged,c1="Export",c2="Import",newcol='GNI')
    print("merged Export-Import dataframe with GNI looks like this:")
    print(data.merged.head(10))

if __name__=="__main__":
    main()




