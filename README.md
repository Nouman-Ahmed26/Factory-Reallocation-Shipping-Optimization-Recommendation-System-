# 🍬 Nassau Candy Factory Reallocation & Shipping Optimization System

## 📌 Project Overview
This project builds a **Factory Reallocation & Shipping Optimization Recommendation System** for Nassau Candy Distributor. It combines data analysis, machine learning, and an interactive dashboard to help leadership make data-driven decisions about factory assignments.

---

## 🎯 Problem Statement
Nassau Candy currently assigns products to factories using static rules, leading to:
- Suboptimal shipping distances
- High lead times for certain regions
- Margin erosion due to logistics inefficiencies

---

## 💡 Solution
An intelligent decision system that:
- ✅ Predicts shipping outcomes under different configurations
- ✅ Recommends which products should be reassigned to alternative factories
- ✅ Balances shipping efficiency and profitability

---

## 🏭 Factories
| Factory | Location |
|---|---|
| Lot's O' Nuts | Arizona |
| Wicked Choccy's | Georgia |
| Sugar Shack | Minnesota |
| Secret Factory | Illinois |
| The Other Factory | Tennessee |

---

## 📊 Dataset
- **10,194 orders**
- **18 columns**
- **15 products** across 3 divisions
- **4 regions** — Atlantic, Gulf, Interior, Pacific
- **4 ship modes** — Standard, First, Second, Same Day

---

## 🛠️ Tech Stack
| Tool | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data manipulation |
| Numpy | Numerical computing |
| Matplotlib & Seaborn | Data visualization |
| Scikit-learn | Machine learning models |
| Plotly | Interactive charts |
| Streamlit | Web dashboard |

---

## 🤖 ML Models Used
| Model | MAE | RMSE | R2 |
|---|---|---|---|
| Linear Regression | 215.04 | 266.14 | 0.00 |
| Random Forest | 225.04 | 277.24 | -0.09 |
| Gradient Boosting | 215.78 | 267.60 | -0.01 |

---

## 🖥️ Streamlit Dashboard Pages
1. 🏠 **Home Dashboard** — KPIs, charts, factory map
2. 🏭 **Factory Optimizer** — Product vs factory performance
3. 🔀 **What-If Scenario** — Compare current vs proposed
4. 🏆 **Recommendations** — Ranked reassignment table
5. ⚠️ **Risk & Impact** — Profit alerts & warnings

---

## 🔍 Key Findings
- **The Other Factory** has the fastest average lead time (1,280 days)
- **Sugar Shack** is the slowest factory (1,340 days)
- **Ship mode and region** have minimal impact on lead time
- **Factory assignment** is the primary driver of lead time
- **Lickable Wallpaper** is the most profitable product ($41.81 avg profit)
- **Hair Toffee** has the worst lead time (1,455 days)

---

## 🏆 Top Recommendations
| Product | Current Factory | Recommended Factory | Improvement |
|---|---|---|---|
| Hair Toffee | The Other Factory | The Other Factory | 174 days |
| Everlasting Gobstopper | Secret Factory | The Other Factory | 114 days |
| SweeTARTS | Sugar Shack | The Other Factory | 103 days |
| Laffy Taffy | Sugar Shack | The Other Factory | 102 days |

---

## 🚀 How to Run
1. Clone this repository
2. Install requirements: pip install streamlit pandas numpy plotly scikit-learn
   Run the app: streamlit run app.py

---

## 👨‍💻 Author
**Mohammed Nouman Ahmed**
Data Analyst Intern — Unified Mentor
