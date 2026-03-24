from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def run_segmentation(df: pd.DataFrame):
    # Create a reference point for 'Recency' (1 day after the latest transaction)
    snapshot_date = df['tran_date'].max() + pd.Timedelta(days=1)
    
    # Aggregate into RFM using 'customer_Id'
    rfm_df = df.groupby('customer_Id').agg({
        'tran_date': lambda x: (snapshot_date - x.max()).days, # Result is an INT
        'transaction_id': 'count',                            # Frequency
        'total_amt': 'sum'                                    # Monetary
    })
    
    # Rename for the Model
    rfm_df.columns = ['Recency', 'Frequency', 'Monetary']
    
    # Scaling - This will now work because 'Recency' is a number of days, not a date
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(rfm_df)
    
    # Run K-Means
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    rfm_df['Cluster'] = kmeans.fit_predict(scaled_features)
    
    logger.info("Segmentation complete. K-Means clusters assigned.")
    return rfm_df