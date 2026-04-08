import pyodbc

# On utilise le Driver 17 que tu as sur Windows
DRIVER = '{ODBC Driver 17 for SQL Server}'
SERVER = 'localhost,1433'
DATABASE = 'OlistDW'
UID = 'sa'
PWD = 'Admin123!'

conn_str = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={UID};PWD={PWD};TrustServerCertificate=yes;'

try:
    print(f"Tentative sur Windows avec {DRIVER}...")
    conn = pyodbc.connect(conn_str, timeout=5)
    print("✅ SUCCÈS : Ton SQL Server (sa) est bien configuré sur Windows !")
    conn.close()
except Exception as e:
    print(f"❌ ÉCHEC : {e}")