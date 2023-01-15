import pandas as pd
import numpy as np

# individual contribution 2022 file, pick committe_id, name, employer, transaction date, amount. Figureo out these column names from year 2000 file, which is small
# to open. The reason to read only these 5 columns is that year 2020 file is too large to operate. 

# use the next two blocks for year 2020.
# fec_df= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/indiv20/' + 'itcont' + '.txt', sep = '|', 
#                      header = None, skiprows=[20175605-1, 20194909-1], usecols = [0, 7, 8 ,9,10,11 ,13, 14])
# dfindivheader= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/' + 'indiv_header_file' + '.csv', 
#                            usecols = [0, 7, 8,9,10,11 ,13, 14])

# use the following blocks for other years, 2010 has some latin words so do it separately.
# change indiv00 to indiv02, indiv04 .... indiv18 etc.
fec_df= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/indiv00/' + 'itcont' + '.txt', sep = '|', 
                       header = None, skiprows=[])

# # use the following for year 2010. A row has some special characters, using latin as encoding
# fec_df= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/indiv10/' + 'itcont' + '.txt', sep = '|', 
#                        header = None, encoding='latin1')

dfindivheader= pd.read_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/' + 'indiv_header_file' + '.csv')

lst = dfindivheader.columns
fec_df.columns = lst

# # pick relevant columns
fec_df = fec_df[['CMTE_ID', 'NAME', 'CITY', 'STATE', 'ZIP_CODE', 'EMPLOYER', 'TRANSACTION_DT', 'TRANSACTION_AMT']]   

# take a subsample to try it out
# jk1 = fec_df.iloc[0:100000, :]
# jk1 = dfindiv.loc[:, :]
# jk1.sort_values(by = ['NAME'], ascending=True)
# fec_df2 = jk1[jk1['TRANSACTION_AMT'] > 200]

# selecting rows based on condition
fec_df.dropna(subset = ['TRANSACTION_DT'], inplace = True)      # Remove rows with NaN]
#fec_df.dropna(subset = ['TRANSACTION_AMT'], inplace = True)      # Remove rows with NaN
# convert string to numeric, somehow there are strings in 2020 donations
fec_df['TRANSACTION_AMT'] = pd.to_numeric(fec_df['TRANSACTION_AMT'], errors='coerce')
fec_df = fec_df[fec_df['TRANSACTION_AMT'] > 200]

# save each processed file. Original data is too large and I have them in dropbox. Needs to change years in two places before save.
fec_df.to_csv('C:/Users/d_huang/Documents/PythonProjects/Execucompdata/indiv20/' + 'itcont' + '2020' + '.csv')



