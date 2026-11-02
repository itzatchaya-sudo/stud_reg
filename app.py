
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def create_table():
    con = sqlite3.connect("students.db")
    con.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
    """)
    con.commit()
    con.close()

@app.route("/", methods=["GET", "POST"])
def home():
    create_table()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        con = sqlite3.connect("students.db")
        con.execute(
            "INSERT INTO students (name, email) VALUES (?, ?)",
            (name, email)
        )
        con.commit()
        con.close()

    con = sqlite3.connect("students.db")
    students = con.execute(
        "SELECT * FROM students"
    ).fetchall()
    con.close()

    return render_template("index.html", students=students)

if __name__ == "__main__":
    create_table()
    app.run(host="0.0.0.0", port=5000)
