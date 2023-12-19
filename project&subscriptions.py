#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 18:55:28 2023

@author: andrew
"""

#!/usr/bin/env python
# coding: utf-8

# # Projects and subscriptions assignment

# ###  Required: 1. Projects completed by year   2. Projects started by year   3. Projects in progress in 2021

# ### 4. Report for 2022    5. Report for 2023    6. Deferred income 

# ### Importing relevant libraries

import pandas as pd
import numpy as np
import datetime as dt


# ### Reading our datasets in Pandas

df1 = pd.read_excel('/Users/andrew/Downloads/internship files/Projects_subscriptions.xlsx')

df1.info()

df2 = pd.read_excel('/Users/andrew/Downloads/internship files/Projects_subscriptions.xlsx',sheet_name='SAAS')

df2.info()

df1.head()


# ## Implementation dataset manipulation

# ### Splitting date columns to create separate columns for Start year, End year, End month and Day of month


df1['Start year'] = df1['Start date'].dt.year

df1['End year'] = df1['End date'].dt.year

df1['End month'] = df1['End date'].dt.month

df1['Day of month'] = df1['End date'].dt.day

df1.head(5)

# ### Replacing null values in End year column with 9999 

df1['End year'].fillna(9999, inplace=True) 


# ### Replacing null values in End month and Day of month columns with 'In progress - indefinite end date'

df1['End month'].fillna('In progress - indefinite end date', inplace=True) 

df1['Day of month'].fillna('In progress - indefinite end date', inplace=True) 

df1.tail(5)

# ### Adding a status of project column using IF ELSE statements

Status = []
current_year = 2023
current_month = 7
current_day = 16
for row in range(0, len(df1)):
    if df1['End year'][row] <= 2021:
        status = 'Completed by 2021'
    elif df1['End year'][row] == 2022:
        status = 'Completed in 2022'
    elif df1['End year'][row] == current_year and df1['End month'][row] < current_month:        
        status = 'Completed in 2023'
    elif df1['End year'][row] == current_year and df1['End month'][row] == current_month and df1['Day of month'][row] <= current_day:
        status = 'Completed in 2023'
    elif df1['End year'][row] == current_year and df1['End month'][row] == current_month and df1['Day of month'][row] > current_day:
        status = 'In progress'
    elif df1['End year'][row] == current_year and df1['End month'][row] > current_month:
        status = 'In progress'
    elif df1['End year'][row] == 9999:
        status = 'In progress - indefinite end date'
    elif df1['End year'][row] > current_year:
        status = 'In progress'
    else:
        status = 'Undetermined'
    Status.append(status)

df1['Status of project'] = Status

df1.head(3)

# ## Projects completed by year

projects_completed = pd.pivot_table(df1, index = ['Category','Status of project'],values = ['Client'],aggfunc = 'count')

projects_completed.head(5)

projects_completed.to_excel('/Users/andrew/Downloads/internship files/Projects_completed_by_year_COPY.xlsx')

# ## Projects started per year

projects_started = pd.pivot_table(df1, index = ['Category','Start year'],values=['Client'], aggfunc = 'count')

projects_started.to_excel('/Users/andrew/Downloads/internship files/Projects_started_by_year_COPY.xlsx')

projects_started.head(5)

# ### Saving data to PC hard drive

df1.to_excel('/Users/andrew/Downloads/internship files/implementations_final._COPY.xlsx')

# ### Number of projects in progress in 2021

count = 0
for row in range(0, len(df1)):
    if  df1['Status of project'][row] == 'In progress' and df1['Start year'][row] <= 2021 and df1['End year'][row] > 2021 :
        count += 1
    else:
        continue
print("The number of projects in progress in 2021 is ",count)        


# #### The number of projects in progress in 2021 is  5

# ## SAAS dataset manipulation

# ### Creating a column for number of days of subscription


number_days = (df2['End'] - df2['Start']).dt.days


""" The datetime library does not count the current day. So the next function adds 1 to each of the number of days figures"""

def days(data):
    Days = []
    for item in data:
        item = item +1
        Days.append(item)
    return Days

days_subscribed = days(number_days)


# ### Creating a new column for days subscribed

df2['Days_subscribed'] = days_subscribed

df2.head(3)


# ### Computing the amount per day (dollar amount) by dividing the figures in the Total column by days subscribed

df2['Amount_per_day'] = df2['Total'] / df2['Days_subscribed']

df2.head(3)

# ### Extracting day, month and year figures from the Start and End columns

df2['Start Day'] = df2['Start'].dt.day
df2['Start Month'] = df2['Start'].dt.month
df2['Start year'] = df2['Start'].dt.year
df2['End Day'] = df2['End'].dt.day
df2['End Month'] = df2['End'].dt.month
df2['End Year'] = df2['End'].dt.year

df2.head(3)


# ### Using IF ELSE statements to create a status column

Status = []
for row in range(0, len(df2)):
    if df2['End Year'][row] < 2022:
        status = 'Completed before accounting periods of interest'
        Status.append(status)
    elif df2['End Year'][row] == 2022:
        status = 'Completed in 2022'
        Status.append(status)
    elif df2['End Year'][row] == 2023 and df2['End Month'][row] <= 4 and df2['End Day'][row] <=30:
        status = 'Completed by end of April 2023'
        Status.append(status)
    else:
        status = 'Not Completed by end of April 2023'
        Status.append(status)
    
df2['Status'] = Status


# ### Creating datetime objects representing end and start of accounting periods


""" These will be useful for calculating number of days subscribed in particular periods"""

from datetime import datetime 

end_2022  = '2022/12/31 23:59:59'
end_2022_obj = datetime.strptime(end_2022, "%Y/%m/%d %H:%M:%S")

start_2022 = '2022/01/01 00:00:00'
start_2022_obj = datetime.strptime(start_2022, "%Y/%m/%d %H:%M:%S")

end_2023 = '2023/04/30 23:59:59'
end_2023_obj = datetime.strptime(end_2023, "%Y/%m/%d %H:%M:%S")

start_2023 = '2023/01/01 00:00:00'
start_2023_obj = datetime.strptime(start_2023, "%Y/%m/%d %H:%M:%S")


"""fin_year = []
for row in range(0, len(df2)):
    if df2['End Year'][row] > 2022:
        if df2['Start year'][row] <= 2022 and df2['End Year'][row] == 2022:
            fin_yr = 2022
            fin_year.append(fin_yr)
        elif df2['Start year'][row] <= 2022 and df2['End Year'][row] == 2023:
            fin_yr = 2023
            fin_year.append(fin_yr)
        else:
            fin_yr = 2024
            fin_year.append(fin_yr)
    else:
        fin_yr = 2021
        fin_year.append(fin_yr)"""
            

#df2['financial_period'] = fin_year


num_days_2022 = []
num_days_2023 = []
for row in range(0, len(df2)):
    if df2['End Year'][row] == 2022 and df2['Start year'][row] < 2022:
        num_day_2022 = (df2['End'][row] - start_2022_obj).days
        num_day_2023 = -1
    elif df2['End Year'][row] == 2022 and df2['Start year'][row] == 2022:
        num_day_2022 = (df2['End'][row] - df2['Start'][row]).days
        num_day_2023 = -1
    elif df2['End Year'][row] == 2023 and df2['Start year'][row] == 2022:
        num_day_2022 = (end_2022_obj - df2['Start'][row]).days
        num_day_2023 = (end_2023_obj - start_2023_obj).days
    elif df2['End Year'][row] == 2023 and df2['Start year'][row] == 2023:
        num_day_2022 = -1
        num_day_2023 = (df2['End'][row] - df2['Start'][row]).days        
    else:
        num_day_2022 = -1
        num_day_2023 = -1
    num_days_2022.append(num_day_2022)
    num_days_2023.append(num_day_2023)
    

df2['Days_subscribed_2022'] = days(num_days_2022)
df2['Days_subscribed_2023'] = days(num_days_2023)

df2.head(3)


# ### Calculating number of days subscribed after 04/30/2023


df2['Subscription_days_after 04/30/2023'] = (df2['End'] - end_2023_obj).dt.days


df2.head(3)


# ### Assigning 0 to days of subscription days before 04/30/2023 in order to calculate deferred income


Subscription_days_after_04_30_2023 = []
for row in range(0, len(df2)):
    if df2['Subscription_days_after 04/30/2023'][row] <= 0:
        days_ = -1
        Subscription_days_after_04_30_2023.append(days_)
    else:
        days_ = df2['Subscription_days_after 04/30/2023'][row]
        Subscription_days_after_04_30_2023.append(days_)
        
df2['Subscription_days_after_04_30_2023'] = days(Subscription_days_after_04_30_2023)

df2.head(3)


# ### Calculation of 2022 and 2023 (Jan 1st - Apr 30th) subscriptions; and deferred income

df2['Subscriptions_2022'] = df2['Days_subscribed_2022'] * df2['Amount_per_day']
df2['Subscriptions_2023'] = df2['Days_subscribed_2023'] * df2['Amount_per_day']
df2['Deferred income'] = df2['Subscription_days_after_04_30_2023'] * df2['Amount_per_day']

df2.head(3)

df2['Subscriptions_2022'] = df2['Subscriptions_2022'].astype('int64')
df2['Subscriptions_2023'] = df2['Subscriptions_2023'].astype('int64')
df2['Deferred income'] = df2['Deferred income'].astype('int64')
pd.pivot_table(df2, index=['Prod'], values=['Subscriptions_2022','Subscriptions_2023','Deferred income'],aggfunc=np.sum)

# Saving deferred income by product to PC
#deferred_income_by_product.to_excel('/Users/andrew/Downloads/internship files/Projects_subscriptions__SAAS_INCOME_BY_YR_COPY.xlsx')


# ## Deferred income (income for services to be delivered after April 30, 2023)

print("Deferred subscription income for the company is ", round(df2['Deferred income'].sum(),3))

# Saving final df2 dataset to PC
df2.to_excel('/Users/andrew/Downloads/internship files/Projects_subscriptions_SAAS__FINAL_COPY.xlsx')



