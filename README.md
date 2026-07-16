# Groq-App-To-Retrieve-SQL-Data
AI-powered Text-to-SQL application built with Groq, Streamlit, and SQLite. Converts natural language into SQL queries using Llama 3.3, executes them on a SQLite database, and returns accurate results through an interactive web interface.


## Features

* Convert natural language to SQL
* Powered by Groq Llama 3.3-70B
* Interactive Streamlit web interface
* SQLite database integration
* SQL query validation before execution
* Session-based chat history
* Secure API key management using `.env`

## Tech Stack

* Python
* Groq API
* Llama 3.3-70B Versatile
* Streamlit
* SQLite
* python-dotenv

## Project Structure

```text
├── app.py                 # Streamlit application
├── sql.py                 # Creates and populates SQLite database
├── student.db             # SQLite database
├── .env                   # Groq API key
├── Pipfile
├── Pipfile.lock
└── README.md
```

## Installation

### Clone the repository

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### Install dependencies

```bash
pipenv install
```

### Activate the virtual environment

```bash
pipenv shell
```

### Add your Groq API Key

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
```

### Create the SQLite database

```bash
python sql.py
```

### Run the application

```bash
streamlit run app.py
```

## Sample Questions

* Show all students.
* How many students are there?
* Show students from Data Science class.
* What is the average marks?
* Show students with marks greater than 80.
* Which student scored the highest marks?
* Display all students from Section A.

## How It Works

1. Enter a question in plain English.
2. Groq Llama 3.3 converts it into an SQL query.
3. The application validates the generated SQL.
4. SQLite executes the query.
5. Results are displayed in the Streamlit application.

## Future Improvements

* Support MySQL and PostgreSQL
* Export results to CSV/Excel
* Query explanation feature
* Data visualization dashboards
* Multi-table database support
* Conversation memory using LangChain

## Author

**Piyush Kumar**

If you found this project useful, consider giving it a ⭐ on GitHub!

