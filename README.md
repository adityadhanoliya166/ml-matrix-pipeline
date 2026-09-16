# ML Matrix Pipeline

A Python and FastAPI data engineering pipeline that converts raw, messy CSV datasets into clean, scaled, and encoded feature matrices ready for machine learning model training.

## Key Features

* **Automated Data Cleaning:** Safe numerical casting with `pd.to_numeric` and automated missing-value imputation (median for numeric features, `"Missing"` for categorical features).
* **Feature Encoding & Scaling:** Applies `StandardScaler` to continuous numeric columns and `OneHotEncoder` to categorical variables using Scikit-Learn's `ColumnTransformer`.
* **Instant ML Readiness Score:** Integrates a `RandomForestClassifier` baseline evaluation step to immediately score the processed data's quality.
* **Minimalist Interface:** Clean, dark-themed UI built with standard web technologies for quick file uploads and instant feature previews.

## Tech Stack

* **Backend:** Python, FastAPI, Pandas, Scikit-Learn, Uvicorn
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)

## Project Structure

```text
ML Matrix Pipeline/
│
├── main.py             # FastAPI server and quality evaluation logic
├── transformer.py      # Core data processing & feature matrix engine
├── requirements.txt    # Project dependencies
└── Frontend/
    ├── index.html      # Dark-theme web interface
    ├── style.css       # Custom styling
    └── script.js       # Asynchronous upload & table rendering logic