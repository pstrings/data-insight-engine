import argparse

from engine.loader import load_data
from engine.cleaner import clean_data
from engine.analyzer import analyze_data
from engine.visualizer import generate_plots
from engine.insights import generate_insights
from engine.reporter import generate_report

from engine.logger import get_logger

logger = get_logger()


def main():
    parser = argparse.ArgumentParser(
        description="Automated Data Insight Engine")

    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to input CSV file"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="reports/report.pdf",
        help="Path to output PDF report"
    )

    args = parser.parse_args()

    try:
        logger.info("Starting Data Insight Engine")

        # 1. Load data
        df = load_data(args.file)

        # 2. Clean data
        df_clean, missing_summary = clean_data(df)

        # 3. Analyze data
        analysis_results = analyze_data(df_clean)

        # 4. Generate plots
        generate_plots(df_clean, analysis_results)

        # 5. Generate insights
        insights = generate_insights(df_clean, analysis_results)

        # 6. Generate report
        generate_report(
            df_clean,
            missing_summary,
            insights,
            output_path=args.output
        )

        logger.info("Data Insight Engine completed successfully")

    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")


if __name__ == "__main__":
    main()
