import numpy as np
import pandas as pd
import preprocessing_lib as prep

from sklearn.cluster import KMeans


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


def recommend_leads(portfolio_labels, market_labels):
    
    """
    Return a pandas dataframe with the recommended leads given a portfolio.
    
    Parameters
    ----------
    portfolio_labels : pandas dataframe
        Pandas dataframe with the portfolio leads and respective cluster labels.
            
    market_labels : pandas dataframe
        The dataframe with market leads and respective cluster labels
    
    Returns
    -------
    leads_recommended : pandas matrix
        Pandas matrix containing the recommended leads.
    """
    
    leads_recommended = pd.DataFrame(market_labels['id'][market_labels['label'] == int(portfolio_labels.label.mode())])
    leads_recommended.drop(leads_recommended[leads_recommended['id'].isin(portfolio_labels['id'])].index, axis=0, inplace=True)
    return leads_recommended
