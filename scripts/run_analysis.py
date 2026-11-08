
from pathlib import Path
import pandas as pd

# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "telco_customer_churn.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "customer_churn_clean.csv"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Load raw dataset
# --------------------------------------------------

df = pd.read_csv(RAW_FILE)

print("=" * 60)
print("CUSTOMER CHURN DATA CLEANING")
print("=" * 60)

print(f"\nOriginal records: {len(df)}")

# --------------------------------------------------
# 3. Remove duplicate records
# --------------------------------------------------

duplicate_count = df.duplicated().sum()

df = df.drop_duplicates().copy()

print(f"Duplicate records removed: {duplicate_count}")

# --------------------------------------------------
# 4. Validate customer IDs
# --------------------------------------------------

df["customerID"] = df["customerID"].astype(str).str.strip()

duplicate_ids = df["customerID"].duplicated().sum()

print(f"Duplicate customer IDs: {duplicate_ids}")

if duplicate_ids > 0:
    raise ValueError("Duplicate customer IDs found.")

# --------------------------------------------------
# 5. Clean numeric columns
# --------------------------------------------------

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"].astype(str).str.strip(),
    errors="coerce"
)

# Blank TotalCharges values belong to customers
# with zero tenure in the standard IBM dataset.
blank_total_charges = df["TotalCharges"].isna().sum()

print(f"Blank/invalid TotalCharges before cleaning: {blank_total_charges}")

zero_tenure_rows = df["tenure"] == 0

df.loc[
    zero_tenure_rows & df["TotalCharges"].isna(),
    "TotalCharges"
] = 0

remaining_invalid = df["TotalCharges"].isna().sum()

if remaining_invalid > 0:
    raise ValueError(
        f"{remaining_invalid} TotalCharges values remain invalid."
    )

# --------------------------------------------------
# 6. Validate numeric values
# --------------------------------------------------

numeric_columns = [
    "SeniorCitizen",
    "tenure",
    "MonthlyCharges",
    "TotalCharges"
]

for column in numeric_columns:
    if df[column].isna().any():
        raise ValueError(f"Missing values found in {column}")

if (df["tenure"] < 0).any():
    raise ValueError("Negative tenure values found.")

if (df["MonthlyCharges"] < 0).any():
    raise ValueError("Negative monthly charges found.")

if (df["TotalCharges"] < 0).any():
    raise ValueError("Negative total charges found.")

# --------------------------------------------------
# 7. Standardize categorical columns
# --------------------------------------------------

categorical_columns = df.select_dtypes(
    include="object"
).columns

for column in categorical_columns:
    df[column] = df[column].str.strip()

# Validate churn labels
if not set(df["Churn"].unique()).issubset({"Yes", "No"}):
    raise ValueError("Unexpected values found in Churn.")

# --------------------------------------------------
# 8. Create analytical features
# --------------------------------------------------

# Binary churn indicator
df["Churn_Flag"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})

# Tenure groups
df["Tenure_Group"] = pd.cut(
    df["tenure"],
    bins=[-1, 12, 24, 48, 72],
    labels=[
        "0-12 Months",
        "13-24 Months",
        "25-48 Months",
        "49-72 Months"
    ]
)

# Monthly charge groups
df["Monthly_Charge_Band"] = pd.cut(
    df["MonthlyCharges"],
    bins=[0, 35, 70, 100, float("inf")],
    labels=[
        "Low",
        "Medium",
        "High",
        "Very High"
    ]
)

# --------------------------------------------------
# 9. Final validation
# --------------------------------------------------

print("\nFINAL DATA QUALITY CHECK")

print(f"Clean records: {len(df)}")
print(f"Missing values: {df.isna().sum().sum()}")
print(f"Duplicate customer IDs: {df['customerID'].duplicated().sum()}")

print("\nChurn distribution:")
print(df["Churn"].value_counts())

churn_rate = df["Churn_Flag"].mean() * 100

print(f"\nOverall churn rate: {churn_rate:.2f}%")

# --------------------------------------------------
# 10. Save cleaned dataset
# --------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)

print("\nCleaned dataset saved successfully!")
print(f"Location: {OUTPUT_FILE}")


# --------------------------------------------------
# EXPLORATORY DATA ANALYSIS
# --------------------------------------------------

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
CHART_DIR = BASE_DIR / "outputs" / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

print("\nStarting EDA...")

# 1. Churn summary
churn_summary = (
    df.groupby("Churn", observed=False)
    .agg(
        Customers=("customerID", "count"),
        Average_Tenure=("tenure", "mean"),
        Average_Monthly_Charges=("MonthlyCharges", "mean"),
        Average_Total_Charges=("TotalCharges", "mean")
    )
    .reset_index()
)

churn_summary.to_csv(PROCESSED_DIR / "churn_summary.csv", index=False)

# 2. Churn by contract
contract_summary = df.groupby("Contract", observed=False).agg(
    Customers=("customerID", "count"),
    Churned_Customers=("Churn_Flag", "sum")
).reset_index()

contract_summary["Churn_Rate"] = (
    contract_summary["Churned_Customers"]
    / contract_summary["Customers"] * 100
)
contract_summary.to_csv(PROCESSED_DIR / "churn_by_contract.csv", index=False)

# 3. Churn by tenure
tenure_summary = df.groupby("Tenure_Group", observed=False).agg(
    Customers=("customerID", "count"),
    Churned_Customers=("Churn_Flag", "sum")
).reset_index()

tenure_summary["Churn_Rate"] = (
    tenure_summary["Churned_Customers"]
    / tenure_summary["Customers"] * 100
)
tenure_summary.to_csv(PROCESSED_DIR / "churn_by_tenure.csv", index=False)

# 4. Churn by payment method
payment_summary = df.groupby("PaymentMethod", observed=False).agg(
    Customers=("customerID", "count"),
    Churned_Customers=("Churn_Flag", "sum")
).reset_index()

payment_summary["Churn_Rate"] = (
    payment_summary["Churned_Customers"]
    / payment_summary["Customers"] * 100
)
payment_summary.to_csv(PROCESSED_DIR / "churn_by_payment_method.csv", index=False)

# 5. Churn by internet service
internet_summary = df.groupby("InternetService", observed=False).agg(
    Customers=("customerID", "count"),
    Churned_Customers=("Churn_Flag", "sum")
).reset_index()

internet_summary["Churn_Rate"] = (
    internet_summary["Churned_Customers"]
    / internet_summary["Customers"] * 100
)
internet_summary.to_csv(PROCESSED_DIR / "churn_by_internet_service.csv", index=False)

# 6. Churn by monthly charge
charge_summary = df.groupby("Monthly_Charge_Band", observed=False).agg(
    Customers=("customerID", "count"),
    Churned_Customers=("Churn_Flag", "sum")
).reset_index()

charge_summary["Churn_Rate"] = (
    charge_summary["Churned_Customers"]
    / charge_summary["Customers"] * 100
)
charge_summary.to_csv(PROCESSED_DIR / "churn_by_monthly_charge.csv", index=False)

# 7. Generate charts
plt.figure(figsize=(7, 5))
df["Churn"].value_counts().plot(kind="bar")
plt.title("Customer Churn Distribution")
plt.ylabel("Customers")
plt.tight_layout()
plt.savefig(CHART_DIR / "churn_distribution.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 5))
plt.bar(contract_summary["Contract"], contract_summary["Churn_Rate"])
plt.title("Churn Rate by Contract")
plt.ylabel("Churn Rate (%)")
plt.tight_layout()
plt.savefig(CHART_DIR / "churn_by_contract.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 5))
plt.bar(tenure_summary["Tenure_Group"].astype(str), tenure_summary["Churn_Rate"])
plt.title("Churn Rate by Tenure")
plt.ylabel("Churn Rate (%)")
plt.tight_layout()
plt.savefig(CHART_DIR / "churn_by_tenure.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 5))
plt.bar(charge_summary["Monthly_Charge_Band"].astype(str), charge_summary["Churn_Rate"])
plt.title("Churn Rate by Monthly Charge")
plt.ylabel("Churn Rate (%)")
plt.tight_layout()
plt.savefig(CHART_DIR / "churn_by_monthly_charge.png", dpi=150)
plt.close()

print("\nEDA RESULTS")
print("\nChurn Summary:")
print(churn_summary.round(2).to_string(index=False))
print("\nContract:")
print(contract_summary.round(2).to_string(index=False))
print("\nTenure:")
print(tenure_summary.round(2).to_string(index=False))
print("\nPayment Method:")
print(payment_summary.round(2).to_string(index=False))
print("\nInternet Service:")
print(internet_summary.round(2).to_string(index=False))
print("\nMonthly Charges:")
print(charge_summary.round(2).to_string(index=False))

print("\nEDA completed successfully.")
print(f"Charts saved to: {CHART_DIR}")
