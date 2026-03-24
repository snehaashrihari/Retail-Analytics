import pandas as pd
import logging

logger = logging.getLogger(__name__)

def load_and_merge_data(base_path: str) -> pd.DataFrame:
    """Combines transactions, customer, and category data based on provided headers."""
    try:
        # 1. Load the files
        # Ensure filenames match exactly (case-sensitive in Docker/Linux)
        trans = pd.read_csv(f"{base_path}/Transactions.csv")
        cust = pd.read_csv(f"{base_path}/Customer.csv")
        cat = pd.read_csv(f"{base_path}/prod_cat_info.csv")
        
        # 2. Merge Transactions and Customers
        # Left: 'cust_id' | Right: 'customer_Id'
        df = trans.merge(
            cust, 
            left_on="customer_Id", 
            right_on="customer_Id", 
            how="left"
        )
        
        # 3. Merge with Product Category Info
        # We merge on both subcat and cat codes to ensure unique mapping
        df = df.merge(
            cat, 
            on=["prod_sub_cat_code", "prod_cat_code"], 
            how="left"
        )
        
        logger.info(f"Data successfully merged. total records: {len(df)}")
        return df

    except FileNotFoundError as e:
        logger.error(f"File missing in {base_path}: {e}")
        raise
    except KeyError as e:
        logger.error(f"Column name mismatch: {e}")
        raise