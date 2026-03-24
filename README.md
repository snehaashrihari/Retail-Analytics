# Retail Analytics Foundry

A production-grade data engineering pipeline designed to automate the ingestion of raw retail datasets, execute customer behavioral segmentation, and generate actionable business personas. The system transitions raw transactional data into a structured analytical environment using a modular, containerized architecture.

## Project Architecture

The pipeline is built with a decoupled functional architecture to ensure scalability and maintainability. Each module handles a distinct stage of the ETL (Extract, Transform, Load) and modeling process.

* **Data Ingestion (`src/data_loader.py`)**: Manages multi-source ingestion of transaction, customer, and product category datasets. It implements schema mapping to resolve naming discrepancies across legacy systems.
* **Data Transformation (`src/processor.py`)**: Executes data cleaning, type standardization, and handles missing values. It performs feature engineering to prepare the dataset for statistical modeling.
* **Statistical Modeling (`src/models.py`)**: The analytical engine utilizing RFM (Recency, Frequency, Monetary) analysis and K-Means Clustering to segment the customer base.
* **Orchestration (`src/main.py`)**: The central controller that manages the end-to-end execution flow, logging, and data persistence.

## Technical Features

* **Containerization**: Fully dockerized environment using Docker Compose to ensure environment parity and simplified deployment.
* **Data Persistence**: Utilizes Docker Volumes to map containerized output back to the local host, ensuring analytical results are accessible post-execution.
* **Production Observability**: Integrated Python standard logging to track pipeline health, execution stages, and data volume metrics.
* **Defensive Engineering**: Implemented robust error handling for schema mismatches and IO exceptions to prevent pipeline silent failures.

## Customer Persona Mapping

The pipeline translates abstract cluster data into high-value business personas based on behavioral metrics:

| Persona | Behavioral Profile | Strategic Action |
| :--- | :--- | :--- |
| **Platinum Champions** | Highest frequency and monetary spend ($15k+). | Implement VIP loyalty rewards and exclusive access. |
| **Loyal Growers** | Consistent spenders with moderate recency. | Execute upselling campaigns to increase lifetime value. |
| **Recent Trialers** | Recent shoppers with lower initial transaction totals. | Deploy welcome sequences to secure secondary purchases. |
| **At-Risk Customers** | Inactive for 700+ days; formerly active. | Launch re-engagement and win-back marketing initiatives. |



## Installation and Execution

### 1. Prerequisites
* Docker and Docker Desktop
* Docker Compose

### 2. Setup
Clone the repository and navigate to the root directory:
```bash
git clone [https://github.com/snehaashrihari/Retail-Analytics.git](https://github.com/snehaashrihari/Retail-Analytics.git)
cd Retail-Analytics
docker-compose up --build
```