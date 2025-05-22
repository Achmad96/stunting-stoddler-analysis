# Stunting Toddler Analysis Dashboard

This dashboard is a Streamlit-based web application for analyzing and visualizing toddler stunting data, focusing on height and nutrition status compared to WHO standards.

---

## Installation Guide

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/stunting-toddler-analysis.git
cd stunting-toddler-analysis
```

### 2. (Optional) Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:

```bash
pip install streamlit pandas plotly
```

### 4. Run the Application

```bash
streamlit run stunting_toddler_analysis.py
```

Open the provided URL (usually http://localhost:8501) in your browser.

---

## User Guide

### Dashboard Features

- **Data Preview**: View and download the filtered dataset.
- **Statistical Analysis**: See summary statistics and metrics.
- **Growth Status Distribution**: Bar chart of nutrition status.
- **WHO Standards Comparison**: Compare height data with WHO standards.
- **Gender-Based Analysis**: Pie charts by gender.
- **Height-Age Correlation**: Scatter plot of height vs. age.
- **Age Distribution Analysis**: Line chart of nutrition status by age.

### How to Use

1. **Filter Data**: Use the sidebar to filter by gender, age, and nutrition status.
2. **Explore Visualizations**: All charts and tables update based on your filters.
3. **Download Data**: Click "Unduh sebagai CSV" to download the filtered data.

### Data Classification

- **Severely Stunted**: Height far below standard
- **Stunted**: Height below standard
- **Normal**: Height within standard
- **Above Average**: Height above standard

WHO height standards are shown in the dashboard for reference.

---

## Data Source

Dataset: [Stunting Toddler (Balita) Detection (121K rows)](https://www.kaggle.com/datasets/rendiputra/stunting-balita-detection-121k-rows)

---

## Troubleshooting

- **Dashboard not loading**: Check dependencies and Streamlit installation.
- **No visualizations**: Ensure Plotly is installed and data file exists.
- **Filter errors**: Reset filters or check dataset columns.

For more help, see the GitHub repository or contact the maintainer.
