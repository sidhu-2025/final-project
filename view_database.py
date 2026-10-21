import sqlite3
import os
import sys

db_path = os.path.join(os.path.dirname(__file__), "backend_yathra", "yathrakerala.db")

def print_banner():
    print("=" * 80)
    print("       YATHRA KERALA - COMPLETE SQL DATABASE VIEWER")
    print(f"       Database File: {os.path.abspath(db_path)}")
    print("=" * 80)

def get_all_tables():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    tables = [t[0] for t in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall()]
    conn.close()
    return tables

def show_tables_summary():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    tables = get_all_tables()
    print("\nDATABASE TABLES SUMMARY:")
    print("-" * 80)
    print(f"{'#':<4} {'Table Name':<22} {'Row Count':<12} {'Description'}")
    print("-" * 80)
    
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

    for idx, t in enumerate(tables, 1):
        count = c.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        desc = descriptions.get(t, "System table")
        print(f"{idx:<4} {t:<22} {count:<12} {desc}")
    print("-" * 80)
    conn.close()

def inspect_table(table_name, limit=None):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try:
        query = f"SELECT * FROM {table_name}"
        if limit:
            query += f" LIMIT {limit}"
        rows = c.execute(query).fetchall()
        
        print(f"\n=======================================================")
        print(f"  SQL QUERY: SELECT * FROM {table_name}; ({len(rows)} rows fetched)")
        print(f"=======================================================")
        
        if not rows:
            print(f"  [Table '{table_name}' has 0 records]\n")
            return
        
        headers = rows[0].keys()
        
        # Display each row in a clear key-value format
        for i, row in enumerate(rows, 1):
            print(f"  --- Record #{i} ---")
            for h in headers:
                val = row[h]
                if val is not None and str(val).strip():
                    print(f"    {h:<20} : {val}")
        print("-" * 55)
    except Exception as e:
        print(f"Error querying table {table_name}: {e}")
    finally:
        conn.close()

def fetch_and_show_all_data():
    """Fetches ALL data from EVERY table in the database."""
    tables = get_all_tables()
    print("\n" + "#" * 80)
    print("  FETCHING ALL DATA ACROSS ENTIRE DATABASE (ALL TABLES & ALL ROWS)")
    print("#" * 80)
    for t in tables:
        inspect_table(t, limit=None)

if __name__ == "__main__":
    print_banner()
    show_tables_summary()
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].strip().lower()
        if arg in ["all", "--all", "-a", "dump"]:
            fetch_and_show_all_data()
        else:
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
            inspect_table(arg, limit=limit)
    else:
        print("\n--- SAMPLE VIEW (Top Records from Core Tables) ---")
        inspect_table("users", limit=4)
        inspect_table("vehicles", limit=4)
        inspect_table("routes", limit=4)
        print("\nHOW TO USE THIS COMMAND:")
        print("  1. To fetch ALL data from ALL tables:")
        print("     python view_database.py all")
        print("\n  2. To fetch ALL rows from a specific table:")
        print("     python view_database.py users")
        print("     python view_database.py vehicles")
        print("     python view_database.py routes")
        print("     python view_database.py stops")
        print("     python view_database.py timings 10")
