from flask import Flask, request, jsonify
import psycopg2
from datetime import date, time, timedelta

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
        print("Databasanslutning lyckades")
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
    colnames = [desc[0] for desc in cur.description]

    result = []
    for row in rows:
        row_dict = {}
        for i in range(len(colnames)):
            value = row[i]
            if isinstance(value, (date, time, timedelta)):
                row_dict[colnames[i]] = str(value)
            else:
                row_dict[colnames[i]] = value
        result.append(row_dict)

    cur.close()
    conn.close()
    return jsonify(result)

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

@app.route('/working_hours/<int:id>', methods=['PATCH'])
def update_working_hours(id):
    data = request.get_json()
    fields = []
    values = []

    for key, value in data.items():
        fields.append(f"{key} = %s")
        values.append(value)

    if not fields:
        return jsonify({'error': 'Inga fält att uppdatera'}), 400

    query = f"UPDATE working_hours SET {', '.join(fields)} WHERE id = %s"
    values.append(id)

    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Kan inte ansluta till databasen'}), 500

    cur = conn.cursor()
    try:
        cur.execute(query, tuple(values))
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': f'Arbetsrad med id {id} uppdaterad'}), 200

@app.route('/working_hours/<int:id>', methods=['DELETE'])
def delete_working_hours(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Kan inte ansluta till databasen'}), 500

    cur = conn.cursor()
    cur.execute("DELETE FROM working_hours WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'message': f'Arbetsrad med id {id} raderad'}), 200

if __name__ == '__main__':
    app.run(debug=True)
