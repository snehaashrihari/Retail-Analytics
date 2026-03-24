import os
import logging
import pandas as pd
from data_loader import load_and_merge_data
from processor import clean_data
from models import run_segmentation

# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def generate_summary_report(clusters_df):
    """Prints a high-level summary of the customer segments."""
    summary = clusters_df.groupby('Cluster').agg({
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': 'mean'
    }).round(2)
    
    logging.info("\n--- CUSTOMER SEGMENTATION SUMMARY ---\n%s", summary)

def main():
    logging.info("Starting Retail Analytics Pipeline...")
    
    # 1. Load
    raw_data = load_and_merge_data("data/raw")
    
    # 2. Transform
    processed_data = clean_data(raw_data)
    
    # 3. Analyze
    clusters = run_segmentation(processed_data)

    # 4. Report
    generate_summary_report(clusters)
    
    # 5. Save 
    output_dir = "data/processed"
    output_file = os.path.join(output_dir, "customer_segments.csv")
    
    # Create directory if it doesn't exist inside the container
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the dataframe
    clusters.to_csv(output_file)
    
    logging.info(f"Results successfully saved to {output_file}")
    logging.info("Pipeline execution finished.")
    

if __name__ == "__main__":
    main()