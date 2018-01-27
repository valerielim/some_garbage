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
# matplotlib line graphs

import matplotlib.pyplot as plt
import pandas as pd

# load data
file = pd.read_csv("file.csv")
file['date'] = pd.to_datetimes(['date'])

# format x-axis labels to be displayed vertically
plt.xticks(rotation = 90)

# titles
plt.xlabel("Month")
plt.ylabel("Unemployment Rate")
plt.title("Monthly Unemployment Trends, 1948")

plt.show()
# ---------------------------------------------------------------------------- #


