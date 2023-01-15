import pandas as pd
import numpy as np
#aa = df.iloc[0:2000,:]

# execucomp data
# df0= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/' + 'ExecuComp' + '.csv')
df0 = pd.read_sas('C:/Users/d_huang/Documents/PythonProjects/ESGDATA/compuexec.sas7bdat',encoding = 'ISO-8859-1')
# pick the row ceoindicator = ceo.
df = df0[(df0['CEOANN'] == 'CEO')]
df.rename(columns={"year": "YEAR"}, inplace=True)
df= df[['EXEC_FULLNAME', 'CONAME', 'YEAR']]

# df.to_csv('C:/Users/d_huang/Documents/PythonProjects/ESGDATA/' + 'CEO' + '.csv')

# candidate 
dfcn= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/cn22/' + 'cn' + '.txt', sep = '|', header = None)
dfcnheader= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/' + 'cn_header_file' + '.csv')
lst = dfcnheader.columns
dfcn.columns = lst

# candidate committee link
dfccl= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/ccl22/' + 'ccl' + '.txt', sep = '|', header = None)
dfcclheader= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/' + 'ccl_header_file' + '.csv')
lst = dfcclheader.columns
dfccl.columns = lst

# merge cn with ccl to pin down candidate's committee
outmerge1 = pd.merge(dfcn, dfccl, how = "left", on = ["CAND_ID"])

# # committee summary, seems useless for the project
# dfcm= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/cm22/' + 'cm' + '.txt', sep = '|', header = None)
# dfcmheader= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/' + 'cm_header_file' + '.csv')
# lst = dfcmheader.columns
# dfcm.columns = lst

# individual contribution
dfindiv= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/indiv22/' + 'itcont' + '.txt', sep = '|', 
                     header = None, skiprows=[20175605-1, 20194909-1])
dfindivheader= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/' + 'indiv_header_file' + '.csv')
lst = dfindivheader.columns
#dfindiv.columns = lst

# take a subsample to try it out
# jk = dfindiv.loc[1:10000, :]
jk = dfindiv.loc[:, :]

jk.columns = lst
# jk1 = jk[['CMTE_ID', 'NAME' ,'ZIP_CODE', 'EMPLOYER', 'OCCUPATION', 'TRANSACTION_DT', 'TRANSACTION_AMT']]
jk1 = jk[['CMTE_ID', 'NAME', 'EMPLOYER', 'TRANSACTION_DT', 'TRANSACTION_AMT']]


# selecting rows based on condition
rslt_df = jk1[jk1['TRANSACTION_AMT'] > 0]
rslt_df.dropna(subset = ['TRANSACTION_DT'], inplace = True)      # Remove rows with NaN]
# parse out the years when contribution occurred
rslt_df['TRANSACTION_DT'] = rslt_df['TRANSACTION_DT'].apply(str)
# take the string to the left of . in date
rslt_df['TRANSACTION_DT'] = rslt_df['TRANSACTION_DT'].apply(lambda x:str(x).split('.')[0])
# take the last four digit to be year
rslt_df['TRANSACTION_DT'] = rslt_df['TRANSACTION_DT'].str[-4:]


# convert data from string to numeric
rslt_df['TRANSACTION_DT'] = rslt_df['TRANSACTION_DT'].astype(int)
# clean noises in data, FEC data
rslt_df['NAME']= rslt_df['NAME'].replace(['MR.', 'MBA', 'PH.D.', 'CPA', 'MS.', 'JD', 'DR.' ,
                                          'MD', 'MR', 'MS', 'MRS', 'Adm' , 'Bri' , 'Cap' , 'Dr.' , 
                                          'Gen' , 'Gov' , 'Hon' , 'H.R' , 'Lie' 
                                          , 'Mr.', 'Ms.', 'NAMEPREFIX', 'Pro', 'Sir', 'PhD', 'PHD', 
                                          'JR', 'JR.', 'II', 'III', 'IV', 'V'],'', regex=True)


# split names into last name, first name, and other noise by ,
rslt_df[['NAMEL', 'NAMEO', 'junk', 'junk1', 'junk2', 'junk3']] = rslt_df['NAME'].str.split(pat = ',', expand = True)
rslt_df.drop(['NAME', 'junk',  'junk1',  'junk2',  'junk3'], axis = 1, inplace = True)

# rslt_df[['NAMEL', 'NAMEO', 'junk']] = rslt_df['NAME'].str.split(pat = ',', expand = True)
# rslt_df.drop(['NAME', 'junk'], axis = 1, inplace = True)



# delete the leading blank space
rslt_df['NAMEO'] = rslt_df['NAMEO'].str.lstrip()
#rslt_df['NAMEL'] = rslt_df['NAME'].apply(lambda x:str(x).split(',')[0])
# combine first name/middlename etc + last name because the buzzywuzz seems to work on first name last name format matching
rslt_df['NAME_FEC']=rslt_df['NAMEO'] + ' ' + rslt_df['NAMEL']
rslt_df.drop(['NAMEO', 'NAMEL'], axis = 1, inplace = True)
# selecting rows based on condition, in fec
rslt_df = rslt_df[rslt_df['TRANSACTION_DT'] == 2021]
# #remove all blanks in a string
rslt_df['NAME_FEC'] = rslt_df['NAME_FEC'].str.replace(" ", "")
#remove all , in a string
rslt_df['NAME_FEC'] = rslt_df['NAME_FEC'].str.replace(",", "")
#remove all . in a string
rslt_df['NAME_FEC'] = rslt_df['NAME_FEC'].str.replace(".", "")
rslt_df['NAME_FEC'] = rslt_df['NAME_FEC'].str.upper()


# selecting rows based on condition, in execucomp
df1 = df[df['YEAR'] == 2020]
# clean noises in data, execucomp data
df1['EXEC_FULLNAME']= df1['EXEC_FULLNAME'].replace(['MR.', 'MBA', 'PH.D.', 'CPA', 'MS.', 'JD', 'DR.' ,
                                          'MD', 'MR', 'MS', 'MRS', 'Adm' , 'Bri' , 'Cap' , 'Dr.' , 
                                          'Gen' , 'Gov' , 'Hon' , 'H.R' , 'Lie' 
                                          , 'Mr.', 'Ms.', 'NAMEPREFIX', 'Pro', 'Sir', 'PhD', 'PHD',
                                          'JR', 'JR.', 'II', 'III', 'IV', 'V'],'', regex=True)
# #remove all blanks in a string
df1['EXEC_FULLNAME'] = df1['EXEC_FULLNAME'].str.replace(" ", "")
#remove all , in a string
df1['EXEC_FULLNAME'] = df1['EXEC_FULLNAME'].str.replace(",", "")
#remove all . in a string
df1['EXEC_FULLNAME'] = df1['EXEC_FULLNAME'].str.replace(".", "")
df1['EXEC_FULLNAME'] = df1['EXEC_FULLNAME'].str.upper()



# find diffent columns in the second dataset to merge
outmerge6 = df1.merge(rslt_df, how = "left", left_on = 'EXEC_FULLNAME', right_on = 'NAME_FEC')


#ryan
outmerge7 = outmerge6.drop_duplicates(subset=['NAME_FEC'], keep='first')
outmerge7.dropna(subset = ['NAME_FEC'], inplace = True)

outmerge7.reset_index(inplace=True)




import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#df1['name_from_fec'] = df1['EXEC_FULLNAME'].apply(lambda x: process.extractOne(x, rslt_df['NAME_FEC'].to_list(),score_cutoff=80))



df1 = pd.read_excel('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/Top-10-richest.xlsx', sheet_name= "Sheet1")
df2 = pd.read_excel('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/Top-10-richest.xlsx', sheet_name= "Sheet2")


df1['name_from_df2'] = df1['Name'].apply(lambda x: process.extractOne(x, df2['Name'].to_list(),score_cutoff=80))
name_from_df2_list = df1['name_from_df2'].to_list()
name_from_df2_list = [_[0] if _ != None else None for _ in name_from_df2_list]
df1['name_from_df2'] = name_from_df2_list

df1 = df1.merge(df2, left_on = 'name_from_df2', right_on = 'Name', suffixes=('','_2'))
df1.drop(['Name_2','name_from_df2'],axis=1, inplace=True)


#pip nameparser








