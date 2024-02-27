#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 12 17:46:09 2022

@author: andrew
"""

import pandas as pd

data = pd.read_csv('transaction.csv')

data = pd.read_csv('transaction.csv',sep=';')

# Summary of the data

data.head()
data.info()

CostPerItem = data['CostPerItem']

NumberofItemsPurchased = data['NumberOfItemsPurchased']

CostPerTransaction = CostPerItem * NumberofItemsPurchased

# Adding new column to datraframe

data['CostPerTransaction'] = CostPerTransaction

# Alternatively
# data['CostPerTransaction'] = data['CostPerItem'] * data['NumberOfItemsPurchased']

# Sales per transaction

data['SalesPerTransaction'] = data['SellingPricePerItem'] * data['NumberOfItemsPurchased']

# Calculating profit per transaction

data['ProfitPerTransaction'] = data['SalesPerTransaction'] - data['CostPerTransaction']

# Calculating markup per transaction
#markup =(sales - cost)/cost

data['Markup'] = (data['SalesPerTransaction'] - data['CostPerTransaction']) / data['CostPerTransaction']

#alternatively
#data['Markup'] = data['ProfitPerTransaction]/data['CostPerTransaction]

#rounding markup to the nearest 2 decimals

data['Markup'] = round(data['Markup'],2)

#combining date fields
my_date = 'Day' + '-' + 'Month' + '-' + 'Year'

day = data['Day'].astype(str)
print(day.dtype)

year = data['Year'].astype(str)
print(year.dtype)

my_date= day + '-' + data['Month'] + '-' + year

data['Date'] = my_date

#using split to split the client keywords field
#new_var = column.str.split('sep', expand = True)

split_col = data['ClientKeywords'].str.split(',',expand=True)

#creating new columns for the split columns in client keywords

data['ClientAge'] = split_col[0]
data['ClientType'] = split_col[1]
data['LengthContract'] = split_col[2]

#using replace function to remove square brackets

data['ClientAge'] = data['ClientAge'].str.replace('[','')
data['LengthContract'] = data['LengthContract'].str.replace(']','')

#using lower function to change case of string

data['ItemDescription'] = data['ItemDescription'].str.lower()

#merging files
#bringing in a new dataset

seasons = pd.read_csv('value_inc_seasons.csv',sep=';')

#merging files: merge.]_df = pd.merge(df_old,df_new,on='key)

data = pd.merge(data , seasons, on = 'Month') 

#dropping ClientKeywords columns

data = data.drop('ClientKeywords', axis = 1)

#dropping Year and Month columns

data = data.drop(['Year', 'Month'], axis = 1)

#exporting to csv

data.to_csv('ValueInc_cleaned.csv', index = False)
