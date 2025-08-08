from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

@app.route('/lead', methods=['POST'])
def receive_lead():
    data = request.json

    try:
        conn = psycopg2.connect(
            host=os.environ['SUPABASE_HOST'],
            dbname=os.environ['SUPABASE_DB'],
            user=os.environ['SUPABASE_USER'],
            password=os.environ['SUPABASE_PASSWORD'],
            port=5432
        )
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO leads (name, email, utm_source, utm_medium, user_agent)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data.get("name"),
            data.get("email"),
            data.get("utm_source"),
            data.get("utm_medium"),
            data.get("user_agent")
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500
