# Nassau Candy - Factory Optimization & Distribution Analysis

Data analysis and decision support dashboard for factory assignment optimization, shipping lead-time reduction, and gross profit analysis at Nassau Candy Distributors.

## Live Dashboard

Built with **Streamlit** featuring interactive analytics:

- **Factory Performance Overview** -- Compare production facilities on average lead times, total items shipped, gross profits, and geographical distribution.
- **Factory Assignment Optimization** -- Dynamic product assignment simulation. Adjust the priority weight between lead time and gross profit to see optimal factory-product recommendations.
- **Product-Level Insights** -- Detailed analysis of lead times, profit margins, and distribution counts for individual confectionery products.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Visualizations | Plotly (maps, bar charts, scatter plots) |
| Data Processing | Pandas, NumPy |
| Modelling | Custom recommendation engine (multi-attribute utility scoring) |

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Dataset & Files

- `Nassau_Candy_Distributor.csv` -- Transactional distribution data containing order dates, ship dates, product names, gross profits, and quantities.
- `Nassau_Candy_Analysis.ipynb` -- Jupyter notebook containing exploratory data analysis (EDA), data cleaning, and prototype factory assignment logic.
- `recommendations.csv` -- Saved output of optimal product-to-factory recommendations.

## Optimization Engine Methodology

To optimize product assignments, the custom recommendation engine computes a score for each factory based on two metrics:
1. **Normalized Lead Time (T)** (aiming to minimize)
2. **Normalized Gross Profit (P)** (aiming to maximize)

The score is calculated using an adjustable priority weight ($w$):

$$\text{Score} = w \cdot (1 - \overline{T}) + (1 - w) \cdot \overline{P}$$

The product is recommended to the factory that yields the highest score for that product.

## Project Structure

```
Nassau_Candy_Project/
    app.py                           # Streamlit dashboard
    Nassau_Candy_Analysis.ipynb      # EDA notebook
    Nassau_Candy_Distributor.csv     # Distribution dataset
    Nassau_Candy_Research_Paper.docx # Detailed research findings
    Nassau_Candy_Executive_Summary.docx # Exec summary
    recommendations.csv              # Model recommendations output
    requirements.txt                 # Dependencies
```

## Author

Built by **Nouman Ahmed** as part of the Unified Mentor internship program.
