import pandas as pd
import numpy as np
import plotly.express as px
import folium
from folium import plugins

def describe_column(col):
    """
    Return important information about a specific column
    
    Parameters
    ----------
     col : Pandas series 
            A slice of a pandas matrix with the column to be analyzed
    """
    print("Unique values: %s" %col.unique())
    print("Number of unique values: %i" % col.nunique())
    print("Percentage of not NaN data: %.2f" % (sum(col.notna())/float(len(col))*100))
    

def plotcorr(df, var1, var2, colorvar='none'):
    
    """
    Return a pandas matrix after some preprocessing
    
    Parameters
    ----------
    df : pandas DataFrame
             The Data Frame to be analyzed
            
    var1 : string
        Name of the first variable inside the DataFrame to be analyzed
        
    var2 : string
        Name of the second variable inside the DataFrame to be analyzed
        
    colorvar : string, optional
        Name of the third variable inside the DataFrame to be plot as a different color
        to help the visualization of a possible trend.
        'default = "none"'
    
    Returns
    -------
    corr2 : float
        Correlation value between the two variables.
    """

    font=20

    corr = df[[var1,var2]].corr(method='pearson')
    #PLOT
    if colorvar != 'none':
        fig = px.scatter(df, x=var1, y=var2, color=colorvar)
    else:
        fig = px.scatter(df, x=var1, y=var2)

    #Styles
    fig.update_layout(title="Correlation value: %.2f" % (corr.iloc[0,1]))
    fig.update_layout({
    "plot_bgcolor": "rgba(0, 0, 0, 0)",
    "paper_bgcolor": "rgba(0, 0, 0, 0)",
    })

    #Show
    fig.show()
    corr2 = corr.iloc[0,1]
    return corr2


def brazilheatmap(mapcoords):
    
    """
    Return a heatmap zoomed on Brazil with the position of the companies in the list
    
    Parameters
    ----------
    mapcoords : list
        list of the coordinates(lat,long) corresponding to each company to plot on the map.
            
    
    Returns
    -------
    mapa : object
    """
    
    mapa = folium.Map(location=[-8.788497,-53.879873],tiles='Stamen Terrain',zoom_start=5)

    mapa.add_child(plugins.HeatMap(mapcoords))
    mapa
    return mapa