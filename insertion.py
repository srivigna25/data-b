from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException
from mako.lookup import TemplateLookup
import mysql.connector

app = FastAPI()

templates = TemplateLookup(directories=["templates"])

# Database connection details
DB_CONFIG = {
    "host" :"localhost",
    "port":3306,
    "user":"root",
    "password":"Srivign@143",
    "database":"films"
    }
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

@app.get("/form", response_class=HTMLResponse)
async def show_form(request: Request):
    categories = ["Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance"]
    template = templates.get_template("form.html")
    return template.render(request=request, categories=categories)

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    name: str = Form(...),
    category: str = Form(...),
    release_year: int = Form(...)
):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO movies (name, category, release_year) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, category, release_year))
        connection.commit()
        template = templates.get_template("success.html")
        return template.render(request=request, name=name, category=category, release_year=release_year)
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error inserting data into the database")
    finally:
        cursor.close()
        connection.close()


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