
x = ("Split lines \
  like this")

# prints types, counts, titles
data.info()

# gives quartiles, means
data.describe(include = 'all') 

# Create new dataframe
exchangerate = pd.DataFrame([['THB', 0.0415],
                             ['MYR', 3.35],
                             ['SGD', 1],
                             ['IDR', 0.000415]], # includes exponents 
                            columns=['currencycode','exchg_value'])
# ---------------------------------------------------------------------------- #
# Dictionary

# Can have mixed keys (i.e., string, integer)
my_dict = {'name': 'John', 1: [2, 4, 3]}
my_dict = dict({1:'apple', 2:'ball'}) ## dict()
my_dict = dict([(1,'apple'), (2,'ball')]) ## from sequence

# Calling values from keys:
print(my_dict['name'])
print(my_dict.get('age')) ## get value by key name

# Remove a key
my_dict.pop(4) #remove key-pair with '4'
my_dict.popitem() ##remove random item
del my_dict[5] ##remove index 5

# ---------------------------------------------------------------------------- #
# Sorting Data

# Sorts the DataFrame in-place, rather than returning a new DataFrame.
df.sort_values("col1", inplace=True)

# Descending Order
df.sort_values("col1", inplace=True, ascending=False)

# ---------------------------------------------------------------------------- #
# Null, NaN, Missing Data

# Find & count how many null values in a column

  target = df['column_name']
  null_values = target[pd.isnull(target)]
  non_null_values = target[pd.NOTnull(target)]
  count_null = len(null_values)

""" Notes: Functions like MEAN() automatically exclude NULL values """

# Count null values in EACH COLUMN within a dataframe

  def count_null(column):
      x = column[column.isnull()]
      x = len(x)
      return x 
  column_null_count = df.apply(count_null)

# Drop rows/columns with NA

"""
DROP ROWS: Specifying axis=0 or axis='index' will drop any rows that have null values. [r-0-ws]
DROP COLUMNS: Specifying axis=1 or axis='columns' will drop any columns that have null values. [co-1-umns] 
Note: opposite of APPLY() function which applies functions to each rows (axis = 1) or columns (axis = 0)
"""

# Drops rows/columns
drop_na_rows = df.dropna(axis=0)
drop_na_columns = df.dropna(axis=1)

# Drop within subset of column names
drop_na_subset = df.dropna(axis=0, subset = ["age", "sex"])

# Drop rows that have at least 2 non-NA values
drop_na_subset = df.dropna(axis=0, subset = ["age", "sex"], thresh=2)

# ---------------------------------------------------------------------------- #
# Subset & Filter

# STANDARD SELECTION USING ILOC, LOC
  """ 
  LOC = column label
  ILOC = column INDEX 
  """
one_row_one_col = df.iloc[0,0]
all_rows_one-to-three_columns = df.iloc[:,0:3]
row_index_123_col1 = df.loc[123,"col1"]

# Iterate over list, use column1 to filter, then find MEAN value for column2

  col1 = [1, 2, 3]
  mean_by_levels = {}

  for levels in col1:
      target = df['col1'] == levels
      mean_values = df[target]['col2'].mean()
      fares_by_class[levels] = mean_values
      
# Iterate all levels of column1, then find the MEAN value for each on column2

  unique_ranks = df['col1'].unique()
  output = dict()

  for ranks in unique_ranks:
      subset = df[df['col1'] == ranks]
      total_per_group = subset['col2'].sum()
      output[ranks] = total_per_group

# Select rows with first name Antonio, # and all columns between 'city' and 'email'
df.loc[df['first_name'] == 'Antonio', 'city':'email']
df.loc[df['first_name'] == 'Antonio', [1:4]]

# Select rows where the email column ends with 'hotmail.com', include all columns
df.loc[df['email'].str.endswith("hotmail.com")]   
 
# Select rows with first_name equal to some values, retrieve all columns
df.loc[df['first_name'].isin(['France', 'Tyisha', 'Eric'])]   
       
# Select rows with first name Antonio AND has a gmail addresses
df.loc[df['email'].str.endswith("gmail.com") & (df['first_name'] == 'Antonio')] 
 
# select rows with id column between 100 and 200, and just return 'postal' and 'web' 
df.loc[(df['id'] > 100) & (df['id'] <= 200), ['postal', 'web']] 
 
# A lambda function that yields True/False values can also be used.
  # Method 1
  # Select rows where the company name has 4 words in it.
  df.loc[df['company_name'].apply(lambda x: len(x.split(' ')) == 4)] 

  # Method 2
  # Retrieve all rows with company names with 4 words 
  subset = df['company_name'].apply(lambda x: len(x.split(' ')) == 4)
  # Select only the True values in 'idx' and only the 3 columns specified:
  df.loc[subset, ['email', 'first_name', 'company']]

# ---------------------------------------------------------------------------- #
# Pivot table

# As dataframe, include [] brackets
output = df.pivot_table(index = ["groupby1", "groupby2"], 
                        values = ["value1", "value2"], 
                        aggfunc = np.mean)

# As Series object, leave out [] brackets
output = df.pivot_table(index = "col1", 
                        values = "col2",
                        aggfunc = np.mean)

# Aggregate multiple columns in different ways:
output = df.groupby('group_by_col').aggregate({'col1':np.sum, 
                                               'col2':np.mean, 
          'col3': lambda x: x.value_counts().count}) # count unique, drop NAs
                                               
# Flatten pivot table as dataframe
new_df = pd.DataFrame(old_df.to_records())
new_df.columns = ['name1', 'name2', 'name3']

# ---------------------------------------------------------------------------- #
# Reset index 

# Creates new column with old index
df_reindexed = df.reset_index(drop=True)

# ---------------------------------------------------------------------------- #
# Functions

# For each level of X (column1), find the mean value of Y (column2)
  results = {}
  Types_of_X = df['column1'].unique()
  for X in Types_of_X:
      subset = df[df['column1'] == X]
      avg_Y = subset['column2'].mean()
      results[X] = avg_Y

# For all approved values, flag active as 1
df['final_state'] = 0         # reset all to declined first
df["final_state"][df['target'].str.contains("APPROVED")] = 1

# ---------------------------------------------------------------------------- #
# Join tables

# Join
all_data = df1.join(df2.set_index('df2_column'), on = 'df1_column')

# Merge
all_data = pd.merge(df1, df2, how='left', left_on=['df1_column'], right_on=['df2_column'])

# Group by 
df.groupby(['index'])
df.groupby(['index', 'index2'])['values'].mean()

# ---------------------------------------------------------------------------- #
# Graphs

# !pip install ggplot
from ggplot import *

# Bar Charts
ggplot(aes(x='factor(variable)', 
           weight='variable', 
           fill = 'variable'), 
       data = df) + \
            ylim(0.80, 1.0) + \
     geom_bar() + facet_wrap('variable')
                                               
# ---------------------------------------------------------------------------- #
# MODELS

# Linear Regression 
import statsmodels.api as sm
from sklearn import datasets ## imports datasets from scikit-learn

# Load data
data = datasets.load_boston()

# define the data/predictors as the pre-set feature names  
df = pd.DataFrame(data.data, columns=data.feature_names)

# Put the X values (housing value -- 'MEDV') in another DataFrame
target = pd.DataFrame(data.target, columns=["MEDV"])

## Define columns 
X = df[['RM', 'LSTAT']] ## add other columns in here
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model, OPTIONAL
y = target['MEDV']

# Note the difference in argument order
model = sm.OLS(y, X).fit()
predictions = model.predict(X) # make the predictions by the model

# Print out the statistics
model.summary()


