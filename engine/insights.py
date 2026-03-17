import pandas as pd

from engine.logger import get_logger

CORRELATION_THRESHOLD = 0.8
IMBALANCE_THRESHOLD = 0.8
SKEW_THRESHOLD = 1
CARDINALITY_THRESHOLD = 0.5

logger = get_logger()


def generate_insights(df: pd.DataFrame, analysis_results: dict) -> list[str]:
    insights = []

    insights += detect_correlations(analysis_results)
    insights += detect_skewness(df, analysis_results)
    insights += detect_imbalance(df, analysis_results)
    insights += detect_cardinality(df, analysis_results)

    return insights


def detect_correlations(analysis_results: dict) -> list[str]:
    corr_matrix = analysis_results["correlation_matrix"]

    if corr_matrix is None or corr_matrix.empty:
        return []

    cols = corr_matrix.columns
    correlations = []

    for i in range(len(cols)):
        for j in range(i+1, len(cols)):
            col1 = cols[i]
            col2 = cols[j]

            corr_value = corr_matrix.loc[col1, col2]

            if pd.isna(corr_value):
                continue

            if abs(corr_value) >= CORRELATION_THRESHOLD:
                correlations.append(
                    f"Strong correlation detected between {col1} and {col2} ({corr_value:.2f})")

    return correlations


def detect_skewness(df: pd.DataFrame, analysis_results: dict) -> list[str]:
    numerical_columns = analysis_results["numerical_columns"]

    insights = []

    for col in numerical_columns:
        data = df[col].dropna()

        if len(data) < 10:
            continue

        if data.nunique() <= 1:
            continue

        skew_value = data.skew()
        skew_value = float(skew_value)

        logger.info(f"Skew detected in {col}: {skew_value:.2f}")

        if skew_value > SKEW_THRESHOLD:
            insights.append(
                f"Feature '{col}' is highly right-skewed ({skew_value:.2f})")

        elif skew_value < -SKEW_THRESHOLD:
            insights.append(
                f"Feature '{col}' is highly left-skewed ({skew_value:.2f})")

    return insights


def detect_imbalance(df: pd.DataFrame, analysis_results: dict) -> list[str]:
    insights = []
    categorical_columns = analysis_results["categorical_columns"]

    for col in categorical_columns:
        data = df[col].dropna()

        if data.empty:
            continue

        if len(data) < 10:
            continue

        value_counts = data.value_counts(normalize=True)
        top_ratio = value_counts.iloc[0]
        top_category = value_counts.index[0]
        top_percent = top_ratio * 100

        logger.info(f"Imbalance detected in {col}: {top_ratio:.2f}")

        if top_ratio > IMBALANCE_THRESHOLD:
            insights.append(
                f"Feature '{col}' is highly imbalanced ({top_category} = {top_percent:.1f}%)")

    return insights


def detect_cardinality(df: pd.DataFrame, analysis_results: dict) -> list[str]:
    insights = []

    numerical_cols = set(analysis_results["numerical_columns"])

    if len(df) == 0:
        return []

    for col in df.columns:
        data = df[col].dropna()

        if data.empty:
            continue

        if len(data) < 10:
            continue

        if col in numerical_cols:
            continue

        unique_ratio = data.nunique() / len(data)
        unique_ratio_percent = unique_ratio * 100

        logger.info(f"Cardinality detected in {col}: {unique_ratio:.2f}")

        if unique_ratio > 0.95:
            insights.append(
                f"Feature '{col}' appears to be an identifier column ({unique_ratio_percent:.1f}%+ unique values)")
        elif unique_ratio > CARDINALITY_THRESHOLD:
            insights.append(
                f"Feature '{col}' has high cardinality ({unique_ratio_percent:.1f}% unique values)")

    return insights
