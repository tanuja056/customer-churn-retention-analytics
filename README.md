
# Customer Retention & Churn Analytics

## Project Overview
An end-to-end customer analytics project using Python, SQL, SQLite, and Power BI to investigate customer churn patterns and identify high-risk customer segments.

## Business Objective
Understand which customer groups have higher churn rates and provide actionable insights to support customer retention strategies.

## Dataset
IBM Telco Customer Churn dataset containing 7,043 customer records and 21 original attributes.

Source: https://github.com/IBM/telco-customer-churn-on-icp4d

## Tools & Technologies
- Python: Pandas, NumPy, Matplotlib
- SQL: SQLite, aggregations, CTEs, window functions
- Power BI: KPI cards, interactive slicers, churn analysis
- Git and GitHub

## Project Workflow
1. Data acquisition and inspection
2. Data cleaning and validation
3. Exploratory data analysis
4. SQL analysis and customer segmentation
5. Power BI dashboard development

## Key Findings
- Overall customer churn: 26.54%
- Month-to-month contract churn: 42.71%
- One-year contract churn: 11.27%
- Two-year contract churn: 2.83%
- Customers with 0–12 months of tenure have a 47.44% churn rate.
- Electronic check users have a 45.29% churn rate.
- Fiber-optic customers have a 41.89% churn rate.

These findings describe associations in the dataset and do not establish causation.

## Dashboard
Power BI report: `powerbi/customer_churn_dashboard.pbix`

Dashboard screenshot: `outputs/charts/customer_churn_dashboard.png`

## Repository Structure
```text
customer-churn-retention-analytics/
├── data/
│   ├── raw/
│   └── processed/
├── scripts/
│   ├── download_data.py
│   ├── run_analysis.py
│   └── run_sql.py
├── sql/
│   └── churn_analysis.sql
├── notebooks/
├── powerbi/
│   └── customer_churn_dashboard.pbix
├── outputs/
│   └── charts/
├── README.md
└── requirements.txt
```

Generated datasets and the SQLite database are stored locally and are not included in the repository.

## How to Run
```bash
pip install -r requirements.txt
python scripts/download_data.py
python scripts/run_analysis.py
python scripts/run_sql.py
```

## Business Recommendation
Prioritize retention analysis for new customers and month-to-month subscribers. Investigate the reasons behind higher churn among electronic check users and fiber-optic customers before designing targeted retention initiatives.
