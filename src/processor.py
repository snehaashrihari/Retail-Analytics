import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Use the format and dayfirst=True to handle the dates correctly
    df['tran_date'] = pd.to_datetime(df['tran_date'], dayfirst=True, errors='coerce')
    
    # Use your new 'customer_Id' name here
    df = df.dropna(subset=['customer_Id', 'transaction_id', 'tran_date'])
    
    # Filter out returns or invalid quantities
    df = df[df['Qty'] > 0]
    
    logger.info(f"Cleaning complete. Available columns: {df.columns.tolist()}")
    return df

def create_rfm_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineers Recency, Frequency, and Monetary features for clustering.
    """
    # Use the max date in the dataset as the reference point
    snapshot_date = df['tran_date'].max() + pd.Timedelta(days=1)
    
    rfm = df.groupby('customer_Id').agg({
        'tran_date': lambda x: (snapshot_date - x.max()).days, # Recency
        'transaction_id': 'count',                             # Frequency
        'total_amt': 'sum'                                     # Monetary
    })
    
    rfm.rename(columns={
        'tran_date': 'Recency',
        'transaction_id': 'Frequency',
        'total_amt': 'Monetary'
    }, inplace=True)
    
    logger.info("RFM features successfully engineered.")
    return rfm