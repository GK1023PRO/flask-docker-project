import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"]
    )

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, description FROM tasks;")
    tasks = [{"id": row[0], "description": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (description) VALUES (%s) RETURNING id;", (data["description"],))
    task_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": task_id, "description": data["description"]}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)