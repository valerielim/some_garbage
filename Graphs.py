# ---------------------------------------------------------------------------- #
# Graphs

-- Matplotlib Pyplot
-- ggplot (Python version stolen from R)
-- seaborne

# ---------------------------------------------------------------------------- #
# Pyplot

"""
Using the different pyplot functions, we can create, customize, and display a plot. 

``py
plt.plot()
plt.show()
``

Because we didn't pass in any arguments, the `plot()` function would generate 
an empty plot with just the axes and ticks and the `show()` function would display 
that plot. 

You'll notice that we didn't assign the plot to a variable and then call a method
on the variable to display it. We instead called 2 functions on the pyplot 
module directly.

This is because every time we call a pyplot function, the module maintains and
updates the plot internally (also known as state). When we call show(), the plot is 
displayed and the internal state is destroyed. 

While this workflow isn't ideal when we're writing functions that create plots 
on a repeated basis as part of a larger application, it's useful when exploring data.

**Jupyter Notebook**

To run in Jupyter Notebook, and display plots inline, run this: 

  `%matplotlib inline`

This renders the plots within the cells. 
"""

# ---------------------------------------------------------------------------- #
# ggplot

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
# LINE GRAPHS

  """
  SYMBOL OPTIONS: [COLOUR] + [SYMBOL]
    '*' = star            |   'r' = red
    'o' = circle          |   'b' blue
    's' = square          |   'g' = green
    '-' = straight line   |   'k' = black
    '--' = dotted line    |   'w' = white
    '^' = triangle        |   'y' = yellow
  """

  import matplotlib.pyplot as plt
  import pandas as pd

  plt.plot(x_values = DATA['X'], y_values = DATA['Y'], 'ro')

  # labels
  plt.xticks(rotation = 90) # format x-axis labels to be displayed vertically
  plt.xlabel("Month")
  plt.ylabel("Unemployment Rate")
  plt.title("Monthly Unemployment Trends, 1948")
  plt.show()

### METHOD 1; MANUAL MULTI-PLOT

# 1. Build container Figure
  fig = plt.figure(figsize=(12,6)) # units in inches

# 2. Specify subplots in Figure
  ax1 = fig.add_subplot(2,1,1) # nrows, ncols, order 
  ax2 = fig.add_subplot(2,1,2) # 2 rows, 1 column, 2nd graph

# 3. Insert data by subsets
  year1 = data[0:12]
  year2 = data[13:24]
  ax1.plot(year1['DATE'], year1['VALUE'], 'ro')
  ax2.plot(year2['DATE'], year2['VALUE'], 'b-')

# 4. titles
  ax1.set_title("Monthly Unemployment Rate, 1948")
  ax2.set_title("Monthly Unemployment Rate, 1949")

### METHOD 2; AUTOMATIC MULTIPLOT, WITH LOOPS, FACET BY YEAR

  fig = plt.figure(figsize=(12,12)) # units in inches  
  for i in range(0,5): # num years you want
    
    start_num = (i*12)+1 # 0, 13, 25
    end_num = (i+1)*12 # 12, 24, 36
    subset = data[start_num : end_num]
    
    plotter = fig.add_subplot(5,1,i+1)
    plotter.plot(subset['DATE'], subset['VALUE'])

  plt.show()

### METHOD 3; NO FACET, MANY LINES ON SINGLE GRAPH

fig = plt.figure(figsize = (10, 6))
colors = ['red', 'blue', 'green', 'orange', 'black']
year = 1948

for i in range(0,5):
    start_num = i*12 # 0, 12, 24
    end_num = (i+1)*12 # 12, 24, 36
    subset = unrate[start_num:end_num]
    label_name = str(year + i)
    plt.plot(subset['MONTH'], subset['VALUE'], c = colors[i], label = label_name)
    
plt.legend(loc = 'top right')
plt.show()
    
# ---------------------------------------------------------------------------- #


