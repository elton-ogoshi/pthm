import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np
from plotnine import (
    ggplot,
    ggsave,
    aes,
    geom_tile,
    geom_text,
    scale_y_reverse,
    scale_color_manual,
    coord_equal,
    theme,
    theme_void,
    element_rect,
    element_text,
)
from plotnine.scales import scale_fill_gradientn
import pandas as pd
from pymatgen.core import Element


class PeriodicTableHeatMap:
    """A class to generate heatmap of periodic table using plotnine.

    Attributes
    ----------
    df : pandas.DataFrame
        A pandas dataframe containing properties of elements of periodic table. It should contain
    cmap : matplotlib colormap
        A colormap instance or registered colormap name.
    """

    def __init__(self, df: pd.DataFrame, cmap='YlGnBu', default_property_val=None):
        """
        Construct all the necessary attributes for the PeriodicTableHeatMap object.

        Parameters
        ----------
            df : pandas.DataFrame
                Dataframe containing properties of elements of periodic table.
            cmap : str, optional
                Name of the matplotlib colormap (default is 'YlGnBu').
            default_property_val: None
                In case that the dataframe does not contain a row for every element, this value is set to the missing elements
        """

        for element in Element:
            if element.row == 6 and element.group == 3:
                group_index = element.Z - 53
                row_index = 9
            elif element.row == 7 and element.group == 3:
                group_index = element.Z - 85
                row_index = 10
            else:
                group_index = element.group
                row_index = element.row

            # Hardcoded row and group information for the elements
            self.rows = {element.symbol: element.row for element in Element}
            self.groups = {
                element.symbol: element.group for element in Element}

            # Ensure all elements are present in dataframe
            for element in Element:
                if element.symbol not in df['symbol'].values:
                    df = df.append({
                        'symbol': element.symbol,
                        'property': default_property_val,
                    }, ignore_index=True)

            # Create 'row' and 'group' columns based on 'symbol'
            df['row'] = df['symbol'].map(self.rows)
            df['group'] = df['symbol'].map(self.groups)

        self.df = df
        cmap = plt.get_cmap(cmap)
        self.colors = [matplotlib.colors.rgb2hex(
            cmap(i)) for i in range(cmap.N)]

    def plot(self):
        """
        Plot the heatmap of periodic table.

        Returns
        -------
        plotnine.ggplot.ggplot
            The plotnine ggplot object.
        """
        df = self.df

        # Separate into groups that are going to display a font with light color or black color
        df['p_group'] = pd.cut(df['property'], (df.property.min(), df.property.quantile(
            0.75), df.property.max()), labels=("low", 'high'), include_lowest=True)

        # Create the top df just for displays the ticks for rows and groups indexes
        top = df[df.row < 8]
        groupdf = top.groupby('group').agg(y=('row', np.min)).reset_index()

        return (
            ggplot(df, aes('group', 'row', fill='property'))
            # Add thicker black border to each tile
            + geom_tile(color="white", size=2)
            + geom_text(aes(label='symbol', color='p_group'),
                        size=14, show_legend=False)
            + geom_text(aes(label='number', color='p_group'), size=7,
                        nudge_y=0.3, nudge_x=-0.3, show_legend=False)
            + geom_text(aes(label='property_str', color='p_group'),
                        size=7, nudge_y=-0.3, show_legend=False)
            + scale_color_manual(['black', 'lightgray'])
            # Use the YlGnBu colormap
            + scale_fill_gradientn(colors=self.colors)
            + coord_equal(expand=False)
            + geom_text(groupdf, aes('group', 'y', label='group'), color='gray', nudge_y=.525,
                        va='bottom', fontweight='normal', size=9, inherit_aes=False)
            # Reverse the y-axis
            + scale_y_reverse(breaks=range(1, 8), limits=(0, 10.5))
            + theme_void()
            + theme(figure_size=(12, 8),
                    plot_background=element_rect(fill='white'),
                    axis_text_y=element_text(
                        margin={'r': 5}, color='gray', size=9)
                    )
        )

    def save_fig(self, filename: str):
        """
        Save the plot as a PDF file.

        Parameters
        ----------
            filename : str
                Name of the output PDF file.
        """
        ggsave(self.plot(), filename)
