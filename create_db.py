import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("invoice.db")
cursor = conn.cursor()

# Create table for storing scenarios
cursor.execute("""
CREATE TABLE IF NOT EXISTS scenarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scenario_name TEXT NOT NULL,
    monthly_invoice_volume REAL,
    num_ap_staff REAL,
    avg_hours_per_invoice REAL,
    hourly_wage REAL,
    error_rate_manual REAL,
    error_cost REAL,
    time_horizon_months REAL,
    one_time_implementation_cost REAL,
    monthly_savings REAL,
    payback_months REAL,
    roi_percentage REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
print("invoice.db created with 'scenarios' table!")
