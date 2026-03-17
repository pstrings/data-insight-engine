import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from engine.logger import get_logger
from pathlib import Path

logger = get_logger()
sns.set_theme(style="whitegrid")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PLOTS_DIR = PROJECT_ROOT / "plots"


def generate_plots(df: pd.DataFrame, analysis_results: dict):
    make_directory()

    # Histograms for numeric data
    generate_histograms(df, analysis_results["numerical_columns"])

    # Boxplots to see outliers in numerical data
    generate_boxplots(df, analysis_results["numerical_columns"])

    # Heatmap for correlation matrix
    if len(analysis_results["numerical_columns"]) >= 2:
        generate_heatmap(analysis_results["correlation_matrix"])

    #  Categorical countplot for categorical data
    generate_categorical_countplots(
        df, analysis_results["categorical_columns"])


def make_directory():
    distributions_path = PLOTS_DIR / "distributions"
    correlations_path = PLOTS_DIR / "correlations"
    categorical_path = PLOTS_DIR / "categorical"
    outliers_path = PLOTS_DIR / "outliers"

    distributions_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Directory created at path: {distributions_path}")

    correlations_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Directory created at path: {correlations_path}")

    categorical_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Directory created at path: {categorical_path}")

    outliers_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Directory created at path: {outliers_path}")


def generate_histograms(df: pd.DataFrame, numerical_cols: list):

    output_dir = PLOTS_DIR / "distributions"
    output_dir.mkdir(parents=True, exist_ok=True)

    for col in numerical_cols[:20]:

        try:
            if df[col].dropna().empty:
                logger.warning(f"Skipping {col} (no valid values)")
                continue

            if df[col].nunique() <= 1:
                logger.info(f"Skipping {col} (constant column)")
                continue

            fig, ax = plt.subplots(figsize=(8, 5))

            sns.histplot(df[col].dropna(), bins=30, ax=ax)

            ax.set_title(f"{col} Distribution")
            ax.set_xlabel(col)
            ax.set_ylabel("Frequency")

            file_path = output_dir / f"{col}_hist.png"
            plt.tight_layout()
            plt.savefig(file_path)
            plt.close()

            logger.info(f"Histogram saved: {file_path}")

        except Exception as e:
            logger.warning(f"Skipping histogram for {col}: {e}")


def generate_boxplots(df: pd.DataFrame, numerical_cols: list):
    output_dir = PLOTS_DIR / "outliers"
    output_dir.mkdir(parents=True, exist_ok=True)

    for col in numerical_cols[:20]:
        try:
            if df[col].dropna().empty:
                logger.warning(f"Skipping {col} (no valid values)")
                continue

            if df[col].nunique() <= 1:
                logger.info(f"Skipping {col} (constant column)")
                continue

            fig, ax = plt.subplots(figsize=(8, 5))

            sns.boxplot(x=df[col].dropna(), ax=ax)
            ax.set_title(f"{col} Boxplot (Outlier Detection)")
            ax.set_xlabel(col)

            file_path = output_dir / f"{col}_boxplot.png"
            plt.tight_layout()
            plt.savefig(file_path)
            plt.close()

            logger.info(f"Boxplot saved: {file_path}")
        except Exception as e:
            logger.warning(f"Skipping boxplot for {col}: {e}")


def generate_heatmap(correlation_matrix: pd.DataFrame):
    output_dir = PLOTS_DIR / "correlations"
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        if correlation_matrix.shape[0] < 2:
            logger.info("Skipping heatmap (not enough numeric columns)")
            return

        fig, ax = plt.subplots(figsize=(10, 8))

        sns.heatmap(correlation_matrix, annot=True,
                    cmap='coolwarm', center=0, ax=ax)
        ax.set_title("Correlation Heatmap")

        file_path = output_dir / "correlation_heatmap.png"
        plt.tight_layout()
        plt.savefig(file_path)
        plt.close()

        logger.info(f"Heatmap saved: {file_path}")
    except Exception as e:
        logger.warning(f"Skipping heatmap for: {e}")


def generate_categorical_countplots(df: pd.DataFrame, categorical_columns: list):
    output_dir = PLOTS_DIR / "categorical"
    output_dir.mkdir(parents=True, exist_ok=True)

    for col in categorical_columns[:15]:
        try:
            if df[col].dropna().empty:
                logger.warning(f"Skipping {col} (no valid values)")
                continue
            if df[col].nunique() > 30:
                logger.info(f"Skipping {col} (unique values more than 30)")
                continue

            fig, ax = plt.subplots(figsize=(8, 5))
            sns.countplot(x=df[col].dropna(), ax=ax)
            ax.set_title(f"{col} Categorical Countplot")
            ax.tick_params(axis="x", rotation=45)

            file_path = output_dir / f"{col}_countplot.png"
            plt.tight_layout()
            plt.savefig(file_path)
            plt.close()

            logger.info(f"Countplot saved: {file_path}")
        except Exception as e:
            logger.warning(f"Skipping countplot for {col}: {e}")
