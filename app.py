from dotenv import load_dotenv
load_dotenv()  ## load all the environment variables

import streamlit as st
import os
import sqlite3

from groq import Groq

## Configure Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

## Function To Load Groq Model and provide queries as response

def get_groq_response(question, prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": prompt[0]},
            {"role": "user", "content": question}
        ],
        temperature=0
    )
    sql = response.choices[0].message.content

    # --- Sanitize the SQL string ---
    sql = sql.strip()

    if sql.startswith("```"):
        sql = sql.strip("`")
        if sql.lower().startswith("sql"):
            sql = sql[3:]

    sql = sql.strip()

    return sql

## Function To retrieve query from the database

def read_sql_query(sql, db):
    valid_starts = ("SELECT", "INSERT", "UPDATE", "DELETE", "WITH")
    if not sql.strip().upper().startswith(valid_starts):
        raise ValueError(
            "The model did not return a valid SQL query. "
            f"It responded instead with:\n\n{sql}"
        )

    print("Running SQL:", repr(sql))
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

## Define Your Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION, MARKS.

    Rules you must always follow:
    1. ALWAYS return a single valid SQL query — nothing else.
    2. NEVER include explanations, notes, or plain English text of any kind.
    3. Do not wrap the query in ``` or prefix it with the word sql.

    Example 1 - How many entries of records are present? 
    -> SELECT COUNT(*) FROM STUDENT;

    Example 2 - Tell me all the students studying in Data Science class? 
    -> SELECT * FROM STUDENT WHERE CLASS="Data Science";

    Example 3 - What is the average marks of students? 
    -> SELECT AVG(MARKS) FROM STUDENT;

    Example 4 - What is the average marks for each class? 
    -> SELECT CLASS, AVG(MARKS) FROM STUDENT GROUP BY CLASS;
    """
]

## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Groq App To Retrieve SQL Data")

# --- Initialize chat history in session state (persists across reruns) ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of dicts: {"question": ..., "sql": ..., "result": ...}

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

# if submit is clicked
if submit and question:
    sql = get_groq_response(question, prompt)
    print(sql)

    try:
        result = read_sql_query(sql, "student.db")
        # --- Save this Q&A into session history ---
        st.session_state.chat_history.append({
            "question": question,
            "sql": sql,
            "result": result,
            "error": None
        })
    except (ValueError, sqlite3.OperationalError) as e:
        st.session_state.chat_history.append({
            "question": question,
            "sql": sql,
            "result": None,
            "error": str(e)
        })

# --- Display full chat history (most recent first) ---
#st.subheader("Chat History")  --it will show subheader

if not st.session_state.chat_history:
    st.write("No questions asked yet.")
else:
    for entry in reversed(st.session_state.chat_history):
        st.markdown(f"**Q: {entry['question']}**")
        if entry["error"]:
            st.error(entry["error"])
        else:
            for row in entry["result"]:
                if len(row) == 1:
                    st.write(row[0])   # single value -> print just the value
                else:
                    st.write(row)      # multiple columns -> print as-is
        st.markdown("---")