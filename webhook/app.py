from flask import Flask, request, jsonify
import os
import psycopg2

app = Flask(__name__)

@app.route('/lead', methods=['POST'])
def receive_lead():
    data = request.json

    try:
        conn = psycopg2.connect(
            host=os.environ['SUPABASE_HOST'],
            port=os.environ.get('SUPABASE_PORT', 5432),
            dbname=os.environ['SUPABASE_DB'],
            user=os.environ['SUPABASE_USER'],
            password=os.environ['SUPABASE_PASSWORD']
        )

        cur = conn.cursor()
        cur.execute("""
            INSERT INTO leads (name, email, utm_source, utm_medium, user_agent)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data.get('name'),
            data.get('email'),
            data.get('utm_source'),
            data.get('utm_medium'),
            data.get('user_agent')
        ))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Lead stored successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ ADD THIS PART SO THE APP RUNS ON RAILWAY
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

