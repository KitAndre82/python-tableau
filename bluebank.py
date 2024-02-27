#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 17 13:34:09 2022

@author: andrew
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#method 1 to read json data

json_file = open('loan_data_json.json')
data = json.load(json_file)

#method 2

with open('loan_data_json.json') as json_file:
    data = json.load(json_file)

loandata = pd.DataFrame(data)

#finding unique values for the purpose column
loandata['purpose'].unique()

#describe the data
loandata.describe()

#to show the columns in the dataframe
loandata.info()

#describe the data for a particular column
loandata['int.rate'].describe()
loandata['fico'].describe()
loandata['dti'].describe()

#using EXP() to get annual income
income = np.exp(loandata['log.annual.inc'])
loandata['annualincome'] = income



   
# Categorizing FICO scores
length=len(loandata)

fico_category=[]
    
for x in range(0,length):
    category = loandata['fico'][x]
    try:
        if category>=300 and category<400:
            fico_cat ='Very Poor'
        elif category>=400 and category<600:
            fico_cat = 'Poor'
        elif category>=600 and category<660:
            fico_cat = 'Fair'
        elif category>=660 and category<780:
            fico_cat = 'Good'
        elif category>=780:
            fico_cat = 'Excellent'
        else:
            fico_cat='Unknown'
    except:
        fico_cat='Unknown'
    fico_category.append(fico_cat)
        
# To create the row in our data  
fico_category = pd.Series(fico_category)
loandata['fico.category'] = fico_category

# conditional statements
# df.loc[df[columname]condition, newcolumn]='value if condition is met'

loandata.loc[loandata['int.rate']>0.12, 'int.rate.type']= 'High'
loandata.loc[loandata['int.rate']<=0.12, 'int.rate.type']= 'Low'

loandata['int.rate']

# Number of loans/rows by fico_category size

cat_size = loandata.groupby(loandata['fico.category']).size()
cat_size.plot.bar(color='yellow', width=0.2)
plt.show()

rate_size=loandata.groupby(loandata['int.rate.type']).size()
rate_size.plot.bar()
plt.show()

purpose_count = loandata.groupby(loandata['purpose']).size()
purpose_count.plot.bar()
plt.show()

# Scatter plot of annual income vs dti

loandata.info()

y = loandata['annualincome']
x = loandata['dti']
plt.scatter(x,y, color='red')
plt.show()

#saving cleaned data in csv file
loandata.to_csv('loan_cleaned.csv', index=True)
