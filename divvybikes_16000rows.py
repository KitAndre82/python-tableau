#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 17:43:19 2023

@author: andrew
"""

""" Porgramme that combines 4 csv files into one file with 3.6 million rows and then uses 
pivot tables to break it down into less  than 17000 rows that include the data by day of week

"""

import pandas as pd

# Load csv files and isplay the columns 
df1 = pd.read_csv('/Users/andrew/Downloads/BIDM/bidm assignment 3 files/Divvy_Trips_2018_Q1 3.csv')
df1.columns

df2 = pd.read_csv('/Users/andrew/Downloads/BIDM/bidm assignment 3 files/Divvy_Trips_2018_Q2.csv')
df2.columns

df3 = pd.read_csv('/Users/andrew/Downloads/BIDM/bidm assignment 3 files/Divvy_Trips_2018_Q3.csv')
df3.columns

df4 = pd.read_csv('/Users/andrew/Downloads/BIDM/bidm assignment 3 files/Divvy_Trips_2018_Q4.csv')
df4.columns

# The files have different column names. So the code below ensures that all 4 dataframes have the same column names

df1.rename(columns ={'01 - Rental Details Rental ID':'trip_id', '01 - Rental Details Local Start Time':'start_time',
       '01 - Rental Details Local End Time':'end_time', '01 - Rental Details Bike ID':'bikeid',
       '01 - Rental Details Duration In Seconds Uncapped':'tripduration',
       '03 - Rental Start Station ID':'from_station_id', '03 - Rental Start Station Name':'from_station_name',
       '02 - Rental End Station ID':'to_station_id', '02 - Rental End Station Name':'to_station_name',
       'User Type':'usertype', 'Member Gender':'gender',
       '05 - Member Details Member Birthday Year':'birthyear'},inplace=True)


# Concatenate the dataframes into a single dataframe
df = pd.concat([df1, df2, df3, df4], ignore_index=True)


df.info()


# Convert date strings to datetime objects
df['Start_time_converted'] = pd.to_datetime(df['start_time'], format="%Y-%m-%d %H:%M:%S")
df['End_time_converted'] = pd.to_datetime(df['end_time'], format="%Y-%m-%d %H:%M:%S")

# Drop the 'Unnamed: 0' column if it exists
if 'Unnamed: 0' in df.columns:
    df.drop(columns=['Unnamed: 0'], inplace=True)


def day_of_week(data):
    return data.strftime('%A') # Define the function to extract the day of the week from a datetime object

# Apply the function to get the day of the week for 'Start_time_converted' and 'End_time_converted'
df['Start Day of week'] = df['Start_time_converted'].apply(day_of_week)
df['End Day of week'] = df['End_time_converted'].apply(day_of_week)


df.info()

df.head(3)

# Getting the duration of the trips

df['duration'] = (df['End_time_converted'] - df['Start_time_converted'])

df.head(2)

# Some rows in the tripduration column have figures separated by comma. The code below extracts the commas and converts the column into a float data type
df['tripduration'] = df['tripduration'].str.replace(',', '')

df['tripduration'] = df['tripduration'].astype('float64')


df['tripduration_hours'] =  df['tripduration'] / 60 #converting duration from minutes to hours

# Extracting month, year and day from Start_time_converted column
import datetime as dt
df['month'] = df['Start_time_converted'].dt.month
df['year'] = df['Start_time_converted'].dt.year
df['day'] = df['Start_time_converted'].dt.day

# Creating a quarter column
Quarter = []
def quarter(data):
    for item in data:
        if item in [1,2,3]:
            quart = 1
        elif item in [4,5,6]:
            quart = 2
        elif item in [7,8,9]:
            quart = 3
        else:
            quart = 4
        Quarter.append(quart)
    return Quarter            

df['Quarter'] = quarter(df['month'])

# Creating a month name column
def month_name(data):
    return data.strftime('%B')

# Apply the function to get the month name from 'Start_time_converted' 
df['Month name'] = df['Start_time_converted'].apply(month_name)


df.head(2)

# Creating Startdate column with only day, month and year
StartDate = []
for row in range(0, len(df)):
    date = str(df['year'][row]) + '-' + str(df['month'][row]) + '-' + str(df['day'][row])
    StartDate.append(date)    

df['StartDate'] = pd.to_datetime(StartDate, format="%Y-%m-%d")

df['hour'] = df['Start_time_converted'].dt.hour #creating a column for hoir of the day

#Using pivot tables to create our data warehouse of less than 17000 rows
import numpy as np
df_wh = pd.pivot_table(df, index=['StartDate','Quarter','month','Month name','Start Day of week','hour','usertype'], values=['bikeid','tripduration_hours'], aggfunc={'bikeid':'count','tripduration_hours':'mean'})

df_wh.info()

#Renaming some of the columns

df_wh.rename(columns={'bikeid':'Rides started','tripduration_hours':'tripduration_average(hrs)'},inplace=True)

df_wh.head(3)

# Saving dataw warehouse on my PC
df_wh.to_excel('/Users/andrew/Downloads/BIDM/bidm assignment 3 files/divvy_bikes_datawarehouse.xlsx')

import seaborn as sns
sns.histplot(x ='usertype', data=df_wh, color='green') #histplot of usertype

quarter_df = pd.pivot_table(df_wh, index=['Quarter'], values=['Rides started'],aggfunc='count') #rides per quarter

quarter_df

sns.scatterplot(quarter_df)

rides_bymonth = pd.pivot_table(df_wh, index=['month','Month name'], values=['Rides started'],aggfunc='count') #rides per month

rides_bymonth

sns.barplot(data=rides_bymonth, x='Month name',y='Rides started')

rides_byhour = pd.pivot_table(df_wh, index=['hour'], values=['Rides started'],aggfunc='count').plot() #rides per hour

rides_byduration = pd.pivot_table(df_wh, index=['hour'], values=['tripduration_average(hrs)'],aggfunc='mean').plot() #average duration of rides per hour

rides_byday = pd.pivot_table(df_wh, index=['Start Day of week'], values=['Rides started'],aggfunc='count').plot() #rides started per week







