import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

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

def transform(df):
    
    """
    Return a numpy array with the dataframe values after some transformations
    
    Parameters
    ----------
    df : pandas dataframe
             The Data Frame to be transformed
    
    Returns
    -------
    df_transformed : numpy array
        Numpy array contain all the lines and columns after some transformations.
    """
    
    cat_idade = ['<= 1', '1 a 5', '5 a 10', '10 a 15', '15 a 20', '> 20']
    cat_saude = ['SEM INFORMACAO', 'VERMELHO', 'LARANJA', 'AMARELO', 'CINZA', 'AZUL', 'VERDE']
    cat_nivel = ['SEM INFORMACAO', 'MUITO BAIXA', 'BAIXA', 'MEDIA', 'ALTA']
    cat_faturamento = ['SEM INFORMACAO', 'ATE R$ 81.000,00', 'DE R$ 81.000,01 A R$ 360.000,00', 
              'DE R$ 360.000,01 A R$ 1.500.000,00', 'DE R$ 1.500.000,01 A R$ 4.800.000,00', 
              'DE R$ 4.800.000,01 A R$ 10.000.000,00','DE R$ 10.000.000,01 A R$ 30.000.000,00',
              'DE R$ 30.000.000,01 A R$ 100.000.000,00','DE R$ 100.000.000,01 A R$ 300.000.000,00',
              'DE R$ 300.000.000,01 A R$ 500.000.000,00','DE R$ 500.000.000,01 A 1 BILHAO DE REAIS',
              'ACIMA DE 1 BILHAO DE REAIS']
    
    cols_cat = ['idade_emp_cat', 'de_saude_tributaria', 'de_nivel_atividade',
               'de_faixa_faturamento_estimado', 'de_faixa_faturamento_estimado_grupo']
    df[cols_cat] = df[cols_cat].astype('category')
    
    categories = [cat_idade, cat_saude, cat_nivel, cat_faturamento, cat_faturamento]
    
    for i in range(len(cols_cat)):
        df[cols_cat[i]].cat.reorder_categories(categories[i],inplace=True)
        df[cols_cat[i]] = df[cols_cat[i]].cat.codes
        
    col_bool = df.select_dtypes(include=['bool']).columns
    df[col_bool] = df[col_bool].astype('int8')
    
    cols_dummies = ['sg_uf', 'natureza_juridica_macro', 'setor']
    for i in cols_dummies:
        df = df.merge(pd.get_dummies(df[i]), left_index=True, right_index=True)
        
    df.drop(cols_dummies, axis=1, inplace=True)
    
    df['qt_filiais'] = np.log(df['qt_filiais']+1)
    
    df_transformed = MinMaxScaler().fit_transform(df)

    return df_transformed