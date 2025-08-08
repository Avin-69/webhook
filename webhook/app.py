from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Root route to accept POST webhook
@app.route("/", methods=["POST"])
def receive_lead():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON received"}), 400

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

        return jsonify({"message": "Lead received successfully!"}), 200
    except Exception as e:
        print("Error inserting lead:", e)
        return jsonify({"error": str(e)}), 500

# Optional GET route to verify it's alive
@app.route("/", methods=["GET"])
def index():
    return "Webhook is alive!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

