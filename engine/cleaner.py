import pandas as pd

from engine.logger import get_logger


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Cleans the dataframe and generate report about missing data.
    """
    logger = get_logger()
    df = df.dropna(how="all")

    logger.info("Removed rows with all values missing")

    missing_series = df.isna().sum()
    missing_percentage_series = (missing_series * 100) / len(df)

    missing_summary_df = pd.DataFrame({
        "Missing Values": missing_series,
        "Missing Value Percentage (%)": missing_percentage_series
    })

    missing_summary_df = missing_summary_df.reset_index()
    missing_summary_df.rename(columns={"index": "feature"}, inplace=True)

    missing_summary_df = missing_summary_df.sort_values(
        by='Missing Value Percentage (%)', ascending=False)

    missing_more_than_40 = missing_summary_df.loc[
        missing_summary_df['Missing Value Percentage (%)'] > 40, 'feature']

    # Logging warnings
    high_missing = missing_summary_df[
        missing_summary_df["missing_percent"] > 40
    ]["feature"]

    if not high_missing.empty:
        logger.warning(
            f"WARNING! Columns with >40% missing values: {list(high_missing)}"
        )

    severe_missing = missing_summary_df[
        missing_summary_df["missing_percent"] > 70
    ]["feature"]

    if not severe_missing.empty:
        logger.critical(
            f"CRITICAL! Columns with >70% missing values: {list(severe_missing)}"
        )

    return df, missing_summary_df
