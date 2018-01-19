# Pretty cheat sheets for my lazy ass self

-------------------------------------------------------------- 
# Common Mistakes

* In NumPy, the **shape** property starts from ONE. However the **arrays** property starts from zero.  
* If having problems converting data types, likely because NA, NaN, '' exist. Remove garbage and try again. 

-------------------------------------------------------------- 
# Workflows

Calculate the total amount of alcohol drank for each country, 
for a given year. 

```py
import numpy as np

data = np.genfromtxt("world_alcohol.csv", delimiter = ",", skip_header = 1, dtype = "U75")

totals = {}

# keep data from relevant year only
year = '1989'
is_year = (data[:,0] == year)
correct_data = data[is_year]

# loop through to find total for each country
for country in countries:    
    criteria = (correct_data[:,2] == country)
    country_consumption = correct_data[criteria]
    
    # replace '' with 0s then convert to float
    toberemoved = (country_consumption[:,4] == '')
    country_consumption[toberemoved, 4] = 0
    
    # sum it up
    alcohol_consumed = (country_consumption[:,4]).astype(float)    
    total_alcohol = alcohol_consumed.sum()
    
    # add to dictionary
    totals[country] = total_alcohol

print(totals)
```

-------------------------------------------------------------- 
### Working with CSV

Search the third column of file for number of times 'Patriots' appears. 

Using `csv` module: 
```py
import csv

searchterm = "New England Patriots"
patriots_wins = 0

with open('nfl.csv', 'r') as file:
     reader = csv.reader(file, delimiter=',')
     for row in reader:
          if searchterm == row[2]: 
              patriots_wins = patriots_wins + 1 
```
Using `numpy` module:
```py
import numpy as np

file = np.genfromtxt("filename.csv", delimiter = ","
                      skip_header = 1 # skip one row
                      dtype = "U75")  # read as unicode, see strings 
patriots = data[(data[:,2] == 'New England Patriots')]
patriots_wins = len(patriots) # length of array; num lists aka num rows
```

-------------------------------------------------------------- 
# NumPy

`nd-arrays` are a core data type of NumPy. A 1-dimensional array is often 
referred to as a **vector** while a 2-dimensional array is often referred to as a **matrix**. 
Meanwhile, items in that array are called **elements**.

```py
vector = np.array([10,20,30])
matrix = np.array([[5,10,15], # fuggin list of lists yo
                  [20,25,30],
                  [35,40,45]])
```

### Shape & Reshape

```py
x = np.array([[10,20,30],
             [1, 2, 3]]) # (2,3)
y = np.reshape(x, (3,2) # new dimensions here
y = np.reshape(x, (3, -1) # infers dimensions when left as -1
```
### Indexing

```py
middle_item = matrix[1][1]
allrows_third_column = matrix[:, 2] 
first_two_rows_allcols = matrix[0:2,:] 
```

### Replacing 

```py
toreplace = (data[:,0] == '1986') 
data[toreplace, 0] = '2014'

remove_NA = data[:,1] == 'NA' # select
data[remove_NA, 1] = '0' # replace
```

### Changing data types

```py
data = data.astype(float) 
```

### Math functions

For matrix, need to specify axis: `0` for `columns` and `1` for rows (alphabetical order!)

* `vector.mean()`
* `matrix.sum(axis = 0)`
* `matrix.max(axis = 1)`

### Standard data types

Check the type of a variable using `data.dtype`.

| Name | Description | Sub-Types |
| ---- | ----------- | --------- |
| bool | boolean | True, False |
| int  | integer | int16, int32, or int64
| float | floating point values | float16, float32, or float64
| string | String values, text | string, unicode |

-------------------------------------------------------------- 
# Pandas

### Viewing data

```py
first_rows = data.head()
data.head(3) 
column_names = data.columns
dimensions = data.shape # (x, y)
```

### Indexing 

```py
# DataFrame containing the ROWS 4, 5, 6, 7 returned.
data.loc[3:6]

# DataFrame containing the ROWS 2, 5, and 10 returned. 
food_info.loc[ [1,4,9] ]

# DataFrame with LAST 5 ROWS returned.
num_rows = data.shape[0]
last_rows = data.loc[num_rows-5:num_rows-1] # zero-index
```
Columns
```py
# one column
cats_column = data[cats]

# multiple columns
zinc_copper = food_info[["Zinc_(mg)", "Copper_(mg)"]]

```
