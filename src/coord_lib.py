import pandas as pd
import numpy as np
import unicodedata
import random

def getting_latlong(path):
    """
    Function to open the full latlong IBGE database and save only relevant information
    after removing special characters
    
    Parameters
    ----------
     path : string
            full path to the .csv data set
    """

    coord_df=pd.read_csv(path)
    # agora, tem que criar um dataframe com o nome das regiões e coordenadas geográficas.
    # será usada a média, ou seja, mais ou menos o centro da região,
    # obtida a partir dos dados dos municípios

    # o nome do estado também ficará junto.
    coord_micro = coord_df.groupby(['nm_micro', 'nm_uf'])['lng', 'lat'].mean()
    nomes = coord_micro.index.get_level_values(0)
    
    tempdict={}
    for text in nomes:
        #print(unicodedata.normalize('NFKD', text).encode('ascii', 'ignore'))
        tempdict[text]=unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

    coord_micro.rename(tempdict, inplace=True) 
    # TODO: a mudança também foi aplicada para nm_uf (SÃO PAULO ficou sem til), mas não para todos os estados.
    # Verificar e corrigir caso seja feita busca pelo nome do estado.
    coord_micro.reset_index(level=['nm_micro'], inplace=True)
    coord_micro.head(3)

    coord_micro.to_csv("../data/coord_micro.csv")
    
    
    

def getlatlong_list(df, coord_micro, flag_ramo=False, flag_miss=False):
    
    """
    Return a list with the coordinates(lat,long) of each company
    
    Parameters
    ----------
    df : pandas DataFrame
             The Data Frame to be analyzed
    
    coord_micro : pandas DataFrame
             The Data Frame contaning the lat,long of each micro region
    
    Returns
    -------
    mapcoords : list
        list of the coordinates(lat,long) corresponding to each company of the pandas datagrame input.
    
    n : int
        number of entries without a corresponding micro region
    """
    
    mapcoords = []
    n = 0
    for ind in df.index:
        coord = coord_micro[coord_micro['nm_micro'] == df.nm_micro_regiao[ind]][['lat', 'lng']]
        
        if not coord.empty:
            if flag_ramo:
                mapcoords.append([coord['lat'].values[0]-random.uniform(0, 0.25),
                                  coord['lng'].values[0]-random.uniform(0, 0.25),
                                'id:'+df.id[ind][:10]+' ramo:'+df.de_ramo[ind]]) # only to not plot at the exactly same position
            else:
                mapcoords.append([coord['lat'].values[0]-random.uniform(0, 0.25),
                                  coord['lng'].values[0]-random.uniform(0, 0.25)])
        else:
            n+=1
    print("%d companies without information about the belonging micro region" % n)
    
    if flag_miss:
        return mapcoords,n
    else:
        return mapcoords
