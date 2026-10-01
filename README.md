# SQL E-Commerce Business Analysis

A normalized SQLite e-commerce database plus business-focused SQL analysis covering revenue, customers, products, countries and retention.

## Skills demonstrated
- SQL joins
- GROUP BY / HAVING
- CTEs
- Window functions
- SQLite
- Business KPI analysis
- Relational data modeling

## Repository structure
- `data/` — local dataset so the project runs without downloading anything
- `src/main.py` — complete reproducible pipeline
- `outputs/` — generated metrics, tables and visualizations
- `notebook.ipynb` — notebook launcher
- `requirements.txt` — Python dependencies
- `LINKEDIN_POST.md` — concise project description for LinkedIn

## Run
```bash
pip install -r requirements.txt
python src/main.py
```

The random seed is fixed where applicable, so results are reproducible.
