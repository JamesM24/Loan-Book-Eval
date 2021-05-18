#!/usr/bin/env python
# coding: utf-8

# In[55]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


# In[56]:


#Import Loan Book as a pandas data frame
loan_data = pd.read_csv('Loan Book.csv')


# In[57]:


type(loan_data)


# In[58]:


#Import Property Data as a pandas data frame
property_data = pd.read_csv('Property Data.csv')


# In[59]:


type(property_data)


# In[60]:


type(property_data['Original Value'])


# In[61]:


property_data.dtypes


# In[62]:


loan_data.dtypes


# In[63]:


#Remove commas / spaces from the values in the data set 

property_data['Original Value'] = property_data['Original Value'].str.replace(',', '')


# Examine the Data to take useful metrics and identify how to analyse the data.

# In[64]:


property_data['Original Value'] = pd.to_numeric(property_data['Original Value'])


# In[65]:


# To see the values that emp_length takes
loan_data['Borrower ID'].nunique()


# In[66]:


loan_data['Original Loan Term (in Months)'].nunique()


# In[67]:


loan_data['Loan Start Date'].nunique()


# In[68]:


loan_data['Original Loan Term (in Months)'].unique()


# In[69]:


#To see the values that emp_length takes
loan_data['Current Nominal Rate'].unique()


# In[70]:


loan_data['Current Nominal Rate'].nunique()


# In[71]:


property_data['Property Location'].unique()


# In[72]:


# Find the number of properties in each region
property_data.pivot_table(index=['Property Location'], aggfunc='size')


# In[73]:


#Number of individual borrowers
loan_data['Borrower ID'].nunique()


# In[74]:


type(property_data['Property Location'])


# In[75]:


#convert to a string so .groupby can be used
property_data['Property Location'].apply(str)


# In[76]:


property_data['Original Value'].apply(str)


# In[77]:


#Total valuation by region will be helpful when analysing the loan book.
property_sums = property_data.groupby('Property Location')['Original Value'].sum()


# In[78]:


# Print the total property values by region
print(property_sums)


# In[79]:


property_sums.plot.barh(color='green') 


# The next step is to define a series of functions which return the output we want. In this case the total amount of interest paid over the life time of the loan and the total monthly loan repayment with a changing reverse interest rate and change in balance of principal payment and interest payment.

# In[80]:


#Define a function which calculates the total interest paid over the lifetime of each loan.

def cumulative_interest(start_date,repayment_amount,months_period, loan_amount, initial_interest, final_interest, reversion_date):
    date = start_date
    delta = timedelta(days=30*int(months_period))
    outstanding_loan_amount = int(loan_amount)
    total_interest = 0
    while outstanding_loan_amount>0:
        interest_paid = initial_interest * outstanding_loan_amount
        total_interest += interest_paid
        outstanding_loan_amount -= repayment_amount
        date += delta
        print(date, outstanding_loan_amount, interest_paid)
    return(total_interest)


# In[81]:


#Define a function which calculates the monthly payment with a fixed interest rate

def single_rate_payment(p,n,r):
  r = r /100.0
  rf = (1 + r)**n
  c = r*p*rf/(rf - 1)
  return c

#Define a function which calculates the monthly payment with a changing rate (reverse rate)

def monthly_payment(loan_amount,periods_to_today,original_rate_period,original_rate,reverse_rate):
  P = loan_amount
  N = periods_to_today
  M = original_rate_period
  r = original_rate / 100
  s = reverse_rate / 100
  ifr = (1 + r) ** M
  ifs = (1 + s) ** (N - M)
  C = r*P*ifr*ifs/(ifr*ifs - 1)
  return C


# In[82]:


#call function and print total monthly repayment for a test loan.

monthly = monthly_payment(12000, 180, 60, 5.35, 4.30)
print(monthly)


# In[87]:


#call function for cumulative interest over the loan's life time using a test loan.

time_in_string = "01-01-2005"
test_date = datetime.strptime(time_in_string, "%d-%m-%Y")
total_paid_interest = cumulative_interest(test_date, 642, 230, 12000, 0.053, 0.043, "2015-05-10")
print(total_paid_interest) 


# In[84]:


total_loan_payment = (total_paid_interest + 12000)
print(total_loan_payment)


# The final stage is to take the functions and apply them to the data frame instead of having to input individual loan data as we have done so far.

# In[35]:


loan_data['Monthly payment'] = loan_data.apply(monthly_payment('Original Loan', 'Loan To Today', 'Original Rate Period', 'Original Rate', 'Current Nominal Rate'), axis=1)


# In[ ]:




