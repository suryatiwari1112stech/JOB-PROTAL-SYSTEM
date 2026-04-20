from flask import Flask, render_template, request, redirect, session, send_from_directory
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"

# ==============================
# UPLOAD FOLDER
# ==============================
UPLOAD_FOLDER = "resumes"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ==============================
# DB FUNCTION
# ==============================
def get_db():
    return sqlite3.connect("jobportal.db")


# ==============================
# HOME
# ==============================
@app.route("/")
def home():
    return render_template("login.html")


# ==============================
# SIGNUP
# ==============================
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("signup.html")


# ==============================
# LOGIN
# ==============================
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        session["user"] = username
        return redirect("/dashboard")

    return "Invalid Login"


# ==============================
# DASHBOARD
# ==============================
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    return render_template("dashboard.html", user=session["user"])


# ==============================
# LOGOUT
# ==============================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# ==============================
# ADD JOB (ADMIN ONLY)
# ==============================
@app.route("/add_job")
def add_job():

    if "user" not in session:
        return redirect("/")

    if session["user"] != "admin":
        return "Only admin can add jobs"

    return render_template("add_job.html")


# ==============================
# SAVE JOB (ADMIN ONLY)
# ==============================
@app.route("/save_job", methods=["POST"])
def save_job():

    if "user" not in session:
        return redirect("/")

    if session["user"] != "admin":
        return "Only admin can post jobs"

    title = request.form["title"]
    company = request.form["company"]
    location = request.form["location"]
    description = request.form["description"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO jobs (title, company, location, description) VALUES (?, ?, ?, ?)",
        (title, company, location, description)
    )

    conn.commit()
    conn.close()

    return redirect("/jobs")


# ==============================
# VIEW JOBS
# ==============================
@app.route("/jobs")
def jobs():

    if "user" not in session:
        return redirect("/")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()

    conn.close()

    return render_template("jobs.html", jobs=jobs)


# ==============================
# APPLY JOB
# ==============================
@app.route("/apply/<int:job_id>", methods=["GET", "POST"])
def apply(job_id):

    if "user" not in session:
        return redirect("/")

    if request.method == "POST":

        file = request.files["resume"]
        filename = file.filename

        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO applications (username, job_id, resume, status) VALUES (?, ?, ?, ?)",
            (session["user"], job_id, filename, "applied")
        )

        conn.commit()
        conn.close()

        return redirect("/jobs")

    return render_template("apply.html", job_id=job_id)


# ==============================
# MY APPLICATIONS
# ==============================
@app.route("/my_applications")
def my_applications():

    if "user" not in session:
        return redirect("/")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM applications WHERE username=?",
        (session["user"],)
    )

    apps = cursor.fetchall()
    conn.close()

    return render_template("my_applications.html", applications=apps)


# ==============================
# ADMIN VIEW APPLICATIONS
# ==============================
@app.route("/all_applications")
def all_applications():

    if "user" not in session:
        return redirect("/")

    if session["user"] != "admin":
        return "Only admin allowed"

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications")
    apps = cursor.fetchall()

    conn.close()

    return render_template("all_applications.html", applications=apps)


# ==============================
# DOWNLOAD RESUME
# ==============================
@app.route("/resumes/<filename>")
def resume_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)