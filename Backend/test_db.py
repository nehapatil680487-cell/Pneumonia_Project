from database import get_connection

conn = get_connection()
if conn.is_connected():
    print("✅ Connected to MySQL database successfully!")
    conn.close()
else:
    print("❌ Connection failed.")