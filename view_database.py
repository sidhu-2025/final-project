import sqlite3
import os
import sys

db_path = os.path.join(os.path.dirname(__file__), "backend_yathra", "yathrakerala.db")

def print_banner():
    print("=" * 70)
    print("       YATHRA KERALA - DATABASE INSPECTION VIEWER (SQLite3)")
    print(f"       Database File: {os.path.abspath(db_path)}")
    print("=" * 70)

def show_tables():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    tables = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall()
    print("\nDATABASE TABLES SUMMARY:")
    print("-" * 70)
    print(f"{'#':<4} {'Table Name':<20} {'Row Count':<12} {'Description'}")
    print("-" * 70)
    
    descriptions = {
        "users": "Passenger & Driver accounts, passwords, roles, plates",
        "vehicles": "Bus fleet, live GPS coordinates (lat/lng), active status",
        "routes": "Transit corridors (start, destination, distance in km)",
        "stops": "Bus stop names with physical GPS latitude & longitude",
        "stop_allocation": "Ordered sequence of stops along corridors",
        "timings": "Bus timetable departure/arrival times & stage fares",
        "vehicle_routes": "Mapping of buses assigned to specific corridors",
        "travel_history": "Passenger ticket bookings and trip receipts",
        "taxi_fares": "Base & per-km tariff rates for Autos, Cabs & Taxis",
        "gps_tracking": "Historical breadcrumb telemetry logs"
    }

    for idx, (t,) in enumerate(tables, 1):
        count = c.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        desc = descriptions.get(t, "System table")
        print(f"{idx:<4} {t:<20} {count:<12} {desc}")
    print("-" * 70)
    conn.close()

def inspect_table(table_name, limit=10):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try:
        rows = c.execute(f"SELECT * FROM {table_name} LIMIT {limit}").fetchall()
        if not rows:
            print(f"\n[Table '{table_name}' is currently empty]\n")
            conn.close()
            return
        
        headers = rows[0].keys()
        print(f"\nTABLE: {table_name.upper()} (Showing first {len(rows)} records):")
        print("-" * 90)
        # Print formatted rows
        for i, row in enumerate(rows, 1):
            print(f"Record #{i}:")
            for h in headers:
                val = row[h]
                if val is not None and str(val).strip():
                    print(f"   {h:<20}: {val}")
            print("-" * 45)
    except Exception as e:
        print(f"Error querying table {table_name}: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print_banner()
    show_tables()
    
    # If table name provided as CLI argument
    if len(sys.argv) > 1:
        target = sys.argv[1].strip()
        inspect_table(target, limit=int(sys.argv[2]) if len(sys.argv) > 2 else 10)
    else:
        print("\nSHOWING CORE TABLES DATA:")
        inspect_table("users", limit=5)
        inspect_table("vehicles", limit=5)
        inspect_table("routes", limit=4)
        print("\nTip: To view any specific table, run: python view_database.py <table_name>")
        print("Example: python view_database.py vehicles")
