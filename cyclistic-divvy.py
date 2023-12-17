#!/usr/bin/env python
# coding: utf-8

# # Establishing how riders with an annual membership use bikes differently from members without one (casual members)

#libraries needed
import pandas as pd
import numpy as np
import datetime as dt
from zipfile import ZipFile
from io import BytesIO 
import requests
import seaborn as sns
import matplotlib.pyplot as plt


#setting the style of the visualisations
sns.set_style('whitegrid')


# function that extracts different datasets 
def extract_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        zip_file = ZipFile(BytesIO(response.content))
        files = zip_file.namelist()
        with zip_file.open(files[0]) as csv_file:
            df = pd.read_csv(csv_file)
            return df
    else:
        return 'Error'


# zip files to be extracted
url1 = 'https://divvy-tripdata.s3.amazonaws.com/202201-divvy-tripdata.zip'
url2 = 'https://divvy-tripdata.s3.amazonaws.com/202202-divvy-tripdata.zip'
url3 = 'https://divvy-tripdata.s3.amazonaws.com/202203-divvy-tripdata.zip'
url4 = 'https://divvy-tripdata.s3.amazonaws.com/202204-divvy-tripdata.zip'
url5 = 'https://divvy-tripdata.s3.amazonaws.com/202205-divvy-tripdata.zip'
url6 = 'https://divvy-tripdata.s3.amazonaws.com/202206-divvy-tripdata.zip'
url7 = 'https://divvy-tripdata.s3.amazonaws.com/202207-divvy-tripdata.zip'
url8 = 'https://divvy-tripdata.s3.amazonaws.com/202208-divvy-tripdata.zip'
url9 = 'https://divvy-tripdata.s3.amazonaws.com/202209-divvy-tripdata.zip'
url10 = 'https://divvy-tripdata.s3.amazonaws.com/202210-divvy-tripdata.zip'
url11 = 'https://divvy-tripdata.s3.amazonaws.com/202211-divvy-tripdata.zip'
url12 = 'https://divvy-tripdata.s3.amazonaws.com/202212-divvy-tripdata.zip'

# Extracted dataframes  
df1 = extract_data(url1)
df2 = extract_data(url2)
df3 = extract_data(url3)
df4 = extract_data(url4)
df5 = extract_data(url5)
df6 = extract_data(url6)
df7 = extract_data(url7)
df8 = extract_data(url8)
df9 = extract_data(url9)
df10 = extract_data(url10)
df11 = extract_data(url11)
df12 = extract_data(url12)


df2.head(1)


df1.head(1)


#checking column names...if they differ, renaming is required 
df1.columns


df2.columns


#merging the monthly dataframes into one for the year
merged_df = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12],ignore_index=True)

merged_df.info()


#checking the unique rideable types
merged_df['rideable_type'].unique()

merged_df[merged_df['rideable_type']=='docked_bike'].info()

docked = (merged_df['rideable_type'] == 'docked_bike')

docked.info()

#deleting rows with docked_bike as rideable_type
df = merged_df[~docked]

df['started_at'] = pd.to_datetime(df['started_at'])

df['ended_at'] = pd.to_datetime(df['ended_at'])

df['ride_length'] = df['ended_at'] - df['started_at']

#establishing how many rides were less than 1 minute long.
df[df['ride_length'].apply(lambda x:x.total_seconds()/60) < 1].info()

#establishing the rides with a trip duration of less than 1 minute
short_ride_length = df['ride_length'].apply(lambda x:x.total_seconds()/60)<1

#deleting the rows where trip duration is less than 1 minute
df = df[~short_ride_length]

df.rideable_type.unique()

df.info()

#checking for null values
#no rows with only null values
df.isnull().sum()

#def weekday(data):
#    return data.strftime('%A')

#new columns created out of the started_at column
#essential for aggregation

df['day_of_week'] = df['started_at'].apply(lambda x:x.strftime('%A'))

df['month'] = df['started_at'].dt.month

df['year'] = df['started_at'].dt.year

df['MONTH'] = df['started_at'].apply(lambda x:x.strftime('%B'))

df['quarter'] = df['started_at'].dt.quarter

df['hour'] = df['started_at'].dt.hour

#function that determines the season of the year
def get_season(month):
    if 3 <= month <= 5:
        return 'Spring'
    elif 6 <= month <= 8:
        return 'Summer'
    elif 9 <= month <= 11:
        return 'Fall'
    else:
        return 'Winter'

df['season'] = df['month'].apply(get_season)

df['ride_length_in_minutes'] = df['ride_length'].apply(lambda x:x.total_seconds()/60)

days={'Sunday':1,'Monday':2,'Tuesday':3,'Wednesday':4,'Thursday':5,'Friday':6,'Saturday':7}

df['day'] = df['day_of_week'].map(days)

df.head(1)

df.isnull().sum()

#df_trimmed = df[['ride_id','rideable_type','start_lat','start_lng','end_lat','end_lng','member_casual']]

df.head(2)


# ### Annual members V casual riders

users = df.groupby('member_casual'
                  ).count()['ride_id'].reset_index().rename(
columns={'member_casual':'user_type','ride_id':'#rides'})

users

import matplotlib.pyplot as plt

data = users['#rides']
labels = users['user_type'].unique()
explode = [0.1, 0]

plt.pie(data, labels=labels, explode=explode, autopct='%1.2f%%',colors=['orange','green'])
plt.title('Number of rides by user type',loc='left')
plt.show()


# ### Average ride length

df['ride_length'].mean()


# ### Maximum ride length

max(df['ride_length'])


# ### Average ride length by day

rides_by_day = pd.pivot_table(
    df,index=['day_of_week',],
    values=['ride_length_in_minutes'],
    aggfunc='mean'
).reset_index()

#order={'Sunday':1,'Monday':2,'Tuesday':3,'Wednesday':4,'Thursday':5,'Friday':6,'Saturday':7}
#rides_by_day['Day_Order'] = rides_by_day['day_of_week'].map(order)

rides_by_day.rename(
    columns={'ride_length_in_minutes':"Average ride length (minutes)"},inplace=True)

order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

plt.figure(figsize=(12,5))
sns.barplot(rides_by_day,
            x='day_of_week',
            y="Average ride length (minutes)",
            order=order,
            palette=sns.color_palette('colorblind')
           )
plt.xlabel('Day of week')
plt.title('Average ride length by day of week',loc='left') 
plt.show()

rides_by_day_users = pd.pivot_table(df,
                                    index=['day_of_week','member_casual'],
                                    values=['ride_length_in_minutes'],
                                    aggfunc='mean'
                                   ).reset_index().rename(
    columns={'ride_length_in_minutes':'avg_ride_length_in_minutes'})

rides_by_day_users['day' ]= rides_by_day_users['day_of_week'].map(days)

rides_by_day_users = rides_by_day_users.sort_values(by='day')

plt.figure(figsize=(12,5))
sns.lineplot(rides_by_day_users,
             x='day_of_week',
             y='avg_ride_length_in_minutes',          
             hue='member_casual',
             palette=['orange','green']
            )
plt.xlabel('Day of week')
plt.ylabel('Average ride length in minutes')
plt.title('Average ride length by day of week and user type',loc='left')
plt.show()

cnt_by_day = pd.pivot_table(df,
                            index=['day_of_week','day'],
                            values=['ride_id'],
                            aggfunc='count'
                           ).reset_index().rename(
    columns={'ride_id':'#rides'})

plt.figure(figsize=(10,5))
sns.barplot(cnt_by_day,
            x='day_of_week',
            y='#rides',
            order=order,
            hue='day_of_week',
            palette=sns.set_palette('pastel')          
           )
plt.xlabel('Day of week')
plt.ylabel('Number of rides')
plt.title('Number of rides by day of week',loc='left')
plt.show()

cnt_by_day_user = pd.pivot_table(df,
              index=['day_of_week','member_casual'],
              values=['ride_id'],
              aggfunc='count'
              ).reset_index().sort_values(by='ride_id',ascending=False
                                         ).rename(columns={'ride_id':'#rides'})

cnt_by_day_user['day']=cnt_by_day_user['day_of_week'].map(days)

cnt_by_day_users = cnt_by_day_user.sort_values(by='day')

plt.figure(figsize=(12,5))
sns.lineplot(cnt_by_day_users,
            x='day_of_week',
            y='#rides',
            hue='member_casual',
            palette=['green','orange'])
plt.xlabel('Day of week')
plt.ylabel('Number of rides')
plt.title('Number of rides by day of the week and user type',loc='left')
plt.show()

#sunday_df = df[df['day_of_week']=='Sunday']

#sunday_rides = pd.pivot_table(sunday_df,
#               index=['member_casual'],
#               values=['ride_id'],
#               aggfunc='count').reset_index().rename(columns={'ride_id':'#rides'})

#sunday_rides

#data=sunday_rides['#rides']
#labels=sunday_rides['member_casual'].unique()
#explode = [0.1,0]
#plt.pie(data,labels=labels,explode=explode,autopct='%1.2f%%',colors=['orange','green'])
#plt.title('Proportion of annual members to casual riders',loc='left')
#plt.show()

#data = sunday_rides['#rides']
#labels = sunday_rides['member_casual'].unique()
#explode = [0.1, 0]

# Create a pie chart
#fig, ax = plt.subplots()
#wedges, texts, autotexts = ax.pie(data, labels=labels, explode=explode, autopct='%1.0f%%',colors=['orange','green'])

# Add actual values as labels inside the pie chart
#for i, (text, autotext) in enumerate(zip(texts, autotexts)):
#    text.set_text(f"{labels[i]}: {data.iloc[i]} rides")  # Display label and value
#    autotext.set_text('')  # Remove percentage labels

#plt.show()


# ### Rides by hour

rides_by_hour = pd.pivot_table(df,
               index=['hour'],
               values=['ride_id'],
               aggfunc='count'
              ).reset_index().rename(columns={'ride_id':'#rides'})

plt.figure(figsize=(14,5))
sns.barplot(rides_by_hour,
             x='hour',
             y='#rides',
            palette=sns.color_palette('colorblind')
            )
plt.xlabel('Hour of the day')
plt.ylabel('Number of rides')
plt.title('Number of rides by hour of the day',loc='left')
plt.show()   

rides_by_hour_users = pd.pivot_table(df,
               index=['hour','member_casual'],
               values=['ride_id'],
               aggfunc='count'
              ).reset_index().rename(columns={'ride_id':'#rides'}
                                    )

plt.figure(figsize=(14,5))
sns.lineplot(rides_by_hour_users,
             x='hour',
             y='#rides',
             hue='member_casual',
             palette=['orange','green']
            )
plt.xlabel('Hour of the day')
plt.ylabel('Number of rides')
plt.title('Number of rides by hour and user type',loc='left')
plt.show()


# ### Average ride length by hour

avg_rides_by_hr = pd.pivot_table(df,
            index=['hour'],
            values=['ride_length'],
            aggfunc='mean'
           ).reset_index().rename(columns={'ride_length':"Average ride length (minutes)"})

plt.figure(figsize=(14,5))
sns.barplot(avg_rides_by_hr,
            x='hour',
            y=avg_rides_by_hr["Average ride length (minutes)"].apply(lambda x:x.total_seconds()/60),
            palette=sns.color_palette('Set1')
           )
plt.xlabel('Hour of the day')
plt.title('Average ride length by hour',loc='left')
plt.show()


# In[74]:


avg_rides_by_hr_users = pd.pivot_table(df,
               index=['hour','member_casual'],
               values=['ride_length'],
               aggfunc='mean'
              ).reset_index().rename(columns={'ride_length':"Average ride length (minutes)"})                                         

plt.figure(figsize=(14,5))
sns.lineplot(avg_rides_by_hr_users,
             x='hour',
             y=avg_rides_by_hr_users["Average ride length (minutes)"].apply(lambda x:x.total_seconds()/60),
             hue='member_casual',
             palette=['orange','green']
            )
plt.xlabel('Hour of the day')
plt.title('Average ride length by hour and user type', loc='left')
plt.show()


# ### Mode of day of week

df['day_of_week'].mode()


# ### Average ride length for annual members and casual riders

avg_by_usertype = pd.pivot_table(df,
index=['member_casual'],
values=['ride_length_in_minutes'],
aggfunc='mean'
).reset_index()

avg_by_usertype.rename(
    columns={'ride_length_in_minutes':"avg_ride_length (minutes)",
            'member_casual':'User Type'},inplace=True)

avg_by_usertype

sns.barplot(x=avg_by_usertype["avg_ride_length (minutes)"],
            y=avg_by_usertype['User Type'],
            palette=['orange','green']
           )
plt.ylabel('User type')
plt.xlabel('Average ride length in minutes')
plt.title('Average ride length by user type',loc='left')
plt.show()


# ### Average ride length by season

seasons_ord = ['Spring','Summer','Fall','Winter']

avg_by_season = pd.pivot_table(df,
                              index=['season'],
                              values=['ride_length'],
                              aggfunc='mean'
                              ).reset_index().rename(
columns={'ride_length':'avg_ride_length'}
)

avg_by_season

sns.barplot(avg_by_season,
    x='season',
    y=avg_by_season['avg_ride_length'].apply(lambda x:x.total_seconds()/60),
    order=seasons_ord,
    hue='season',
    palette = sns.color_palette('deep')
)
plt.xlabel('Season')
plt.ylabel('Average ride length')
plt.title('Average length of ride by season',loc='left')
plt.show()

avg_by_season_users = pd.pivot_table(df,
                              index=['season','member_casual'],
                              values=['ride_length'],
                              aggfunc='mean'
                              ).reset_index().rename(
columns={'ride_length':'avg_ride_length'}
)

sns.barplot(
    x=avg_by_season_users['season'],
    y=avg_by_season_users['avg_ride_length'].apply(lambda x:x.total_seconds()/60),
    hue=avg_by_season_users['member_casual'],
    palette=['orange','green'],
    order=seasons_ord
)
plt.xlabel('Season')
plt.ylabel('Average ride length')
plt.title('Average ride length by season by user type',loc='left')
plt.show()


# ### Number of rides by season

cnt_rides_season = pd.pivot_table(df,
                                       index=['season'],
                                       values=['ride_id'],
                                       aggfunc='count'
                                      ).reset_index().rename(
    columns={'ride_id':'#rides'})

sns.barplot(cnt_rides_season,
            x='season', 
            y='#rides',
            order=seasons_ord,
            hue='season',
            palette=sns.color_palette('colorblind'))
plt.xlabel('Season')
plt.ylabel('Number of rides')
plt.title('Number of rides by season',loc='left')
plt.show()

cnt_rides_season_users = pd.pivot_table(df,
                                 index=['season','member_casual'],
                                 values= ['ride_id'],
                                 aggfunc='count'
                                 ).reset_index().rename(
columns={'ride_id':'#rides'})

sns.barplot(cnt_rides_season_users,
            x='season',
            y='#rides',
            hue='member_casual',
            palette=['orange','green'],
            order=seasons_ord)
plt.xlabel('Season')
plt.ylabel('Number of rides')
plt.title('Number of rides by season and user type',loc='left')
plt.show()


# ### Number of rides by month

rides_by_month = pd.pivot_table(df,
              index=['month','MONTH'],
              values=['ride_id'],
              aggfunc='count'
              ).reset_index().rename(columns={'ride_id':'#rides'})

plt.figure(figsize=(12,5))
sns.lineplot(rides_by_month,
            x='MONTH',
            y='#rides')
plt.xlabel('Month')
plt.ylabel('Number of rides')
plt.title('Number of rides by month',loc='left')
plt.show()

rides_by_month_users = pd.pivot_table(df,
              index=['month','MONTH','member_casual'],
              values=['ride_id'],
              aggfunc='count'
              ).reset_index().rename(columns={'ride_id':'#rides'})

plt.figure(figsize=(12,5))
sns.lineplot(rides_by_month_users.drop('month',axis=1),
             x='MONTH',
             y='#rides',
             hue='member_casual',
             palette=['orange','green']
            )
plt.xlabel('Month')
plt.ylabel('Number of rides')
plt.title('Number of rides by user type by month',loc='left')
plt.show()


# ### Average ride length by month

avg_ride_length_month = pd.pivot_table(df,
              index=['month','MONTH'],
              values=['ride_length'],
              aggfunc='mean'
              ).reset_index().rename(columns={'ride_length':'avg_ride_length'})

plt.figure(figsize=(13,5))
sns.lineplot(x=avg_ride_length_month['MONTH'],
            y=avg_ride_length_month['avg_ride_length'].apply(lambda x:x.total_seconds()/60)
            )
plt.xlabel('Month')
plt.ylabel('Average ride length')
plt.title("Average ride length (in minutes) by month",loc='left')
plt.show()

avg_ride_length_month_users = pd.pivot_table(df,
              index=['month','MONTH','member_casual'],
              values=['ride_length'],
              aggfunc='mean'
              ).reset_index().rename(columns={'ride_length':'avg_ride_length'})

plt.figure(figsize=(14,5))
sns.lineplot(x=avg_ride_length_month_users['MONTH'],
             y=avg_ride_length_month_users['avg_ride_length'].apply(lambda x:x.total_seconds()/60),
             hue=avg_ride_length_month_users['member_casual'],
             palette=['orange','green']
            )
plt.xlabel('Month')
plt.ylabel('Average ride length')
plt.title('Average ride length by month by user type',loc='left')
plt.show()


# ### Rideable type (also type of bike)

by_ride_type = pd.pivot_table(df,
              index=['rideable_type'],
              values=['ride_id'],
              aggfunc='count'
              ).reset_index().rename(columns={'ride_id':'#rides'})

by_ride_type

data = by_ride_type['#rides']
labels = by_ride_type['rideable_type']
plt.pie(data,labels=labels,autopct='%1.2f%%')
plt.title('Number of rides by bike type',loc='left')
plt.show()

by_ride_type_users = pd.pivot_table(df,
              index=['rideable_type','member_casual'],
              values=['ride_id'],
              aggfunc='count'
              ).reset_index().rename(columns={'ride_id':'#rides'})

sns.barplot(by_ride_type_users,
           x='rideable_type',
           y='#rides',
           hue='member_casual',
           palette=['orange','green'])
plt.xlabel('User type')
plt.ylabel('Number of rides')
plt.title('Number of rides by bike type and user type',loc='left')
plt.show()


# ### Average ride length by bike type

avg_by_ride_type = pd.pivot_table(df,
              index=['rideable_type'],
              values=['ride_length'],
              aggfunc='mean'
              ).reset_index().rename(columns={'ride_length':"avg_ride_length (minutes)"})


avg_by_ride_type

sns.barplot(avg_by_ride_type,
           x=avg_by_ride_type['rideable_type'],
           y=avg_by_ride_type["avg_ride_length (minutes)"].apply(lambda x:x.total_seconds()/60),
           palette=sns.color_palette('muted')
           )
plt.xlabel('Type of bike')
plt.ylabel('Average ride length in minutes')
plt.title('Average ride length by bike type',loc='left')
plt.show()

avg_by_ride_type_users = pd.pivot_table(df,
              index=['rideable_type','member_casual'],
              values=['ride_length'],
              aggfunc='mean'
              ).reset_index().rename(columns={'ride_length':"avg_ride_length (minutes)"})

avg_by_ride_type_users

sns.barplot(avg_by_ride_type_users,
           x=avg_by_ride_type_users['rideable_type'],
           y=avg_by_ride_type_users["avg_ride_length (minutes)"].apply(lambda x:x.total_seconds()/60),
           hue=avg_by_ride_type_users['member_casual'],
           palette=['orange','green']
           )
plt.xlabel('Type of bike')
plt.ylabel('Average length of ride')
plt.title('Average ride length by bike type and user type',loc='left')
plt.show()

#sns.scatterplot(df,
#               x='start_lat',
#               y='start_lng',
#               hue='member_casual',
#               palette=['orange','green'])
#plt.title('Start location by user type')
#plt.show()

#sns.scatterplot(df,
#               x='end_lat',
#               y='end_lng',
#               hue='member_casual',
#               palette=['orange','green'])
#plt.title('End location by user type')
#plt.show()


# ### Top 10 busiest stations

df['start_station_name'].nunique()

start_stns = df.groupby(['start_station_name']
          )['ride_id'
           ].count().reset_index().rename(columns={'ride_id':'#rides'
                                                  }).sort_values(by='#rides',ascending=False)


start_stns.head(10)

plt.figure(figsize=(12,5))
sns.barplot(start_stns.head(10),
            y='start_station_name',
            x='#rides',
            hue='start_station_name',
            palette = sns.color_palette('pastel'))
plt.xlabel('Number of rides')
plt.ylabel('Start Station name')
plt.title('Top ten most popular start stations',loc='left')
plt.show()

end_stns = df.groupby('end_station_name'
                     )['ride_id'
                      ].count().reset_index().rename(columns={'ride_id':'#rides'
                                                             }).sort_values(by='#rides',ascending=False)
end_stns.head(10)

plt.figure(figsize=(12,6))
sns.barplot(end_stns.head(10),
            y='end_station_name',
            x='#rides',
            hue='end_station_name',
            palette=sns.color_palette('muted'))
plt.xlabel('Number of rides')
plt.ylabel('End Station name')
plt.title('Top ten most popular end stations',loc='left')
plt.show()       

list(start_stns['start_station_name'].head(10))

busiest_stns = df[df['start_station_name'].isin(list(start_stns['start_station_name'].head(10)))]

busiest_stations_users = pd.pivot_table(busiest_stns,
               index=['start_station_name','member_casual'],
               values=['ride_id'],
               aggfunc='count'
              ).reset_index().rename( columns={'ride_id':'#rides'
                                     }).sort_values(by='#rides',ascending=False)

plt.figure(figsize=(8,6))
sns.barplot(busiest_stations_users,
            x='#rides',
            y='start_station_name',
            hue='member_casual',
            palette=['orange','green'])
plt.xlabel('Number of rides')
plt.ylabel('Start station name')
plt.title('Top ten busiest stations by number of rides and usertype',loc='left')
plt.show()

#busiest_stations = list(start_stns.start_station_name[start_stns['#rides']>20000])

#busiest_stations


# ## Plotting start and end stations on map of Chicago

import folium

# Create a map centered around Chicago
chicago_map = folium.Map(location=[41.8781, -87.6298], zoom_start=3)

# Display the map
chicago_map

#filtering to create df of only start latitudes and longitudes
start_points_df = df[['start_lat','start_lng']]

#filtering to create df of only end latitudes and longitudes
end_points_df = df[['end_lat','end_lng']] 

#function that creates a list of the points
def points_list(data):
    points = []
    for x in range(len(data)):
        point = list(data.iloc[x])
        points.append(point)
    return points

start_points = points_list(start_points_df)

end_points = points_list(end_points_df.dropna())

import random

#getting random sample of 1000 start points 
start_points_sample = random.sample(start_points, 1000)

#getting random sample of 1000 end points
end_points_sample = random.sample(end_points, 1000)

#plotting start points on Chicago map
for point in start_points_sample:
    folium.CircleMarker(point,radius = 5,color = 'green',fill = True).add_to(chicago_map)

#for point in start_points_sample:
#    folium.Marker(point, popup='Point').add_to(chicago_map1)

#plotting end points on Chicago map
for point in end_points_sample:
    folium.CircleMarker(point,radius = 5,color = 'red',fill = True).add_to(chicago_map)

#displaying map after points have been plotted
chicago_map

