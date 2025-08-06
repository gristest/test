
import sqlite3

db_path = '/workspace/test/ai_chat/data.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get table list
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Database tables:")
for table in tables:
    print(f"- {table[0]}")
    # Get table schema
    cursor.execute(f"PRAGMA table_info({table[0]});")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[1]} ({col[2]})")

conn.close()
