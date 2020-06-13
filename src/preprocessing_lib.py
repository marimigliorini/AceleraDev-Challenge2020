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

def process(df):
   
    """
    Return a pandas matrix after some preprocessing
    
    Parameters
    ----------
    df : pandas dataframe
             The Data Frame to be processed
    
    Returns
    -------
    df_processed : pandas dataframe
        Pandas matrix contain all the lines but filtered some columns.
    """
    
    df.drop(df.columns[df.isna().sum()/len(df) >= 0.3], axis=1, inplace=True)
    
    df['fl_rm'] = [True if i == 'SIM' else False for i in df['fl_rm']]
    cols_obj2bool = df.select_dtypes(include=['object']).columns[df.select_dtypes(include=['object']).nunique() == 2]
    df[cols_obj2bool] = df[cols_obj2bool].astype('bool')
    
    bool_threshold = 0.8
    cols_bool2drop = []
    for i in df.select_dtypes(include=['bool']).columns:
        if (df[i].value_counts()/len(df) > bool_threshold).any():
            cols_bool2drop.append(i)
    df.drop(cols_bool2drop, axis=1, inplace=True)
    
    cols_toDrop = ['id','qt_socios_pf', 'qt_socios_pj', 'nm_meso_regiao', 'nm_micro_regiao', 'idade_empresa_anos',
           'nm_divisao', 'nm_segmento', 'de_natureza_juridica', 'de_ramo','dt_situacao','de_saude_rescencia',
           'qt_socios', 'vl_faturamento_estimado_aux', 'vl_faturamento_estimado_grupo_aux', 'fl_mei', 
           'vl_total_veiculos_pesados_grupo', 'vl_total_veiculos_leves_grupo', 'nu_meses_rescencia', 'sg_uf_matriz']
    df.drop(cols_toDrop, axis=1,inplace=True)
    
    df['setor'] = df['setor'].fillna(value='OUTRO')
    col_fillna = df.columns[df.isna().sum() != 0]
    df[col_fillna] = df[col_fillna].fillna(value='SEM INFORMACAO')
    
    df_processed = df
    return df_processed
