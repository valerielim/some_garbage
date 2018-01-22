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
1_row_1_col = df.iloc[0,0]
all_rows_1-3_columns = df.iloc[:,0:3]
row_index_123_col1 = df.loc[123,"col1"]

# Iterate over list, use column1 to filter, then find MEAN value for column2

  col1 = [1, 2, 3]
  mean_by_levels = {}

  for levels in col1:
      target = df['col1'] == levels
      mean_values = df[target]['col2'].mean()
      fares_by_class[levels] = mean_values
      
# Select rows with first name Antonio, # and all columns between 'city' and 'email'
df.loc[df['first_name'] == 'Antonio', 'city':'email']
 
# Select rows where the email column ends with 'hotmail.com', include all columns
df.loc[df['email'].str.endswith("hotmail.com")]   
 
# Select rows with first_name equal to some values, search in all columns
df.loc[df['first_name'].isin(['France', 'Tyisha', 'Eric'])]   
       
# Select rows with first name Antonio AND has a gmail addresses
df.loc[df['email'].str.endswith("gmail.com") & (df['first_name'] == 'Antonio')] 
 
# select rows with id column between 100 and 200, and just return 'postal' and 'web' columns
df.loc[(df['id'] > 100) & (df['id'] <= 200), ['postal', 'web']] 
 
# A lambda function that yields True/False values can also be used.
# Select rows where the company name has 4 words in it.
df.loc[df['company_name'].apply(lambda x: len(x.split(' ')) == 4)] 
 
# Selections can be achieved outside of the main .loc for clarity:
  # Form a separate variable with your selections:
  idx = df['company_name'].apply(lambda x: len(x.split(' ')) == 4)
  # Select only the True values in 'idx' and only the 3 columns specified:
  df.loc[idx, ['email', 'first_name', 'company']]

# ---------------------------------------------------------------------------- #
# Pivot table

# As dataframe, include [] brackets
output = df.pivot_table(index = ["groupby1", "groupby2"], 
                        values = ["value1", "value2], 
                        aggfunc = np.mean)
       
# As Series object, leave out [] brackets
output = df.pivot_table(index = "col1", 
                        values = "col2",
                        aggfunc = np.mean)
# ---------------------------------------------------------------------------- #
# Reset index 
titanic_reindexed = new_titanic_survival.reset_index(drop=True)
