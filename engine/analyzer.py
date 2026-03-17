import pandas as pd

from engine.logger import get_logger


def analyze_data(df: pd.DataFrame) -> dict:
    """
    This method analyzes data and returns key information about a dataset.
    """
    logger = get_logger()

    shape = df.shape
    total_missing_value = df.isna().sum().sum()

    logger.info(f"Dataset shape: {shape[0]} rows, {shape[1]} columns")
    logger.info(f"Total missing values: {total_missing_value}")

    numerical_cols, categorical_cols, identifier_cols = classifier(df)

    logger.info(f"Detected {len(numerical_cols)} numeric columns")
    logger.info(f"Detected {len(categorical_cols)} categorical columns")
    logger.info(f"Detected {len(identifier_cols)} identifier columns")

    basic_stats = df[numerical_cols].describe()
    logger.info(
        f"Basic statistic calculated for {len(numerical_cols)} columns")

    if len(numerical_cols) > 1:
        correlation_matrix = df[numerical_cols].corr()
        logger.info(
            f"Correlation matrix computed ({len(numerical_cols)} x {len(numerical_cols)})")
    else:
        correlation_matrix = None
        logger.info("Correlation matrix skipped(not enough numeric columns)")

    categorical_summary = pd.DataFrame({
        "column": categorical_cols,
        "unique_values": df[categorical_cols].nunique().values
    })

    return {
        "dataset_shape": shape,
        "numerical_columns": numerical_cols,
        "categorical_columns": categorical_cols,
        "identifier_columns": identifier_cols,
        "basic_stats": basic_stats,
        "correlation_matrix": correlation_matrix,
        "unique_values": categorical_summary
    }


def classifier(df: pd.DataFrame):

    numeric_cols = []
    categorical_cols = []
    identifier_cols = []

    rows = len(df)

    for col in df.columns:

        unique_count = df[col].nunique()
        unique_ratio = unique_count / rows

        if unique_ratio > 0.95:
            identifier_cols.append(col)

        elif pd.api.types.is_float_dtype(df[col]):
            numeric_cols.append(col)

        elif pd.api.types.is_integer_dtype(df[col]):

            if unique_count < 20 or unique_ratio < 0.05:
                categorical_cols.append(col)
            else:
                numeric_cols.append(col)

        else:
            categorical_cols.append(col)

    return numeric_cols, categorical_cols, identifier_cols
