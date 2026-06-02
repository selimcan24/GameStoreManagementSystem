# 🎮 Nexus Game Store

A full-stack Django e-commerce and Point of Sale (POS) application built with a modern dark-mode UI, real-time analytics, and external API integration.

## ✨ Key Features
* **Modern UI/UX:** Sleek dark theme powered by Bootstrap 5.
* **Inventory Management:** Full CRUD capabilities for staff to add, edit, and delete games and genres.
* **Simulated Checkout:** Working "Buy Now" system that automatically updates stock and records transaction revenue.
* **Business Analytics:** Real-time revenue and unit-sold data visualizations using **Chart.js**.
* **Data Export:** Instantly generate `.xlsx` Excel ledgers of all historical sales using `openpyxl`.
* **API Integration:** Fetches live trending games using the RAWG API.

## 🛠️ Tech Stack
* **Backend:** Python, Django, Django REST Framework
* **Frontend:** HTML, CSS, Bootstrap 5, Chart.js
* **Database:** SQLite3
* **Extras:** `requests` (API), `openpyxl` (Excel)

## 🚀 How to Run Locally

1. **Clone the repository** (or download the source code).
2. **Activate your virtual environment**.
3. **Install dependencies:**
   ```bash
   pip install django requests openpyxl djangorestframework
