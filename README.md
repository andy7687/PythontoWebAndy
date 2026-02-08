# 📊 Andy's Analytics

A modern, interactive data analytics dashboard built with **Streamlit** and **Plotly**. Analyze your Excel data with powerful visualizations, filters, and real-time statistics.

## ✨ Features

- **📈 5 Chart Types**: Bar, Line, Area, Scatter, and Pie charts for flexible data visualization
- **🔍 Smart Filtering**: 
  - Multi-select filters for categorical columns
  - Dynamic numeric range sliders
  - Real-time data filtering with instant updates
- **📊 Key Metrics Dashboard**: 
  - Total, Average, and Maximum calculations
  - Context-aware KPI cards
- **📋 Data Management**:
  - Full data preview with head/tail toggle
  - Column type inspection (schema view)
  - Download filtered or full datasets as CSV
- **📈 Statistical Analysis**:
  - Descriptive statistics (mean, std, min, max, quartiles)
  - Distribution histograms
  - Summary tables for multiple columns
- **⚙️ Advanced Controls**:
  - X/Y axis selector for custom analysis
  - Sort by metric (ascending/descending)
  - Chart type selector with dynamic validation
- **🎯 Robust Error Handling**:
  - File validation (missing/empty file detection)
  - Type checking for chart compatibility
  - Graceful fallbacks for edge cases

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip or conda package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/andy7687/PythontoWebAndy.git
   cd PythontoWebAndy
   ```

2. **Create and activate virtual environment** (recommended):
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # macOS/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your data**:
   - Place your `data.xlsx` file in the project root directory (next to `app.py`)

### Running the App

#### Option 1: Using the batch file (Windows)
```bash
run_app.bat
```

#### Option 2: Using Python directly
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
PythontoWebAndy/
├── app.py                 # Main Streamlit application
├── data.xlsx             # Your data file (add here)
├── requirements.txt      # Python dependencies
├── run_app.bat          # Windows batch script to run app
└── README.md            # This file
```

## 📦 Dependencies

- **streamlit** (1.29.0) - Interactive web app framework
- **pandas** (2.1.3) - Data manipulation and analysis
- **plotly** (5.18.0) - Interactive charting library
- **openpyxl** (3.1.2) - Excel file support

## 🎯 Usage Guide

### 1. **Prepare Your Data**
   - Ensure your Excel file has headers in the first row
   - Supported columns: Text (categorical) and numbers (numeric)
   - Recommended format: `Product`, `Sales`, `Date`, etc.

### 2. **Load the Dashboard**
   - Run the app and it automatically loads `data.xlsx`
   - Check file status in the sidebar ("Data Controls" section)

### 3. **Filter Data**
   - Open "🔍 Filters" in sidebar
   - Select products or categories from dropdown
   - Use numeric sliders to filter by value range
   - Data updates in real-time

### 4. **Visualize Data**
   - Open "📈 Visualization" in sidebar
   - Select X-axis (categorical preferred)
   - Select Y-axis (numeric required for most charts)
   - Choose chart type (Bar, Line, Area, Scatter, Pie)
   - Check "Sort by Y" to order by metric descending

### 5. **Analyze Statistics**
   - Scroll to "📈 Summary Statistics"
   - View descriptive stats and distribution histogram
   - Expander shows stats for all numeric columns

### 6. **Export Data**
   - Open "📥 Export" in sidebar
   - Download filtered data (applies current filters)
   - Download full data (all rows, unfiltered)

## 🔧 Python Interpreter Selection

This project uses a virtual environment (`.venv`) to isolate dependencies.

**VS Code Users:**
1. Press `Ctrl + Shift + P`
2. Search for "Python: Select Interpreter"
3. Choose `.venv` from the list
4. Restart the terminal for changes to take effect

**Command Line:**
```bash
# Windows
.venv\Scripts\python -m streamlit run app.py

# macOS/Linux
source .venv/bin/activate
python -m streamlit run app.py
```

## 📊 Data Format Example

| Product | Sales | Region | Date |
|---------|-------|--------|------|
| Widget A | 1500 | North | 2024-01-15 |
| Widget B | 2300 | South | 2024-01-15 |
| Widget A | 1800 | East | 2024-01-16 |

**Recommended structure**: First row = headers, consistent data types per column.

## 🎨 Customization

### Change App Title
Edit `app.py` line 11:
```python
page_title="Andy's Analytics",  # Change here
```

### Adjust Colors/Styling
Edit the CSS section in `app.py` (lines 18-40) to customize theme colors and spacing.

### Add More Chart Types
In `app.py`, expand the chart selector logic to include additional Plotly chart types.

### Default Filter Columns
Modify `app.py` line ~160 to change default filters:
```python
if "Product" in categorical_cols:  # Change "Product" to your column name
```

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| "File not found" | Place `data.xlsx` next to `app.py` in project root |
| "Excel file is empty" | Check that your Excel file contains data in worksheet |
| Chart won't display | Ensure Y-axis column is numeric (numbers, not text) |
| Filters not working | Verify column names match your data (case-sensitive) |
| Slow performance | For large files (100k+ rows), consider filtering to relevant rows |

## 📝 License

MIT License - feel free to use and modify for your needs.

## 👤 Author

Created by **Andy** - [GitHub Profile](https://github.com/andy7687)

## 🤝 Contributing

Have ideas for improvements? Feel free to fork, modify, and submit pull requests!

---

## 📞 Support

For issues or questions:
1. Check the **Troubleshooting** section above
2. Review the **Quick Start** guide
3. Inspect `data.xlsx` file format
4. Check Python version: `python --version` (requires 3.10+)

---

**Last Updated:** February 8, 2026  
**Current Version:** 1.0
