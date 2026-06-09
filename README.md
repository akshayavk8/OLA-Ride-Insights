# 🚖 OLA Ride Insights

**Ride-Sharing & Mobility Analytics | July 2024**

A full-stack data analytics capstone project analysing **1,03,024 OLA ride records** across data cleaning, SQL querying, Power BI dashboarding, and an interactive Streamlit web application.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ola-ride-insights-mvngdsxoravv5zbaacrr57.streamlit.app)

---

## 📌 Project Overview

The rise of ride-sharing platforms has transformed urban mobility. OLA generates vast amounts of data related to ride bookings, driver availability, fare calculations, and customer preferences. This project extracts actionable insights from OLA's July 2024 ride data to support data-informed decisions around operational efficiency, customer satisfaction, and revenue optimisation.

---

## 📁 Repository Structure

```
ola-ride-insights/
│
├── app.py                          # Streamlit web application
├── requirements.txt                # Python dependencies
├── OLA_DataSet.xlsx                # Raw dataset (103,024 rows, July 2024)
├── ola_clean.csv                   # Cleaned dataset (output of Colab notebook)
├── OLA_Ride_Insights_Colab.ipynb   # Google Colab notebook (data cleaning + SQL)
├── OLA_Dashboard.pbix              # Power BI dashboard file
├── Ola-Slides.pptx                 # Project presentation with Power BI dashboard screenshots
└── README.md
```

---

## 📊 Dataset

| Attribute | Details |
|-----------|---------|
| **Source** | OLA Ride-Sharing Data |
| **Period** | July 2024 (01 Jul – 31 Jul) |
| **Total Records** | 1,03,024 rides |
| **Raw File** | `OLA_DataSet.xlsx` (original, uncleaned) |
| **Clean File** | `ola_clean.csv` (preprocessed, used by Streamlit app and Power BI) |
| **Columns** | 22 (after cleaning) |

**Key columns:**

| Column | Description |
|--------|-------------|
| `Date`, `Time` | Ride date and time |
| `Booking_ID` | Unique ride identifier |
| `Booking_Status` | Success / Canceled by Customer / Canceled by Driver / Driver Not Found |
| `Customer_ID` | Unique customer identifier |
| `Vehicle_Type` | Prime Sedan, Prime SUV, Prime Plus, Mini, Auto, Bike, eBike |
| `Pickup_Location`, `Drop_Location` | Ride origin and destination |
| `Booking_Value` | Fare amount (₹) |
| `Payment_Method` | Cash, UPI, Credit Card, Debit Card |
| `Ride_Distance` | Distance covered (km) |
| `Driver_Ratings`, `Customer_Rating` | Ratings out of 5 |
| `Canceled_Rides_by_Customer` | Reason for customer cancellation |
| `Canceled_Rides_by_Driver` | Reason for driver cancellation |
| `Incomplete_Rides_Reason` | Reason for incomplete ride |

---

## 🔢 Key Metrics

| Metric | Value |
|--------|-------|
| Total Rides | 1,03,024 |
| Successful Rides | 63,967 (62.1%) |
| Cancelled by Driver | 18,434 (17.9%) |
| Cancelled by Customer | 10,499 (10.2%) |
| Driver Not Found | 10,124 (9.8%) |
| Total Revenue (Successful) | ₹3,50,80,467 |
| Average Ride Distance | 14.19 km |
| Vehicle Types | 7 |
| Payment Methods | 4 |

---

## 🧹 Data Cleaning & Preprocessing

Performed in **Google Colab** (`OLA_Ride_Insights_Colab.ipynb`):

- Dropped trailing empty column and non-analytical `Vehicle Images` column
- Converted `Date` column to proper datetime format
- Replaced string `'null'` values with `NaN` throughout the dataset
- Cast numeric columns (`Booking_Value`, `Ride_Distance`, `Driver_Ratings`, `Customer_Rating`, `V_TAT`, `C_TAT`) to float
- Stripped whitespace from all text/categorical columns
- Derived helper columns: `Hour`, `DayOfWeek`, `DateOnly`
- Null values in cancellation/reason columns were **intentionally retained** — they represent rides that were not cancelled or incomplete, which is valid data

---

## 🗄️ SQL Analysis

All 10 queries executed in **SQLite (in-memory)** via Google Colab. No external database required.

| # | Question | Key Insight |
|---|----------|-------------|
| Q1 | Retrieve all successful bookings | 63,967 successful rides |
| Q2 | Average ride distance per vehicle type | Prime SUV has the highest avg distance |
| Q3 | Total cancellations by customers | 10,499 rides |
| Q4 | Top 5 customers by number of rides | Identifies high-frequency users |
| Q5 | Driver cancellations due to personal/car issues | Quantifies vehicle-related attrition |
| Q6 | Max & min driver ratings for Prime Sedan | Rating range analysis |
| Q7 | All rides paid via UPI | Digital payment adoption |
| Q8 | Average customer rating per vehicle type | Service quality by segment |
| Q9 | Total booking value of successful rides | ₹3.5 Cr revenue |
| Q10 | All incomplete rides with reason | Operational gaps identification |

---

## 📈 Power BI Dashboard

**File:** `OLA_Dashboard.pbix`

An interactive 5-page dashboard built in Power BI Desktop, connected to `ola_clean.csv`.

| Page | Visuals |
|------|---------|
| **Overall** | Ride Volume Over Time · Booking Status Breakdown |
| **Vehicle Type** | Top 5 Vehicle Types by Ride Distance |
| **Revenue** | Revenue by Payment Method · Top 5 Customers by Booking Value · Ride Distance Distribution Per Day |
| **Cancellation** | Cancelled Rides Reasons (Customer) · Cancelled Rides Reasons (Driver) |
| **Ratings** | Driver Ratings Distribution · Customer Ratings Distribution · Customer vs Driver Ratings |

**DAX Measures created:**
- `Total Rides`, `Successful Rides`, `Success Rate %`
- `Total Revenue`, `Avg Driver Rating`, `Avg Customer Rating`
- `Customer Cancellations`, `Driver Cancellations`

---

## 🌐 Streamlit Application

**Live App:** [ola-ride-insights.streamlit.app](https://ola-ride-insights-mvngdsxoravv5zbaacrr57.streamlit.app)

An interactive web dashboard with 6 sections mirroring the Power BI views, built with Streamlit + Plotly.

**Features:**
- 📊 **Overall** — KPI cards, ride volume trend, booking status donut chart
- 🚗 **Vehicle Type** — summary table, distance bar charts
- 💰 **Revenue** — payment method breakdown, top customers, daily distance trend
- ❌ **Cancellation** — reason breakdowns, cancellation trend over time
- ⭐ **Ratings** — rating distributions, grouped comparison by vehicle type
- 🔍 **SQL Explorer** — all 10 project queries pre-loaded, editable, with auto-charts and CSV download

**Tech stack:** `streamlit` · `plotly` · `pandas` · `sqlite3` · `numpy`

### Run Locally

```bash
# Clone the repo
git clone https://github.com/akshayavk8/ola-ride-insights.git
cd ola-ride-insights

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 🛠️ Tools & Technologies

| Category | Tools |
|----------|-------|
| **Language** | Python 3 |
| **Data Processing** | Pandas, NumPy |
| **SQL** | SQLite (via Python) |
| **Visualisation** | Power BI Desktop, Plotly |
| **Web App** | Streamlit |
| **Notebook** | Google Colab |
| **Deployment** | Streamlit Community Cloud |
| **Version Control** | Git, GitHub |

---

## 💡 Business Insights

- **62.1% success rate** — over a third of all bookings fail to complete, pointing to supply-demand gaps
- **Driver cancellations (17.9%)** are nearly double customer cancellations (10.2%), suggesting driver-side operational issues
- **UPI and Cash** dominate payment methods, indicating a mixed digital-physical user base
- **Prime Sedan and Prime SUV** cover the longest distances, driving the majority of revenue
- **Ratings are consistently high** across all vehicle types (avg above 4.0), indicating good overall service quality

---

## 👩‍💻 Author

**Akshayaa V. Kumar**
Marine Biologist & Data Science Practitioner
HCL GUVI — Data Science with ML & AI Certification

[![GitHub](https://img.shields.io/badge/GitHub-akshayavk8-181717?style=flat&logo=github)](https://github.com/akshayavk8)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/akshayavinodkumar)

---

*This project was completed as part of the GUVI Data Science with ML & AI certification capstone.*

