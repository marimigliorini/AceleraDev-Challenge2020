import numpy as np
import pandas as pd
import preprocessing_lib as prep

from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity


def kMeans_training(df, n_clusters=25, seed=42):
    
    """
    Return the KMeans model trained with the provided data.
    
    Parameters
    ----------
    df : pandas dataframe or numpy array
        The Data Frame to be used in the training.
            
    n_clusters : int, optional
        Number of clusters. 'default = 25'
        
    seed : string, optional
        Seed used to make the randomness deterministic.
        'default = 42'
    
    Returns
    -------
    kmeans : KMeans model
        KMeans clustering model trained.
    """
    
    kmeans = KMeans(n_clusters = n_clusters, random_state=seed).fit(df)
    return kmeans


def market_clusters(kmeans):
    
    """
    Return a pandas dataframe with the market leads id and respective clusters label.
    
    Parameters
    ----------
    kmeans : KMeans model trained
        The KMeans model used to predict the clusters.
    
    Returns
    -------
    market_labels : pandas dataframe
        Pandas dataframe containing the market leads and respective cluster labels.
    """
    
    market = prep.loading_data('../data/estaticos_market.csv')
    
    market_labels = pd.DataFrame()                   
    market_labels['id'] = market.id       
    market_labels['label'] = kmeans.labels_
    return market_labels


def portfolio_clusters(market_labels, portfolio):
    
    """
    Return a pandas dataframe with the portfolio leads id and clusters label.
    
    Parameters
    ----------
    market_labels : pandas dataframe
        The dataframe with market leads and respective cluster labels
            
    portfolio : pandas dataframe
        Dataframe with the clients information.
    
    Returns
    -------
    portfolio_labels : pandas dataframe
        Pandas dataframe containing the portfolio leads and respective cluster labels.
    """
    
    portfolio_labels = pd.DataFrame()
    portfolio_labels['id'] = portfolio.id
    portfolio_labels['label'] = np.array(market_labels['label'][market_labels['id'].isin(portfolio.id)])
    return portfolio_labels

def recommend_leads(portfolio, df, market_labels):
    
    """
    Return a pandas dataframe with the recommended leads given a portfolio.
    
    Parameters
    ----------
    portfolio : pandas dataframe
        Pandas dataframe with the portfolio leads and respective cluster labels
        
    df : pandas dataframe
        Pandas dataframe with market features
            
    market_labels : pandas dataframe
        The dataframe with market leads and respective cluster labels
    
    Returns
    -------
    leads_recommended : pandas matrix
        Pandas matrix containing 5000 recommended leads.
    """
    
    cols_dummies = ['sg_uf', 'natureza_juridica_macro', 'setor']
    for i in cols_dummies:
        df = df.merge(pd.get_dummies(df[i]), left_index=True, right_index=True)
        
    df.drop(cols_dummies, axis=1, inplace=True)
    
    value_counts = portfolio['label'].value_counts(normalize=True)
    value_counts = value_counts[value_counts >= 0.15].index.tolist()
    
    leads_clusters = pd.DataFrame(market_labels['id'][market_labels['label'].isin(value_counts)])
    leads_clusters.drop(leads_clusters[leads_clusters['id'].isin(portfolio['id'])].index, axis=0, inplace=True)
    
    leads_features = df.loc[leads_clusters.index]
    
    portfolio_index = portfolio[portfolio['label'].isin(value_counts)]
    portfolio_features = pd.DataFrame(market_labels['id'][market_labels['id'].isin(portfolio_index['id'])])
    portfolio_features = df.loc[portfolio_features.index]
    

    leads_features.reset_index(drop=True, inplace=True)
    leads_clusters.reset_index(drop=True, inplace=True)
    portfolio_features.reset_index(drop=True, inplace=True)
    
    cosine_sim = pd.DataFrame(cosine_similarity(portfolio_features, leads_features))
    cosine_sim = cosine_sim[cosine_sim >= 0.9].fillna(0)
    recommended_index = cosine_sim[cosine_sim > 0].count().sort_values(ascending=False)[0:5000].index

    leads_recommended = leads_clusters.loc[recommended_index]
    return leads_recommended
        