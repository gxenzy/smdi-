from sqlalchemy import create_engine

# Replace with your actual connection string
engine = create_engine('mysql://smdi_admin:MYSQL@DM1NP@SSW0RD@127.0.0.1:3306/smdi')

try:
    connection = engine.connect()
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")