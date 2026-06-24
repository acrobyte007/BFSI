# BFSI Reputation System

A comprehensive reputation management and classification system for the Banking, Financial Services, and Insurance (BFSI) sector. This project leverages AI-powered taxonomy classification, data cleaning pipelines, and a user-friendly Streamlit dashboard to analyze and categorize reputation-related data.

## Features

- **Taxonomy Database**: Structured database for BFSI reputation categories and subcategories.
- **Data Cleaning Pipeline**: Jupyter notebook for preprocessing raw data into cleaned datasets.
- **AI Classification**: Uses Mistral API for intelligent classification of reputation events and mentions.
- **Interactive Dashboard**: Streamlit-based web interface for visualization and exploration of results.

## Project Structure

```bash
bfsi/
├── data/                  # Raw and processed data
├── notebooks/             # Jupyter notebooks for data processing
├── taxonomy_db.py         # Taxonomy database initialization
├── classification.py      # Main classification pipeline
├── app.py                 # Streamlit dashboard
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
└── README.md
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/acrobyte007/BFSI
cd bfsi
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

**Activate the environment:**

- **Windows:**

  ```bash
  venv\Scripts\activate


### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Copy the example environment file and add your API key:

```bash
cp .env.example .env
```

Edit `.env` and add your Mistral API key:

```bash
MISTRAL_API_KEY=your_api_key_here
```

### 5. Initialize Taxonomy Database

```bash
python taxonomy_db.py
```

### 6. Run Data Cleaning Notebook

```bash
jupyter notebook
```

Open `notebooks/analysis.ipynb` and run all cells. This will generate `cleaned_data.csv`.

### 7. Run Classification Pipeline

```bash
python classification.py
```

This processes the cleaned data and outputs results to `data/final_output.csv`.

### 8. Launch Streamlit Dashboard

```bash
streamlit run main.py
```

Open your browser and navigate to: [http://localhost:8501](http://localhost:8501)

## Usage

1. Ensure the taxonomy database is initialized and data is cleaned.
2. Run the classification pipeline to generate categorized outputs.
3. Launch the Streamlit app to explore visualizations, filters, and insights.

## Technologies Used

- Python
- Mistral AI API
- Pandas, NumPy
- Jupyter Notebooks
- Streamlit
- SQLite (for taxonomy database)
- Langchain
