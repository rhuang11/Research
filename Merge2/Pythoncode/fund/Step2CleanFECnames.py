import pandas as pd
import numpy as np

###############################################################################
path = './Merge2/CN/'
dfcna = pd.DataFrame() 
# pathname that will loop through, from file L0F0.rar prepared by Jing.
lst = ['2000', '2002', '2004', '2006', '2008', '2010', '2012', '2014', '2016', '2018', '2020']
#lst = ['2000', '2002']
for pathname in lst:
    # separation in the data is |, and do not read header becuase there is no header in the data
    dfcni= pd.read_csv(path + pathname + '/' + 'cn' + '.txt',sep = '|', header = None)
    # write a new column = candiate year using the pathname becuase the year in candiate file is misleading.
    dfcni['cnyear'] = int(pathname)
    # stack the DataFrames dfa to dfindiv using append(), assgin it back to the same name dfindiv so that 
    # it is updated before it is used for append in the next round
    dfcna = dfcna.append([dfcni], ignore_index=True)

dfcnheader= pd.read_csv('./Merge2/' + 'cn_header_file' + '.csv')
lst = list(dfcnheader.columns)
lst.append('CNYEAR')
dfcna.columns = lst
###############################################################################
# work on the CCL files. loop through all years in lst, folder used year as names
path = './Merge2/CCL/'
dfccla = pd.DataFrame() 
# pathname that will loop through, from file L0F0.rar prepared by Jing.
lst = ['2000', '2002', '2004', '2006', '2008', '2010', '2012', '2014', '2016', '2018', '2020', '2022']
#lst = ['2000']
for pathname in lst:
    # separation in the data is |, and do not read header becuase there is no header in the data
    dfccli= pd.read_csv(path + pathname + '/' + 'ccl' + '.txt',sep = '|', header = None)
    # stack the DataFrames dfa to dfindiv using append(), assgin it back to the same name dfindiv so that 
    # it is updated before it is used for append in the next round
    dfccla = dfccla.append([dfccli], ignore_index=True)

dfcclheader= pd.read_csv('./Merge2/' + 'ccl_header_file' + '.csv')
lst = dfcclheader.columns
dfccla.columns = lst
###############################################################################
# work on individual files
# pathname that will loop through, from file L0F0.rar prepared by Jing.
lst = ['2000', '2002', '2004', '2006', '2008', '2010', '2012', '2014', '2016', '2018', '2020']

# try one or two years in the line below. uncomment
lst = ['2008']
# common path that use will used for individual contribution. Other data specify explicitly
path = './Merge2/'
# individual donation file across years have the same file name
filename = 'indiv'
# defind an empty dataframe in pandas, use it to store each individual file
dfindiv = pd.DataFrame()

# loop through all years in lst, folder used year as names
for filename2 in lst:
    jk1 = str(filename2)[-2:]
    # separation in the data is |, and do not read header becuase there is no header in the data
    dfa= pd.read_csv(path + filename + jk1 + '/' + 'itcont' + filename2 + '.csv', header = None)
    # dfa= pd.read_csv(path + filename + jk1 + '/' + 'itcont' + filename2 + '.csv')
    dfa = dfa.iloc[1:, 1:]
    
    # stack the DataFrames dfa to dfindiv using append(), assgin it back to the same name dfindiv so that 
    # it is updated before it is used for append in the next round
    # dfindiv = dfindiv.append([dfa], ignore_index=True)

    # individual header    
    dfindivheader= pd.read_csv('./Merge2/' + 'indiv_header_file' + '.csv', 
                           usecols = [0, 7, 8, 9 , 10, 11 ,13, 14])
    lst = list(dfindivheader.columns)

    fec_df = dfa.loc[:, :]
    # # rename columns using lst
    fec_df.columns = lst

    # # selecting rows based on condition, no need to do it anymore since data is already processed in an earlier code.
    # jk.dropna(subset = ['TRANSACTION_AMT'], inplace = True)      # Remove rows with NaN
    # # convert string to numeric
    # jk['TRANSACTION_AMT'] = pd.to_numeric(jk['TRANSACTION_AMT'], errors='coerce')
    # fec_df = jk[jk['TRANSACTION_AMT'] > 200]
    # fec_df['TRANSACTION_DTBackup'] = fec_df['TRANSACTION_DT']

    # fec_df.dropna(subset = ['TRANSACTION_DT'], inplace = True)      # Remove rows with NaN]
    # parse out the years when contribution occurred
    fec_df['TRANSACTION_DT'] = fec_df['TRANSACTION_DT'].apply(str)
    # take the string to the left of . in date
    fec_df['TRANSACTION_DT'] = fec_df['TRANSACTION_DT'].apply(lambda x:str(x).split('.')[0])
    # take the last four digit to be year
    fec_df['TRANSACTION_DT'] = fec_df['TRANSACTION_DT'].str[-4:]
    # convert data from string to numeric
    if fec_df['TRANSACTION_DT'].dtype == str:
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
    # pick the second string from the left, this is the first name and other names
    fec_df['NAMEF'] = fec_df['NAMEO'].apply(lambda x:str(x).split(' ')[0])


    fec_df['NAME_FEC']=fec_df['NAMEF'] + ' ' + fec_df['NAMEL']
    # drop some columns
    # fec_df.drop(['NAMEO', 'NAMEL', 'NAMEF', 'namehasstring'], axis = 1, inplace = True)
    fec_df.drop(['NAMEO', 'namehasstring'], axis = 1, inplace = True)

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

    # drop duplicates for those donations to the same committee on the same day by the same person
    fec_df.drop_duplicates(subset=['NAME_FEC', 'EMPLOYER_FEC', 'CMTE_ID', 'TRANSACTION_DT', 'TRANSACTION_AMT'], keep='first', inplace=True)

    lst = fec_df.columns
    fec_df.dtypes
    fec_df['TRANSACTION_DT'] = fec_df['TRANSACTION_DT'].apply(str)
    fec_df['TRANSACTION_AMT'] = pd.to_numeric(fec_df['TRANSACTION_AMT'], errors='coerce')
    
    
    # # file is too large, no need to merge it. 
    # fec_df.to_csv('./Merge2/' + 'fecdonations0020' + '.csv')
   
    # compute political view for each person or each two years
    outmerge2 = fec_df.groupby(['TRANSACTION_DT','NAME_FEC','CITY', 'STATE', 'ZIP_CODE',
                                'EMPLOYER_FEC','CMTE_ID'])['TRANSACTION_AMT'].sum().reset_index()
    # drop duplicates
    outmerge2 = outmerge2.drop_duplicates(subset=['TRANSACTION_DT','NAME_FEC','CITY', 'STATE', 'ZIP_CODE',
                                'EMPLOYER_FEC','CMTE_ID'], keep='first')
    # check how many unique companies donated
    # outmerge3 = outmerge2.groupby(['YEAR','NAMEL','NAMEF','CONAME'])['TRANSACTION_AMT'].sum().reset_index()
   
    # pick years from 2000 to 2020
    dfccl = dfccla[dfccla['FEC_ELECTION_YR'] == int(filename2)]
    dfcn = dfcna[dfcna['CNYEAR'] == int(filename2)]
    # merge cn with ccl to pin down candidate's committee
    df_cnccl = pd.merge(dfcn, dfccl, how = "left", on = ["CAND_ID"])
    df_cnccl = df_cnccl[['CAND_NAME','CAND_PTY_AFFILIATION', 'CMTE_ID']]
    df_cnccl.dropna(subset = ['CMTE_ID'], inplace = True)      # Remove rows with NaN

    # let democratic take a value of 1 and republic take a value of 0, then select only dem/rep
    df_cnccl.loc[df_cnccl["CAND_PTY_AFFILIATION"] == "DEM", "CAND_PTY_AFFILIATION"] = 1
    df_cnccl.loc[df_cnccl["CAND_PTY_AFFILIATION"] == "REP", "CAND_PTY_AFFILIATION"] = 0
    df_cnccl = df_cnccl[(df_cnccl['CAND_PTY_AFFILIATION'] == 1) | (df_cnccl['CAND_PTY_AFFILIATION'] == 0)] 
   
    df_cnccl.drop_duplicates(subset=['CAND_NAME', 'CMTE_ID'], keep='first', inplace=True)

    # merge comittie and candidate informaton to the execucomp/fec data, outmerge 4 has ceo donation to multiple committees, in a year. each committee we know 
    # if it has democratic or republican candidate, CEO or other executive may have donated to other committees other than the candidate committee
    # so by merging with candate committee information, outmerge4 keeps only candidate committees that are in data outmerge2, which has all committees.
    # so outmerge4 is smaller than outmerge2. In a left merge, candidate name when merged on to outmerge2, is missing if it is other kinds of committee.
   
    outmerge4 = outmerge2.merge(df_cnccl, how = "left", left_on = ['CMTE_ID'], right_on = ['CMTE_ID'])
   
    # the next line reduces the sample. # Remove rows with NaN, keep donations that went to a candidate
    outmerge4.dropna(subset = ['CAND_NAME'], inplace = True)         
  
    # relable republican to be -1
    outmerge4.loc[outmerge4["CAND_PTY_AFFILIATION"] == 0, "CAND_PTY_AFFILIATION"] = -1
    # compute Democratic minus republica donation
    outmerge4['DMR'] = outmerge4['TRANSACTION_AMT'] * outmerge4['CAND_PTY_AFFILIATION'] 
    outmerge5a = outmerge4.groupby(['TRANSACTION_DT','NAME_FEC','CITY', 'STATE', 'ZIP_CODE',
                                'EMPLOYER_FEC','CMTE_ID'])['TRANSACTION_AMT'].sum().reset_index()
    outmerge5b = outmerge4.groupby(['TRANSACTION_DT','NAME_FEC','CITY', 'STATE', 'ZIP_CODE',
                                'EMPLOYER_FEC','CMTE_ID'])['DMR'].sum().reset_index()

    # DMR is difference between donation to D candidate and R candidates, Total_AMT is the sum of donation to D and R cnadidates
    outmerge5b['PoliticalView'] = outmerge5b['DMR'] / outmerge5a['TRANSACTION_AMT']  
    outmerge5b['Total_AMT'] = outmerge5a['TRANSACTION_AMT']
    
    outmerge5b['PoliticalView'] = pd.to_numeric(outmerge5b['PoliticalView'], errors='coerce')
    
    # outmerge5b.describe()
    # outmerge5b.dtypes
    
    dfindiv = dfindiv.append([outmerge5b], ignore_index=True)

outmerge5b.to_csv("./Merge2/Pythoncode/fund/outmerge5b.csv", index=False)

# use the code below to find matches in the political donation data. 


    # # find the name columns in the second dataset to merge with the name in the fist dataset. require exact merge
    # outmerge1 = df1i.merge(fec_df2, how = "left", left_on = ['YEAR', 'NAME_EXEC'], right_on = ['YEAR', 'NAME_FEC'])
    
    # # load a module that can compare distance and similarity of strings, ratcliff_obershelp 
    # import textdistance

    # T = len(outmerge1)
    # dfsim = pd.DataFrame()
    # tmp1 = outmerge1[['EMPLOYER_FEC','CONAME_EXEC']]

    # # loop through all rows in tmp1, which has companies names from two datasets
    # for i in range(0, T, 1):
    #     print(i)
    #     # pick the ith row
    #     tmp2 = tmp1.iloc[i, :]
    #     # pick the first element, first company name
    #     c0 = tmp2.iloc[0]
    #     #pick the second element, second company name
    #     c1 = tmp2.iloc[1]
    #     # if both names are missing, the isna sum equals 2
    #     c2 = pd.isna(c0) + pd.isna(c1)
    #     # compare string only when c2 = 0, so neither company name is missing.
    #     if c2 == 0:
    #         # Ratcliff Obershelp provides similariy score, from 0 to 1, with 1 being the highest.
    #         a    = textdistance.ratcliff_obershelp.normalized_similarity(c0, c1)
    #     else:
    #         a    = 0
    #     # score similarity score to dfsim. be careful with loc [usually use column names] and iloc [usually used numeric indexes]. 
    #     dfsim.loc[i,0] = a 

    # # assign dfsim to a new column in outmerge1 that is called similarity    
    # outmerge1['similarity'] = dfsim
    
    # cutoff = 0.75
    # # pick rows where company name similarity score is larger than 0.75
    # outmerge1 = outmerge1[outmerge1['similarity'] > cutoff]
        
    
    

