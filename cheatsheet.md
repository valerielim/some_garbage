# Cheat sheets for lazy people 

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

`nd-arrays` are a core data type of NumPy. 
A 1-dimensional array is often referred to as a **vector** while a 2-dimensional array is often referred to as a **matrix**. 
Meanwhile, items in that array are called **elements**.

```py
vector = np.array([10,20,30])
matrix = np.array([[5,10,15], # fuggin list of lists yo
                  [20,25,30],
                  [35,40,45]])
```
### Indexing

* Row : Column 
* Remember that it starts from ZERO!!! noob.
```
middle_item = matrix[1][1]
thirty-five = matrix[2][0]

third_column = matrix[:, 2] 
first_two_rows = matrix[0:2,:] 
first_two_columns = matrix[:,0:2] 
```

This is different from measuring the length/ size of the object. 

* For ndarrays, the **shape** property contains a `tuple` with `n` elements (it's dimensions). 
* Unlike indexes, tuples start from ONE, not zero, because it counts items.

```py
vector = numpy.array([1, 2, 3, 4])
vector_shape = vector.shape() # wrong
print(vector.shape) # correct, output is (4, ) # four items
```

### Data manipulation

**Replace items in matrix**

```py
# Replace 1986 with 2014 within the first column
toreplace = (data[:,0] == '1986') 
data[toreplace, 0] = '2014'
```

**Change the data type**

* May will return an error if there are empty strings, NA, or NaN
* Best to select and remove all of them first 

```py
data = np.genfromtext( ... ) 
removeNA = data[:,:] == ''
data[removeNA, :] = '0' # or whatever type you want
data = data.astype(float) 
```

**Math functions**

For vectors, leave tail args blank. 
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


## Data

| Year | Continent | Country | stuff | unit |
| ---- | ---- | ---- | ---- | ---- | 
| 1986 | Western Pacific | Viet Nam |	Wine | 0
| 1986 | Americas	| Uruguay	| Other	| 0.5
| 1985 | Africa |	Cote d'Ivoire	| Wine | 1.62

This is a 3x5 matrix; 15 elements, 2-dimensional, 3 rows, 5 columns.




