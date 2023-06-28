# Periodic Table Heatmap

This project generates a heatmap of the periodic table, implemented by using plotnine The heat values can represent any element property, like atomic radius, atomic mass, etc.

## Installation

To install the necessary dependencies for this project, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

Here is an example of how to use the code:

```python
from periodic_table_heatmap import PeriodicTableHeatMap
import pandas as pd

# Create a dataframe 'df' with necessary columns (In this example: 'elements' and 'atomic_radius')

heatmap = PeriodicTableHeatMap(df)
heatmap.plot('atomic_radius')
heatmap.save_fig('heatmap.pdf')
```

In this code, `df` is a pandas DataFrame containing a column for the elements (`element`) and columns for the properties. The `PeriodicTableHeatMap` class is used to generate and save the heatmap.

The notebook `demo.ipynb` demonstrates how to use the class `PeriodicTableHeatMap` defined at `pthm/core.py` to plot the heatmap.

The result is something like the plot below

![periodic table heatmap](etc/atomic_radius.png "Atomic_radius")

## License

This project is licensed under the MIT License.
