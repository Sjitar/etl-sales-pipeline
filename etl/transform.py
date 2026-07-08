import pandas as pd
from etl.logger import get_logger
from etl.config import RAW_DIR, PROCESSED_DIR
from etl.validation import validate_file_exists, validate_sales_data
logger = get_logger(__name__)

def transform_dataframe(df):
    """
    Validate and transform sales data.
    """

    validate_sales_data(df)

    result = df.copy()

    result["total"] = result["quantity"] * result["price"]

    return result

def transform_sales():
    raw_file = RAW_DIR / "sales.csv"
    processed_file = PROCESSED_DIR / "sales_clean.csv"

    validate_file_exists(raw_file)

    df = pd.read_csv(raw_file)

    transformed_df = transform_dataframe(df)

    processed_file.parent.mkdir(parents=True, exist_ok=True)
    transformed_df.to_csv(processed_file, index=False)

    logger.info("Rows processed: %s", len(df))
    logger.info("Saved cleaned sales data to %s", processed_file)

if __name__ == "__main__":
    transform_sales()