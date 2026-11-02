# Data Cleaning & Visualization Project

A beginner-friendly Python project demonstrating data cleaning, preprocessing, exploratory data analysis (EDA), and visualization.

## Objective
Clean a raw customer-purchases dataset, assess data quality, explore sales patterns, and communicate findings through charts and a short report.

## Tools
- Python
- Pandas and NumPy
- Matplotlib and Seaborn

## Dataset
`data/raw_dataset.csv` is a small educational sample dataset. It intentionally includes missing values and invalid/extreme values so the cleaning workflow can be demonstrated. It is not a real company's customer data.

## Workflow
1. Load and inspect the raw CSV.
2. Standardize column names and text values.
3. Convert columns to numeric and date data types.
4. Identify and remove exact duplicate rows.
5. Replace invalid ages and ratings with missing values.
6. Impute numeric values with medians and categorical values with modes.
7. Detect extreme unit prices using the interquartile range (IQR) and cap values beyond the IQR fences.
8. Add `total_sales` and `purchase_month` features.
9. Save a cleaned CSV, data-quality summary, report, and charts.

## Project structure
```text
data-cleaning-visualization-project/
├── data/
│   └── raw_dataset.csv
├── outputs/
│   ├── cleaned_dataset.csv
│   ├── data_quality_summary.csv
│   ├── project_report.md
│   ├── category_purchases.png
│   ├── monthly_sales_trend.png
│   ├── customer_age_distribution.png
│   ├── unit_price_boxplot.png
│   └── correlation_heatmap.png
├── src/
│   └── analysis.py
├── requirements.txt
└── README.md
```

## Run locally
Python 3.9+ is recommended.

```bash
python -m venv .venv
```

Activate the environment:
- Windows: `.venv\Scripts\activate`
- macOS/Linux: `source .venv/bin/activate`

Install dependencies and run:
```bash
pip install -r requirements.txt
python src/analysis.py
```

The script creates or refreshes the generated files in `outputs/`.

## Visualizations
- Purchases by product category
- Monthly sales trend
- Customer age distribution
- Unit-price boxplot by category
- Correlation heatmap

## Important methodology note
Outliers are not automatically errors in every dataset. This project uses domain checks for impossible ages/ratings and IQR fences for extreme unit prices. The chosen treatment is documented so the analysis remains transparent.

## Learning outcomes
- Inspecting and cleaning tabular data with Pandas
- Handling missing and invalid values
- Removing duplicates
- Detecting and capping outliers
- Creating derived columns and summary metrics
- Producing charts and communicating findings

## Author
Add your name here before submitting.
