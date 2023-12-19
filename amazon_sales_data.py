#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 20:54:54 2023

@author: andrew
"""

""" Cleaning Amazon dataset, and calculating sales tax for California and Iowa"""

import pandas as pd

df = pd.read_csv('/Users/andrew/Downloads/internship files/amazonsales data.csv')

df.head(3)

#dictionary of US states and their abbreviations

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
    
list_states = list(us_state_to_abbrev.keys()) #extracting US states abbreviations

us_state_to_abbrev.get('Iowa')

#function that assigns a US state abbreviation or "International" if region outside the US to a column 
def state_abbrevs(data, list_states):
    order_states = []
    for row in range(len(df)):
        row_data = str(data[row])
        if len(row_data) > 2:
            if row_data.title() in list_states:
                state = us_state_to_abbrev.get(row_data.title())
                order_states.append(state)
            else:
                state = 'International'
                order_states.append(state)
        else:
            state = row_data.upper()
            order_states.append(state)
    return order_states


Order_states = state_abbrevs(df['order state'],list_states)

#creating column for Order state abbreviations
df['Order_states'] = Order_states

df.head(2)

df.to_excel('/Users/andrew/Downloads/internship files/amazonsales_data2_edited.xlsx')

df.head(2)

IA_data = df.loc[df['Order_states'] == 'IA'] #separate dataframe for Iowa data

CA_data = df.loc[df['Order_states'] =='CA'] #separate dataframe for California data

IA_data.to_excel('/Users/andrew/Downloads/internship files/iowa_data_edited.xlsx')

CA_data.to_excel('/Users/andrew/Downloads/internship files/california_data_edited.xlsx')

#function that calculates tax 
def tax_calc(data, rate):
    sales_tax = []
    for item in data:
        tax = item - (item/(1+rate)) 
        sales_tax.append(round(tax,2))
    return sales_tax

#sales tax has a portion that goes to the state and a portion that goes to a locality in a state
#portion going to state

IA_tax_state = tax_calc(IA_data['product sales'], 0.06)
CA_tax_state = tax_calc(CA_data['product sales'], 0.0725)


#portion going to locality
IA_tax_avg_local = tax_calc(IA_data['product sales'], 0.0094)
CA_tax_avg_local = tax_calc(CA_data['product sales'], 0.0157)

#creating column for sales tax portion going to state
IA_data['sales_tax_state'] = IA_tax_state
CA_data['sales_tax_state'] = CA_tax_state

IA_#creating a column for sales tax portion going to locality
data['sales_tax_avg_local'] = IA_tax_avg_local
CA_data['sales_tax_avg_local'] = CA_tax_avg_local

#creating a cloumn for net sales
IA_data['net_sales'] = IA_data['product sales'] + IA_data['selling fees'] - IA_data['sales_tax_state'] - IA_data['sales_tax_avg_local']
CA_data['net_sales'] = CA_data['product sales'] + CA_data['selling fees'] - CA_data['sales_tax_state'] - CA_data['sales_tax_avg_local']

#Concatenating IA and CA datasets
ia_ca_data = pd.concat([IA_data, CA_data])

#Saving concatenating dataset on hard drive
ia_ca_data.to_excel('/Users/andrew/Downloads/internship files/Iowa_california_combined_edited.xlsx')

ia_ca_data.info()

#net sales calculation
#selling fees are negative figures in dataset...that's why we add them in this case
net_sales = ia_ca_data['product sales'].sum() + ia_ca_data['selling fees'].sum()

#alternative calulation of net sales
ia_ca_data['net_sales'].sum()

#creating separate dataset for type - 0rder
orders = ia_ca_data.loc[ia_ca_data['type'] == 'Order']

orders.to_excel('/Users/andrew/Downloads/internship files/orders_data_edited.xlsx')


#creating separate dataset for type - Refund
refunds = ia_ca_data.loc[ia_ca_data['type'] == 'Refund']

refunds.to_excel('/Users/andrew/Downloads/internship files/refunds_data_edited.xlsx')

#sum of product sales less selling fees --> sales revenue
orders['net_sales'].sum()

#total refunds 
refunds['product sales'].sum()

type(ia_ca_data['date/time'])

#sorting concatenated IA and CA dataframe by date
from datetime import datetime
ia_ca_data['date/time'] = pd.to_datetime(ia_ca_data['date/time'])
ia_ca_data.sort_values(by='date/time')

#saving dataframe to PC
ia_ca_data.to_excel('/Users/andrew/Downloads/internship files/Iowa_california_combined_edited_sorted.xlsx')





