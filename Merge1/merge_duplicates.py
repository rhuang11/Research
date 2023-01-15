import pandas as pd

#read the data from the two files with specific encoding
company_data = pd.read_csv("./MergeData/Merge1/CompanyDetails.txt", encoding='latin-1')
people_data = pd.read_csv("./MergeData/Merge1/PeopleDetails.txt", encoding='latin-1')

#merging the data on 'ProductReference' column
merged_data = pd.merge(people_data, company_data, on='ProductReference', how='outer')

# remove duplicates
merged_data.drop_duplicates(inplace=True)

#saving the merged data in the new file
merged_data.to_csv("./MergeData/Merge1/merged_file_with_duplicates.csv", index=False)