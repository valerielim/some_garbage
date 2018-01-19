# Workings for Thanksgiving exercise 
# Date: 18-19 Jan 2018
# Course: Working Project, DataQuest

import pandas as pd
import numpy as np
import re 

data = pd.read_csv("thanksgiving.csv", encoding = "Latin-1")

# Check out first few rows
data.head()

# check out column names
data.columns

# Q1: How many people celebrate thanksgiving? 
thanksgiving = data['Do you celebrate Thanksgiving?']
thanksgiving.value_counts()

>>> output
Yes    980
No      78
Name: Do you celebrate Thanksgiving?, dtype: int64

# Q2: What's the main dish at your thanksgiving?
data['What is typically the main dish at your Thanksgiving dinner?'].value_counts()

>>> output
Turkey                    859
Other (please specify)     35
Ham/Pork                   29
Tofurkey                   20
Chicken                    12
Roast beef                 11
I don't know                5
Turducken                   3
Name: What is typically the main dish at your Thanksgiving dinner?, dtype: int64

# Q3: Of those who eat Tofurkey, do they typically have gravy?
maindishqn = data['What is typically the main dish at your Thanksgiving dinner?']
tofurkey = data.loc[maindishqn == 'Tofurkey']
tofurkey['Do you typically have gravy?'].value_counts()

>>> output
Yes    12
No      8
Name: Do you typically have gravy?, dtype: int64

# Q4: How many people ate pies?
# Notes: there are 3 types of pies; people who did NOT eat will have null values in that column
apples_isnull = data['Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Apple'].isnull()
pumpkin_isnull = data['Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pumpkin'].isnull()
pecan_isnull = data['Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pecan'].isnull()

ate_pies = (apples_isnull & pumpkin_isnull & pecan_isnull)
ate_pies.value_counts()

>>> output 
False    876
True     182
dtype: int64

# Q5a: Age
# How many people of each age are there? 

age = data['Age']     
age.value_counts()

>>> output 
45 - 59    286
60+        264
30 - 44    259
18 - 29    216
Name: Age, dtype: int64

# Q5b: Clean the age up to reflect only the first digit in that string.

def clean_age(in_str):
    if pd.isnull(in_str):
        return None
    else:
        split_str = in_str.split(" ")
        age_str = re.sub('\+$', '', split_str[0])
        return int(age_str)

# Apply:
data['int_age'] = data['Age'].apply(get_int_age)
int_age.describe()

count    1025.000000
mean       39.383415
std        15.398493
min        18.000000
25%        30.000000
50%        45.000000
75%        60.000000
max        60.000000
Name: Age, dtype: float64

# Q6: Income
# Clean up the income column to reflect only the first value of each bucket.

def clean_income(income):
    if pd.isnull(income):
        return None
    elif income == "Prefer not to answer":
        return None
    elif income == "$200,000 and up":
        return int(200000)
    else:
        split_str = income.split(" to ")
        income_str = re.sub('[\$\,]', '', split_str[0])
        return int(income_str)

# single instance cases
test1 = "$75,000 to $99,999"
test2 = "Prefer not to answer"
test3 = "$200,000 and up"
test4 = None
test5 = "$0 to $9,999"

# test
clean_income(test1)

# Apply
income_input = data['How much total combined money did all members of your HOUSEHOLD earn last year?']
data['int_income'] = income_input.apply(clean_income)
data['int_income'].value_counts()

# Q8: Will poorer people travel farther to join family for thanksgiving? 
# Notes: Split income at $150K boundary.

lowincome = data["int_income"] < 150000.0
lowincome = data[lowincome]
lowincome['How far will you travel for Thanksgiving?'].value_counts()

highincome = data["int_income"] >= 150000.0
highincome = data[highincome]
highincome['How far will you travel for Thanksgiving?'].value_counts()

# Q9: Make a pivot table: Will younger people have more "friendsgiving", 
# or be more likely to attend one with friends?

pd.pivot_table(data,
               index=['Have you ever tried to meet up with hometown friends on Thanksgiving night?'],
               values=["int_age"],
               columns=['Have you ever attended a "Friendsgiving?"'],
               aggfunc=[np.mean])


