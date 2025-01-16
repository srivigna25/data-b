from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from mako.template import Template
from datetime import datetime
import mysql.connector

app = FastAPI()

# Database connection details
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="Srivign@143",
            database="films"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to database MySQL: {e}")
        return None

def fetch_movies_data_from_db(order="ASC"):
    connection = get_db_connection()
    if not connection:
        return {"message": "Database connection failed"}

    try:
        cur = connection.cursor(dictionary=True)
        query = f"SELECT * FROM movies ORDER BY movie_id {order}"
        cur.execute(query)
        results = cur.fetchall()
        return results
    except Error as e:
        print(f"Error fetching movies data: {e}")
        return []
    finally:
        if connection.is_connected():
            cur.close()
            connection.close()


@app.get("/fetch-data")
def fetch_data():
    data = fetch_movies_data_from_db()
    return data

@app.get("/")
def fetch_data():
    data = fetch_movies_data_from_db(order = "DESC")
    return data