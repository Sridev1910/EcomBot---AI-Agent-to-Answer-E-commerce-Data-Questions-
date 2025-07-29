## 🧠 EcomBot — AI Agent to Answer E-commerce Data Questions

**EcomBot** is an AI-powered assistant designed to answer natural language questions about product-level e-commerce sales data. It intelligently translates user questions into SQL, fetches data from a structured database, and delivers insightful answers — with optional visualizations.

---

## 📌 Features

✅ Ask natural language questions
✅ Automatic SQL generation using **Google Gemini AI**
✅ Executes queries on a **SQLite database**
✅ Returns **human-readable summaries**
✅ Displays **bar charts** when suitable
✅ Easy-to-use **Streamlit web interface**
✅ Optional watermark branding with custom logo

---

## 📂 Folder Structure

```
├── app.py                    # Main Streamlit application
├── plasm.csv                 # Product-Level Ad Sales and Metrics
├── pltsm.csv                 # Product-Level Total Sales and Metrics
├── plet.csv                  # Product-Level Eligibility Table
├── logo.png                  # Watermark logo (low opacity)
├── ecommerce_data.db         # SQLite database (auto-generated)
└── README.md                 # Project description
```

---

## 🖥️ How to Run (Locally or via Google Colab)

### 🔧 1. Install Required Packages

```bash
pip install streamlit pandas matplotlib google-generativeai
```

### 🔧 2. Set Your Google Gemini API Key

```bash
export GOOGLE_API_KEY=your_gemini_api_key_here
```

### 🔧 3. Run the App

```bash
streamlit run app.py
```

Or in **Google Colab**, use `pyngrok` to expose it:

```python
!pip install pyngrok streamlit
```

---

## 🌐 Demo Screenshot

![screenshot](screenshot.png) <!-- Optional: replace with real screen capture -->

---

## 🤖 Example Questions to Ask

* What is my total sales?
* Which product had the highest CPC?
* Show top 5 products by ROAS.
* Compare total sales by product category.

---

## 📊 Data Sources

* **plasm.csv**: Ad performance metrics
* **pltsm.csv**: Total sales metrics
* **plet.csv**: Product eligibility info

---

## ⚙️ Technologies Used

* [Streamlit](https://streamlit.io/) – UI Framework
* [Google Gemini API](https://aistudio.google.com/app/apikey) – LLM for SQL generation
* [SQLite](https://www.sqlite.org/index.html) – Embedded database
* [Matplotlib](https://matplotlib.org/) – Charting library

---

## 📈 Future Enhancements

* Add support for CSV uploads
* Improve SQL query validation
* Add download/export for query results
* Deploy as a public web app (Streamlit Cloud / Hugging Face Spaces)

---

## ✍️ Author

Name: **Sridev S**
Email: **sridev.s1654@gmail.com**
