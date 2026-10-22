from pathlib import Path
import pandas as pd

RAW_FILE = "data/raw/finance_transactions.csv"


def load_transactions(file_path=RAW_FILE):
    """Load the raw finance transactions from a CSV file."""
    return pd.read_csv(file_path)


def profile_transactions(df):
    """Display basic data-quality information."""
    print("Dataset dimensions:", df.shape)

    print("\nMissing values by column:")
    print(df.isnull().sum())

    print("\nExact duplicate rows:", df.duplicated().sum())

    print("\nNegative amount records:")
    print(df[df["amount"] < 0])

def remove_exact_duplicates(df):
    """Remove exact duplicate rows while preserving the original DataFrame."""
    cleaned = df.drop_duplicates().copy()
    return cleaned


def standardise_departments(df):
    """Standardise department names using approved mappings."""
    cleaned = df.copy()

    department_mapping = {
        "finance": "Finance",
        "hr": "HR",
        "it": "IT",
        "procurement": "Procurement",
    }

    cleaned["department"] = (
        cleaned["department"]
        .str.strip()
        .str.casefold()
        .map(department_mapping)
        .fillna(cleaned["department"])
    )

    return cleaned

def add_quality_flags(df):
    """Flag transactions that require data-quality review."""
    cleaned = df.copy()

    cleaned["missing_vendor"] = cleaned["vendor"].isna()
    cleaned["missing_amount"] = cleaned["amount"].isna()
    cleaned["negative_amount"] = cleaned["amount"] < 0

    cleaned["requires_review"] = cleaned[
        ["missing_vendor", "missing_amount", "negative_amount"]
    ].any(axis=1)

    return cleaned

    

def run_pipeline():
    """Run the complete finance transaction data pipeline."""

    raw_df = load_transactions()
    rows_loaded = len(raw_df)

    deduplicated_df = remove_exact_duplicates(raw_df)
    standardised_df = standardise_departments(deduplicated_df)
    processed_df = add_quality_flags(standardised_df)

    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    processed_path = output_dir / "finance_transactions_processed.csv"
    processed_df.to_csv(processed_path, index=False)

    review_df = processed_df[processed_df["requires_review"]].copy()
    review_path = output_dir / "transactions_requiring_review.csv"
    review_df.to_csv(review_path, index=False)

    print("\n--- Pipeline Execution Summary ---")
    print(f"Rows loaded: {rows_loaded}")
    print(f"Rows after duplicate removal: {len(deduplicated_df)}")
    print(f"Rows requiring review: {len(review_df)}")
    print(f"Processed data saved to: {processed_path}")
    print(f"Review records saved to: {review_path}")

    return processed_df


if __name__ == "__main__":
    run_pipeline()

