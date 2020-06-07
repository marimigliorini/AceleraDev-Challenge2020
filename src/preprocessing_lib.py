import pandas as pd
import numpy as np

def loading_data(filepath):
    """
     filepath : string
            The path for the .csv file to be analyzed
    """
    df_file=pd.read_csv(filepath,index_col=0)
    return df_file

def preprocessamento(file_path,porc = 30, fillna_param = 'zero'):
    
    """
    Return a pandas matrix after some preprocessing
    
    Parameters
    ----------
    file_path : string
             The Data Frame to be analyzed
            
    porc : int, optional
        porcentage of missing data that would be allowed for
        a column to not be discarted. 'default = 30'
        
    fillna_param : string, optional
        This parameters chose the 'fill' method for the columns that had passed
        porcentage threshold. The options are: 'zero', 'media' and 'mediana'.
        'default = "zero"'
    
    Returns
    -------
    filtered_df : pandas matrix
        Pandas matrix contain all the lines but filtered some columns.
    """
    
    EM=file_path
    missing=((EM.isna().sum()/EM.shape[0]*100))
    types=EM.dtypes
    columns=EM.columns
    tent=pd.DataFrame({'column':columns,'missing':missing,'type':types})
    tent2=tent.loc[tent['missing'] < porc ]
    if fillna_param == 'zero':
        filtered_df= EM[tent2.column].fillna(0).select_dtypes(include=['float64','int64'])
    elif fillna_param == 'media':
        E= EM[tent2.column].select_dtypes(include=['float64','int64'])
        media=E.mean()
        filtered_df=E.fillna(media)
    elif fillna_param == 'mediana':
        E= EM[tent2.column].select_dtypes(include=['float64','int64'])
        mediana=E.median()
        filtered_df=E.fillna(mediana)
    else:
        filtered_df = 0
        print("Fill method wrong or not implemented yet")
    return filtered_df    
