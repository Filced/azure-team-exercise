import psycopg2
import pandas as pd

def generate_report():
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

    df['date'] = pd.to_datetime(df['date'])
    df['starttime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['starttime'].astype(str))
    df['endtime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['endtime'].astype(str))
    df['lunchbreak'] = pd.to_timedelta(df['lunchbreak'])
    df['worked_hours'] = (df['endtime'] - df['starttime'] - df['lunchbreak']).dt.total_seconds() / 3600

    daily = df.groupby(['consultantname', 'date'])['worked_hours'].sum().reset_index()
    df['week'] = df['date'].dt.isocalendar().week
    weekly = df.groupby(['consultantname', 'week'])['worked_hours'].sum().reset_index()

    cumulative_df = df.groupby(['consultantname', 'customername'])['worked_hours'].sum().reset_index()

    average_df = df.groupby(['consultantname'])['worked_hours'].mean().reset_index()
    average_df.rename(columns={'worked_hours': 'average_hours'}, inplace=True)

    with open("rapport.txt", "w") as f:
        f.write("Daglig tid:\n")
        for _, row in daily.iterrows():
            f.write(f"{row['date'].date()} - {row['consultantname']}: {row['worked_hours']:.2f} timmar\n")

        f.write("\nVeckovis tid:\n")
        for _, row in weekly.iterrows():
            f.write(f"Vecka {row['week']} - {row['consultantname']}: {row['worked_hours']:.2f} timmar\n")

        f.write('\nTotala timmar per konsult/kund\n')
        for _, row in cumulative_df.iterrows():
            f.write(f"{row['consultantname']} - {row['customername']}: {row['worked_hours']} timmar\n")

        f.write('\nGenomsnittliga timmar/dag\n')
        for _, row in average_df.iterrows():
            f.write(f"{row['consultantname']}: {row['average_hours']} timmar\n")

    print("Rapport skapad som rapport.txt")

