#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 12 17:46:09 2022

@author: andrew
"""

import pandas as pd

#file_name=pd.read_csv('file.csv')

data=pd.read_csv('transaction.csv')

data=pd.read_csv('transaction.csv',sep=';')

#summary of the data

data.head()
data.info()
#playing around with variables

var = 'Hello, world'

#working with calculations
#defining variables

CostPerItem = 11.73
SellingPricePerItem = 21.11
NumberofItemsPurchased = 6

ProfitPerItem = 21.11-11.73

ProfitPerItem = SellingPricePerItem -CostPerItem

ProfitPerTransaction = NumberofItemsPurchased * ProfitPerItem
CostPerTransaction = CostPerItem * NumberofItemsPurchased
SellingPricePerItem = SellingPricePerItem * NumberofItemsPurchased

#CostPerTransaction =CostPerItem * NumberofItemsPurchased
#variable = dataframe['column_name']

CostPerItem = data['CostPerItem']
NumberofItemsPurchased = data['NumberOfItemsPurchased']
CostPerTransaction = CostPerItem * NumberofItemsPurchased

#adding new column to datraframe

data['CostPerTransaction'] = CostPerTransaction

#alternatively

#data['CostPerTransaction'] = data['CostPerItem'] * data['NumberOfItemsPurchased']

#Sales per transaction

data['SalesPerTransaction'] = data['SellingPricePerItem'] * data['NumberOfItemsPurchased']

#profit calculation = sales - cost

data['ProfitPerTransaction'] = data['SalesPerTransaction'] - data['CostPerTransaction']

#markup =(sales - cost)/cost

data['Markup'] = (data['SalesPerTransaction'] - data['CostPerTransaction'])/data['CostPerTransaction']

#alternatively
#data['Markup'] = data['ProfitPerTransaction]/data['CostPerTransaction]

#rounding markup

data['Markup'] = round(data['Markup'],2)

#combining date fields
my_date = 'Day'+'-'+'Month'+'-'+'Year'

day=data['Day'].astype(str)
print(day.dtype)
year=data['Year'].astype(str)
print(year.dtype)

my_date= day+'-'+data['Month']+'-'+year

data['Date']=my_date

#using iloc to view specific colums/rows
data.iloc[0] #views row with index=0
data.iloc[0:3] #first three rows
data.iloc[:5] #first five rows
data.iloc[-5:] #last five rows
data.head(3)
data.iloc[:,2] #all rows but 2 columns
data.iloc[4,2] #fourth row second column

#using split to split the client keywords field
#new_var = column.str.split('sep', expand = True)

split_col = data['ClientKeywords'].str.split(',',expand=True)

#creating new columns for the split columns in client keywords

data['ClientAge'] = split_col[0]
data['ClientType'] = split_col[1]
data['LengthContract'] = split_col[2]

#using replace function

data['ClientAge'] = data['ClientAge'].str.replace('[','')
data['LengthContract'] = data['LengthContract'].str.replace(']','')

#using lower function to chase case of string

data['ItemDescription'] = data['ItemDescription'].str.lower()

#merging files
#bringing in a new dataset

seasons = pd.read_csv('value_inc_seasons.csv',sep=';')

#merging files: merge.]_df = pd.merge(df_old,df_new,on='key)

data = pd.merge(data , seasons, on = 'Month') 

#dropping columns

#df = df.drop['columnname' , axis = 1]

data = data.drop('ClientKeywords', axis = 1)

#dropping multiple columns

data = data.drop(['Year', 'Month'], axis = 1)

#exporting to csv

data.to_csv('ValueInc_cleaned.csv', index = False)
