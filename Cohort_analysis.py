# ---------------------------------------------------------------------------- #
# Cohort analysis

### 1. Define order periods in buckets, e.g., of months
  # Convert strings/floats to DATE
  df['date'] = small_data['creationdate'].dt.date
  df['date'].value_counts() ##print dates
  # Split by month
  df['OrderPeriod'] = df.OrderDate.apply(lambda x: x.strftime('%Y-%m'))

### 2. Determine user cohort by their first order
  df.set_index('UserId', inplace=True)

  # Group by User Ids, create multi-index frame to select the minimum order date within each 
  df['CohortGroup'] = df.groupby(level=0)['OrderDate'].min().\
          # apply(lambda x: x.strftime('%Y-%m')) (remove this part)
  df.reset_index(inplace=True)
  
  # Reset date format to string for easy reference later
  df['date'].astype(str)
  df['CohortGroup'].astype(str)
  df.dtypes

### 3. Aggregate by users, orders within each month. Count number of users and total orders.

  grouped = df.groupby(['CohortGroup', 'OrderPeriod'])

  # count the unique users, orders, and total revenue per Group + Period
  cohorts = grouped.agg({'UserId': pd.Series.nunique,
                         'OrderId': pd.Series.nunique,
                         'TotalCharges': np.sum})

  # make the column names more meaningful
  cohorts.rename(columns={'UserId': 'TotalUsers',
                          'OrderId': 'TotalOrders'}, inplace=True)
  cohorts.head()  
  
### 4. Label the cohort groups with numbers for easy access later

  def cohort_period(df):
      df['CohortPeriod'] = np.arange(len(df)) + 1
      return df

  cohorts = cohorts.groupby(level=0).apply(cohort_period)
  cohorts.head()
  
### 5. Find retention by cohort period and size. start by finding size of
       #each cohort group.
  
  # Method1: 
  # reindex the DataFrame
  cohorts.reset_index(inplace=True)
  cohorts.set_index(['CohortGroup', 'CohortPeriod'], inplace=True)

  # create a Series holding the total size of each CohortGroup
  cohort_group_size = cohorts['TotalUsers'].groupby(level=0).first()
  cohort_group_size.head()
  
  # Method 2: 
  # convert the aggregated pivot table to new dataframe for counting
  forsize = pd.DataFrame(cohorts.to_records())

  # Sum up users in each cohort group
  uniquegroups = forsize['CohortGroup'].unique()
  cohort_group_size = {}
  for groups in uniquegroups:
      groupsize = forsize['TotalUsers'][forsize['CohortGroup'] == groups].sum()
      cohort_group_size[groups] = groupsize

  # convert dictionary to series, "cohort_group_size"
  cohort_group_size = pd.Series(cohort_group_size, name='totalusers')
  cohort_group_size.index.name = 'cohortgroup'
  cohort_group_size.head()

### 6. Create matrix of cohort periods X days
  cohorts['TotalUsers'].unstack(0).head()

### 7. Divide by cohort size to get weighted percentage of how many users were engaged in each period
  user_retention = cohorts['TotalUsers'].unstack(0).divide(cohort_group_size, axis=1)

### 8. MAKE PLOTS
  user_retention[['2009-06', '2009-07', '2009-08']].plot(figsize=(10,5))
  plt.title('Cohorts: User Retention')
  plt.xticks(np.arange(1, 12.1, 1))
  plt.xlim(1, 12)
  plt.ylabel('% of Cohort Purchasing');
  
  # PLOT FOR SEABORN HEATMAP
  import seaborn as sns
  sns.set(style='white')

  plt.figure(figsize=(12, 8))
  plt.title('Cohorts: User Retention')
  sns.heatmap(user_retention.T, mask=user_retention.T.isnull(), annot=True, fmt='.0%');
  # source: http://www.gregreda.com/2015/08/23/cohort-analysis-with-python/
