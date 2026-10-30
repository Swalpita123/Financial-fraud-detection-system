# 🛡️ Financial Fraud & Anomaly Detection System

An end-to-end Machine Learning project designed to analyze financial transactions and identify potentially fraudulent activities using Python and Scikit-learn. It includes a REST API built with FastAPI and Pydantic, along with an interactive Streamlit dashboard for transaction analysis, fraud prediction, batch processing, and model evaluation.

## 🚀 Project Overview

Financial fraud detection is an important application of machine learning in the financial industry. This project demonstrates how transaction data can be processed, analyzed, and used to train a classification model to identify potentially fraudulent transactions.

The system provides individual and batch transaction predictions, interactive visualizations, and model performance evaluation through a user-friendly dashboard.

**Note:** This is an educational demonstration using synthetic, rule-labelled transaction data. It is not a production-ready fraud detection system.

## ✨ Key Features

- **Data Analysis:** Explore transaction patterns using Pandas and NumPy.
- **Data Visualization:** Interactive charts for transaction distributions, fraud trends, and feature correlations.
- **Machine Learning:** Train a Scikit-learn classification model to predict potentially fraudulent transactions.
- **Model Evaluation:** Evaluate performance using Accuracy, Precision, Recall, F1-score, Average Precision, and a Confusion Matrix.
- **Individual Prediction:** Enter transaction details and receive a fraud prediction.
- **Batch Prediction:** Upload a CSV file containing multiple transactions for fraud classification.
- **Data Explorer:** Filter and explore transaction records.
- **Interactive Dashboard:** Dark-themed Streamlit dashboard with separate sections for analytics, evaluation, predictions, batch detection, and data exploration.
- **REST API:** FastAPI and Pydantic for structured transaction validation and prediction integration.

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas, NumPy |
| Data Visualization | Matplotlib, Plotly |
| Machine Learning | Scikit-learn |
| API Development | FastAPI |
| Data Validation | Pydantic |
| Dashboard | Streamlit |
| Model Persistence | Joblib |
| Version Control | Git, GitHub |

## 📊 Dashboard Modules

### 1. Analytics
- Total transactions analyzed
- Fraud-labelled records
- Labelled fraud rate
- Held-out F1-score
- Transaction amount distribution
- Fraud trends by hour
- Transaction feature analysis
- Feature correlation matrix

### 2. Model Evaluation
- Accuracy
- Precision
- Recall
- F1-score
- Average Precision
- Confusion Matrix
- Precision-Recall Curve
- Feature Importance / Coefficients

### 3. Predict Transaction
Enter individual transaction details to generate a model prediction.

### 4. Batch Fraud Detection
Upload a CSV file containing transaction records and generate predictions for multiple transactions.

### 5. Explore Data
Explore transaction records and filter data based on transaction labels.

## 📁 Project Structure

```text
financial-fraud-detection-system/
│
├── dashboard.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── data.py
│   ├── features.py
│   └── train.py
│
├── dashboard_components/
│   ├── __init__.py
│   ├── styles.py
│   ├── overview.py
│   ├── model_evaluation.py
│   ├── predictions.py
│   ├── batch_prediction.py
│   └── data_explorer.py
│
├── data/
│   └── transactions.csv
│
└── artifacts/
    ├── fraud_model.joblib
    ├── metrics.json
    └── evaluation charts
```

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Swalpita123/Financial-fraud-detection-system.git
```

### 2. Navigate to the Project Directory

```bash
cd financial-fraud-detection-system
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Train the Machine Learning Model

Run the following command from the project root:

```bash
python -m src.train
```

This prepares the required model and evaluation artifacts.

### 6. Launch the Streamlit Dashboard

```bash
streamlit run dashboard.py
```

Open the local URL displayed in your terminal to access the dashboard.

## 📈 Model Evaluation

The model is evaluated using multiple classification metrics:

- **Accuracy:** Measures overall classification correctness.
- **Precision:** Measures how many predicted fraud cases are actually labelled as fraud.
- **Recall:** Measures how many labelled fraud cases are correctly identified.
- **F1-score:** Balances precision and recall.
- **Average Precision:** Summarizes precision-recall performance.

These metrics help assess model performance, particularly when working with imbalanced transaction data.

## 🔮 Future Improvements

- Experiment with additional classification algorithms.
- Improve fraud detection using real-world datasets.
- Apply advanced anomaly detection techniques.
- Add model explainability using SHAP.
- Implement authentication and role-based access.
- Add real-time transaction monitoring.
- Deploy the application using cloud infrastructure.

## 👩‍💻 Author

**Swalpita Ray Nayak**

- GitHub: https://github.com/YOUR_USERNAME

## 📄 License

This project is intended for educational and learning purposes. Add an appropriate open-source license if you want others to reuse or distribute the code.
