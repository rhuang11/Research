import pandas as pd
import numpy as np

# candidate 
# dfcn= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/cn18/' + 'cn' + '.txt', sep = '|', header = None)
# dfcnheader= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/' + 'cn_header_file' + '.csv')
# lst = dfcnheader.columns
# dfcn.columns = lst

# # candidate committee link
# dfccl= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/ccl18/' + 'ccl' + '.txt', sep = '|', header = None)
# dfcclheader= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/' + 'ccl_header_file' + '.csv')
# lst = dfcclheader.columns
# dfccl.columns = lst
###############################################################################
###############################################################################
###############################################################################

path = 'C:/Users/d_huang/Documents/PythonProjects/Execucompdata/CN/'
dfcna = pd.DataFrame() 
# pathname that will loop through, from file L0F0.rar prepared by Jing.
lst = ['2000', '2002', '2004', '2006', '2008', '2010', '2012', '2014', '2016', '2018', '2020', '2022']
# lst = ['2000', '2002']
for pathname in lst:
    # separation in the data is |, and do not read header becuase there is no header in the data
    dfcni= pd.read_csv(path + pathname + '/' + 'cn' + '.txt',sep = '|', header = None)
    # write a new column = candiate year using the pathname becuase the year in candiate file is misleading.
    dfcni['cnyear'] = int(pathname)
    # stack the DataFrames dfa to dfindiv using append(), assgin it back to the same name dfindiv so that 
    # it is updated before it is used for append in the next round
    dfcna = dfcna.append([dfcni], ignore_index=True)

dfcnheader= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/' + 'cn_header_file' + '.csv')
lst = list(dfcnheader.columns)
lst.append('CNYEAR')
dfcna.columns = lst
###############################################################################
###############################################################################
###############################################################################

# work on the CCL files. loop through all years in lst, folder used year as names
path = 'C:/Users/d_huang/Documents/PythonProjects/Execucompdata/CCL/'
dfccla = pd.DataFrame() 
# pathname that will loop through, from file L0F0.rar prepared by Jing.
lst = ['2000', '2002', '2004', '2006', '2008', '2010', '2012', '2014', '2016', '2018', '2020', '2022']
# lst = ['2000']
for pathname in lst:
    # separation in the data is |, and do not read header becuase there is no header in the data
    dfccli= pd.read_csv(path + pathname + '/' + 'ccl' + '.txt',sep = '|', header = None)
    # stack the DataFrames dfa to dfindiv using append(), assgin it back to the same name dfindiv so that 
    # it is updated before it is used for append in the next round
    dfccla = dfccla.append([dfccli], ignore_index=True)

dfcclheader= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/' + 'ccl_header_file' + '.csv')
lst = dfcclheader.columns
dfccla.columns = lst
###############################################################################
###############################################################################
###############################################################################

# work on individual files
# pathname that will loop through, from file L0F0.rar prepared by Jing.
lst = ['2000', '2002', '2004', '2006', '2008', '2010', '2012', '2014', '2016', '2018', '2020', '2022']
# try one or two years in the line below. uncomment
# lst = ['1992', '1994']
# common path that use will used for individual contribution. Other data specify explicitly
path = 'C:/Users/d_huang/Documents/PythonProjects/Execucompdata/L0F0/'
# individual donation file across years have the same file name
filename = 'itcont_L0F0'
# defind an empty dataframe in pandas, use it to store each individual file
dfindiv = pd.DataFrame()

# loop through all years in lst, folder used year as names
for pathname in lst:
    # separation in the data is |, and do not read header becuase there is no header in the data
    dfa= pd.read_csv(path + pathname + '/' + filename + '.txt',sep = '|', header = None)
    # stack the DataFrames dfa to dfindiv using append(), assgin it back to the same name dfindiv so that 
    # it is updated before it is used for append in the next round
    dfindiv = dfindiv.append([dfa], ignore_index=True)

# individual header    
dfindivheader= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/' + 'indiv_header_file' + '.csv')
lst = dfindivheader.columns
# pick the first 100000 rows and all columns
# jk = dfindiv.loc[1:100000, :]

jk = dfindiv.loc[:, :]

# rename columns using lst
jk.columns = lst
# jk1 = jk[['CMTE_ID', 'NAME' ,'ZIP_CODE', 'EMPLOYER', 'OCCUPATION', 'TRANSACTION_DT', 'TRANSACTION_AMT']]
# pick relevant columns
jk1 = jk[['CMTE_ID', 'NAME', 'EMPLOYER', 'TRANSACTION_DT', 'TRANSACTION_AMT']]    

# selecting rows based on condition
fec_df = jk1[jk1['TRANSACTION_AMT'] > 200]
fec_df.dropna(subset = ['TRANSACTION_DT'], inplace = True)      # Remove rows with NaN]
# parse out the years when contribution occurred
fec_df['TRANSACTION_DT'] = fec_df['TRANSACTION_DT'].apply(str)
# take the string to the left of . in date
fec_df['TRANSACTION_DT'] = fec_df['TRANSACTION_DT'].apply(lambda x:str(x).split('.')[0])
# take the last four digit to be year
fec_df['TRANSACTION_DT'] = fec_df['TRANSACTION_DT'].str[-4:]
# convert data from string to numeric
fec_df['TRANSACTION_DT'] = fec_df['TRANSACTION_DT'].astype(int)


# check if name has , in it
fec_df['namehasstring'] = fec_df['NAME'].str.contains(',', regex=False)
# keep names that has , in it
fec_df = fec_df[fec_df['namehasstring'] == True]

# pick the first string from the left, this is the last name
fec_df['NAMEL'] = fec_df['NAME'].apply(lambda x:str(x).split(',')[0])
# pick the second string from the left, this is the first name and other names
fec_df['NAMEO'] = fec_df['NAME'].apply(lambda x:str(x).split(',')[1])
# delete the leading blank space
fec_df['NAMEO'] = fec_df['NAMEO'].str.lstrip()

# clean noises in data, FEC data, 
# (MR.)$ specifies that the string MR. is at the end of the whole string, etc 
# otherwise, it may delete string in the middle. Put III in front of II, otherwise a III will be deleted II and there is a I left.
fec_df['NAMEO']= fec_df['NAMEO'].replace(['(MR.)$', '(MBA)$', '(PH.D.)$', '(CPA)$', '(MS.)$', '(JD)$', '(DR.)$' ,
                                          '(MD)$', '(MR)$', '(MS)$', '(MRS)$', '(Adm)$' , '(Bri)$' , '(Cap)$' , '(Dr.)$' , 
                                          '(Gen)$' , '(Gov)$' , '(Hon)$' , '(H.R)$' , '(Lie)$' 
                                          , '(Mr.)$', '(Ms.)$', '(NAMEPREFIX)$', '(Pro)$', '(Sir)$', '(PhD)$', '(PHD)$', 
                                          '(JR)$', '(JR.)$', '(III)$', '(II)$', '(IV)$', '(V)$', '(Jr.)$'
                                          , '(Jr.)$' , '(Sr.)$', '(J.D.)$', '(Esq.)$', '(P.E.)$' , '(Ph.D.)$'],'', regex=True)

#fec_df['NAMEL'] = fec_df['NAME'].apply(lambda x:str(x).split(',')[0])
# combine first name/middlename etc + last name because the other data is firstname other name last name format
fec_df['NAME_FEC']=fec_df['NAMEO'] + ' ' + fec_df['NAMEL']
# drop some columns
fec_df.drop(['NAMEO', 'NAMEL', 'namehasstring'], axis = 1, inplace = True)

# #remove all blanks in a string
fec_df['NAME_FEC'] = fec_df['NAME_FEC'].str.replace(" ", "")
#remove all , in a string
fec_df['NAME_FEC'] = fec_df['NAME_FEC'].str.replace(",", "")
#remove all . in a string
fec_df['NAME_FEC'] = fec_df['NAME_FEC'].str.replace(".", "")
fec_df['NAME_FEC'] = fec_df['NAME_FEC'].str.upper()

# now work on the company names in FEC data
fec_df['EMPLOYER_FEC']= fec_df['EMPLOYER'].replace(['(CO)$', '(GROUP)$', '(INC)$', '(CORP)$', '(CORPORATION)$', '(COMPANY)$', '(COM)$',
                                                '(LTD)$', '(LLC)$', '(Ltd)$', '(L.L.C.)$' '(L.T.D.)$'],'', regex=True)
fec_df['EMPLOYER_FEC'] = fec_df['EMPLOYER_FEC'].str.replace(" ", "")
#remove all , in a string
fec_df['EMPLOYER_FEC'] = fec_df['EMPLOYER_FEC'].str.replace(",", "")
#remove all . in a string
fec_df['EMPLOYER_FEC'] = fec_df['EMPLOYER_FEC'].str.replace(".", "")
#remove all & in a string
fec_df['EMPLOYER_FEC'] = fec_df['EMPLOYER_FEC'].str.replace("&", "")
#remove all - in a string
fec_df['EMPLOYER_FEC'] = fec_df['EMPLOYER_FEC'].str.replace("-", "")
fec_df['EMPLOYER_FEC'] = fec_df['EMPLOYER_FEC'].str.upper()
###############################################################################
###############################################################################
###############################################################################

# work on execucomp data
# df0= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/' + 'ExecuComp' + '.csv')
# df0 = pd.read_sas('C:/Users/d_huang/Documents/PythonProjects/ESGDATA/compuexec.sas7bdat',encoding = 'ISO-8859-1')
# pick the row ceoindicator = ceo.
# df = df0[(df0['CEOANN'] == 'CEO')]

# # the CEO data is processed in SAS by combining execucomp and compustat becuase of the issue of the fiscal years used in execucomp
df= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/' + 'CEO' + '.csv')
df.rename(columns={"year": "YEAR"}, inplace=True)
df1= df[['EXEC_FULLNAME', 'CONAME', 'YEAR', 'EXEC_LNAME', 'EXEC_FNAME' ,'EXEC_MNAME', 'GVKEY']]
# df.to_csv('C:/Users/d_huang/Documents/PythonProjects/ESGDATA/' + 'CEO' + '.csv')
# df0.to_csv('C:/Users/d_huang/Documents/PythonProjects/ESGDATA/' + 'TOP5' + '.csv')


# clean noises in data, execucomp data
df1['EXEC_LNAME']= df1['EXEC_LNAME'].replace(['(MR.)$', '(MBA)$', '(PH.D.)$', '(CPA)$', '(MS.)$', '(JD)$', '(DR.)$' ,
                                          '(MD)$', '(MR)$', '(MS)$', '(MRS)$', '(Adm)$' , '(Bri)$' , '(Cap)$' , '(Dr.)$' , 
                                          '(Gen)$' , '(Gov)$' , '(Hon)$' , '(H.R)$' , '(Lie)$' 
                                          , '(Mr.)$', '(Ms.)$', '(NAMEPREFIX)$', '(Pro)$', '(Sir)$', '(PhD)$', '(PHD)$', 
                                          '(JR)$', '(JR.)$', '(III)$', '(II)$', '(IV)$', '(V)$', '(Jr.)$'
                                          , '(Jr.)$' , '(Sr.)$', '(J.D.)$', '(Esq.)$', '(P.E.)$' , '(Ph.D.)$'],'', regex=True)

df1['NAME_EXEC']=df1['EXEC_FNAME'] + ' ' +  df1['EXEC_MNAME'] + ' ' + df1['EXEC_LNAME']
#drop some columns
df1.drop(['EXEC_FNAME', 'EXEC_MNAME','EXEC_LNAME'], axis = 1, inplace = True)
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

# now loop through all years and save data to outmerge4a recursively. 
outmerge4a = pd.DataFrame()

for wyear in range(2000, 2021, 2): 
    print(wyear)
    # pick relevant year from cn and ccl files
    dfccl = dfccla[dfccla['FEC_ELECTION_YR'] == wyear]
    dfcn = dfcna[dfcna['CNYEAR'] == wyear]
    # pick relevant years from execucomp, election cycle is two years, so for fec and excucomp data pick two years each time, 
    # for instance, pick 2001 and 2002 , or pick 2003 and 2004 etc.
    df1i = df1[(df1['YEAR'] == wyear) | (df1['YEAR'] == wyear - 1)]
    # selecting rows based on condition, in fec, select a particular year from fec data
    fec_df2 = fec_df[(fec_df['TRANSACTION_DT'] == wyear) | (fec_df['TRANSACTION_DT'] == wyear - 1)]

    fec_df2.rename(columns={"TRANSACTION_DT": "YEAR"}, inplace=True)

    # # find the name columns in the second dataset to merge with the name in the fist dataset. require exact merge
    outmerge1 = df1i.merge(fec_df2, how = "left", left_on = ['YEAR', 'NAME_EXEC'], right_on = ['YEAR', 'NAME_FEC'])

    # load a module that can compare distance and similarity of strings, ratcliff_obershelp 
    import textdistance

    T = len(outmerge1)
    dfsim = pd.DataFrame()
    tmp1 = outmerge1[['EMPLOYER_FEC','CONAME_EXEC']]

    # loop through all rows in tmp1, which has companies names from two datasets
    for i in range(0, T, 1):
        print(i)
        # pick the ith row
        tmp2 = tmp1.iloc[i, :]
        # pick the first element, first company name
        c0 = tmp2.iloc[0]
        #pick the second element, second company name
        c1 = tmp2.iloc[1]
        # if both names are missing, the isna sum equals 2
        c2 = pd.isna(c0) + pd.isna(c1)
        # compare string only when c2 = 0, so neither company name is missing.
        if c2 == 0:
            # Ratcliff Obershelp provides similariy score, from 0 to 1, with 1 being the highest.
            a    = textdistance.ratcliff_obershelp.normalized_similarity(c0, c1)
        else:
            a    = 0
        # score similarity score to dfsim. be careful with loc [usually use column names] and iloc [usually used numeric indexes]. 
        dfsim.loc[i,0] = a 

    # assign dfsim to a new column in outmerge1 that is called similarity    
    outmerge1['similarity'] = dfsim
    
    cutoff = 0.75
    # pick rows where company name similarity score is larger than 0.75
    outmerge1 = outmerge1[outmerge1['similarity'] > cutoff]

    # a = textdistance.hamming.normalized_similarity('test', 'te0tbv')
    # textdistance.ratcliff_obershelp.normalized_similarity('test', 'te0tbv')

    # sum donation to the same committee
    outmerge2 = outmerge1.groupby(['YEAR','NAME', 'NAME_EXEC', 'CONAME', 'CONAME_EXEC', 'GVKEY', 'CMTE_ID'])['TRANSACTION_AMT'].sum().reset_index()
    # drop duplicates
    outmerge2 = outmerge2.drop_duplicates(subset=['YEAR', 'NAME_EXEC', 'CONAME_EXEC', 'CMTE_ID'], keep='first')
    # check how many unique companies donated
    outmerge3 = outmerge2.groupby(['YEAR','NAME', 'CONAME'])['TRANSACTION_AMT'].sum().reset_index()

    # merge cn with ccl to pin down candidate's committee
    df_cnccl = pd.merge(dfcn, dfccl, how = "left", on = ["CAND_ID"])
    df_cnccl = df_cnccl[['CAND_NAME','CAND_PTY_AFFILIATION', 'CMTE_ID']]
    df_cnccl.dropna(subset = ['CMTE_ID'], inplace = True)      # Remove rows with NaN

    # let democratic take a value of 1 and republic take a value of 0, then select only dem/rep
    df_cnccl.loc[df_cnccl["CAND_PTY_AFFILIATION"] == "DEM", "CAND_PTY_AFFILIATION"] = 1
    df_cnccl.loc[df_cnccl["CAND_PTY_AFFILIATION"] == "REP", "CAND_PTY_AFFILIATION"] = 0
    df_cnccl = df_cnccl[(df_cnccl['CAND_PTY_AFFILIATION'] == 1) | (df_cnccl['CAND_PTY_AFFILIATION'] == 0)] 

    # merge comittie and candidate informaton to the execucomp/fec data, outmerge 4 has ceo donation to multiple committees, in a year. each committee we know 
    # if it has democratic or republican candidate
    outmerge4 = outmerge2.merge(df_cnccl, how = "left", left_on = ['CMTE_ID'], right_on = ['CMTE_ID'])
    outmerge4.dropna(subset = ['CAND_NAME'], inplace = True)      # Remove rows with NaN

    # how many CEOs donated and total amount each CEO donated 
    # outmerge5 = outmerge4.groupby(['YEAR','NAME_EXEC', 'CONAME_EXEC'])['TRANSACTION_AMT'].sum().reset_index()
    outmerge4a = outmerge4a.append([outmerge4], ignore_index=True)

outmerge4a.loc[outmerge4a["CAND_PTY_AFFILIATION"] == 0, "CAND_PTY_AFFILIATION"] = -1

outmerge4a['DMR'] = outmerge4a['TRANSACTION_AMT'] * outmerge4a['CAND_PTY_AFFILIATION'] 
outmerge5a = outmerge4a.groupby(['YEAR','NAME_EXEC', 'CONAME_EXEC', 'GVKEY'])['TRANSACTION_AMT'].sum().reset_index()
outmerge5b = outmerge4a.groupby(['YEAR','NAME_EXEC', 'CONAME_EXEC', 'GVKEY'])['DMR'].sum().reset_index()

# DMR is difference between donation to D candidate and R candidates, Total_AMT is the sum of donation to D and R cnadidates
outmerge5b['PoliticalView'] = outmerge5b['DMR'] / outmerge5a['TRANSACTION_AMT']  
outmerge5b['Total_AMT'] = outmerge5a['TRANSACTION_AMT']


jk1 =  outmerge5b[(outmerge5b['YEAR'] == 2018)]



# do it separately for year 2021 
outmerge4a = pd.DataFrame()

for wyear in range(2021, 2022, 1): 
    print(wyear)
    # pick relevant year from cn and ccl files
    dfccl = dfccla[dfccla['FEC_ELECTION_YR'] == wyear+1]
    dfcn = dfcna[dfcna['CNYEAR'] == wyear+1]
    # pick relevant years from execucomp, election cycle is two years, so for fec and excucomp data pick two years each time, 
    # for instance, pick 2001 and 2002 , or pick 2003 and 2004 etc.
    df1i = df1[(df1['YEAR'] == wyear)]
    # selecting rows based on condition, in fec, select a particular year from fec data
    fec_df2 = fec_df[(fec_df['TRANSACTION_DT'] == wyear)]

    fec_df2.rename(columns={"TRANSACTION_DT": "YEAR"}, inplace=True)

    # # find the name columns in the second dataset to merge with the name in the fist dataset. require exact merge
    outmerge1 = df1i.merge(fec_df2, how = "left", left_on = ['YEAR', 'NAME_EXEC'], right_on = ['YEAR', 'NAME_FEC'])

    # load a module that can compare distance and similarity of strings, ratcliff_obershelp 
    import textdistance

    T = len(outmerge1)
    dfsim = pd.DataFrame()
    tmp1 = outmerge1[['EMPLOYER_FEC','CONAME_EXEC']]

    # loop through all rows in tmp1, which has companies names from two datasets
    for i in range(0, T, 1):
        print(i)
        # pick the ith row
        tmp2 = tmp1.iloc[i, :]
        # pick the first element, first company name
        c0 = tmp2.iloc[0]
        #pick the second element, second company name
        c1 = tmp2.iloc[1]
        # if both names are missing, the isna sum equals 2
        c2 = pd.isna(c0) + pd.isna(c1)
        # compare string only when c2 = 0, so neither company name is missing.
        if c2 == 0:
            # Ratcliff Obershelp provides similariy score, from 0 to 1, with 1 being the highest.
            a    = textdistance.ratcliff_obershelp.normalized_similarity(c0, c1)
        else:
            a    = 0
        # score similarity score to dfsim. be careful with loc [usually use column names] and iloc [usually used numeric indexes]. 
        dfsim.loc[i,0] = a 

    # assign dfsim to a new column in outmerge1 that is called similarity    
    outmerge1['similarity'] = dfsim
    
    cutoff = 0.75
    # pick rows where company name similarity score is larger than 0.75
    outmerge1 = outmerge1[outmerge1['similarity'] > cutoff]

    # a = textdistance.hamming.normalized_similarity('test', 'te0tbv')
    # textdistance.ratcliff_obershelp.normalized_similarity('test', 'te0tbv')

    # sum donation to the same committee
    outmerge2 = outmerge1.groupby(['YEAR','NAME', 'NAME_EXEC', 'CONAME', 'CONAME_EXEC', 'GVKEY', 'CMTE_ID'])['TRANSACTION_AMT'].sum().reset_index()
    # drop duplicates
    outmerge2 = outmerge2.drop_duplicates(subset=['YEAR', 'NAME_EXEC', 'CONAME_EXEC', 'CMTE_ID'], keep='first')
    # check how many unique companies donated
    outmerge3 = outmerge2.groupby(['YEAR','NAME', 'CONAME'])['TRANSACTION_AMT'].sum().reset_index()

    # merge cn with ccl to pin down candidate's committee
    df_cnccl = pd.merge(dfcn, dfccl, how = "left", on = ["CAND_ID"])
    df_cnccl = df_cnccl[['CAND_NAME','CAND_PTY_AFFILIATION', 'CMTE_ID']]
    df_cnccl.dropna(subset = ['CMTE_ID'], inplace = True)      # Remove rows with NaN

    # let democratic take a value of 1 and republic take a value of 0, then select only dem/rep
    df_cnccl.loc[df_cnccl["CAND_PTY_AFFILIATION"] == "DEM", "CAND_PTY_AFFILIATION"] = 1
    df_cnccl.loc[df_cnccl["CAND_PTY_AFFILIATION"] == "REP", "CAND_PTY_AFFILIATION"] = 0
    df_cnccl = df_cnccl[(df_cnccl['CAND_PTY_AFFILIATION'] == 1) | (df_cnccl['CAND_PTY_AFFILIATION'] == 0)] 

    # merge comittie and candidate informaton to the execucomp/fec data, outmerge 4 has ceo donation to multiple committees, in a year. each committee we know 
    # if it has democratic or republican candidate
    outmerge4 = outmerge2.merge(df_cnccl, how = "left", left_on = ['CMTE_ID'], right_on = ['CMTE_ID'])
    outmerge4.dropna(subset = ['CAND_NAME'], inplace = True)      # Remove rows with NaN

    # how many CEOs donated and total amount each CEO donated 
    # outmerge5 = outmerge4.groupby(['YEAR','NAME_EXEC', 'CONAME_EXEC'])['TRANSACTION_AMT'].sum().reset_index()
    outmerge4a = outmerge4a.append([outmerge4], ignore_index=True)

outmerge4a.loc[outmerge4a["CAND_PTY_AFFILIATION"] == 0, "CAND_PTY_AFFILIATION"] = -1

outmerge4a['DMR'] = outmerge4a['TRANSACTION_AMT'] * outmerge4a['CAND_PTY_AFFILIATION'] 
outmerge6a = outmerge4a.groupby(['YEAR','NAME_EXEC', 'CONAME_EXEC', 'GVKEY'])['TRANSACTION_AMT'].sum().reset_index()
outmerge6b = outmerge4a.groupby(['YEAR','NAME_EXEC', 'CONAME_EXEC', 'GVKEY'])['DMR'].sum().reset_index()

# DMR is difference between donation to D candidate and R candidates, Total_AMT is the sum of donation to D and R cnadidates
outmerge6b['PoliticalView'] = outmerge5b['DMR'] / outmerge5a['TRANSACTION_AMT']  
outmerge6b['Total_AMT'] = outmerge5a['TRANSACTION_AMT']

outmerge5b = outmerge5b.append([outmerge6b], ignore_index=True)














