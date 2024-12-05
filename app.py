from flask import Flask, render_template, request
import psycopg2
import os

template_dir = os.path.abspath('templates/')
app = Flask(__name__, template_folder=template_dir)

conn = psycopg2.connect(
        host="db",
        database="Robiyabonu",
        user='student',
        password='password'
)

cur = conn.cursor()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        level = request.form.get("level", "")
        return render_template("timetable.html", level=level, data=[], message="Loading timetable...")
    
    return render_template("index.html")

@app.route("/timetable", methods=["GET"])
def timetable():
    level = request.args.get("level")
    if not level:
        return render_template("timetable.html", data=[], message="Level is required.")
    
    query = "SELECT * FROM Timetable WHERE level = %s;"
    cur.execute(query, (level,))
    rows = cur.fetchall()
    message = "No data found for this level." if not rows else None
    return render_template("timetable.html", data=rows, message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

