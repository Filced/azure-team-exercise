from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="fde-db-v2.postgres.database.azure.com",
            port="5432",
            database="time-management",
            user="fde",
            password="Password!",
            sslmode="require"
        )
        print("✅ Databasanslutning lyckades")
        return conn
    except Exception as e:
        print("Databasanslutning misslyckades:", e)
        return None


@app.route('/working_hours', methods=['GET'])
def get_working_hours():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Kan inte ansluta till databasen!'}), 500
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM working_hours")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(rows)

@app.route('/working_hours', methods=['POST'])
def add_working_hours():
    data = request.get_json()

    date = data.get('date')
    starttime = data.get('starttime')
    endtime = data.get('endtime')
    lunchbreak = data.get('lunchbreak')
    consultantname = data.get('consultantname')
    customername = data.get('customername')

    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Kan inte ansluta till databasen'}), 500
    
    cur = conn.cursor()

    insert_query = """
    INSERT INTO working_hours (date, starttime, endtime, lunchbreak, consultantname, customername)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cur.execute(insert_query, (date, starttime, endtime, lunchbreak, consultantname, customername))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({'message': 'Tid sparad i databasen!'}), 201

if __name__ == '__main__':
    app.run(debug=True)
