"""Merging people with outmerge."""
import pandas as pd
import time

start_time = time.time()
#read the data from the two files with specific encoding
people_data = pd.read_csv("./Merge1/merged_file_with_duplicates.csv")
#test  people_data = pd.read_csv("./MergeData/Merge1/merge.csv")
#test  outmerge_data = pd.read_csv("./MergeData/Merge2/Pythoncode/fund/outmerge5b.csv")
outmerge_data = pd.read_csv("./Merge2/Pythoncode/fund/outmerge5b.csv")

#separates the first name and middle initial which is typically one space from the 'First" column and makes middle into new column, example: "John A." becomes "John" and "A"
people_data['First'], people_data['Middle'] = people_data['First'].str.split(' ', 1).str  # type: ignore

#removes any periods from the middle initial, example: "A." becomes "A"
people_data['Middle'] = people_data['Middle'].str.replace('.', '')  # type: ignore

#combines the first name, middle initial, and last name into one column capitalized named 'NAME_FEC', example: "John A. Smith" becomes "JOHNSMITHA"
people_data['NAME_FEC'] = people_data['First'] + people_data['Last']

#adds middle initial to the end of 'NAME_FEC' if it exists, example: "JOHNSMITHA" becomes "JOHNSMITHAA"
people_data['NAME_FEC'] = people_data['NAME_FEC'] + people_data['Middle'].fillna('')  # type: ignore

#capitalizes the 'NAME_FEC' column, example: "JOHNSMITHAA" becomes "JOHNSMITHAA"        
people_data['NAME_FEC'] = people_data['NAME_FEC'].str.upper()  # type: ignore

#removes any strange suffixes or prefixes from the 'NAME_FEC' column'
people_data['NAME_FEC'] = people_data['NAME_FEC'].replace(['(MR.)$', '(MBA)$', '(PH.D.)$', '(CPA)$', '(MS.)$', '(JD)$', '(DR.)$' ,
                                          '(MD)$', '(MR)$', '(MS)$', '(MRS)$', '(Adm)$' , '(Bri)$' , '(Cap)$' , '(Dr.)$' , 
                                          '(Gen)$' , '(Gov)$' , '(Hon)$' , '(H.R)$' , '(Lie)$' 
                                          , '(Mr.)$', '(Ms.)$', '(NAMEPREFIX)$', '(Pro)$', '(Sir)$', '(PhD)$', '(PHD)$', 
                                          '(JR)$', '(JR.)$', '(III)$', '(II)$', '(IV)$', '(V)$', '(Jr.)$'
                                          , '(Jr.)$' , '(Sr.)$', '(J.D.)$', '(Esq.)$', '(P.E.)$' , '(Ph.D.)$'],'', regex=True)

#people_data['NAME_FEC_final'] = people_data['NAME_FEC']

#removes spaces from the 'Company Name' column, example: Falcon Point Capital LLC becomes FALCONPOINTCAPITALLLC
people_data['EMPLOYER_FEC'] = people_data['CompanyName'].str.replace(' ', '')  # type: ignore

#removes any strange suffixes or prefixes from the 'EMPLOYER_FEC' column, example: FALCONPOINTCAPITALLLC becomes FALCONPOINTCAPITAL'
people_data['EMPLOYER_FEC'] = people_data['EMPLOYER_FEC'].replace(['(LLC)$', '(LP)$', '(L.P.)$', '(L.L.C.)$', '(L.P)$', '(L.L.C)$', '(LP.)$', '(LLC.)$', '(LLP)$', '(LLP.)$', '(LLP)$', '(LLP.)$', '(LLC)$', '(LLC.)$', '(LTD)$', '(LTD.)$', '(LTD)$', '(LTD.)$', '(INC)$', '(INC.)$', '(INC)$', '(INC.)$', '(CORP)$', '(CORP.)$', '(CORP)$', '(CORP.)$', '(CO)$', '(CO.)$', '(CO)$', '(CO.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANY)$', '(COMPANY.)$', '(CORPORATION)$', '(CORPORATION.)$', '(CORPORATION)$', '(CORPORATION.)$', '(CORP)$', '(CORP.)$', '(CORP)$', '(CORP.)$', '(COMP)$', '(COMP.)$', '(COMP)$', '(COMP.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANY)$', '(COMPANY.)$', '(COMP)]$'], '', regex=True)
outmerge_data['EMPLOYER_FEC'] = outmerge_data['EMPLOYER_FEC'].replace(['(LLC)$', '(LP)$', '(L.P.)$', '(L.L.C.)$', '(L.P)$', '(L.L.C)$', '(LP.)$', '(LLC.)$', '(LLP)$', '(LLP.)$', '(LLP)$', '(LLP.)$', '(LLC)$', '(LLC.)$', '(LTD)$', '(LTD.)$', '(LTD)$', '(LTD.)$', '(INC)$', '(INC.)$', '(INC)$', '(INC.)$', '(CORP)$', '(CORP.)$', '(CORP)$', '(CORP.)$', '(CO)$', '(CO.)$', '(CO)$', '(CO.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANY)$', '(COMPANY.)$', '(CORPORATION)$', '(CORPORATION.)$', '(CORPORATION)$', '(CORPORATION.)$', '(CORP)$', '(CORP.)$', '(CORP)$', '(CORP.)$', '(COMP)$', '(COMP.)$', '(COMP)$', '(COMP.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANY)$', '(COMPANY.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANIES)$', '(COMPANIES.)$', '(COMPANY)$', '(COMPANY.)$', '(COMP)]$'], '', regex=True)


people_data['EMPLOYER_FEC_final'] = people_data['EMPLOYER_FEC'].str.upper()  # type: ignore

#people_data.drop('NAME_FEC', axis=1, inplace=True)
people_data.drop('EMPLOYER_FEC', axis=1, inplace=True)

end_time = time.time()
print("Step 1 took: ", end_time - start_time, " seconds.")


#merging the data on 'NAME_FEC' column that are exact matches with name as well as company name
#merged_data = pd.merge(people_data, outmerge_data, on=['NAME_FEC', 'EMPLOYER_FEC'], how='left')
merged_data = pd.merge(people_data, outmerge_data, on=['NAME_FEC'], how='left')

#saving the merged data in the new file
merged_data.to_csv("./Merge2/Pythoncode/fund/merged_file.csv", index=False)

#merging the data on 'NAME_FEC' column that are close matches but not exact matches
#outmerge1 = people_data.merge(outmerge_data, how = "left", left_on = ['EMPLOYER_FEC'], right_on = outmerge_data['EMPLOYER_FEC'])
#print(outmerge1)

# load a module that can compare distance and similarity of strings, ratcliff_obershelp 


import textdistance

'''## For people names
merged_data2 = pd.concat([people_data, outmerge_data], axis=1)
T = len(outmerge_data['NAME_FEC'])
dfsim = pd.DataFrame()

tmp1 = merged_data2[['NAME_FEC_final','NAME_FEC']]

# loop through all rows in tmp1, which has names from two datasets
for i in range(0, T, 1):
    #print(i)
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
        a = textdistance.ratcliff_obershelp.normalized_similarity(c0, c1)
    else:
        a = 0
    # score similarity score to dfsim. be careful with loc [usually use column names] and iloc [usually used numeric indexes]. 
    dfsim.loc[i,0] = a 

# assign dfsim to a new column in outmerge1 that is called similarity    
merged_data2['similarity_names'] = dfsim
print(merged_data2)

cutoff = 0.75
# pick rows where company name similarity score is larger than 0.75
outmerge1 = merged_data2[merged_data2['similarity_names'] > cutoff] 

end_time = time.time()
print("Step 2 took: ", end_time - start_time, " seconds.")
'''

## For company names

#outmerge1['EMPLOYER_FEC_x'] = outmerge_data['EMPLOYER_FEC']


U = len(merged_data['EMPLOYER_FEC'])
dfsim2 = pd.DataFrame()
tmp3 = merged_data[['EMPLOYER_FEC_final','EMPLOYER_FEC']]

# loop through all rows in tmp1, which has companies names from two datasets
for k in range(0, U, 1):
    start_time = time.time()
    #print(i)
    # pick the ith row
    tmp4 = tmp3.iloc[k, :]
    # pick the first element, first company name
    d0 = tmp4.iloc[0]
    #pick the second element, second company name
    d1 = tmp4.iloc[1]
    # if both names are missing, the isna sum equals 2
    d2 = pd.isna(d0) + pd.isna(d1)
    # compare string only when c2 = 0, so neither company name is missing.
    if d2 == 0:
        # Ratcliff Obershelp provides similariy score, from 0 to 1, with 1 being the highest.
        b = textdistance.ratcliff_obershelp.normalized_similarity(d0, d1)
    else:
        b = 0
    # score similarity score to dfsim. be careful with loc [usually use column names] and iloc [usually used numeric indexes]. 
    dfsim2.loc[k,0] = b 

    end_time = time.time()
    print(f"Step {k} took: ", end_time - start_time, " seconds.")

# assign dfsim to a new column in outmerge1 that is called similarity    
merged_data['similarity_company'] = dfsim2

cutoff = 0.75
# pick rows where company name similarity score is larger than 0.75
outmerge2 = merged_data[merged_data['similarity_company'] > cutoff] 

outmerge2.to_csv("./Merge2/Pythoncode/fund/final_merge.csv", index=False) 

