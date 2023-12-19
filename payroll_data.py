#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 18:23:52 2023

@author: andrew
"""

#Code that calculates payroll taxes for employees and also the company's monthly expenditure on salaries

import pandas as pd
import numpy as np

file = pd.ExcelFile('/Users/andrew/Downloads/Payroll-datafile.xlsx')

df1 = pd.read_excel(file, 'Payroll data')

df1.drop(columns = ['Tax Status','Resident','xx','xxx','xxxx','xxxxxx','xv','Total Actual Hrs']) #dropping unnecessary columns

df1['Actual Wage($)'] = (df1['Total Paid in Hrs'] * df1['Wage per hr ($)']) - df1['Unpaid Break Deducted $'] #calculating actual wage

# getting salary per employee per month
salary_per_month = pd.pivot_table(df1, index=['Name','Month'],values=['Actual Wage($)','Total Paid in Hrs'],aggfunc={'Total Paid in Hrs':np.sum,'Actual Wage($)':np.sum})

#df = pd.read_excel("/Users/andrew/Downloads/Payroll-datafile_pivot.xlsx",sheet_name='Sheet2')

# Assigning status for each employee for tax calculation purposes
Status = []
for item in salary_per_month['Name']:
    if item == 'Liz Brooklyn':
        status = 'Married filing jointly'
    elif item == 'Nayomi Linn':
        status = 'Head of Household'
    else:
        status = 'Single'
    Status.append(status)
    
salary_per_month['Status'] = Status

df = salary_per_month 

#Assigning a numerical  order for the months

def month_num(data): 
    Months = []
    for row in data:
        if row == 'January':
            month = 1 
        elif row == 'February':
            month = 2
        elif row == 'March':
            month = 3
        elif row == 'April':
            month = 4
        else:
            month = 5
        Months.append(month)
    return Months
    
months = month_num(df['Month'])

#Creating column for numeric representation of the month
df['month'] = months

#Sorting data for each employee by month so that it follows the order of the months
#Each sorted employee data is saved in a different dataframe
df_brian = df[:5].sort_values(by='month')
df_hamod = df[5:10].sort_values(by='month')
df_jon_josh = df[10:16].sort_values(by='month')
df_karen = df[16:20].sort_values(by='month')
df_liz = df[20:25].sort_values(by='month')
df_nayomi = df[25:30].sort_values(by='month')

#Concatenating the dataframes
df1 = pd.concat([df_brian,df_hamod,df_jon_josh,df_karen,df_liz,df_nayomi])

#df1 is saved on PC then edited in excel and reloaded
df2 = pd.read_csv("/Users/andrew/Downloads/internship files/payroll_data_reworked.csv") 


df2['Net pay($)'] = df2['Gross pay($)'] -df2['FIT (EE)'] -df2['SIT (EE)'] -df2['SS Tax (EE)'] -df2['Medicare (ER)'] #net pay calculation

#dropping employer payroll expenses so that employee pay stubs can be created
df2.drop(['month','SS Tax (ER)','Medicare (ER)','FUTA (ER)','SUTA (ER)'], axis =1, inplace=True) 

#df2 is saved on PC for editing in excel then reloaded
df2 = pd.read_excel('/Users/andrew/Downloads/internship files/payroll_data_reworked_4_paystub.xlsx')

#paystubs are printed
print('Pay stubs for company employees are below:')
for i,j in df2.iterrows(): 
    print(i,j)
    print()

#the file that combines employee and employer data is reloaded
df3 = pd.read_csv("/Users/andrew/Downloads/internship files/payroll_data_reworked.csv") 

#employee tax data is dropped so that full employer payroll expenses can be calculated
df3.drop(['Employee Name','Status','month','FIT (EE)','SIT (EE)','SS Tax (EE)','Medicare (EE)'], axis=1,inplace=True)

#total payroll expenditure for the company
df3['Total Expenditure per month']=df3['Gross pay($)']+df3['SS Tax (ER)']+df3['Medicare (ER)']+df3['FUTA (ER)']+df3['SUTA (ER)']

#total payroll expenditure per month for the company
df4 = pd.pivot_table(df3,index=['Company','Month'],values = ['Gross pay($)','SS Tax (ER)','Medicare (ER)','FUTA (ER)','SUTA (ER)'])

#dataframe is saved on PC
df5 = pd.read_excel("/Users/andrew/Downloads/internship files/Payroll_datafile_4company_pivot_edited.xlsx")

#months are assigned numerical order so that the company expenses per month can be sorted by month
months = month_num(df5['Month']) 
df5['month_']=months
df5 = df5.sort_values(by='month_') 
df5.drop(columns=['month_'],inplace=True)

#Company payroll expenses per month are printed
print('Anti Aging Company Employee expenditure for Jan - May 2023')
print(df5)
print("Total expenditure on salaries: ", round(df5['Total Expenditure per month'].sum(),3))
                     
                     




