import psycopg2
import pandas as pd


conn = psycopg2.connect(
    host="fde-db-v2.postgres.database.azure.com",
    database="time-management",  
    user="fde",
    password="Password!", 
    sslmode="require"
)

 
df = pd.read_sql("SELECT * FROM working_hours", conn)
conn.close()


with open("rapport.txt", "w") as f:
    for index, row in df.iterrows():
        f.write(f"{row['date']} - {row['consultantname']} hos {row['customername']}, {row['starttime']}-{row['endtime']} (Lunch: {row['lunchbreak']})\n")

print("✅ Rapport skapad som rapport.txt")

