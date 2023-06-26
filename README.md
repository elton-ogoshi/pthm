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

# create a dataframe 'df' with necessary columns

heatmap = PeriodicTableHeatMap(df)
heatmap.plot()
heatmap.save_fig('heatmap.pdf')
```

In this code, `df` is a pandas DataFrame containing the properties (`row`, `group`, `property`) of all elements of the periodic table. The `PeriodicTableHeatMap` class is used to generate and save the heatmap.

The notebook `demo.ipynb` demonstrates how to use the class `PeriodicTableHeatMap` defined at `pthm/core.py` to plot the heatmap.

The result is something like the plot below

![Atomic radius heatmap](etc/atomic_radius.png "Atomic_radius")

## License

This project is licensed under the MIT License.
