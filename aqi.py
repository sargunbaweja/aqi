from fastapi import FastAPI
import psycopg2
import psycopg2.extras

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Patiala AQI API running"}

# --- Database Connection ---
def get_connection():
    return psycopg2.connect(
        host="aws-1-ap-southeast-2.pooler.supabase.com",
        database="postgres",
        user="postgres.ubuippjtfzbnvsenwvne",
        password="greenpulseAI@987",
        port=6543,
        sslmode="require"
    )

# --- Route 1: Get all monthly AQI data ---
@app.get("/monthly")
def get_monthly():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM monthly_aqi ORDER BY month_number;")
    data = cursor.fetchall()
    conn.close()
    return {"data": list(data)}

# --- Route 2: Get all hourly AQI data ---
@app.get("/hourly")
def get_hourly():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM hourly_aqi ORDER BY recorded_time;")
    data = cursor.fetchall()
    conn.close()
    return {"data": list(data)}

# --- Route 3: Get a specific year's monthly data ---
@app.get("/monthly/{year}")
def get_monthly_by_year(year: int):
    valid_years = [2020, 2021, 2022, 2025, 2026]
    if year not in valid_years:
        return {"error": f"Year must be one of {valid_years}"}
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(f"SELECT month_name, aqi_{year} as aqi FROM monthly_aqi ORDER BY month_number;")
    data = cursor.fetchall()
    conn.close()
    return {"year": year, "data": list(data)}
