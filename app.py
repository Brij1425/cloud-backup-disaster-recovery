from flask import Flask, render_template, request, redirect, session, send_from_directory
import os
import requests
import shutil
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


SUPABASE_URL = "https://ztoavfdypxiclumvfsnl.supabase.co"
SUPABASE_KEY = "sb_publishable_nfJ17fdwbbpeTst9esx21A_m5jlqToj"

app = Flask(__name__)
app.secret_key = "secret123"

# -------- FOLDERS --------
STORAGE_FOLDER = "storage"
BACKUP_FOLDER = "backups"

os.makedirs(STORAGE_FOLDER, exist_ok=True)
os.makedirs(BACKUP_FOLDER, exist_ok=True)

# -------- DATABASE --------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    cursor.execute("SELECT * FROM users WHERE username=?", ("admin",))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users VALUES (?, ?)",
                       ("admin", generate_password_hash("1234")))

    conn.commit()
    conn.close()

init_db()

# -------- LOGIN --------
@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        url = f"{SUPABASE_URL}/rest/v1/users?username=eq.{username}"

        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }

        response = requests.get(url, headers=headers)

        print("LOGIN:", response.status_code, response.text)

        if response.status_code == 200:
            data = response.json()

            if len(data) > 0:
                stored_hash = data[0]["password"]

                if check_password_hash(stored_hash, password):
                    session["user"] = username
                    return redirect("/dashboard")

        error = "Invalid username or password"

    return render_template("login.html", error=error)


# -------- REGISTER --------
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if len(password) < 4:
            error = "Password must be at least 4 characters"
        else:
            url = f"{SUPABASE_URL}/rest/v1/users"

            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }

            data = {
                "username": username,
                "password": generate_password_hash(password)
            }

            response = requests.post(url, json=data, headers=headers)

            print("REGISTER:", response.status_code, response.text)

            if response.status_code in [200, 201]:
                return redirect("/")
            else:
                error = "User already exists or error occurred"

    return render_template("register.html", error=error)


# -------- DASHBOARD --------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    username = session["user"]
    user_folder = os.path.join(STORAGE_FOLDER, username)
    os.makedirs(user_folder, exist_ok=True)

    files = []

    for f in os.listdir(user_folder):
        path = os.path.join(user_folder, f)

        size = round(os.path.getsize(path) / 1024, 2)
        time = datetime.fromtimestamp(os.path.getctime(path)).strftime("%d-%m-%Y %H:%M")

        files.append({"name": f, "size": size, "time": time})

    return render_template("dashboard.html",
                           files=files,
                           total_files=len(files),
                           user=username)

# -------- BACKUP --------
@app.route("/backup", methods=["POST"])
def backup():
    if "user" not in session:
        return redirect("/")

    file = request.files["file"]

    if file.filename == "":
        return redirect("/dashboard")

    username = session["user"]
    user_folder = os.path.join(STORAGE_FOLDER, username)
    os.makedirs(user_folder, exist_ok=True)

    filename = datetime.now().strftime("%Y%m%d_%H%M%S_") + file.filename
    file.save(os.path.join(user_folder, filename))

    return redirect("/dashboard?msg=upload_success")

# -------- RESTORE --------
@app.route("/restore/<filename>")
def restore(filename):
    username = session["user"]

    src = os.path.join(STORAGE_FOLDER, username, filename)
    dest = os.path.join(BACKUP_FOLDER, username)

    os.makedirs(dest, exist_ok=True)

    if os.path.exists(src):
        shutil.copy(src, os.path.join(dest, filename))

    return redirect("/dashboard")

# -------- DELETE --------
@app.route("/delete/<filename>")
def delete(filename):
    username = session["user"]

    path = os.path.join(STORAGE_FOLDER, username, filename)

    if os.path.exists(path):
        os.remove(path)

    return redirect("/dashboard")

# -------- DOWNLOAD --------
@app.route("/download/<filename>")
def download(filename):
    username = session["user"]

    return send_from_directory(
        os.path.join(STORAGE_FOLDER, username),
        filename,
        as_attachment=True
    )

# -------- ADMIN --------
@app.route("/admin")
def admin():
    if session.get("user") != "admin":
        return "Access Denied"

    all_data = {}

    for user in os.listdir(STORAGE_FOLDER):
        user_path = os.path.join(STORAGE_FOLDER, user)

        if os.path.isdir(user_path):
            files = os.listdir(user_path)
            all_data[user] = files

    return render_template("admin.html", data=all_data)


@app.route("/admin/delete/<username>/<filename>")
def admin_delete(username, filename):
    if session.get("user") != "admin":
        return "Access Denied"

    path = os.path.join(STORAGE_FOLDER, username, filename)

    if os.path.exists(path):
        os.remove(path)

    return redirect("/admin")

# -------- LOGOUT --------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# -------- RUN --------
if __name__ == "__main__":
    app.run(debug=False)
