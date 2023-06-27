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
    labs
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

    def __init__(self,
                 property_df: pd.DataFrame,
                 cmap='YlGnBu',
                 default_property_val=None):
        """
        Construct all the necessary attributes for the PeriodicTableHeatMap object.

        Parameters
        ----------
            property_df : pandas.DataFrame
                Dataframe containing properties of elements of periodic table.
            cmap : str, optional
                Name of the matplotlib colormap (default is 'YlGnBu').
            default_property_val: None
                In the case that the dataframe does not contain a row for every element, this value is set to the missing elements
        """
        df = property_df.copy(deep=True)

        # Ensure all elements are present in dataframe
        for element in Element:
            if element.symbol not in df['element'].values:
                df = df.append({
                    'element': element.symbol,
                    'property': default_property_val,
                }, ignore_index=True)

        # Hardcoded row, group and number information for the elements
        self.rows = dict()
        self.groups = dict()
        self.numbers = dict()
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

            self.rows[element.symbol] = row_index
            self.groups[element.symbol] = group_index
            self.numbers[element.symbol] = element.Z

        # Create 'row' and 'group' columns based on 'element'
        df['row'] = df['element'].map(self.rows)
        df['group'] = df['element'].map(self.groups)
        df['number'] = df['element'].map(self.numbers)

        self.df = df
        cmap = plt.get_cmap(cmap)
        self.colors = [matplotlib.colors.rgb2hex(
            cmap(i)) for i in range(cmap.N)]

    def plot(self, property_col: str,
             legend_title: str = None,
             show_number: bool = True,
             show_values: bool = True):
        """
        Plot the heatmap of periodic table.

        Parameters
        ----------
            property_col : str
                Name of dataframe column that contains the property to plot.
            legend_title : str
                Legend to be placed above the colorbar of the heatmap.

        Returns
        -------
        plotnine.ggplot.ggplot
            The plotnine ggplot object.
        """
        df = self.df[['element', 'row', 'group',
                      'number', property_col]].copy(deep=True)
        df['property_str'] = df[property_col].apply(str)

        if legend_title is None:
            legend_title = property_col

        # Separate into groups that are going to display a font with light color or black color
        df['p_group'] = pd.cut(df[property_col], (df[property_col].min(), df[property_col].quantile(
            0.75), df[property_col].max()), labels=("low", 'high'), include_lowest=True)

        # Create the top df just for displays the ticks for rows and groups indexes
        top = df[df.row < 8]
        groupdf = top.groupby('group').agg(y=('row', np.min)).reset_index()

        plot = (
            ggplot(df, aes('group', 'row', fill=property_col))
            # Add thicker black border to each tile
            + geom_tile(color="white", size=2)
            + geom_text(aes(label='element', color='p_group'),
                        size=14, show_legend=False)
            + scale_color_manual(['black', 'lightgray'])
            # Use the YlGnBu colormap
            + scale_fill_gradientn(colors=self.colors)
            + labs(fill=legend_title)  # rename the legend
            + coord_equal(expand=False)
            + geom_text(groupdf, aes('group', 'y', label='group'), color='gray', nudge_y=.525,
                        va='bottom', fontweight='normal', size=9, inherit_aes=False)
            # Reverse the y-axis
            + scale_y_reverse(breaks=range(1, 8), limits=(0, 10.5))
            + theme_void()
            + theme(figure_size=(12, 8),
                    plot_background=element_rect(fill='white'),
                    axis_text_y=element_text(
                        margin={'r': 5}, color='gray', size=9),
                    legend_title=element_text(size=12)
                    )
        )

        if show_number:
            plot += geom_text(aes(label='number', color='p_group'),
                              size=7, nudge_y=0.3, nudge_x=-0.3, show_legend=False)
        if show_values:
            plot += geom_text(aes(label='property_str', color='p_group'),
                              size=7, nudge_y=-0.3, show_legend=False)

        self.last_plot = plot

        return plot

    def save_fig(self, filename: str):
        """
        Save the plot as a PDF file.

        Parameters
        ----------
            filename : str
                Name of the output PDF file.
        """
        ggsave(self.last_plot, filename)
