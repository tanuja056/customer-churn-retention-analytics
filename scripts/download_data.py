
from pathlib import Path
import urllib.request

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset destination
DATA_DIR = BASE_DIR / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATA_URL = (
    "https://raw.githubusercontent.com/"
    "IBM/telco-customer-churn-on-icp4d/"
    "master/data/Telco-Customer-Churn.csv"
)

OUTPUT_FILE = DATA_DIR / "telco_customer_churn.csv"

print("Downloading customer churn dataset...")

urllib.request.urlretrieve(DATA_URL, OUTPUT_FILE)

print("Download completed!")
print(f"Saved to: {OUTPUT_FILE}")
    