"""Merging the data from PeopleDetails.txt and CompanyDetails.txt files into a single file using the ProductReference as the key."""

import pandas as pd

# read the data from the two files
company_data = pd.read_csv("MergeData\CompanyDetails.txt", encoding='latin-1')
people_data = pd.read_csv("MergeData\PeopleDetails.txt", encoding='latin-1')

# group the company data by 'ProductReference' and aggregate the rest of the columns
grouped_data = company_data.groupby('ProductReference').agg({'CompanyTypeID':'first','CompanyType':'first'}).reset_index()

# merge the grouped company data with people data
merged_data = pd.merge(people_data, grouped_data, on='ProductReference', how='outer')

# remove duplicates
merged_data.drop_duplicates(inplace=True)

# saving the merged data in the new file
merged_data.to_csv("MergeData\merged_file_with_no_duplicates.csv", index=False)

