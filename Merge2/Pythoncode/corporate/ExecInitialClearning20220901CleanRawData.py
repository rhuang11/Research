import pandas as pd
import numpy as np


# # the CEO data is processed in SAS by combining execucomp and compustat becuase of the issue of the fiscal years used in execucomp
# df= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/' + 'CEO' + '.csv')

# names of top 5 CEOS
df= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/' + 'TOP5' + '.csv')


df.rename(columns={"year": "YEAR"}, inplace=True)
df1= df[['EXEC_FULLNAME', 'CONAME', 'YEAR', 'EXEC_LNAME', 'EXEC_FNAME' ,'EXEC_MNAME', 'GVKEY', 'CEOANN']]
# df.to_csv('C:/Users/d_huang/Documents/PythonProjects/ESGDATA/' + 'CEO' + '.csv')
# df0.to_csv('C:/Users/d_huang/Documents/PythonProjects/ESGDATA/' + 'TOP5' + '.csv')


# clean noises in data, execucomp data
df1['EXEC_LNAME']= df1['EXEC_LNAME'].replace(['(MR.)$', '(MBA)$', '(PH.D.)$', '(CPA)$', '(MS.)$', '(JD)$', '(DR.)$' ,
                                          '(MD)$', '(MR)$', '(MS)$', '(MRS)$', '(Adm)$' , '(Bri)$' , '(Cap)$' , '(Dr.)$' , 
                                          '(Gen)$' , '(Gov)$' , '(Hon)$' , '(H.R)$' , '(Lie)$' 
                                          , '(Mr.)$', '(Ms.)$', '(NAMEPREFIX)$', '(Pro)$', '(Sir)$', '(PhD)$', '(PHD)$', 
                                          '(JR)$', '(JR.)$', '(III)$', '(II)$', '(IV)$', '(V)$', '(Jr.)$'
                                          , '(Jr.)$' , '(Sr.)$', '(J.D.)$', '(Esq.)$', '(P.E.)$' , '(Ph.D.)$'],'', regex=True)

# df1['NAME_EXEC']=df1['EXEC_FNAME'] + ' ' +  df1['EXEC_MNAME'] + ' ' + df1['EXEC_LNAME']

df1['NAME_EXEC']=df1['EXEC_FNAME'] + ' ' + df1['EXEC_LNAME']

#drop some columns
# df1.drop(['EXEC_FNAME', 'EXEC_MNAME','EXEC_LNAME'], axis = 1, inplace = True)
# df1.drop(['EXEC_FNAME', 'EXEC_MNAME','EXEC_LNAME'], axis = 1, inplace = True)

# #remove all blanks in a string
df1['NAME_EXEC'] = df1['NAME_EXEC'].str.replace(" ", "")
#remove all , in a string
df1['NAME_EXEC'] = df1['NAME_EXEC'].str.replace(",", "")
#remove all . in a string
df1['NAME_EXEC'] = df1['NAME_EXEC'].str.replace(".", "")
df1['NAME_EXEC'] = df1['NAME_EXEC'].str.upper()

#now work on the CONAME in execudata
df1['CONAME_EXEC']= df1['CONAME'].replace(['(CO)$', '(GROUP)$', '(INC)$', '(CORP)$', '(CORPORATION)$', '(COMPANY)$', '(COM)$',
                                      '(LTD)$', '(LLC)$', '(Ltd)$', '(L.L.C.)$' '(L.T.D.)$'],'', regex=True)

df1['CONAME_EXEC'] = df1['CONAME_EXEC'].str.replace(" ", "")
#remove all , in a string
df1['CONAME_EXEC'] = df1['CONAME_EXEC'].str.replace(",", "")
#remove all . in a string
df1['CONAME_EXEC'] = df1['CONAME_EXEC'].str.replace(".", "")
#remove all & in a string
df1['CONAME_EXEC'] = df1['CONAME_EXEC'].str.replace("&", "")
#remove all - in a string
df1['CONAME_EXEC'] = df1['CONAME_EXEC'].str.replace("-", "")
df1['CONAME_EXEC'] = df1['CONAME_EXEC'].str.upper()
###############################################################################
###############################################################################
###############################################################################

# individual contribution 2022 file, pick committe_id, name, employer, transaction date, amount. Figureo out these column names from year 2000 file, which is small
# to open. The reason to read only these 5 columns is that year 2020 file is too large to operate. 
# fec_df= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/indiv20/' + 'itcont' + '.txt', sep = '|', 
#                     header = None, skiprows=[20175605-1, 20194909-1], usecols = [0, 7, 11 ,13, 14])

# fec_df= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/indiv00/' + 'itcont' + '.txt', sep = '|', 
                      # header = None, skiprows=[], usecols = [0, 7, 11 ,13, 14])

fec_df= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/indiv00/' + 'itcont' + '.txt', sep = '|', 
                      header = None, skiprows=[])


# # use the following for year 2020. A row has some special characters, using latin as encoding
# fec_df= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/indiv10/' + 'itcont' + '.txt', sep = '|', 
#                       header = None, usecols = [0, 7, 11 ,13, 14], encoding='latin1')



# dfindivheader= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/' + 'indiv_header_file' + '.csv', usecols = [0, 7, 11 ,13, 14])
dfindivheader= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/' + 'indiv_header_file' + '.csv')


lst = dfindivheader.columns
fec_df.columns = lst

# # pick relevant columns
# fec_df = fec_df[['CMTE_ID', 'NAME', 'EMPLOYER', 'TRANSACTION_DT', 'TRANSACTION_AMT', 'CITY', 'STATE']]   

# take a subsample to try it out
# jk1 = fec_df.iloc[0:100000, :]
# jk1 = dfindiv.loc[:, :]
# jk1.sort_values(by = ['NAME'], ascending=True)

# selecting rows based on condition
fec_df = fec_df[fec_df['TRANSACTION_AMT'] > 0]

# jk1 = fec_df[fec_df['TRANSACTION_AMT'] > 200]


# # check something John Holmes, AEMS, looks like he has a lot of repititions. why?
# jk8 = fec_df[(fec_df['EMPLOYER'] == 'AEMS')]



fec_df.dropna(subset = ['TRANSACTION_DT'], inplace = True)      # Remove rows with NaN]



# check if name has , in it
fec_df['namehasstring'] = fec_df['NAME'].str.contains(',', regex=False)
# keep names that has , in it
fec_df = fec_df[fec_df['namehasstring'] == True]

fec_df.drop(['namehasstring'], axis = 1, inplace = True)

# pick the first string from the left, this is the last name
fec_df['NAMEL'] = fec_df['NAME'].apply(lambda x:str(x).split(',')[0])
# pick the second string from the left, this is the first name and other names
fec_df['NAMEO'] = fec_df['NAME'].apply(lambda x:str(x).split(',')[1])
# delete the leading blank space
fec_df['NAMEO'] = fec_df['NAMEO'].str.lstrip()

# # clean noises in data, FEC data, 
# # (MR.)$ specifies that the string MR. is at the end of the whole string, etc 
# # otherwise, it may delete string in the middle. Put III in front of II, otherwise a III will be deleted II and there is a I left.
# fec_df['NAMEO']= fec_df['NAMEO'].replace(['(MR.)$', '(MBA)$', '(PH.D.)$', '(CPA)$', '(MS.)$', '(JD)$', '(DR.)$' ,
#                                           '(MD)$', '(MR)$', '(MS)$', '(MRS)$', '(Adm)$' , '(Bri)$' , '(Cap)$' , '(Dr.)$' , 
#                                           '(Gen)$' , '(Gov)$' , '(Hon)$' , '(H.R)$' , '(Lie)$' 
#                                           , '(Mr.)$', '(Ms.)$', '(NAMEPREFIX)$', '(Pro)$', '(Sir)$', '(PhD)$', '(PHD)$', 
#                                           '(JR)$', '(JR.)$', '(III)$', '(II)$', '(IV)$', '(V)$', '(Jr.)$'
#                                           , '(Jr.)$' , '(Sr.)$', '(J.D.)$', '(Esq.)$', '(P.E.)$' , '(Ph.D.)$'],'', regex=True)

#fec_df['NAMEL'] = fec_df['NAME'].apply(lambda x:str(x).split(',')[0])
# combine first name/middlename etc + last name because the other data is firstname other name last name format
# pick the second string from the left, this is the first name and other names
fec_df['NAMEF'] = fec_df['NAMEO'].apply(lambda x:str(x).split(' ')[0])


fec_df['NAME_FEC']=fec_df['NAMEF'] + ' ' + fec_df['NAMEL']
# drop some columns
# fec_df.drop(['NAMEO', 'NAMEL', 'NAMEF', 'namehasstring'], axis = 1, inplace = True)
fec_df.drop(['NAMEO', 'NAMEF', 'NAMEL'], axis = 1, inplace = True)

# #remove all blanks in a string
fec_df['NAME_FEC'] = fec_df['NAME_FEC'].str.replace(" ", "")
#remove all , in a string
fec_df['NAME_FEC'] = fec_df['NAME_FEC'].str.replace(",", "")
#remove all . in a string
fec_df['NAME_FEC'] = fec_df['NAME_FEC'].str.replace(".", "")
fec_df['NAME_FEC'] = fec_df['NAME_FEC'].str.upper()


###############################################################################
###############################################################################
###############################################################################

wyear = 2000

# use the line below for each two years, prior to 2021
df1i = df1[(df1['YEAR'] == wyear)  | (df1['YEAR'] == wyear-1) ] 

# # use the next line for year 2021
# df1i = df1[(df1['YEAR'] == wyear)] 

# keep 
outmerge1 = df1i.merge(fec_df, how = "left", left_on = ['NAME_EXEC'], right_on = ['NAME_FEC'])
outmerge1 = outmerge1[['CMTE_ID', 'NAME', 'EMPLOYER', 'TRANSACTION_DT', 'TRANSACTION_AMT', 'CEOANN']]   

# outmerge1.to_csv('C:/Users/d_huang/Documents/PythonProjects/ESGDATA/' + 'individual' + '2021' + '.csv')
outmerge1.to_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/data/' + 'TOP5_' + '2000' + '.csv')











