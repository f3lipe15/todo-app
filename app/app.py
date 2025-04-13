from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "tasks.db"

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, done INTEGER DEFAULT 0)")
        conn.commit()
        conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if request.method == "POST":
        task = request.form.get("task")
        if task:
            c.execute("INSERT INTO tasks (content) VALUES (?)", (task,))
            conn.commit()
        return redirect("/")

    c.execute("SELECT id, content, done FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/done/<int:task_id>")
def mark_done(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
