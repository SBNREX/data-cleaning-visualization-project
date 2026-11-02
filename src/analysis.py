from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / "data", ROOT / "outputs"
OUT.mkdir(exist_ok=True)
raw = pd.read_csv(DATA / "raw_dataset.csv")
df = raw.copy()
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()
for col in ["customer_id", "age", "quantity", "unit_price", "rating"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df["purchase_date"] = pd.to_datetime(df["purchase_date"], errors="coerce")
initial_rows = len(df)
missing_before = int(df.isna().sum().sum())
duplicates_before = int(df.duplicated().sum())
df = df.drop_duplicates().copy()
df.loc[~df["age"].between(13, 100), "age"] = np.nan
df.loc[~df["rating"].between(1, 5), "rating"] = np.nan
df.loc[df["quantity"] <= 0, "quantity"] = np.nan
df.loc[df["unit_price"] <= 0, "unit_price"] = np.nan
for col in ["age", "quantity", "unit_price", "rating"]:
    df[col] = df[col].fillna(df[col].median())
for col in ["gender", "city", "product_category", "payment_method"]:
    mode = df[col].mode()
    df[col] = df[col].fillna(mode.iloc[0] if not mode.empty else "Unknown")
df["purchase_date"] = df["purchase_date"].fillna(df["purchase_date"].median())
q1, q3 = df["unit_price"].quantile([0.25, 0.75])
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
outlier_count = int(((df["unit_price"] < lower) | (df["unit_price"] > upper)).sum())
df["unit_price"] = df["unit_price"].clip(lower=lower, upper=upper)
df["total_sales"] = df["quantity"] * df["unit_price"]
df["purchase_month"] = df["purchase_date"].dt.to_period("M").astype(str)
df.to_csv(OUT / "cleaned_dataset.csv", index=False)
summary = pd.DataFrame({"Metric": ["Rows before cleaning", "Rows after cleaning", "Missing cells before cleaning",
    "Exact duplicate rows found", "Unit-price values beyond IQR fences capped", "Missing cells after cleaning"],
    "Value": [initial_rows, len(df), missing_before, duplicates_before, outlier_count, int(df.isna().sum().sum())]})
summary.to_csv(OUT / "data_quality_summary.csv", index=False)

# Category purchases
counts = df["product_category"].value_counts()
plt.figure(figsize=(9,5)); plt.bar(counts.index, counts.values)
plt.title("Number of Purchases by Product Category"); plt.xlabel("Product category"); plt.ylabel("Number of purchases")
plt.xticks(rotation=15); plt.tight_layout(); plt.savefig(OUT / "category_purchases.png", dpi=160); plt.close()

# Monthly sales
monthly = df.groupby("purchase_month")["total_sales"].sum()
plt.figure(figsize=(9,5)); plt.plot(monthly.index, monthly.values, marker="o")
plt.title("Monthly Sales Trend"); plt.xlabel("Purchase month"); plt.ylabel("Sales")
plt.xticks(rotation=45); plt.tight_layout(); plt.savefig(OUT / "monthly_sales_trend.png", dpi=160); plt.close()

# Age distribution
plt.figure(figsize=(8,5)); plt.hist(df["age"], bins=12, edgecolor="black")
plt.title("Customer Age Distribution"); plt.xlabel("Age"); plt.ylabel("Number of customers")
plt.tight_layout(); plt.savefig(OUT / "customer_age_distribution.png", dpi=160); plt.close()

# Unit-price boxplot by category
categories = list(df["product_category"].dropna().unique())
values = [df.loc[df["product_category"] == c, "unit_price"].values for c in categories]
plt.figure(figsize=(8,5)); plt.boxplot(values, labels=categories)
plt.title("Unit Price by Product Category"); plt.xlabel("Product category"); plt.ylabel("Unit price")
plt.xticks(rotation=15); plt.tight_layout(); plt.savefig(OUT / "unit_price_boxplot.png", dpi=160); plt.close()

# Correlation heatmap
corr = df[["age", "quantity", "unit_price", "rating", "total_sales"]].corr()
fig, ax = plt.subplots(figsize=(8,6)); im = ax.imshow(corr.values, vmin=-1, vmax=1, aspect="auto")
ax.set_xticks(range(len(corr.columns)), labels=corr.columns, rotation=30, ha="right")
ax.set_yticks(range(len(corr.index)), labels=corr.index)
for i in range(len(corr.index)):
    for j in range(len(corr.columns)):
        ax.text(j, i, f"{corr.iloc[i,j]:.2f}", ha="center", va="center")
fig.colorbar(im, ax=ax); ax.set_title("Correlation Heatmap"); fig.tight_layout()
fig.savefig(OUT / "correlation_heatmap.png", dpi=160); plt.close(fig)

sales_by_category = df.groupby("product_category")["total_sales"].sum()
top_category = sales_by_category.idxmax()
report = f"""# Data Cleaning & Visualization — Results

## Data quality
- Rows before cleaning: {initial_rows}
- Rows after cleaning: {len(df)}
- Missing cells before cleaning: {missing_before}
- Exact duplicate rows found: {duplicates_before}
- Unit-price values beyond IQR fences and capped: {outlier_count}
- Missing cells after cleaning: {int(df.isna().sum().sum())}

## Summary findings
- Total sales in this sample: {df["total_sales"].sum():,.2f}
- Average rating: {df["rating"].mean():.2f} out of 5
- Highest-sales category: {top_category} ({sales_by_category.max():,.2f})
- See the monthly sales chart for changes in sales across the year.

## Interpretation note
This is a small educational sample dataset with intentionally introduced data-quality issues. Findings describe this sample only and should not be treated as representative of a real business.
"""
(OUT / "project_report.md").write_text(report, encoding="utf-8")
print(summary.to_string(index=False))
print(report)
