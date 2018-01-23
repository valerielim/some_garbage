
# coding: utf-8

# # Reworking AdYen
# 
# Date: 21st Jan 2018
# 
# Desc: Running through old process for test prac. Topics include cohort analysis, idenitfying, measuring and predicting churn.

# In[338]:


# Set up workspace, import files
import numpy as np
import pandas as pd
import os 

path = 'C:\\Users\\valeriehy.lim\\Documents\\Google Admin\\AdYen' 
newdir = os.chdir(path)
os.getcwd()
os.listdir()


# # Load and clean all csv files

# ### 1. Notes on Payments File
# 
# * **Pspreference**. Payment Service Provider Reference; an unique id we use to keep track of the payments on our platform.
# * **Txvariantid**. Transaction variant identification; an unique id to identify the different payment types.
# * **BIN**. Bank Identification Number - first 6 digits of every card to identify the card type.
# * **Shopper Reference**. An unique reference created by the merchant to keep track of the shoppers.
# * **RawAcquirerResponse**. The response we receive for the outcome of the transactions (tied to generic response to cluster the responses into groups).
# * **Issuercountrycode** refers to the country of the issuing card (Issuers refers to the distributor of cards; usually the banks).

# In[339]:


payment = pd.read_csv("payment.csv")
payment.head(5)


# ### 2. Notes on TX Table
# 
# * **Txvariantid**. Transaction variant identification; an unique id to identify the different payment types.
# * **Txvariantcode**. The description for the txvariantid.
# * **Displayabletxvariantcode**. For the case study, the displayabletxvariantcode would refer to the funding source; i.e. credit or debit or etc (supposedly parent description for the txvariantcode).

# In[340]:


txvariant = pd.read_csv("txvariant.csv")
txvariant.describe(include='all')


# In[341]:


# extract only necessary columns
txvariant = txvariant[['txvariantid', 'txvariant', 'displayabletxvariantcode']]
txvariant.columns = ['txvariantid', 'paymentmethod', 'fundingsource']
txvariant.head()


# ### 3. Notes on Accounts
# 
# * Account Table contains the information for Merchant/Company/Acquirer/AcquireAccount.
# * Merchant account is listed under Company Account and thus for merchant accounts the parentid will be the company account id. Same goes for AcquirerAccount where an Acquirer has multiple AcquirerAccounts.
# * Join them separately to obtain the names for Merchant/Company/Acquirer/AcquirerAccount.
# 
# #### To Do: Will melt and reshape the Accounts table as separate columns for Merchants, Company, Acquirer, and Acquirer Accounts.

# In[342]:


account = pd.read_csv("account.csv")
account.head()


# In[343]:


merchantaccount = account.loc[account["accounttypeid"] == 9, ['accountcode', 'accountid']] 
merchantaccount.rename(columns = {'accountcode':'merchant'}, inplace = True)

companyaccount = account.loc[account["accounttypeid"] == 7, ['accountcode', 'accountid']] 
companyaccount.rename(columns = {'accountcode':'company'}, inplace = True)

acquireraccount = account.loc[account["accounttypeid"] == 3, ['accountcode', 'accountid']] 
acquireraccount.rename(columns = {'accountcode':'acquirer_account'}, inplace = True)

acquirer = account.loc[account["accounttypeid"] == 8, ['accountcode', 'accountid']] 
acquirer.rename(columns = {'accountcode':'acquirer'}, inplace = True)


# ### 4. Notes on Journal
# 
# The journal type of each transaction marks their status.
# 
# Live transactions fall under **“Received”** and could be turned into **“Cancelled”**, **”Authorized”**,
# **”SentforSettle”** and **“Settled”**.
# 
# #### Notes to self: Clean same way as Accounts file: Extract column for `journaltypeid` and save that for merging with main df later. 

# In[344]:


journal = pd.read_csv("journaltype.csv")
journal.columns = ['journaltypeid', 'journal_status'] # rename: journaltype
journal.head()


# ### 5. Notes on Currency table
# 
# As multiple currencies are involved in both processing and settlement currencies of the merchants,
# we have a currency table (original table has daily exchange rates and so on; it’s simplified in this scenario).
# 
# > **Exponent** refers to the _ISO 4217 Standard_ - where banks and businesses all around the world uses to
# define the major currency unit versus minor unit. 
# >
# > For example, USD has an exponent of 2; USD$1 is stored as 100 
# in the database. JPY, with an exponent of 0, has ¥100 been stored as 100 in the database as well.
# >
# >This would mean that, when looking at amounts, currency USD with an amount value of 100 would have to be
# divided by 10^2 to get the actual value; while for JPY it is “not needed” or divided by 10^0.
# 
# #### Notes to self: Clean up currency table to standard form ;ater

# In[345]:


currency = pd.read_csv("currency.csv")
currency.describe(include= "all")
currency.head(10)


# In[346]:


payment.head(5)


# In[347]:


# Join all 5 files

all_data = payment.join(merchantaccount.set_index('accountid'), on = 'merchantaccountid')
all_data = all_data.join(acquireraccount.set_index('accountid'), on = 'acquireraccountid')
all_data = all_data.join(acquirer.set_index('accountid'), on = 'acquirerid')
all_data = all_data.join(journal.set_index('journaltypeid'), on = 'journaltypeid')
all_data = all_data.join(currency.set_index('currencyid'), on = 'currencyid')
all_data = all_data.join(txvariant.set_index('txvariantid'), on = 'txvariantid')
# drop: merchantaccountid, 'Unnamed: 0', 'acquireraccountid', 'journaltypeid', 'currencyid', 'txvariantid'


# # Clean, Format, Shrink dataset

# In[348]:


# dont need the old index
small_data = all_data.drop(['Unnamed: 0'], axis=1)

# drop all duplicated key columns
small_data = small_data.drop(['txvariantid', 'companyaccountid', 'merchantaccountid', 'acquirerid', 'acquireraccountid',
                   'journaltypeid'], axis=1) 

# drop other irrelevant columns to task
small_data = small_data.drop(['directoryresponse', # duplicate
                    'pspreference', # platform creates this for each transaction
                   'shopperreference' # merchants create this for each of their shoppers
                   ], axis=1)


# ## Create new column for overall approved and declined transactions

# In[349]:


small_data['genericresponse'].value_counts()


# In[350]:


# create new column to count approved, declined transactions

small_data['final_state'] = 0         # reset all to declined first
small_data["final_state"][small_data['genericresponse'].str.contains("APPROVED")] = 1
small_data['final_state'].value_counts()


# ## Sort out currency to single unit
# 
# 1. Multiply `exchange rate` by `transaction amount`
# * Divide by 10 to the power of the `exponent`
# * Round float to 2 decimal places
# 

# In[351]:


small_data.groupby(['currencycode'])['exponent'].mean()  # exponent should be the same so mean shouldnt matter


# In[352]:


# Create new exchange rate
exchangerate = pd.DataFrame([['THB', 0.0415],
                             ['MYR', 3.35],
                             ['SGD', 1],
                             ['IDR', 0.000415]], # includes exponents 
                            columns=['currencycode','exchg_value'])

# merge
small_data = pd.merge(small_data, exchangerate, how='left', left_on=['currencycode'], right_on=['currencycode'])

# calculations
small_data['SGD_amount'] = small_data['amount'] * small_data['exchg_value'] / (10 ^ small_data['exponent'])
small_data = small_data.round({'SGD_amount':2})


# ## Clean up Date format

# In[353]:


# convert format
small_data['creationdate'] = pd.to_datetime(small_data['creationdate'])

# keep date only
small_data['date'] = small_data['creationdate'].dt.date
# updated['date'].value_counts() # Not run: basically contains ALL dates in OCT


# ## Check NULL values

# In[354]:


# Count null values per column

def count_null(column):
    x = column[column.isnull()]
    x = len(x)
    return x 

small_data.apply(count_null)


# ## Final: Drop unnecessary columns

# In[355]:


# clean up table
clean_data = small_data.drop(['currencyid', 'amount', 'exponent', 'exchg_value', "creationdate", 
                        "rawacquirerresponse", "genericresponse"], axis=1)
clean_data.head()


# # Exploratory Graphs

# In[356]:


import matplotlib as plt
pd.options.display.mpl_style = 'default'


# In[357]:


clean_data.groupby('final_state').SGD_amount.hist(alpha=0.4)


# In[358]:


import matplotlib.pyplot as plt

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()


# In[359]:


# !pip install ggplot
from ggplot import *
ggplot(aes(x='factor(merchant)', weight='final_state'), data=clean_data) +             ylim(0.80, 1.0) +      geom_bar(colour='black') + facet_wrap('currencycode')


# # General queries

# ## What percentage of transactions succeeded for each merchant?

# In[360]:


results = {}
categories = clean_data['merchant'].unique()

for category in categories:
    category_data = clean_data[clean_data['merchant'] == category]

    # find total number of transactions attempted
    total_attempted = category_data.shape[0] # total rows

    # find total number of transactions succeeded
    passed = category_data[category_data['final_state'] == 1]
    succeeded = passed.shape[0]

    # percentage successful
    perc_successful = round(succeeded / total_attempted, 2)
    results[category] = perc_successful

results


# # What percentage of transactions succeeded for each payment method?

# In[361]:


results = {}
categories = clean_data['paymentmethod'].unique()

for category in categories:
    category_data = clean_data[clean_data['paymentmethod'] == category]

    # find total number of transactions attempted
    total_attempted = category_data.shape[0] # total rows

    # find total number of transactions succeeded
    passed = category_data[category_data['final_state'] == 1]
    succeeded = passed.shape[0]

    # percentage successful
    perc_successful = round(succeeded / total_attempted, 2)
    results[category] = perc_successful

results


# # How about authentication rates by currency and company?

# In[362]:


output = clean_data.groupby([#'acquirer_account',
                          'currencycode', 
                          'merchant']).\
aggregate({'final_state':np.mean}).\
sort_values('final_state', ascending = False) # count unique, drop NAs
output = pd.DataFrame(output.to_records())
output


# In[363]:


# acquirer, paymentmethod, countrycode, merchant, bin
# issuercountrycode, bin, merchant, acquirer_account, paymentmethod

output = clean_data.groupby(['acquirer_account', 'paymentmethod','currencycode', 'issuercountrycode', 'bin', 'merchant']).aggregate({'final_state':np.mean, 'acquirer': 'count'}).sort_values("final_state", ascending=False) # count unique, drop NAs


# # Cohort Analysis
# 
# * Treat each row as one transaction
# * Define our cohort timeframe in DAYS (gross, but we only have 1 mth of data, might as well chop it up)
# * Treat each bin as a 'customer id'. 
# 
# *Note: If want to use other variables (i.e., names, merchants), must convert the column to numeric / assign a number, for the sake of setting an index.*

# ## Create new column for the FIRST time any transaction was routed through a 'merchant' (bin)

# In[364]:


# create copy
dupe_data = clean_data

# create new bins
dupe_data.set_index('bin', inplace=True)
dupe_data['CohortGroup'] = dupe_data.groupby(level=0)['date'].min()
dupe_data.reset_index(inplace=True)


# In[365]:


# interrupt to CONVERT DATE TO STRING
dupe_data['date'].astype(str)
dupe_data['CohortGroup'].astype(str)
dupe_data.dtypes


# ## Aggregate by CohortGroup and OrderPeriod (the transaction period)

# In[366]:


# grouped = data.groupby(['CohortGroup', 'date'])

# Create new column with fake "order ID" to identify rows
dupe_data['Transaction_ID'] = dupe_data.index + 1


# In[400]:


# Group by stuff
grouped = dupe_data.groupby(['CohortGroup', 'OrderPeriod'])

# count the unique users, orders, and total revenue per Group + Period
cohorts = grouped.agg({'bin': pd.Series.nunique,
                       'Transaction_ID': pd.Series.nunique,
                       'SGD_amount': np.sum})

# make the column names more meaningful
cohorts.rename(columns={'bin': 'TotalUsers',
                        'Transaction_ID': 'TotalOrders',
                       'SGD_amount': 'TotalValue'}, inplace=True)
cohorts.head(5)


# ## Create new column with numbers representing each CohortGroup

# In[368]:


def cohort_period(df):
    df['OrderPeriod'] = np.arange(len(df)) + 1
    return df

cohorts = cohorts.groupby(level=0).apply(cohort_period)
cohorts.head()


# # User retention/ engagement by Cohort Group
# 
# * Find total size of each cohort group
# * Divide OrderPeriod total by CohortGroup total to get percentage

# ## Find total of each cohort group

# In[369]:


# convert pivot table to new dataframe for counting
forsize = pd.DataFrame(cohorts.to_records())

# Sum up users in each cohort group
uniquegroups = forsize['CohortGroup'].unique()
cohort_group_size = {}
for groups in uniquegroups:
    groupsize = forsize['TotalUsers'][forsize['CohortGroup'] == groups].sum()
    cohort_group_size[groups] = groupsize

# convert dictionary to series  
cohort_group_size = pd.Series(cohort_group_size, name='totalusers')
cohort_group_size.index.name = 'cohortgroup'
cohort_group_size.head()


# ## Unstack and Divide users by their total cohort

# In[370]:


cohorts['TotalUsers'].unstack(0)


# In[371]:


user_retention = cohorts['TotalUsers'].unstack(0).divide(cohort_group_size, axis=1)
user_retention


# columns = ['2017-10-01a', '2017-10-02', '2017-10-03', '2017-10-04', '2017-10-05', '2017-10-06',
#        '2017-10-07', '2017-10-08', '2017-10-09', '2017-10-10', '2017-10-11', '2017-10-12',
#        '2017-10-13', '2017-10-14', '2017-10-15', '2017-10-16', '2017-10-17', '2017-10-18',
#        '2017-10-19', '2017-10-20', '2017-10-21', '2017-10-22', '2017-10-23', '2017-10-24',
#        '2017-10-25', '2017-10-26', '2017-10-27', '2017-10-28', '2017-10-29', '2017-10-30',
#        '2017-10-31']
# a = user_retention.reindex(columns = columns)

# In[372]:


import matplotlib.pyplot as plt
import matplotlib as mpl


# In[373]:


user_retention.plot(figsize=(10,5))
plt.title('Cohorts: User Retention')
plt.xticks(np.arange(1, 10, 1))
plt.xlim(1, 10)
plt.ylabel('% of Cohort Purchasing');


# In[374]:


import seaborn as sns
sns.set(style='white')

plt.figure(figsize=(12, 8))
plt.title('Cohorts: User Retention')
sns.heatmap(user_retention, mask=user_retention.isnull(), annot=True, fmt='.0%');


# # Linear & Logistic Models

# In[375]:


import statsmodels.api as sm
from sklearn import datasets ## imports datasets from scikit-learn
# data = datasets.load_boston()


# In[376]:


clean_data.head()


# In[386]:


# define the data/predictors as the pre-set feature names  
# data = clean_data

# Put the target (housing value -- MEDV) in another DataFrame
target = pd.DataFrame(clean_data, columns=["SGD_amount"])


# In[392]:


# with two Y variables now
import statsmodels.api as sm 

X = clean_data[['bin']] ## add other columns in here
# X = sm.add_constant(X) ## Coeff reduces predictability
y = clean_data["SGD_amount"] ## output column
model = sm.OLS(y, X).fit()
predictions = model.predict(X)
model.summary()

# obviously this is a horrible correlation hypothesis and should be put to sleep 


# ## Results: 
# 
# * R-squared value (percentage of variance explained) is highest with X model
# * Co-efficient values read: Y = 4.90RM - 0.65LSTAT

# # Logistic Regression

# In[397]:


import pylab as pl

clean_data.hist()
pl.show()

