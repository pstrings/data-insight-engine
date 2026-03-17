from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

from datetime import datetime
from pathlib import Path

from engine.logger import get_logger

logger = get_logger()


MAX_IMAGES = 20


def generate_report(
    df,
    missing_summary_df,
    insights,
    plots_dir="plots",
    output_path="reports/report.pdf"
):
    """
    Generate a PDF report from analysis results.
    """

    try:
        # Ensure report directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()

        elements = []

        # -------------------------
        # 1. TITLE
        # -------------------------
        elements.append(
            Paragraph("Automated Data Analysis Report", styles["Title"]))
        elements.append(Spacer(1, 12))

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elements.append(
            Paragraph(f"Generated on: {timestamp}", styles["Normal"]))
        elements.append(Spacer(1, 20))

        logger.info("Added title section to report")

        # -------------------------
        # 2. DATASET OVERVIEW
        # -------------------------
        rows, cols = df.shape

        elements.append(Paragraph("Dataset Overview", styles["Heading2"]))
        elements.append(Paragraph(f"Rows: {rows}", styles["Normal"]))
        elements.append(Paragraph(f"Columns: {cols}", styles["Normal"]))
        elements.append(Spacer(1, 20))

        logger.info("Added dataset overview")

        # -------------------------
        # 3. MISSING DATA TABLE
        # -------------------------
        elements.append(Paragraph("Missing Data Summary", styles["Heading2"]))
        elements.append(Spacer(1, 10))

        table_data = [["Feature", "Missing Count", "Missing %"]]

        for _, row in missing_summary_df.iterrows():
            table_data.append([
                str(row["feature"]),
                str(int(row["missing_count"])),
                f"{row['missing_percent']:.2f}%"
            ])

        table = Table(table_data)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))

        logger.info("Added missing data table")

        # -------------------------
        # 4. INSIGHTS
        # -------------------------
        elements.append(Paragraph("Key Insights", styles["Heading2"]))
        elements.append(Spacer(1, 10))

        if insights:
            for insight in insights:
                elements.append(Paragraph(f"• {insight}", styles["Normal"]))
        else:
            elements.append(
                Paragraph("No significant insights detected.", styles["Normal"]))

        elements.append(Spacer(1, 20))

        logger.info("Added insights section")

        # -------------------------
        # 5. VISUALIZATIONS
        # -------------------------
        elements.append(PageBreak())
        elements.append(Paragraph("Visualizations", styles["Heading2"]))
        elements.append(Spacer(1, 10))

        plot_dir = Path(plots_dir)

        if plot_dir.exists():
            image_paths = list(plot_dir.rglob("*.png"))

            # Sort for better readability
            image_paths = sorted(image_paths)

            for idx, image_path in enumerate(image_paths[:MAX_IMAGES]):

                try:
                    elements.append(
                        Paragraph(image_path.stem, styles["Normal"]))
                    elements.append(Spacer(1, 6))

                    elements.append(
                        Image(str(image_path), width=400, height=250))
                    elements.append(Spacer(1, 12))

                except Exception as e:
                    logger.warning(f"Failed to add image {image_path}: {e}")

        else:
            elements.append(Paragraph("No plots found.", styles["Normal"]))

        logger.info("Added visualizations section")

        # -------------------------
        # BUILD PDF
        # -------------------------
        doc.build(elements)

        logger.info(f"Report generated successfully at {output_path}")

    except Exception as e:
        logger.exception(f"Failed to generate report: {e}")
