# 🚀 Automated Data Insight Engine

An end-to-end automated data analysis tool that generates insights, visualizations, and a professional PDF report from any CSV dataset.

---

## 📌 Features

* 📂 Load and validate CSV datasets
* 🧹 Data cleaning and missing value analysis
* 📊 Automatic data visualization:

  * Histograms
  * Boxplots (outlier detection)
  * Correlation heatmaps
  * Categorical distributions
* 🧠 Intelligent insight generation:

  * Strong correlations
  * Skewed distributions
  * Imbalanced categories
  * High-cardinality features
  * Identifier detection
* 📄 PDF report generation with all results
* 🧾 Logging system for traceability
* ⚙️ CLI-based execution

---

## 🧠 Example Insights Generated

* Strong correlation detected between salary and experience (0.91)
* Feature 'salary' is highly right-skewed (1.87)
* Feature 'department' is highly imbalanced (HR = 92%)
* Feature 'zipcode' appears to be an identifier column (98% unique values)

---

## 🏗️ Project Structure

```
data_insight_engine/

├── main.py
├── requirements.txt
├── logs/
├── reports/
├── plots/
│
└── engine/
    ├── loader.py
    ├── cleaner.py
    ├── analyzer.py
    ├── visualizer.py
    ├── insights.py
    ├── reporter.py
    └── logger.py
```

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/data-insight-engine.git
cd data-insight-engine
pip install -r requirements.txt
```

---

## ▶️ Usage

```bash
python main.py --file data/sample.csv
```

Custom output:

```bash
python main.py --file data/sample.csv --output reports/custom_report.pdf
```

---

## 📦 Output

* 📄 PDF Report → `reports/`
* 📊 Plots → `plots/`
* 🧾 Logs → `logs/engine.log`

---

## 🐳 Docker Support (Optional)

```bash
docker build -t data-insight-engine .
docker run -v $(pwd):/app data-insight-engine --file data/sample.csv
```

---

## 🚀 Future Improvements

* Web interface (upload CSV → download report)
* HTML interactive reports
* AI-generated insights
* Scheduling and automation

---

## 🧑‍💻 Author

Suyash Sharma