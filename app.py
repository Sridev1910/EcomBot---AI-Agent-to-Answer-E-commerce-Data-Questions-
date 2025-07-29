import streamlit as st
import sqlite3
import pandas as pd
import os
import base64
import google.generativeai as genai
import matplotlib.pyplot as plt

# ----------------- CONFIG -----------------
DB_FILE = "ecommerce_data.db"
API_KEY = os.getenv("GOOGLE_API_KEY")
LOGO_FILE = "aichatbot.png"  # Add your logo file in the same folder

# ----------------- BACKGROUND LOGO -----------------
def add_bg_logo(png_file, opacity=0.03, size="25%"):
    with open(png_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-repeat: no-repeat;
        background-position: center;
        background-size: {size};
        opacity: 1 !important;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: inherit;
        background-repeat: inherit;
        background-position: center;
        background-size: {size};
        opacity: {opacity};
        z-index: -1;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ----------------- PAGE SETUP -----------------
st.set_page_config(page_title="📊 E-commerce AI Agent", layout="centered")
if os.path.exists(LOGO_FILE):
    add_bg_logo(LOGO_FILE, opacity=0.03)

# ----------------- GEMINI SETUP -----------------
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.error("Google API Key not found. Please set it as an environment variable.")
    st.stop()

# ----------------- DATABASE LOADER -----------------
def create_database():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    conn = sqlite3.connect(DB_FILE)

    try:
        ad_sales_df = pd.read_csv("plasm.csv")
        ad_sales_df.to_sql("ad_sales", conn, if_exists="replace", index=False)

        total_sales_df = pd.read_csv("pltsm.csv")
        total_sales_df.to_sql("total_sales", conn, if_exists="replace", index=False)

        eligibility_df = pd.read_csv("plet.csv")
        eligibility_df.to_sql("eligibility", conn, if_exists="replace", index=False)

    except Exception as e:
        st.error(f"❌ Error during DB creation: {e}")
        st.info("Please upload all CSV files to your working directory.")
    finally:
        conn.close()

# ----------------- HELPER FUNCTIONS -----------------
def get_db_schema():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    schema = ""
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        schema += f"\n📄 Table '{table_name}':\n"
        for col in columns:
            schema += f"   • {col[1]} ({col[2]})\n"
    conn.close()
    return schema

def execute_sql(query: str):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except sqlite3.OperationalError as e:
        return f"SQL Error: {e}"

def get_sql_from_llm(question: str, schema: str):
    prompt = f"""
You are an expert SQL analyst. Based on the database schema below, write a single, syntactically correct SQL query to answer the user's question.
Only output the SQL query and nothing else.

**Database Schema:**
{schema}

**Question:**
"{question}"

**SQL Query:**
"""
    response = model.generate_content(prompt)
    sql_query = response.text.strip().replace("```sql", "").replace("```", "").strip()
    return sql_query

def get_summary_from_llm(question: str, data: str):
    prompt = f"""
You are a helpful AI assistant. A user asked the following question:
"{question}"

The answer from the database is:
"{data}"

Provide a concise, human-readable answer based on this data.
"""
    response = model.generate_content(prompt)
    return response.text.strip()

def create_visual(data, question):
    if not data:
        st.warning("No data to visualize.")
        return

    try:
        df = pd.DataFrame(data)

        if len(df.columns) == 2:
            st.subheader("📊 Visualization")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(df.iloc[:, 0], df.iloc[:, 1], color='#4A90E2')
            ax.set_xlabel(df.columns[0], fontsize=12)
            ax.set_ylabel(df.columns[1], fontsize=12)
            ax.set_title(question, fontsize=14)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("ℹ️ Chart needs exactly two columns.")
    except Exception as e:
        st.error(f"Could not generate chart: {e}")

# ----------------- MAIN UI -----------------
with st.container():
    st.markdown(
        """
        <style>
        .centered-title {
            text-align: center;
            font-size: 2.2rem;
            font-weight: bold;
            color: #1a73e8;
        }
        .subtitle {
            text-align: center;
            font-size: 1.1rem;
            color: #555;
        }
        .stTextInput>div>input {
            text-align: center;
            font-size: 1rem;
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown("<div class='centered-title'>🤖 E-commerce AI Agent</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Ask your data questions like a boss. We'll handle the SQL.</div><br>", unsafe_allow_html=True)

if 'db_initialized' not in st.session_state:
    with st.spinner("🗄️ Setting up the database..."):
        create_database()
    st.session_state['db_initialized'] = True

user_question = st.text_input("", placeholder="e.g., What is my total sales last month?")

if st.button("🔍 Get Insight"):
    if not user_question:
        st.warning("❗ Please enter a question.")
    else:
        with st.spinner("🧠 Thinking..."):
            try:
                schema = get_db_schema()

                sql_query = get_sql_from_llm(user_question, schema)
                st.markdown("#### 📝 Generated SQL Query")
                st.code(sql_query, language="sql")

                sql_result = execute_sql(sql_query)
                if "SQL Error" in str(sql_result):
                    st.error(f"❌ Query failed: {sql_result}")
                else:
                    st.markdown("#### 📋 Raw SQL Result")
                    st.json(sql_result)

                    final_answer = get_summary_from_llm(user_question, str(sql_result))
                    st.markdown("#### 💡 AI Summary")
                    st.success(final_answer)

                    create_visual(sql_result, user_question)

            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")

st.markdown("---")
st.caption("🚀 Built with ❤️ using Google Gemini + Streamlit")
